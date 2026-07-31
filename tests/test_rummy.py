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


# Challenge tests for contributors

# The tests in this file are intentionally commented out by default. They represent
# the additional checks that a contributor should satisfy when addressing the
# repository's challenge issues. To run them locally, uncomment the tests you want
# to execute (remove the leading # from the test function and any helper imports)
# and run: `uv run python3 -m pytest tests/test_challenge_issues.py -q`

# Note: these tests are stricter than the baseline tests and are meant to be run only on PRs submitted for
# a issue


from rummy.game import RummyGame
from rummy.env import RummyEnv
from rummy.cards import Card


def test_winner_detection_when_hand_becomes_empty():
    """A player who successfully melds and discards down to zero cards should
    be immediately recognized as the winner. This should work through both the
    RummyGame API and the RummyEnv (declare action).
    """
    game = RummyGame(["P1", "P2"], seed=2026)
    # Force a simple scenario: give P1 an empty hand and P2 some cards
    game.players = {"P1": [], "P2": [("Hearts", "A")]}
    # Game-level check
    assert game.is_winner("P1") is True
    # Environment-level declare should succeed and mark done
    env = RummyEnv(["P1", "P2"], seed=2026)
    env.game = game
    obs, reward, done, info = env.step({"type": "declare"})
    assert done is True
    assert reward == 1
    assert info.get("winner") == "P1"


def test_meld_validation_rejects_excessive_jokers_and_duplicate_cards():
    """Meld validation must:
     - reject melds that contain duplicate exact cards
     - reject melds where jokers/wilds are not used according to rules (e.g.,
       number of wilds must be strictly less than number of natural cards and
       maximum wilds allowed is 2)
    """
    game = RummyGame(["A", "B"], seed=42)
    game.wild_rank = "7"
    # duplicate exact same card should be invalid
    duplicate_meld = [("Spades", "5"), ("Spades", "5"), ("Clubs", "5")]
    assert game._validate_card_set(duplicate_meld) is False
    # too many jokers relative to naturals should be invalid
    bad_meld = [("Hearts", "5"), ("Clubs", "JOKER"), ("Diamonds", "JOKER")]
    assert game._validate_card_set(bad_meld) is False


def test_rl_invalid_action_does_not_advance_turn_or_corrupt_state():
    """Submitting an invalid action through the environment should return a
    penalty (negative reward) and must not advance the current player or
    mutate the deck/discard piles.
    """
    env = RummyEnv(["A", "B"], seed=99)
    obs = env.reset()
    before_player = env.game.current_player
    before_deck = len(env.game.deck.cards)
    before_discard = len(env.game.deck.discard_pile)
    observation, reward, done, info = env.step({"type": "discard_card", "card": ("Hearts", "FAKE")})
    assert reward < 0
    # player should remain the same because the action was invalid
    assert env.game.current_player == before_player
    # deck and discard pile should be unchanged
    assert len(env.game.deck.cards) == before_deck
    assert len(env.game.deck.discard_pile) == before_discard

