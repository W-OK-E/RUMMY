# Rummy

A modular Python implementation of the classic Rummy card game - but to be played by *agents* :)

### Quick start (using uv)

All startup, installs and test runs should use the provided uv environment wrapper from this directory.

1. Open a shell in the repository root and change into the RUMMY folder:

    cd RUMMY

2. Run tests and install dev deps (example):

    uv run python3 -m pip install --upgrade pip
    uv run python3 -m pip install pytest
    uv run python3 -m pytest -q

3. Run the example entrypoint (small simulation):

    uv run python3 Rummy.py

Package usage (importing in code)

- From your Python code you can import the environment and game directly:

    from rummy.env import RummyEnv
    from rummy.game import RummyGame

- Create an environment and reset to get the first observation:

    env = RummyEnv(["Alice", "Bob"], seed=42)
    obs = env.reset()

Testing and CI

- The repository contains unit tests under `tests/` that validate deck size, dealing, and meld/sequence validation.
- A GitHub Actions workflow at `.github/workflows/python-app.yml` runs the tests on push and pull requests.

Challenge notes

This repo is intended as a small challenge: some rules and edge cases are intentionally simplified and there are three suggested issues for contributors to improve:

- Fix winner detection and game-end flow
- Improve meld and wildcard validation rules
- Expand the RL observation/action API for agents

Contributing

- Open a PR with targeted changes and include/adjust tests to cover the change.
- The CI workflow will run the test-suite automatically.

License

- This project is provided as-is for educational and challenge purposes. Add a license file if you want to publish it.
