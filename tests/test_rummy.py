from rummy.cards import RANKS, is_wild
from rummy.deck import Deck
from rummy.env import RummyEnv
from rummy.game import RummyGame


def test_deck_contains_expected_card_count() -> None:
    deck = Deck()
    assert len(deck.cards) == len(RANKS) * 4
    assert deck.top_discard() is None


def test_rummy_game_deals_hands_and_sets_wild_joker() -> None:
    game = RummyGame(["Alice", "Bob"], seed=123)
    assert game.wild_rank in RANKS
    assert game.top_discard() is not None
    assert len(game.players["Alice"]) == 13
    assert len(game.players["Bob"]) == 13
    assert sum(len(hand) for hand in game.players.values()) == 26


def test_set_validation_allows_exactly_one_wild_in_three_card_set() -> None:
    game = RummyGame(["Alice", "Bob"], seed=123)
    game.wild_rank = "6"
    cards = [("Hearts", "5"), ("Clubs", "5"), ("Spades", "JOKER")]
    assert game._validate_card_set(cards)
    cards = [("Hearts", "5"), ("Clubs", "JOKER"), ("Diamonds", "JOKER")]
    assert not game._validate_card_set(cards)


def test_sequence_validation_accepts_wildcard_fillers() -> None:
    game = RummyGame(["Alice", "Bob"], seed=123)
    game.wild_rank = "9"
    cards = [("Hearts", "8"), ("Hearts", "JOKER"), ("Hearts", "10")]
    assert game._validate_card_sequence(cards)
    cards = [("Hearts", "8"), ("Clubs", "JOKER"), ("Hearts", "10")]
    assert game._validate_card_sequence(cards)


def test_env_draw_discard_and_discard_cycle_produces_valid_observation() -> None:
    env = RummyEnv(["Alice", "Bob"], seed=123)
    observation = env.reset()
    assert observation["player"] == "Alice"
    assert observation["deck_size"] >= 28
    deck_before = observation["deck_size"]
    env.step({"type": "draw_deck"})
    obs_after_draw, reward, done, info = env.step({"type": "discard_card", "card": env.game.players[env.game.current_player][-1]})
    assert reward == 0
    assert not done
    assert "error" not in info
    assert obs_after_draw["deck_size"] == deck_before - 1


def test_env_invalid_action_returns_penalty() -> None:
    env = RummyEnv(["Alice", "Bob"], seed=123)
    env.reset()
    observation, reward, done, info = env.step({"type": "discard_card", "card": ("Hearts", "JOKER")})
    assert reward == -1
    assert done is False
    assert "error" in info
