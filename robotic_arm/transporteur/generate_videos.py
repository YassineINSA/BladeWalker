# import os
# os.environ["SDL_VIDEODRIVER"] = "dummy"
# import glob
# from stable_baselines3 import PPO, SAC
# from gymnasium.wrappers import RecordVideo

# # Remplace par ton environnement (Pointeur ou Transporteur)
# from transporteur_env import RoboticArmTransporteurEnv 

# def record_model_video(model_path, video_folder, video_name_prefix, env_kwargs, algo_class):
#     # On crée l'environnement en mode rgb_array pour la capture
#     base_env = RoboticArmTransporteurEnv(**env_kwargs, render_mode="rgb_array")
    
#     env = RecordVideo(
#         base_env, 
#         video_folder=video_folder,
#         name_prefix=video_name_prefix,
#         episode_trigger=lambda ep: ep < 3 # 3 épisodes par vidéo
#     )

#     try:
#         model = algo_class.load(model_path)
#     except Exception as e:
#         print(f"❌ Erreur de chargement pour {model_path}: {e}")
#         env.close()
#         return

#     obs, info = env.reset()
#     env.unwrapped.set_difficulty(1.0) # On évalue sur la difficulté maximale

#     episodes_done = 0
#     while episodes_done < 3:
#         action, _ = model.predict(obs, deterministic=True)
#         obs, reward, terminated, truncated, info = env.step(action)
        
#         if terminated or truncated:
#             obs, info = env.reset()
#             episodes_done += 1

#     env.close()
#     print(f"Vidéo générée : {video_name_prefix}")

# if __name__ == "__main__":
#     models_dir = "./models"
#     output_dir = "./videos_results"
#     os.makedirs(output_dir, exist_ok=True)

#     niveaux_energie = {"faible": 0.005, "moyen": 0.05, "fort": 0.5}
#     niveaux_jitter = {"faible": 0.0, "moyen": 0.1, "fort": 1.0}
#     algos = {"ppo": PPO, "sac": SAC}
#     phases = ["peu", "moyen", "tres"]
#     env_name = "transporteur" # ou "pointeur"

#     # On parcours toutes les combinaisons possibles
#     for nom_energie, coef_e in niveaux_energie.items():
#         for nom_jitter, coef_j in niveaux_jitter.items():
#             for algo_name, algo_class in algos.items():
#                 for phase in phases:
                    
#                     # Reconstruction du nom exact du fichier
#                     filename = f"{env_name}_{algo_name}_energie-{nom_energie}_jitter-{nom_jitter}_phase-{phase}"
#                     model_path = os.path.join(models_dir, filename + ".zip")
                    
#                     if os.path.exists(model_path):
#                         env_kwargs = {
#                             "segment_lengths": [1.0, 1.0],
#                             "energy_coef": coef_e,
#                             "jitter_coef": coef_j
#                         }
                        
#                         record_model_video(
#                             model_path=model_path,
#                             video_folder=output_dir,
#                             video_name_prefix=filename,
#                             env_kwargs=env_kwargs,
#                             algo_class=algo_class
#                         )
#                     else:
#                         print(f"⚠️ Fichier introuvable : {model_path}")

import os
# Force un affichage virtuel pour éviter les blocages sur macOS
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
import imageio
import numpy as np
from stable_baselines3 import PPO, SAC

# Remplace par ton environnement (Pointeur ou Transporteur)
from transporteur_env import RoboticArmTransporteurEnv 

# def record_model_video(model_path, video_path, env_kwargs, algo_class):
#     print(f"Génération de {video_path}...")
    
#     # On crée l'environnement. Note : PLUS DE RecordVideo ici !
#     env = RoboticArmTransporteurEnv(**env_kwargs, render_mode="rgb_array")
    
#     try:
#         model = algo_class.load(model_path)
#     except Exception as e:
#         print(f"❌ Erreur de chargement pour {model_path}: {e}")
#         env.close()
#         return

