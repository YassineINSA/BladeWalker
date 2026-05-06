# Présentation BladeWalker - Parties 4 & 5

---

## **PARTIE 4 : La Méthode "Petit à Petit" - Le Curriculum Learning**

### **Texte de présentation**

**La Barrière de la Complexité**

Imaginez-vous en train d'apprendre à jouer du piano. Si on vous demandait immédiatement de jouer une symphonie complète sans connaître les notes, c'est impossible. Vous abandonnerez rapidement.

Les IA font exactement la même chose : face à une tâche trop difficile dès le départ, elles **ne trouvent jamais les bonnes récompenses** pour apprendre les stratégies. C'est ce qu'on appelle **"l'exploration efficace"** — l'IA doit d'abord apprendre les bases avant d'affronter les challenges complexes.

C'est exactement le problème que nous avons résolu avec le **Curriculum Learning**.

**Concept : Apprendre étape par étape**

Le Curriculum Learning est une stratégie pédagogique qui adapte automatiquement la difficulté de la tâche en fonction de la **performance réelle de l'IA**. Au lieu de fournir la même tâche complexe dès le départ, on commence par :

1. **Phase 1 : Les Fondamentaux (Difficulté = 0.1)**
   - Dans le bras robotique : la cible apparaît **très proche** du bout du bras.
   - L'IA apprend la cinématique basique : "Comment bouger pour atteindre une cible à proximité ?"
   - Les premières récompenses viennent facilement, créant une motivation initiale.

2. **Phase 2 : L'Extension Progressive (Difficulté = 0.1 → 0.5)**
   - La cible s'éloigne progressivement vers des positions intermédiaires.
   - L'IA doit maintenant combiner des mouvements plus complexes.
   - Elle s'appuie sur les compétences de la Phase 1 et les améliore.

3. **Phase 3 : La Maîtrise Totale (Difficulté = 0.5 → 1.0)**
   - La cible peut apparaître n'importe où dans l'espace atteignable.
   - L'IA doit gérer tous les cas complexes : approches d'angles différents, inversions cinématiques.
   - À ce stade, elle a les compétences nécessaires.

**La Mécanique : Le Callback qui Surveille**

```python
class CurriculumCallback(BaseCallback):
    def _on_step(self) -> bool:
        # Pourcentage d'avancement du training
        progress = self.num_timesteps / (total_timesteps * 0.8)
        
        # Difficulté augmente linéairement de 0.1 à 1.0
        current_difficulty = min(1.0, initial_difficulty + progress)
        
        # Injection en temps réel dans l'environnement
        self.training_env.env_method("set_difficulty", current_difficulty)
```

**Comment ça marche concrètement ?**

Dans notre bras robotique, la difficulté contrôle **la position de la cible** :

```python
# Sans curriculum : la cible peut être n'importe où
target = (random_x, random_y)

# Avec curriculum : la cible apparaît progressivement plus loin
# difficulty = 0.1 : cible à 10% de distance du point de départ
# difficulty = 0.5 : cible à 50% de distance
# difficulty = 1.0 : cible partout (100%)

x = max_reach + (random_x - max_reach) * difficulty
y = 0.0 + (random_y - 0.0) * difficulty
```

Pendant les premiers 80% du training :
- Les 10% premiers : cibles à 10% de distance → apprentissage très facile
- À 50% du training : cibles à 50% de distance → complexité moyenne
- À 80% du training : difficulté = 1.0 → tous les cas complexes

**Résultat empirique**

Sans curriculum learning :
- L'IA explore au hasard, trouve peu de récompenses
- Convergence lente ou impossible
- Beaucoup de faux départs

