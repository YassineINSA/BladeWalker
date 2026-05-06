# Présentation BladeWalker - Parties 4 & 5 (VERSION 3 MIN)

---

## **PARTIE 4 : Curriculum Learning (1 min)**

### **Texte - A dire rapidement**

"Vous avez déjà essayé d'apprendre le piano en commençant par une symphonie de Beethoven ? Impossible. Notre IA aussi.

**Le problème :** Si on donne une tâche trop difficile dès le départ, l'IA ne trouve jamais les bonnes récompenses pour apprendre. Elle se perd.

**La solution :** On augmente **progressivement** la difficulté pendant l'entraînement. C'est le **Curriculum Learning**.

Concrètement, notre bras robotique apprend en trois phases :
1. **Phase 1** : Cibles très proches → apprentissage rapide
2. **Phase 2** : Cibles s'éloignent progressivement → consolidation
3. **Phase 3** : Cibles partout → maîtrise totale

Un callback automatique gère tout ça en temps réel. Résultat ? **5 à 10 fois plus rapide** qu'sans curriculum learning."

---

## **PARTIE 5 : BladeWalker (2 min)**

### **Texte - A dire rapidement**

"Maintenant, passons au vrai défi : un **robot qui ne tombe pas**.

BladeWalker est un **bipède** avec 2 jambes, 4 articulations (2 hanches + 2 genoux), et il doit lutter **contre la gravité** à chaque instant. C'est le passage du statique au dynamique.

**L'IA reçoit 14 observations :**
- L'inclinaison du torse (danger de chute ?)
- Les angles et vitesses des articulations
- Les contacts au sol (ses pieds touchent-ils le sol ?)

**Elle contrôle 4 moteurs** pour les articulations.

**Le défi :** Ces 14 entrées et 4 sorties créent des **trillions de possibilités**. Comment trouver la bonne marche ?

