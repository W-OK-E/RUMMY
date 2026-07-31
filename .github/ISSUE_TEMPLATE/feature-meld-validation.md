name: Improve meld validation rules
about: Add support for full meld validation and joker handling in the Rummy engine.
title: Improve Rummy meld validation and wildcard rules
labels: enhancement
body:
  - type: markdown
    attributes:
      value: |
        The baseline Rummy engine validates simple melds, but several edge cases remain. Update the validation logic to support:
        - impure sets and sequences that use printed Jokers or selected wild ranks
        - same-suit sequence construction with wildcard fill cards
        - no duplicate cards and correct suit/rank constraints for valid melds
