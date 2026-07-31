from rummy.env import RummyEnv
from rummy.agents import RandomAgent


def main() -> None:
    env = RummyEnv(["Alice", "Bob"], seed=42)
    agent = RandomAgent(seed=42)
    observation = env.reset()
    print("Starting Rummy environment")
    env.render()
    while not env.done:
        action = agent.choose_action(observation)
        observation, reward, done, info = env.step(action)
        if action["type"] in {"draw_deck", "draw_discard"}:
            discard = agent.choose_discard(observation)
            observation, reward, done, info = env.step(discard)
        print(f"Action: {action}, reward: {reward}, done: {done}")
        if done:
            print("Game finished", info)
            break
        observation = env._observation(env.game.current_player)
    print("Final state:")
    env.render()


if __name__ == "__main__":
    main()
