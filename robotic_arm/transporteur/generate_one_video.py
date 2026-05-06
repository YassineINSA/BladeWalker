import os
import argparse
import pygame
import imageio
import numpy as np

# Force un affichage virtuel pour éviter les blocages sur macOS ou serveurs sans écran
os.environ["SDL_VIDEODRIVER"] = "dummy"

from stable_baselines3 import PPO, SAC
from transporteur_env import RoboticArmTransporteurEnv

def main():
    parser = argparse.ArgumentParser(description="Générer une vidéo de test pour un modèle spécifique.")
    parser.add_argument(
        "model_path", 
        type=str, 
        help="Chemin vers le fichier .zip du modèle (ex: models/mon_modele.zip)"
    )
    parser.add_argument(
        "--output", 
        type=str, 
        default="video_test.mp4", 
        help="Chemin de sortie pour la vidéo (par défaut: video_test.mp4)"
    )
    parser.add_argument(
        "--algo", 
        type=str, 
        choices=["ppo", "sac", "auto"], 
        default="auto", 
        help="Algorithme utilisé (ppo, sac, ou auto pour deviner via le nom du fichier)"
    )
    parser.add_argument(
        "--episodes", 
        type=int, 
        default=1, 
        help="Nombre d'épisodes à enregistrer (par défaut: 1)"
    )

    args = parser.parse_args()

    # Déduction automatique de l'algorithme si demandé
    algo_name = args.algo.lower()
    if algo_name == "auto":
        if "sac" in args.model_path.lower():
            algo_name = "sac"
            algo_class = SAC
        else:
            algo_name = "ppo"
            algo_class = PPO
        print(f"🤖 Algorithme déduit du nom de fichier : {algo_name.upper()}")
    else:
        algo_class = PPO if algo_name == "ppo" else SAC

    print(f"⏳ Chargement du modèle depuis : '{args.model_path}'...")
    try:
        model = algo_class.load(args.model_path)
    except Exception as e:
        print(f"❌ Erreur : Impossible de charger le modèle '{args.model_path}'.")
        print(f"Détails : {e}")
        return

    # Initialisation de l'environnement en mode rgb_array pour la capture
    env = RoboticArmTransporteurEnv(segment_lengths=[1.0, 1.0], render_mode="rgb_array")
    
    obs, _ = env.reset()
    
    # Si ton environnement possède la méthode set_difficulty (comme dans generate_videos.py)
    if hasattr(env, 'set_difficulty'):
        env.set_difficulty(1.0)
    elif hasattr(env, 'difficulty'):
        env.difficulty = 1.0

    print(f"🎥 Début de l'enregistrement de {args.episodes} épisode(s)...")

    # On force un premier rendu pour déclencher l'initialisation de pygame
    frame = env.render()
    frames = []
    if frame is not None:
        frames.append(frame)

    episodes_done = 0
    success_count = 0
    
    while episodes_done < args.episodes:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        
        # Capture de l'image
        frame = env.render()
        if frame is not None:
            frames.append(frame)
        
        # Pompage des évènements en toute sécurité pour éviter les blocages
        if pygame.display.get_init():
            pygame.event.pump()
        
        if terminated:
            success_count += 1

        if terminated or truncated:
            episodes_done += 1
            if episodes_done < args.episodes:
                obs, _ = env.reset()

    env.close()
    
    # Compilation et sauvegarde de la vidéo
    if frames:
        print(f"💾 Sauvegarde de la vidéo vers {args.output}...")
        imageio.mimsave(args.output, frames, fps=30)
        print(f"✅ Vidéo générée avec succès : {args.output} (Succès : {success_count}/{args.episodes})")
    else:
        print(f"⚠️ Aucune image capturée lors de l'exécution du modèle.")

if __name__ == "__main__":
    main()