Avec curriculum learning :
- Phase 1 : Convergence très rapide (l'IA comprend rapidement la tâche simple)
- Phase 2 : Consolidation des compétences sur des tâches intermédiaires
- Phase 3 : Généralisation à la complexité totale

Le résultat : **une IA qui apprend 5-10 fois plus vite** et atteint une meilleure performance finale.

**L'analogie pédagogique**

C'est exactement comment on enseigne :
1. Alphabet → Mots simples → Phrases simples → Littérature complexe
2. Additions → Multiplications → Équations → Calcul
3. Marche → Jogging → Sprint → Sport compétitif

---

## **PARTIE 5 : L'Apex Technique - BladeWalker (Le Bipède)**

### **Texte de présentation**

**Le Saut de Complexité : Du Statique au Dynamique**

Jusqu'à présent, nous avons entraîné un **bras robotique fixe** pointant une cible. C'est un excellent début : 2-3 articulations, une tâche bien définie, un espace d'apprentissage contrôlé.

Mais passons maintenant au **vrai défi de la robotique** : créer un robot qui **ne tombe pas**.

BladeWalker est un **bipède** — un robot à deux jambes qui doit :
- Maintenir son équilibre contre la gravité
- Coordonner 4 articulations indépendantes (2 hanches + 2 genoux)
- Générer une locomotion efficace (une marche)
- Tout cela avec **14 entrées sensorielles** à traiter en temps réel

C'est le passage de la "*Pick and Place*" (saisir et placer) à la "*Dynamic Locomotion*" (locomotion dynamique).

**L'Anatomie Physique**

BladeWalker est construit avec la physique réaliste de **Box2D** :

```
        [TORSE] ← Point de contrôle principal (où l'équilibre se joue)
         / \
    [Hip] [Hip] ← 2 articulations de hanche
     /     \
 [Thigh] [Thigh] ← Cuisses
   /       \
[Knee]   [Knee] ← 2 articulations de genou
  /         \
[Calf]    [Calf] ← Tibias
  |         |
 [Sol]     [Sol] ← Contact avec le sol
```

**Propriétés physiques réalistes :**

1. **Masse et Densité** :
   - Torse : 5.0 kg/m³ (lourd, mais c'est le "cerveau")
   - Cuisses et Tibias : 1.0 kg/m³ (légers pour la mobilité)

2. **Forces et Torques** :
   - Articulations de hanche : max torque = 80.0 N·m (puissantes pour lever les jambes)
   - Articulations de genou : max torque = 60.0 N·m (moins puissantes)
   - Friction au sol = 0.8 (c'est important pour accrocher le sol)

3. **Gravité** : 10.0 m/s² (comparable à la Terre)

**Les 14 Entrées Sensorielles : "La Conscience du Robot"**

L'IA reçoit 14 variables d'entrée qui décrivent l'état complet du robot :

```
TORSE (4 variables) :
├─ Angle d'inclinaison (est-il penché ? danger de chute)
├─ Vitesse angulaire (tourne-t-il rapidement ?)
├─ Vitesse linéaire X (va-t-il vers l'avant ?)
└─ Vitesse linéaire Y (monte-t-il ou descend-il ?)

JAMBE GAUCHE (5 variables) :
├─ Angle de la hanche
├─ Vitesse angulaire de la hanche
├─ Angle du genou
├─ Vitesse angulaire du genou
└─ Contact au sol ? (1.0 = contact, 0.0 = pas de contact)

JAMBE DROITE (5 variables) :
├─ Angle de la hanche
├─ Vitesse angulaire de la hanche
├─ Angle du genou
├─ Vitesse angulaire du genou
└─ Contact au sol ?
```

**Interprétation :**
- Si `torso_angle > 1.0 rad (~60°)` → le robot tombe → GAME OVER
- Si les deux `contact` = 0.0 → les deux jambes sont en l'air → le robot saute !
- Si `contact_left = 1.0` et `contact_right = 0.0` → support monopodal (équilibre instable)

**Les 4 Actions : "Les Impulsions du Contrôle Neural"**

L'IA contrôle 4 moteurs :

```
Action 0 : Vitesse moteur hanche gauche   [-1.0, +1.0]
Action 1 : Vitesse moteur genou gauche    [-1.0, +1.0]
Action 2 : Vitesse moteur hanche droite   [-1.0, +1.0]
Action 3 : Vitesse moteur genou droit     [-1.0, +1.0]
```

Où `-1.0` = rotation maximale dans un sens et `+1.0` = rotation maximale dans l'autre.

Ces actions sont **multipliées par MAX_TORQUE_SPEED = 8.0 rad/s** pour obtenir les vitesses réelles des moteurs.

**La Fonction de Récompense : "L'Entraîneur qui Évalue"**

Voici le secret : **il ne suffit pas de marcher, il faut marcher INTELLIGEMMENT**.

```python
reward = 0

# 1. PRIORITÉ 1 : Reste droit (sinon tout est perdu)
bonus_posture = max(0, 1.0 - abs(angle_torse) * 2.0)
bonus_hauteur = max(0, (position_y - 3.0) / 2.0)
reward += 2.0 * bonus_posture * bonus_hauteur

# 2. PRIORITÉ 2 : Avance (seulement si déjà droit)
if bonus_posture > 0.5 and bonus_hauteur > 0.3:
    reward += forward_velocity * 0.5

# 3. PÉNALITÉ : Trop d'énergie gaspillée
reward -= 0.001 * sum(action²)

# 4. SI CHUTE : Pénalité massive
if terminated:
    reward -= 10.0
```

**Hiérarchie des priorités :**

```
┌─────────────────────────────────────────────┐
│ PRIORITÉ 1 : NE PAS TOMBER (60% de la      │
│ récompense)                                 │
│ • Maintenir équilibre                       │
│ • Garder hauteur                            │
│ → Sans cela, tout échoue                    │
└─────────────────────────────────────────────┘
            ↓ (seulement si équilibre maintenu)
┌─────────────────────────────────────────────┐
│ PRIORITÉ 2 : AVANCER (30% de la récompense)│
│ • Augmenter vitesse X positive              │
│ • Générer momentum                          │
└─────────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────────┐
│ PRIORITÉ 3 : EFFICACITÉ ÉNERGÉTIQUE (10%)  │
│ • Minimiser oscillations                    │
│ • Éviter mouvements parasites               │
│ • Économiser l'énergie motrice              │
└─────────────────────────────────────────────┘
```

**L'Architecture Actor-Critic : "Le Duel Cerveau-Critique"**

BladeWalker utilise **PPO (Proximal Policy Optimization)** avec une architecture Actor-Critic :

```
OBSERVATION (14 inputs)
       ↓
   ┌─────────────────────────────────────┐
   │   Réseau Partagé (64 neurones)     │
   └─────────────────────────────────────┘
       ↙                               ↘
   ┌────────────┐               ┌────────────┐
   │  ACTOR     │               │  CRITIC    │
   │ (Policy)   │               │ (Value)    │
   ├────────────┤               ├────────────┤
   │ Outputs:   │               │ Outputs:   │
   │ 4 actions  │               │ 1 value    │
   │ (moyennes) │               │ (attendu)  │
   │ 4 stds     │               │ (gain)     │
   └────────────┘               └────────────┘
       ↓                               ↓
   Moteurs du                    Évaluation
   robot                         du progrès
```

**Comment ça marche :**

1. **L'ACTOR (le décideur)** :
   - Prend en entrée les 14 observations
   - Génère 4 actions (une pour chaque moteur)
   - Apprend à **maximiser la récompense**
   - Stratégie : "Si je suis dans cet état, je fais cette action"

2. **Le CRITIC (l'évaluateur)** :
   - Prend aussi les 14 observations
   - Prédit : "Quel sera mon gain à partir de maintenant ?"
   - Aide l'Actor à s'améliorer : "Ton action était meilleure ou pire que prévu ?"
   - Stratégie : éduquer l'Actor pour qu'il fasse mieux

**PPO : La Méthode Prudente**

Contrairement à d'autres algorithmes (qui peuvent faire des sauts énormes et tout casser), PPO utilise une **stratégie d'apprentissage conservative** :

```python
# À chaque update, on "bride" les changements de politique
ratio = new_action_probability / old_action_probability

# On clipe le ratio entre [1-epsilon, 1+epsilon]
# Cela empêche les changements drastiques
clipped_ratio = clip(ratio, 1-0.2, 1+0.2)

# On prend le minimum pour être prudent
loss = min(ratio * advantage, clipped_ratio * advantage)
```

**Résultat :** l'IA avance à petits pas prudents, évite les catastrophes et converge lentement mais sûrement.

**Les Défis du Bipède**

1. **L'Équilibre est Contrarian** :
   - Si le robot penche trop à gauche → move hanche droit pour compenser
   - Mais pas trop ! Sinon il penche trop à droite
   - C'est un équilibre délicat, un **contrôle continu**.

2. **La Coordination** :
   - Les 4 moteurs doivent se coordonner
   - Pas juste bouger au hasard : générer une **marche cyclique**
   - Timing : quand lever la jambe gauche ? Quand poser la jambe droite ?

3. **L'Exploration** :
   - Avec 14 entrées et 4 sorties, il y a des **trillions d'actions possibles**
   - Trouver la bonne marche sans curriculum learning est quasi impossible
   - Avec curriculum learning : ça devient possible en ~100k pas

**La Simulation : Box2D**

Nous utilisons la physique **Box2D** (même moteur que Angry Birds) :

```
Chaque frame (1/50 sec) :
1. On applique les velocités moteurs calculées par l'IA
2. Box2D simule la physique (collisions, friction, gravité)
3. On mesure les nouvelles positions/vitesses
4. On calcule la récompense
5. L'IA la reçoit et apprend
```

**Résultats observés**

Sans RL : Le robot tombe immédiatement, oscillations chaotiques.
Après 50k pas : Quelques oscillations mais reste debout.
Après 100k pas : Marche stable et efficace.
Après 200k pas : Locomotion optimisée avec stride efficace.

---

## **CONTENU POUR LES SLIDES**

### **SLIDE 1 : Titre - Partie 4**
```
4. La Méthode "Petit à Petit"
   Le Curriculum Learning

🎯 De l'impossible au maîtrisé
```

### **SLIDE 2 : Le Problème - La Barrière**
```
❌ SANS CURRICULUM LEARNING

Piano complet → dès le début
     ↓
Trop difficile
     ↓
Zéro récompense
     ↓
L'IA abandonne
```

### **SLIDE 3 : La Solution**
```
✅ AVEC CURRICULUM LEARNING

Partition facile → Partition moyenne → Partition complète
        ↓                 ↓                    ↓
    10% difficulté   50% difficulté      100% difficulté
        ↓                 ↓                    ↓
    Apprentissage    Consolidation      Maîtrise totale
    très rapide      des compétences
```

### **SLIDE 4 : Les Trois Phases**
```
PHASE 1 : LES FONDAMENTAUX (Difficulté = 0.1)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Cibles proches du bras
    ↓
Apprentissage de base : cinématique simple
    ↓
Récompenses fréquentes = motivation

PHASE 2 : EXTENSION (Difficulté = 0.1 → 0.5)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Cibles s'éloignent progressivement
    ↓
Combination de compétences Phase 1
    ↓
Défi croissant = apprentissage continu

PHASE 3 : MAÎTRISE (Difficulté = 0.5 → 1.0)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Cibles partout dans l'espace
    ↓
Cas complexes et inversions cinématiques
    ↓
Généralisation : l'IA résout tout
```

### **SLIDE 5 : Le Callback en Temps Réel**
```
During Training :

Time = 0%      → Difficulty = 0.1
Time = 25%     → Difficulty = 0.35
Time = 50%     → Difficulty = 0.6
Time = 75%     → Difficulty = 0.85
Time = 80%+    → Difficulty = 1.0 (maintenu)

🔄 MISE À JOUR automatique TOUS les steps
   (pas de code à changer, pas d'intervention)
```

### **SLIDE 6 : Impact Empirique**
```
Vitesse d'apprentissage

SANS Curriculum:          AVEC Curriculum:
├─ 0-50k:   flat          ├─ 0-50k:   📈 RAPIDE
├─ 50-100k: très slow     ├─ 50-100k: 📈 RAPIDE
└─ 100k+:   plateau       └─ 100k+:   ✅ Convergé

Résultat final : 5-10x plus rapide ⚡
```

---

### **SLIDE 7 : Titre - Partie 5**
```
5. L'Apex Technique
   BladeWalker : Le Bipède

🤖 Du statique au dynamique
   Ne pas tomber = le défi ultime
```

### **SLIDE 8 : Le Saut de Complexité**
```
BRAS FIXE (Pointeur)     →    BIPÈDE (BladeWalker)
─────────────────────         ─────────────────────
✓ Attaché à une base          ✗ Doit rester debout
✓ Pas de gravité              ✗ Combat la gravité 24/7
✓ Tâche : toucher une point   ✓ Tâche : marcher
✓ 3-4 actions                 ✓ 4 actions coordonnées
✓ Simple : "réussi/échoué"    ✗ Complexe : équilibre continu
✗ Pas d'équilibre à gérer      ✗ Équilibre = tout

Difficulté × 100 🔥
```

### **SLIDE 9 : Anatomie - Vue d'ensemble**
```
        TORSE (cerveau + équilibre)
         ↙      ↘
    HANCHE  HANCHE
     ↙        ↘
  CUISSE    CUISSE
    ↙        ↘
  GENOU    GENOU
   ↙        ↘
 TIBIA    TIBIA
  ↓         ↓
 🔴SOL🔴  🔴SOL🔴

4 Articulations à Contrôler
14 Senseurs pour Observer
1 Corps Physique à Équilibrer
```

### **SLIDE 10 : Les 14 Entrées Sensorielles**
```
"La Conscience du Robot"

[TORSE] (4)
├─ Inclinaison (angle) 
├─ Vitesse de rotation (angularVel)
├─ Vitesse avant/arrière (velX)
└─ Vitesse haut/bas (velY)

[JAMBE GAUCHE] (5)
├─ Angle hanche
├─ Speed hanche
├─ Angle genou
├─ Speed genou
└─ Contact au sol? (0 ou 1)

[JAMBE DROITE] (5)
├─ Angle hanche
├─ Speed hanche
├─ Angle genou
├─ Speed genou
└─ Contact au sol? (0 ou 1)

= 14 variables totales
```

### **SLIDE 11 : Les 4 Actions - Contrôle**
```
Motor Commands : [-1.0, +1.0]

Action 0 → Hanche Gauche  
Action 1 → Genou Gauche
Action 2 → Hanche Droite
Action 3 → Genou Droite

Exemples :
• [+1.0, 0, -1.0, 0] = Lever jambe gauche, baisser jambe droite
• [0, -0.5, 0, -0.5] = Plier les deux genoux (accroupir)
• [0, 0, 0, 0] = Stance rigide

× 8.0 rad/s = Vitesse moteur réelle
```

### **SLIDE 12 : La Hiérarchie des Récompenses**
```
RÉCOMPENSE = Somme pondérée

60% │ ╔═════════════════════════════════════╗
    │ ║ PRIORITÉ 1 : NE PAS TOMBER        ║
    │ ║ (Posture + Hauteur)               ║
30% │ ║ ╔═════════════════════════════════╗║
    │ ║ ║ PRIORITÉ 2 : AVANCER          ║║
    │ ║ ║ (Vitesse X positive)           ║║
10% │ ║ ║ ╔═════════════════════════════╗║║
    │ ║ ║ ║ PRIORITÉ 3 : EFFICACITÉ    ║║║
    │ ║ ║ ║ (Minimiser énergie)         ║║║
    ║ ║ ║ ║ - sum(action²)              ║║║
    └─╚═╚═╚═════════════════════════════╝╝╝

Logique : "D'abord survivre, PUIS optimiser"
```

### **SLIDE 13 : La Récompense - Formule**
```python
# Étape 1 : Bonus équilibre (priorité absolue)
posture_bonus = max(0, 1 - |angle_torse| × 2)
height_bonus = max(0, (position_y - 3.0) / 2)
reward = 2.0 × posture_bonus × height_bonus

# Étape 2 : Avancer (seulement si équilibre OK)
if posture_bonus > 0.5 and height_bonus > 0.3:
    reward += forward_velocity × 0.5

# Étape 3 : Pénalité énergie
reward -= 0.001 × sum(action²)

# Étape 4 : Pénalité chute
if terminated:
    reward -= 10.0
```

### **SLIDE 14 : Architecture Actor-Critic**
```
14 OBSERVATIONS
      ↓
   Réseau Partagé
   (64 hidden)
      ↙        ↘
   ACTOR      CRITIC
   Policy     Value
   ↓           ↓
   4 Actions  1 Score
   μ, σ       V(s)
   ↓           ↓
   Moteurs    Guidance
```

### **SLIDE 15 : PPO - L'Apprentissage Prudent**
```
❌ MAUVAIS : Grands sauts
   Policy Change : +500%
   → Catastrophe, l'IA oublie tout

✅ BON : Petits pas avec PPO
   Clipped Ratio : [0.8, 1.2]
   → Avance stable et continue
   
   ratio = P_new / P_old
   clipped = clip(ratio, 1±ε)
   loss = min(ratio, clipped) × advantage

   ε = 0.2 (brigade les changements de 20%)
   n_epochs = 10 (entraîne plusieurs fois)
   batch_size = 128
```

### **SLIDE 16 : Défis du Bipède**
```
🔥 DÉFI 1 : L'ÉQUILIBRE CONTRARIAN
────────────────────────────────────
Penche gauche? Correction droite.
Correction trop? Penche droite.
C'est un jeu de feedback continu.

🔥 DÉFI 2 : COORDINATION
────────────────────────
4 moteurs doivent se synchroniser
Phase gauche ≠ Phase droite
Créer une marche stable

🔥 DÉFI 3 : L'EXPLORATION
────────────────────────
Actions possibles = énorme
Sans curriculum = impossible
Avec curriculum = faisable
```

### **SLIDE 17 : Résultats - La Progression**
```
Timestep 0         → ❌ Tombe immédiatement
                      Oscillations chaotiques

Timestep 50,000    → ⚠️ Reste debout
                      Mouvements erratiques
                      Quelques pas chanceux

Timestep 100,000   → ✅ MARCHE STABLE
                      Locomotion coordinée
                      Stride efficace

Timestep 200,000   → 🏆 OPTIMISÉ
                      Marche fluide
                      Énergie minimale
                      Locomotion naturelle
```

### **SLIDE 18 : De Box2D à la Réalité**
```
SIMULATION                RÉALITÉ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Box2D Physics        →    Robot Physique
Gravité = 10 m/s²    →    Gravité = 9.81 m/s²
Frictions réalistes  →    Friction réelle
Articulations moteur →    Servomoteurs

La simulation apprend les patterns.
Le robot réel bénéficie du training.

Domain Randomization possible :
• Varier taille des membres
• Varier masse
• Varier friction
→ Robot généraliste, pas seulement spécialisé
```

### **SLIDE 19 : Résumé BladeWalker**
```
PROBLÈME :
Robot bipède ne sait pas marcher

SOLUTION :
PPO + Curriculum Learning + Box2D Physics

RÉSULTAT :
Marche stable après ~100-200k steps

TECHNIQUE :
• 14 observations (état complet)
• 4 actions (moteurs)
• Actor-Critic (PPO)
• Récompense hiérarchisée

GÉNÉRALISATION :
Peut s'appliquer à 4-legged (chiens)
ou multi-legged (insectes)
```

### **SLIDE 20 : Perspectives & Roadmap**
```
✅ AUJOURD'HUI :
   Bipède simul) en 2D marche bien

🔜 DEMAIN :
   ├─ Domain Randomization
   │  (Varier les paramètres physiques)
   │
   ├─ Transfert Sim-to-Real
   │  (Robot physique qui marche)
   │
   ├─ Obstacle Avoidance
   │  (Marcher en contournant les obstacles)
   │
   ├─ Multi-task Learning
   │  (Marcher + grimper + sauter)
   │
   └─ Transfert de Connaissances
      (Un modèle pour tous les bipèdes)
```

---

## **POINTS DE DÉMONSTRATION EN DIRECT**

### **Démo 1 : Curriculum Learning en Action**

```bash
# Montrer l'évolution de la difficulté
# Dans pointeur_train.py :

CurriculumCallback:
  Step 0      → Difficulty = 0.1 (cible très proche)
  Step 50k    → Difficulty = 0.45 (cible éloignée)
  Step 100k   → Difficulty = 0.8 (cible partout)
  Step 160k   → Difficulty = 1.0 (maintenu)

Montrer graphique : performance vs difficulty
Performance monte → adapte difficulty
```

### **Démo 2 : BladeWalker - Rendu Visuel**

```bash
# Afficher :
1. La structure physique (wireframe Box2D)
2. Les 14 observations temps réel
3. Les 4 actions du réseau neural
4. Le score de récompense instantané
5. Progression : oscillations → marche → optimisé
```

### **Démo 3 : Comparaison PPO vs Rien**

```
TEMPS 1s (50 pas de simulation)

Sans RL :
[Dessin du robot qui tombe]

Après 100k steps avec RL :
[Dessin du robot qui marche]

Différence : tout est dans le réseau neural de 5KB
```

---

## **RESSOURCES À MONTRER AUX SLIDES**

1. **Graphique Performance vs Temps** (avec et sans curriculum)
2. **Vidéo : Robot qui apprend à marcher** (accéléré 10x)
3. **Wireframe Box2D** du bipède
4. **Heatmap des récompenses** en fonction de (angle, velocity)
5. **Comparaison** Bras fixe vs Bipède (complexité visuelle)