#     obs, _ = env.reset()
#     env.set_difficulty(1.0) # On évalue sur la difficulté maximale

#     frames = []
#     episodes_done = 0
    
#     while episodes_done < 3:
#         # Évite le blocage de l'interface graphique sur Mac
#         pygame.event.pump()
        
#         action, _ = model.predict(obs, deterministic=True)
#         obs, reward, terminated, truncated, info = env.step(action)
        
#         # On capture l'image générée par Pygame manuellement
#         frame = env.render()
#         if frame is not None:
#             frames.append(frame)
        
#         if terminated or truncated:
#             obs, _ = env.reset()
#             episodes_done += 1

#     env.close()
    
#     # On compile toutes les images en vidéo MP4 (à 30 FPS)
#     if frames:
#         imageio.mimsave(video_path, frames, fps=30)
#         print(f"✅ Vidéo générée avec succès : {video_path}")
#     else:
#         print(f"⚠️ Aucune image capturée pour {model_path}")

def record_model_video(model_path, video_path, env_kwargs, algo_class):
    print(f"Génération de {video_path}...")
    
    env = RoboticArmTransporteurEnv(**env_kwargs, render_mode="rgb_array")
    
    try:
        model = algo_class.load(model_path)
    except Exception as e:
        print(f"❌ Erreur de chargement pour {model_path}: {e}")
        env.close()
        return

    obs, _ = env.reset()
    env.set_difficulty(1.0) # On évalue sur la difficulté maximale

    # --- CORRECTION ICI ---
    # On force un premier rendu pour déclencher pygame.init() dans ton environnement
    frame = env.render()

    frames = []
    if frame is not None:
        frames.append(frame)

    episodes_done = 0
    
    while episodes_done < 3:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        
        frame = env.render()
        if frame is not None:
            frames.append(frame)
        
        # On peut maintenant pomper les évènements en toute sécurité
        if pygame.display.get_init():
            pygame.event.pump()
        
        if terminated or truncated:
            obs, _ = env.reset()
            episodes_done += 1

    env.close()
    
    if frames:
        imageio.mimsave(video_path, frames, fps=30)
        print(f"✅ Vidéo générée avec succès : {video_path}")
    else:
        print(f"⚠️ Aucune image capturée pour {model_path}")
        
if __name__ == "__main__":
    models_dir = "./models"
    output_dir = "./videos_results"
    os.makedirs(output_dir, exist_ok=True)

    niveaux_energie = {"faible": 0.005, "moyen": 0.05, "fort": 0.5}
    niveaux_jitter = {"faible": 0.0, "moyen": 0.1, "fort": 1.0}
    algos = {"ppo": PPO, "sac": SAC}
    phases = ["peu", "moyen", "tres"]
    env_name = "transporteur" # ou "pointeur"

    # On parcours toutes les combinaisons possibles
    for nom_energie, coef_e in niveaux_energie.items():
        for nom_jitter, coef_j in niveaux_jitter.items():
            for algo_name, algo_class in algos.items():
                for phase in phases:
                    
                    filename = f"{env_name}_{algo_name}_energie-{nom_energie}_jitter-{nom_jitter}_phase-{phase}"
                    model_path = os.path.join(models_dir, filename + ".zip")
                    video_path = os.path.join(output_dir, filename + ".mp4")
                    
                    # On évite de recalculer une vidéo qui existe déjà
                    if os.path.exists(video_path):
                        print(f"⏩ Vidéo déjà existante, ignorée : {filename}.mp4")
                        continue
                        
                    if os.path.exists(model_path):
                        env_kwargs = {
                            "segment_lengths": [1.0, 1.0],
                            "energy_coef": coef_e,
                            "jitter_coef": coef_j
                        }
                        
                        record_model_video(
                            model_path=model_path,
                            video_path=video_path,
                            env_kwargs=env_kwargs,
                            algo_class=algo_class
                        )
                    else:
                        print(f"⚠️ Fichier introuvable : {model_path}")