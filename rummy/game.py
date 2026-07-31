from __future__ import annotations
from typing import Dict, List, Optional, Sequence, Tuple

from .cards import Card, RANKS, STANDARD_ORDER, SUITS, is_wild
from .deck import Deck


class RummyGame:
    def __init__(self, player_names: Sequence[str], seed: int | None = None):
        if len(player_names) < 2 or len(player_names) > 6:
            raise ValueError("Rummy requires between 2 and 6 players")
        self.player_names: List[str] = list(player_names)
        self.seed = seed
        self.players: Dict[str, List[Card]] = {player: [] for player in self.player_names}
        self.wild_rank: Optional[str] = None
        self.deck: Deck = Deck(seed=self.seed)
        self.melds: Dict[str, List[List[Card]]] = {player: [] for player in self.player_names}
        self.current_player_index: int = 0
        self.reset()

    def reset(self) -> None:
        self.deck = Deck(seed=self.seed)
        self.players = {player: [] for player in self.player_names}
        self.melds = {player: [] for player in self.player_names}
        self.current_player_index = 0
        self.wild_rank = None
        self.deal()
        self.select_wild_joker()
        self.discard_first_card()

    def deal(self, cards_per_player: int = 13) -> None:
        for _ in range(cards_per_player):
            for player in self.player_names:
                self.players[player].append(self.deck.draw())

    def select_wild_joker(self) -> None:
        wild_card = self.deck.draw()
        self.wild_rank = wild_card[1]
        self.deck.discard(wild_card)

    def discard_first_card(self) -> None:
        self.deck.discard(self.deck.draw())

    @property
    def current_player(self) -> str:
        return self.player_names[self.current_player_index]

    def top_discard(self) -> Optional[Card]:
        return self.deck.top_discard()

    def draw_from_deck(self, player_name: str) -> Card:
        if not self.deck.cards and len(self.deck.discard_pile) > 1:
            self.deck.restock_from_discard()
        card = self.deck.draw()
        self.players[player_name].append(card)
        return card

    def draw_from_discard(self, player_name: str) -> Card:
        card = self.deck.draw_discard()
        self.players[player_name].append(card)
        return card

    def discard_card(self, player_name: str, card: Card) -> None:
        if card not in self.players[player_name]:
            raise ValueError("Cannot discard a card not in the player's hand")
        self.players[player_name].remove(card)
        self.deck.discard(card)

    def _validate_card_set(self, cards: Sequence[Card]) -> bool:
        if len(cards) < 3 or len(cards) > 4:
            return False
        if len(set(cards)) != len(cards):
            return False
        natural_cards = [card for card in cards if not is_wild(card, self.wild_rank)]
        wild_cards = [card for card in cards if is_wild(card, self.wild_rank)]
        if not natural_cards:
            return False
        if len(wild_cards) >= len(natural_cards):
            return False
        if len(wild_cards) > 2:
            return False
        natural_ranks = {rank for _, rank in natural_cards}
        if len(natural_ranks) != 1:
            return False
        suits = {suit for suit, rank in natural_cards}
        return len(suits) == len(natural_cards)

    def _validate_card_sequence(self, cards: Sequence[Card]) -> bool:
        if len(cards) < 3:
            return False
        if len(set(cards)) != len(cards):
            return False
        natural_cards = [card for card in cards if not is_wild(card, self.wild_rank)]
        wild_cards = [card for card in cards if is_wild(card, self.wild_rank)]
        if not natural_cards:
            return False
        if len(wild_cards) > 2:
            return False
        if len(wild_cards) >= len(natural_cards):
            return False
        suits = {suit for suit, rank in natural_cards}
        if len(suits) != 1:
            return False
        natural_ranks = [STANDARD_ORDER[rank] for _, rank in natural_cards]
        if len(set(natural_ranks)) != len(natural_ranks):
            return False
        suit = natural_cards[0][0]
        sequence_length = len(cards)
        for start_index in range(0, len(RANKS) - sequence_length + 1):
            target_ranks = set(range(start_index, start_index + sequence_length))
            if set(natural_ranks).issubset(target_ranks):
                return True
        return False

    def create_meld(self, player_name: str, cards: Sequence[Card], meld_type: str) -> bool:
        if not all(card in self.players[player_name] for card in cards):
            return False
        validator = self._validate_card_set if meld_type == "set" else self._validate_card_sequence
        if not validator(cards):
            return False
        for card in cards:
            self.players[player_name].remove(card)
        self.melds[player_name].append(list(cards))
        return True

    def is_winner(self, player_name: str) -> bool:
        return len(self.players[player_name]) == 0

    def next_player(self) -> None:
        self.current_player_index = (self.current_player_index + 1) % len(self.player_names)

    def summarize(self) -> Dict[str, object]:
        return {
            "wild_rank": self.wild_rank,
            "top_discard": self.top_discard(),
            "deck_count": len(self.deck.cards),
            "player_hands": {player: len(hand) for player, hand in self.players.items()},
        }
