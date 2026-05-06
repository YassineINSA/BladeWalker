# import os
# from stable_baselines3 import PPO, SAC
# from stable_baselines3.common.callbacks import CallbackList
# from stable_baselines3.common.env_util import make_vec_env
# from stable_baselines3.common.callbacks import BaseCallback
# from transporteur_env import RoboticArmTransporteurEnv
# from transporteur_train import CurriculumCallback 

# class PhaseSaveCallback(BaseCallback):
#     """
#     Callback qui sauvegarde le modèle à des timesteps spécifiques 
#     avec une nomenclature claire.
#     """
#     def __init__(self, algo_name, env_name, energy_name, jitter_name, save_dir, phase_timesteps, verbose=1):
#         super().__init__(verbose)
#         self.algo_name = algo_name
#         self.env_name = env_name
#         self.energy_name = energy_name
#         self.jitter_name = jitter_name
#         self.save_dir = save_dir
        
#         # Dictionnaire liant le timestep au nom de la phase (ex: {50000: "peu"})
#         self.phase_timesteps = phase_timesteps 

#     def _on_step(self) -> bool:
#         # Vérifie si le timestep actuel est un palier que l'on veut sauvegarder
#         if self.num_timesteps in self.phase_timesteps:
#             phase_name = self.phase_timesteps[self.num_timesteps]
            
#             # Création de la nomenclature claire
#             filename = f"{self.env_name}_{self.algo_name}_energie-{self.energy_name}_jitter-{self.jitter_name}_phase-{phase_name}"
#             save_path = os.path.join(self.save_dir, filename)
            
#             # Sauvegarde du modèle
#             self.model.save(save_path)
            
#             if self.verbose > 0:
#                 print(f"\n[SAUVEGARDE] Modèle enregistré pour la phase '{phase_name}' : {filename}.zip\n")
                
#         return True
    

# if __name__ == "__main__":
#     # --- 1. CONFIGURATION DE L'EXPÉRIENCE ---
#     env_name = "transporteur"
#     save_directory = "./models"
#     os.makedirs(save_directory, exist_ok=True)

#     niveaux_energie = {"faible": 0.005, "moyen": 0.05, "fort": 0.5}
#     niveaux_jitter = {"faible": 0.0, "moyen": 0.1, "fort": 1.0}
    
#     # Définition des paliers (timesteps) pour chaque algo
#     paliers_ppo = {50_000: "peu", 250_000: "moyen", 1_000_000: "tres"}
#     paliers_sac = {20_000: "peu", 80_000: "moyen", 300_000: "tres"}
    
#     total_timesteps_ppo = max(paliers_ppo.keys())
#     total_timesteps_sac = max(paliers_sac.keys())

#     # --- 2. BOUCLE SUR LES PÉNALITÉS ---
#     for nom_energie, coef_e in niveaux_energie.items():
#         for nom_jitter, coef_j in niveaux_jitter.items():
            
#             print(f"\n" + "="*50)
#             print(f"LANCEMENT ENTRAÎNEMENT : ÉNERGIE={nom_energie.upper()} | JITTER={nom_jitter.upper()}")
#             print("="*50 + "\n")
            
#             # Configuration de l'environnement avec les pénalités dynamiques
#             env_kwargs = {
#                 "segment_lengths": [1.0, 1.0],
#                 "energy_coef": coef_e,
#                 "jitter_coef": coef_j
#             }

#             # ==========================================
#             # ENTRAÎNEMENT PPO
#             # ==========================================
#             print(f"--- Entraînement PPO ---")
#             vec_env = make_vec_env(RoboticArmTransporteurEnv, n_envs=4, env_kwargs=env_kwargs)
#             for i in range(4):
#                 vec_env.env_method("set_difficulty", 0.1, indices=i)
            
#             curriculum_ppo = CurriculumCallback(total_timesteps=total_timesteps_ppo, initial_difficulty=0.1)
#             save_cb_ppo = PhaseSaveCallback("ppo", env_name, nom_energie, nom_jitter, save_directory, paliers_ppo)
            
#             # On combine les deux callbacks
#             callbacks_ppo = CallbackList([curriculum_ppo, save_cb_ppo])
            
#             model_ppo = PPO("MlpPolicy", vec_env, verbose=0, policy_kwargs=dict(net_arch=[64, 64]))
#             model_ppo.learn(total_timesteps=total_timesteps_ppo, callback=callbacks_ppo)
#             vec_env.close()

#             # ==========================================
#             # ENTRAÎNEMENT SAC
#             # ==========================================
#             print(f"--- Entraînement SAC ---")
#             env_sac = RoboticArmTransporteurEnv(**env_kwargs)
#             env_sac.set_difficulty(0.1)
            
#             curriculum_sac = CurriculumCallback(total_timesteps=total_timesteps_sac, initial_difficulty=0.1)
#             save_cb_sac = PhaseSaveCallback("sac", env_name, nom_energie, nom_jitter, save_directory, paliers_sac)
            
#             # On combine les deux callbacks
#             callbacks_sac = CallbackList([curriculum_sac, save_cb_sac])
            
#             model_sac = SAC("MlpPolicy", env_sac, verbose=0, policy_kwargs=dict(net_arch=[256, 256]))
#             model_sac.learn(total_timesteps=total_timesteps_sac, callback=callbacks_sac)
#             env_sac.close()

#     print("\nEXPÉRIMENTATION COMPLÈTE ! Tous les modèles ont été générés et sauvegardés.")

import os
# Force un affichage virtuel pour éviter les blocages sur macOS
os.environ["SDL_VIDEODRIVER"] = "dummy"

import glob
import pygame
import imageio
from stable_baselines3 import PPO, SAC

# Remplace par ton environnement (Pointeur ou Transporteur)
from transporteur_env import RoboticArmTransporteurEnv 

def record_model_video(model_path, video_path, env_kwargs, algo_class):
    # On force rgb_array pour extraire les pixels
    env = RoboticArmTransporteurEnv(**env_kwargs, render_mode="rgb_array")
    
    try:
        model = algo_class.load(model_path)
    except Exception as e:
        print(f"❌ Erreur de chargement pour {model_path}: {e}")
        env.close()
        return

    obs, _ = env.reset()
    env.set_difficulty(1.0) # On évalue sur la difficulté maximale

    frames = []
    episodes_done = 0
    
    while episodes_done < 3:
        # Évite le blocage de l'interface graphique sur Mac
        pygame.event.pump()
        
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        
        # On capture l'image générée par Pygame
        frame = env.render()
        if frame is not None:
            frames.append(frame)
        
        if terminated or truncated:
            obs, _ = env.reset()
            episodes_done += 1

    env.close()
    
    # On compile toutes les images en vidéo MP4 (à 30 FPS)
    if frames:
        imageio.mimsave(video_path, frames, fps=30)
        print(f"✅ Vidéo générée : {video_path}")
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