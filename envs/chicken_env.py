import gymnasium as gym
from gymnasium import spaces
import numpy as np
import Box2D
from Box2D.b2 import revoluteJointDef
import pygame

from physics_engine import PhysicsApp, capsule, create_world, world2screen, PPM
from chicken import build_chicken, draw_background, draw_chicken

W, H = 1100, 700

class ChickenEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 50}

    def __init__(self, render_mode=None):
        super().__init__()
        self.render_mode = render_mode
        self.dt = 1.0 / 50.0
        self.max_steps = 10_000

        # 4 moteurs : hipR, hipL, kneeR, kneeL
        self.action_space = spaces.Box(
            low=-1.0, high=1.0, shape=(4,), dtype=np.float32
        )

        # Observation : voir ci-dessous
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(14,), dtype=np.float32
        )

        self._b2world = None
        self.screen = None
        self.clock = None

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.steps = 0

        # Recrée le monde Box2D
        if self._b2world is not None:
            # Détruit tous les bodies
            for body in list(self._b2world.bodies):
                self._b2world.DestroyBody(body)
        self._b2world = create_world()

        joints, self.bodies = build_chicken(self._b2world)
        (self.hipR, self.hipL,
         self.kneeR, self.kneeL,
         self.neck_joint) = joints

        self.start_x = float(self.bodies['torso'].position.x)
        self.prev_x  = self.start_x
        self.time    = 0.0

        return self._get_obs(), {}

    def _get_obs(self):
        torso  = self.bodies['torso']
        thighR = self.bodies['thighR']
        thighL = self.bodies['thighL']
        calfR  = self.bodies['calfR']
        calfL  = self.bodies['calfL']

        return np.array([
            # Torse
            torso.angle,
            torso.angularVelocity,
            torso.linearVelocity.x,
            torso.linearVelocity.y,
            torso.position.y,

            # Hanche droite / gauche
            self.hipR.angle,
            self.hipL.angle,

            # Genou droit / gauche
            self.kneeR.angle,
            self.kneeL.angle,

            # Vitesses angulaires membres
            thighR.angularVelocity,
            thighL.angularVelocity,
            calfR.angularVelocity,
            calfL.angularVelocity,

            # Position Y du calf (contact sol approximatif)
            min(calfR.position.y, calfL.position.y),
        ], dtype=np.float32)

    def step(self, action):
        MAX_TORQUE_SPEED = 8.0

        self.hipR.motorSpeed  = float(action[0]) * MAX_TORQUE_SPEED
        self.hipL.motorSpeed  = float(action[1]) * MAX_TORQUE_SPEED
        self.kneeR.motorSpeed = float(action[2]) * MAX_TORQUE_SPEED
        self.kneeL.motorSpeed = float(action[3]) * MAX_TORQUE_SPEED

        self._b2world.Step(self.dt, 8, 3)
        self.steps += 1
        self.time  += self.dt

        obs = self._get_obs()

        torso     = self.bodies['torso']
        torso_y   = float(torso.position.y)
        torso_ang = float(torso.angle)
        x         = float(torso.position.x)

        forward = (x - self.prev_x) / self.dt
        self.prev_x = x

        # --- Récompense ---

        # 1. Posture droite = priorité absolue
        #    Si elle est droite et haute → gros bonus
        bonus_posture = max(0.0, 1.0 - abs(torso_ang) * 2.0)   # 1.0 si droit, 0.0 si >0.5 rad
        bonus_hauteur = max(0.0, (torso_y - 3.0) / 2.0)         # 1.0 si y=5, 0.0 si y=3
        reward = 2.0 * bonus_posture * bonus_hauteur             # les deux doivent être bons

        # 2. Avancer SEULEMENT si elle est déjà droite
        if bonus_posture > 0.5 and bonus_hauteur > 0.3:
            reward += forward * 0.5

        # 3. Pénalité énergie
        reward -= 0.001 * float(np.sum(np.square(action)))

        # --- Fin d'épisode : torse touche le sol ---
        terminated = bool(torso_y < 2.0)
        truncated  = bool(self.steps >= self.max_steps)

        if terminated:
            reward -= 10.0

        return obs, reward, terminated, truncated, {}
    
    def render(self):
        if self.render_mode != "human":
            return

        if self.screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode((W, H))
            pygame.display.set_caption("Chicken RL")
            self.clock = pygame.time.Clock()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()

        self.screen.fill((255, 243, 220))
        draw_background(self.screen, self.time)
        draw_chicken(self.screen, self.bodies)
        pygame.display.flip()
        self.clock.tick(50)

    def close(self):
        if self.screen is not None:
            pygame.quit()
            self.screen = None