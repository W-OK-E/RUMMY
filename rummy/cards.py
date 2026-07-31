from __future__ import annotations
from typing import List, Sequence, Tuple, Mapping

Card = Tuple[str, str]
SUITS: Sequence[str] = ("Spades", "Clubs", "Diamonds", "Hearts")
RANKS: Sequence[str] = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "JACK", "QUEEN", "KING", "JOKER")
STANDARD_ORDER = {rank: index for index, rank in enumerate(RANKS)}


def all_cards() -> List[Card]:
    return [(suit, rank) for suit in SUITS for rank in RANKS]


def is_wild(card: Card, wild_rank: str | None) -> bool:
    return card[1] == "JOKER" or (wild_rank is not None and card[1] == wild_rank)


def card_to_string(card: Card) -> str:
    return f"{card[1]} of {card[0]}"
