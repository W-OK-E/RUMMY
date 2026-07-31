from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple

from .game import RummyGame
from .cards import Card


class RummyEnv:
    def __init__(self, player_names: List[str], seed: int | None = None):
        self.game = RummyGame(player_names, seed=seed)
        self.done = False
        self.info: Dict[str, Any] = {}

    def reset(self) -> Dict[str, Any]:
        self.game.reset()
        self.done = False
        self.info = {}
        return self._observation(self.game.current_player)

    def _observation(self, player_name: str) -> Dict[str, Any]:
        return {
            "player": player_name,
            "hand": list(self.game.players[player_name]),
            "wild_rank": self.game.wild_rank,
            "top_discard": self.game.top_discard(),
            "deck_size": len(self.game.deck.cards),
            "discard_size": len(self.game.deck.discard_pile),
            "remaining_hands": {name: len(hand) for name, hand in self.game.players.items()},
        }

    def step(self, action: Dict[str, Any]) -> Tuple[Dict[str, Any], int, bool, Dict[str, Any]]:
        if self.done:
            raise RuntimeError("Cannot step() after environment is done")

        reward = 0
        player_name = self.game.current_player
        action_type = action.get("type")

        if action_type == "draw_deck":
            try:
                self.game.draw_from_deck(player_name)
            except (IndexError, ValueError) as error:
                reward = -1
                self.info = {"error": str(error)}
                return self._observation(player_name), reward, self.done, self.info
        elif action_type == "draw_discard":
            try:
                self.game.draw_from_discard(player_name)
            except IndexError as error:
                reward = -1
                self.info = {"error": str(error)}
                return self._observation(player_name), reward, self.done, self.info
        elif action_type == "discard_card":
            card = action.get("card")
            if not card or not isinstance(card, tuple) or len(card) != 2:
                reward = -1
                self.info = {"error": "Invalid card payload"}
                return self._observation(player_name), reward, self.done, self.info
            try:
                self.game.discard_card(player_name, tuple(card))
            except ValueError as error:
                reward = -1
                self.info = {"error": str(error)}
                return self._observation(player_name), reward, self.done, self.info
            if self.game.is_winner(player_name):
                self.done = True
                reward = 1
                self.info = {"winner": player_name}
                return self._observation(player_name), reward, self.done, self.info
            self.game.next_player()
        elif action_type == "meld_set" or action_type == "meld_sequence":
            cards = action.get("cards")
            if not isinstance(cards, list) or not all(isinstance(card, tuple) and len(card) == 2 for card in cards):
                reward = -1
                self.info = {"error": "Invalid meld payload"}
                return self._observation(player_name), reward, self.done, self.info
            meld_type = "set" if action_type == "meld_set" else "sequence"
            success = self.game.create_meld(player_name, [tuple(card) for card in cards], meld_type)
            if not success:
                reward = -1
                self.info = {"error": "Invalid meld"}
                return self._observation(player_name), reward, self.done, self.info
        elif action_type == "declare":
            if self.game.is_winner(player_name):
                self.done = True
                reward = 1
                self.info = {"winner": player_name}
            else:
                reward = -1
                self.info = {"error": "Cannot declare without empty hand"}
            return self._observation(player_name), reward, self.done, self.info
        else:
            reward = -1
            self.info = {"error": "Unknown action type"}
            return self._observation(player_name), reward, self.done, self.info

        observation = self._observation(self.game.current_player)
        self.info = {}
        return observation, reward, self.done, self.info

    def render(self) -> None:
        print("Current player:", self.game.current_player)
        print("Wild rank:", self.game.wild_rank)
        print("Top discard:", self.game.top_discard())
        print("Deck size:", len(self.game.deck.cards))
        for player, hand in self.game.players.items():
            print(f"{player}: {len(hand)} cards")
