from .env import RummyEnv


def main() -> None:
    env = RummyEnv(["Alice", "Bob"])
    observation = env.reset()
    print("Starting Rummy environment")
    print("Current observation:", observation)
    env.render()


if __name__ == "__main__":
    main()