**La récompense est hiérarchisée :**
- 60% : **Ne pas tomber** (c'est la priorité absolue)
- 30% : Avancer
- 10% : Économiser l'énergie

Sans cette hiérarchie, le robot oublie complètement l'équilibre.

On utilise **PPO**, un algorithme qui fait des **petits pas prudents**. Pas de grands sauts qui casseraient tout.

**Les résultats :**
- À 50k pas : Oscille mais reste debout
- À 100k pas : Marche stable et coordinée
- À 200k pas : Locomotion optimisée

Et tout ça ? Juste un petit réseau neural de quelques milliers de paramètres."

---

## **LES SLIDES (Version Courte)**

### **SLIDE 1**
```
4. CURRICULUM LEARNING
   La Méthode "Petit à Petit"

🎯 Apprendre pas à pas = Apprendre vite
```

### **SLIDE 2**
```
LE PROBLÈME
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tâche trop difficile
       ↓
Pas de récompense
       ↓
L'IA abandonne
       ↓
Échec

LA SOLUTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Facile → Moyen → Difficile
  ↓        ↓         ↓
Succès  Progrès  Maîtrise
```

### **SLIDE 3**
```
TROIS PHASES

Phase 1 (10%)          Phase 2 (50%)          Phase 3 (100%)
─────────────────      ────────────────       ─────────────
Cibles proches         Cibles moyennes        Cibles partout
    ↓                       ↓                       ↓
Apprentissage         Consolidation           Généralisation
    ↓                       ↓                       ↓
Très rapide           Continu                 Expert
```

### **SLIDE 4**
```
RÉSULTAT

⏱️ SANS CURRICULUM    vs    ⏱️ AVEC CURRICULUM

0-100k: Flat line     →     0-50k:  ✅ Rapide
100k+: Plateau         →    50-100k: ✅ Rapide
                             100k+:  ✅ Converge

GAIN : 5-10x plus vite 🚀
```

---

### **SLIDE 5**
```
5. BLADEWALKER
   Le Robot qui Marche

🤖 14 senseurs
   4 moteurs
   Ne pas tomber = MISSION CRITIQUE
```

### **SLIDE 6**
```
C'EST QUOI ?

BIPÈDE = 2 JAMBES
        ↙        ↘
    [HANCHE]  [HANCHE]
       ↓          ↓
    [GENOU]   [GENOU]
       ↓          ↓
    [TIBIA]   [TIBIA]
```

### **SLIDE 7**
```
OBSERVATIONS (14)

TORSE : angle, vitesse rotation, vitesse X, vitesse Y

JAMBE GAUCHE : angle hanche, vitesse, angle genou, 
               vitesse, contact sol?

JAMBE DROITE : idem

= Vision complète du robot
```

### **SLIDE 8**
```
ACTIONS (4)

Hanche gauche  ┐
Genou gauche   ├─ [-1.0 to +1.0]
Hanche droite  │   (vitesses moteur)
Genou droit    ┘
```

### **SLIDE 9**
```
LA RÉCOMPENSE - PRIORITÉS

60% : NE PAS TOMBER
      (Équilibre + Hauteur)
      
30% : AVANCER
      (Seulement si équilibre OK)
      
10% : EFFICACITÉ
      (Minimiser énergie)

Logique : Survivre → Progresser → Optimiser
```

### **SLIDE 10**
```
ARCHITECTURE : ACTOR-CRITIC

14 Observations
       ↓
   [Réseau 64]
      ↙      ↘
   ACTOR    CRITIC
   (Agir)   (Évaluer)
     ↓         ↓
   4 Actions  Valeur
```

### **SLIDE 11**
```
ALGORITHME : PPO (Proximal Policy Optimization)

❌ Gros changements = Catastrophe

✅ PPO = Petits pas prudents
   • Clipe les changements
   • Apprend lentement mais sûrement
   • Stable et robuste
```

### **SLIDE 12**
```
LES DÉFIS

🔥 ÉQUILIBRE CONTRARIAN
   Penche gauche → Compense droite
   Trop ? → Penche droit
   C'est du feedback continu

🔥 COORDINATION
   4 moteurs doivent se synchroniser
   Phase: Jambe gauche ↑ / Droite ↓

🔥 EXPLORATION
   Trillions d'actions possibles
   Curriculum learning = indispensable
```

### **SLIDE 13**
```
LA PROGRESSION

⏱️ 0 pas         →  ❌ Tombe
                    (Oscillations chaotiques)

⏱️ 50,000 pas    →  ⚠️ Reste debout
                    (Mouvements erratiques)

⏱️ 100,000 pas   →  ✅ MARCHE STABLE
                    (Stride efficace)

⏱️ 200,000 pas   →  🏆 OPTIMISÉ
                    (Locomotion naturelle)
```

### **SLIDE 14**
```
RÉSUMÉ

PROBLÈME : Robot bipède oscille, tombe

SOLUTION :
• Récompense hiérarchisée
• PPO pour apprentissage stable
• Curriculum learning pour exploration

RÉSULTAT : Marche stable en ~100-200k pas

= Un petit réseau neural qu'on peut
  mettre dans un robot réel
```

---

## **TIMING EXACT (3 min)**

```
SLIDE 1:       5 sec   (titre)
SLIDE 2:      15 sec   (le problème/solution)
SLIDE 3-4:    30 sec   (les phases + résultat)

Transition:    5 sec

SLIDE 5:       5 sec   (titre BladeWalker)
SLIDE 6-8:    20 sec   (anatomie + observations + actions)
SLIDE 9:      10 sec   (récompense)
SLIDE 10-11:  20 sec   (architecture + algo)
SLIDE 12:     15 sec   (défis)
SLIDE 13:     20 sec   (progression)
SLIDE 14:     15 sec   (résumé)

Total : ~175 secondes ≈ 3 min
```

---

## **SCRIPT À DIRE (Complet & Chronométré)**

### **INTRODUCTION (30 sec)**

"Nous vous présentons deux innovations clés de BladeWalker : comment apprendre vite, et comment créer un robot qui ne tombe pas.

**Partie 1 : Curriculum Learning.** Quand on veut apprendre quelque chose de difficile, on ne commence pas par le niveau expert. On commence facile. C'est exactement ce qu'on fait avec notre IA."

### **CURRICULUM LEARNING (45 sec)**

"Le problème classique : si on donne une tâche trop difficile, l'IA ne trouve jamais de récompense et abandonne.

Notre solution : on augmente **progressivement** la difficulté pendant l'entraînement.

Pour le bras robotique, c'est simple : au début, la cible apparaît très proche. L'IA apprend les bases rapidement. Puis on éloigne la cible progressivement. À la fin, elle peut être n'importe où.

Résultat : **5 à 10 fois plus rapide** qu'en commençant directement par la tâche complète."

### **TRANSITION (10 sec)**

"Maintenant, parlons du vrai défi technique : BladeWalker, notre bipède."

### **BLADEWALKER - ANATOMIE (30 sec)**

"BladeWalker a 2 jambes, 4 articulations : 2 hanches et 2 genoux. Contrairement au bras qui est attaché à une base fixe, ce robot doit **rester équilibré**.

Il reçoit 14 informations : son inclinaison, la vitesse de rotation, ses vitesses X et Y, et les angles + vitesses de chaque articulation plus le contact au sol.

Il contrôle 4 moteurs. Simple en apparence, mais il y a des **trillions de combinaisons** possibles."

### **LA RÉCOMPENSE - CLÉ DU SUCCÈS (30 sec)**

"Voici le secret : la récompense est **hiérarchisée**.

60% du score : ne pas tomber. C'est la priorité absolue.

30% : avancer. Mais seulement si l'équilibre est maintenu. Si le robot tombe en essayant d'avancer, ça n'a aucun intérêt.

10% : économiser l'énergie. Marcher efficacement, pas gaspiller les moteurs.

Cette hiérarchie force le robot à **apprendre d'abord à survivre**, puis à optimiser."

### **ARCHITECTURE & ALGO (30 sec)**

"On utilise PPO, Proximal Policy Optimization. C'est un algorithme qui fait des **petits pas prudents**.

L'architecture est simple : un réseau neuronal avec 2 branches.
- L'une décide les actions (l'actor)
- L'autre évalue la qualité des actions (le critic)

L'avantage de PPO : c'est stable. Pas de grands sauts qui cassent tout. On apprend lentement mais sûrement."

### **RÉSULTATS & PROGRESSION (20 sec)**

"Voici la progression :
- À 50,000 pas : le robot oscille mais reste debout
- À 100,000 pas : marche stable et coordinée
- À 200,000 pas : locomotion optimisée

Et tout ça ? C'est juste un petit réseau neural qu'on peut mettre dans un robot réel. Pas besoin de supercalculs."

### **CONCLUSION (10 sec)**

"Curriculum Learning + PPO + Récompense Hiérarchisée = Un robot qui marche.

C'est la base de l'IA robotique moderne."

---

**Total scénario : ~3 minutes 05 secondes ⏱️**
