from __future__ import annotations
import random
from typing import List, Tuple, Dict, Any
from .cards import Card


class RandomAgent:
    def __init__(self, seed: int | None = None):
        self._random = random.Random(seed)

    def choose_action(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        hand: List[Card] = observation["hand"]
        top_discard = observation["top_discard"]
        if top_discard is not None and self._random.random() < 0.5:
            return {"type": "draw_discard"}
        return {"type": "draw_deck"}

    def choose_discard(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        hand: List[Card] = observation["hand"]
        if not hand:
            return {"type": "declare"}
        card = self._random.choice(hand)
        return {"type": "discard_card", "card": card}
