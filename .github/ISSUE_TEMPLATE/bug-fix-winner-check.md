name: Fix Rummy winner detection
about: Correct the game completion and winner detection logic in the modular Rummy implementation.
title: Fix winner detection and end-of-game flow
labels: bug
body:
  - type: markdown
    attributes:
      value: |
        The current Rummy implementation should end the game as soon as a player has successfully melded and discarded all cards. Review `rummy/game.py` and `rummy/env.py` to ensure that:
        - empty hands are recognized as winning states
        - invalid actions do not advance the turn or corrupt the deck/discard piles
        - the discard pile is restocked when the deck runs out
