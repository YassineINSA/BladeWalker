from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import CheckpointCallback
from chicken_env import ChickenEnv

env = make_vec_env(ChickenEnv, n_envs=4)  # 4 envs parallèles

checkpoint = CheckpointCallback(
    save_freq=25_000,          # sauvegarde plus souvent
    save_path="./checkpoints/",
    name_prefix="chicken_ppo"
)

model = PPO(
    "MlpPolicy",
    env,
    verbose=1,
    learning_rate=1e-3,        # plus agressif que 3e-4
    n_steps=1024,              # réduit pour apprendre plus vite
    batch_size=64,
    n_epochs=15,               # plus de passes sur chaque batch
    gamma=0.99,
    gae_lambda=0.95,
    clip_range=0.2,
    tensorboard_log="./logs/"
)

model.learn(total_timesteps=500_000, callback=checkpoint)
model.save("chicken_ppo_final")
print("Terminé !")