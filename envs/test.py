from stable_baselines3 import PPO
from chicken_env import ChickenEnv

model = PPO.load("chicken_ppo_final")
env = ChickenEnv(render_mode="human")
obs, _ = env.reset()

episode = 1
steps = 0

while True:
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, _ = env.step(action)
    env.render()
    steps += 1

    if terminated:  # ← seulement si elle tombe, plus de truncated
        print(f"Épisode {episode} terminé (tombée après {steps} steps)")
        episode += 1
        steps = 0
        obs, _ = env.reset()