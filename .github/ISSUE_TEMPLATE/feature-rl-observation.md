name: Design RL-friendly observations and actions
about: Refine the Rummy environment so agents can interact without user prompts.
title: Improve RL environment observation/action design
labels: enhancement
body:
  - type: markdown
    attributes:
      value: |
        The current environment exposes a minimal action API, but there is an opportunity to make it more RL-friendly. Update `rummy/env.py` so that:
        - observations include the current hand, wild rank, top discard, and remaining card counts
        - actions are encoded as structured dictionaries instead of human input
        - invalid actions return a consistent penalty and do not corrupt game state
