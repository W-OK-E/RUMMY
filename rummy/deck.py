from __future__ import annotations
import random
from typing import List
from .cards import all_cards, Card


class Deck:
    def __init__(self, seed: int | None = None):
        self._random = random.Random(seed)
        self.cards: List[Card] = all_cards()
        self.discard_pile: List[Card] = []
        self.shuffle()

    def shuffle(self) -> None:
        self._random.shuffle(self.cards)

    def draw(self) -> Card:
        if not self.cards:
            raise IndexError("No cards left in the deck")
        return self.cards.pop()

    def discard(self, card: Card) -> None:
        self.discard_pile.append(card)

    def draw_discard(self) -> Card:
        if not self.discard_pile:
            raise IndexError("No cards in the discard pile")
        return self.discard_pile.pop()

    def top_discard(self) -> Card | None:
        return self.discard_pile[-1] if self.discard_pile else None

    def restock_from_discard(self) -> None:
        if len(self.discard_pile) <= 1:
            raise ValueError("Not enough cards in the discard pile to restock the deck")
        top = self.discard_pile.pop()
        self.cards = list(self.discard_pile)
        self.discard_pile = [top]
        self.shuffle()
