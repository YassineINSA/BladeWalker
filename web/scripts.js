const themeToggleBtn = document.getElementById('theme-toggle');
const themeIcon = document.getElementById('theme-icon');

if (themeToggleBtn && themeIcon) {
    themeToggleBtn.addEventListener('click', () => {
        document.documentElement.classList.toggle('light-mode');
        
        if (document.documentElement.classList.contains('light-mode')) {
            localStorage.setItem('theme', 'light');
            themeIcon.src = 'img/noir.png'; // Passage au noir pour le fond blanc
        } else {
            localStorage.setItem('theme', 'dark');
            themeIcon.src = 'img/couleur.png'; // Retour à la couleur pour le fond sombre
        }
    });
}
const canvas = document.getElementById('canvas-bg');
const ctx = canvas.getContext('2d');
let particles = [];
const mouse = { x: null, y: null, radius: 150 };

// Ajustement du canvas à la taille de la fenêtre
function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
window.addEventListener('resize', resize);
resize();

// Suivi de la position de la souris
window.addEventListener('mousemove', (e) => { 
    mouse.x = e.x; 
    mouse.y = e.y; 
});

// Désactivation du suivi de la souris lorsque le curseur quitte la fenêtre
window.addEventListener('mouseout', () => {
    mouse.x = null;
    mouse.y = null;
});

// Classe représentant une particule
class Particle {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.size = Math.random() * 2 + 1; // Taille aléatoire
        this.baseX = this.x;
        this.baseY = this.y;
        this.density = (Math.random() * 30) + 1;
        this.vx = (Math.random() - 0.5) * 1;
        this.vy = (Math.random() - 0.5) * 1;
    }

    update() {
        this.x += this.vx;
        this.y += this.vy;

        // Rebond sur les bords
        if (this.x > canvas.width || this.x < 0) this.vx *= -1;
        if (this.y > canvas.height || this.y < 0) this.vy *= -1;

        // Interaction avec la souris
        if (mouse.x != null) {
            let dx = mouse.x - this.x;
            let dy = mouse.y - this.y;
            let distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance < mouse.radius) {
                const forceDirectionX = dx / distance;
                const forceDirectionY = dy / distance;
                const force = (mouse.radius - distance) / mouse.radius;
                const directionX = forceDirectionX * force * this.density * 0.1;
                const directionY = forceDirectionY * force * this.density * 0.1;
                
                this.x -= directionX;
                this.y -= directionY;
            }
        }
    }

    draw() {
        ctx.fillStyle = 'rgba(252, 102, 102, 0.8)';
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }
}

function init() {
    particles = [];
    let numberOfParticles = (canvas.width * canvas.height) / 9000; // Densité
    for(let i = 0; i < numberOfParticles; i++) {
        particles.push(new Particle());
    }
}

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    for (let i = 0; i < particles.length; i++) {
        particles[i].update();
        particles[i].draw();
        
        // Relier les particules entre elles
        for (let j = i; j < particles.length; j++) {
            const dx = particles[i].x - particles[j].x;
            const dy = particles[i].y - particles[j].y;
            const distance = Math.sqrt(dx*dx + dy*dy);
            
            if (distance < 120) {
                ctx.strokeStyle = `rgba(252, 102, 102, ${0.2 - distance/600})`;
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.moveTo(particles[i].x, particles[i].y);
                ctx.lineTo(particles[j].x, particles[j].y);
                ctx.stroke();
            }
        }
    }
    requestAnimationFrame(animate);
}

init();
animate();


const header = document.getElementById('main-nav');
const heroContent = document.querySelector('#hero .container');

window.addEventListener('scroll', () => {
    let scrollPos = window.scrollY;

    if (scrollPos > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }

    if (heroContent) {

        let opacity = 1 - (scrollPos / 400);
        
        if (opacity < 0) {
            opacity = 0;
        }
        
        heroContent.style.opacity = opacity;
        
        heroContent.style.transform = `translateY(${scrollPos * 0.4}px)`;
    }
});

const mapLevels = [
    { 
        id: 0, x: 15, y: 50,
        title: "Zone de Départ", 
        desc: "L'environnement d'entraînement est prêt. R.E.X. est en attente d'instructions. Utilisez la flèche droite ou cliquez sur le niveau suivant.",
        showBtn: false 
    },
    { 
        id: 1, x: 40, y: 30,
        title: "Niveau 1 : Bras Articulé Basique", 
        desc: "Observez les premiers mouvements du bras robotique !",
        showBtn: true 
    },
    { 
        id: 2, x: 65, y: 70,
        title: "Niveau 2 : Bras Articulé de Transport", 
        desc: "Après de longues heures d'entraînement, R.E.X. a appris à transporter des objets !",
        showBtn: true 
    },
    { 
        id: 3, x: 90, y: 40,
        title: "Niveau 3", 
        desc: "???",
        showBtn: false
    }
];

let currentLevelIndex = 0;

const mapContainer = document.querySelector('.map-container');
if (mapContainer) {
    initMap();
}

function initMap() {
    const svgPaths = document.getElementById('map-paths');
    const nodesContainer = document.getElementById('nodes-container');
    
    for (let i = 0; i < mapLevels.length; i++) {
        const lvl = mapLevels[i];
        
        const node = document.createElement('div');
        node.classList.add('map-node');
        node.id = `node-${i}`;
        node.style.left = `${lvl.x}%`;
        node.style.top = `${lvl.y}%`;
        node.onclick = () => moveToLevel(i);
        nodesContainer.appendChild(node);

        if (i < mapLevels.length - 1) {
            const nextLvl = mapLevels[i+1];
            const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
            line.id = `line-${i}`;
            line.setAttribute("x1", `${lvl.x}%`);
            line.setAttribute("y1", `${lvl.y}%`);
            line.setAttribute("x2", `${nextLvl.x}%`);
            line.setAttribute("y2", `${nextLvl.y}%`);
            line.setAttribute("stroke", "rgba(255, 255, 255, 0.3)");
            line.setAttribute("stroke-width", "4");
            line.setAttribute("stroke-dasharray", "10, 10");
            line.style.transition = "opacity 0.8s ease";
            svgPaths.appendChild(line);
        }
    }

    moveToLevel(0);

    window.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight' && currentLevelIndex < mapLevels.length - 1) {
            moveToLevel(currentLevelIndex + 1);
        } else if (e.key === 'ArrowLeft') {
            const minLevel = currentLevelIndex > 0 ? 1 : 0;
            if (currentLevelIndex > minLevel) {
                moveToLevel(currentLevelIndex - 1);
            }
        }
    });
}

function moveToLevel(index) {
    if (index === 0 && currentLevelIndex > 0) return;

    currentLevelIndex = index;
    const lvl = mapLevels[index];
    
    const avatar = document.getElementById('avatar');
    avatar.style.left = `${lvl.x}%`;
    avatar.style.top = `${lvl.y}%`;

    if (index > 0) {
        // Disparition du niveau 0
        document.getElementById('node-0').classList.add('fade-out');
        const startLine = document.getElementById('line-0');
        if (startLine) {
            startLine.style.opacity = '0';
        }
        
        // Décalage du calque pour recentrer la carte
        document.getElementById('map-layer').classList.add('map-centered');
    }

    const nodes = document.querySelectorAll('.map-node');
    nodes.forEach((node, i) => {
        if (i <= index) node.classList.add('active');
        else node.classList.remove('active');
    });

    const infoPanel = document.getElementById('info-panel');
    infoPanel.style.opacity = 0;
    infoPanel.style.transform = 'translateY(10px)';
    
    setTimeout(() => {
        document.getElementById('level-title').innerText = lvl.title;
        document.getElementById('level-desc').innerText = lvl.desc;
        
        const btn = document.getElementById('level-btn');
        if (lvl.showBtn) {
            btn.style.display = 'inline-block';
            btn.href = `level-${lvl.id}.html`;
        } else {
            btn.style.display = 'none';
        }

        infoPanel.style.opacity = 1;
        infoPanel.style.transform = 'translateY(0)';
    }, 300);
}






// --- Logique du Dashboard Niveau 1 ---
const dashboardContainer = document.querySelector('.dashboard-container');

if (dashboardContainer) {
    const video = document.getElementById('ai-video');
    const playPauseBtn = document.getElementById('play-pause-btn');
    const trainBtn = document.getElementById('train-btn');
    const trainStatus = document.getElementById('train-status');
    
    // Sliders et Toggle
    const energySlider = document.getElementById('energy-penalty');
    const shakeSlider = document.getElementById('shake-penalty');
    const energyVal = document.getElementById('energy-val');
    const shakeVal = document.getElementById('shake-val');
    const radioAlgos = document.querySelectorAll('input[name="algo"]');

    // Variables d'état
    let trainCount = 0;
    const MAX_TRAINS = 2;

    const valueMap = { "1": "moyen", "2": "fort" };

    // --- 1. Contrôle Vidéo ---
    playPauseBtn.addEventListener('click', () => {
        if (video.paused) {
            video.play();
            playPauseBtn.innerText = '⏸️ PAUSE';
        } else {
            video.pause();
            playPauseBtn.innerText = '▶️ LECTURE';
        }
    });

    // --- 2. Fonction pour Réinitialiser l'entraînement ---
    function resetTraining() {
        trainCount = 0;
        updateTrainButton();
        trainStatus.innerText = "Paramètres modifiés. Prêt pour un nouvel entraînement.";
        trainStatus.style.color = "#aaa";
        // Optionnel : remettre une vidéo "d'attente"
        // video.src = "videos/attente.mp4"; 
    }

    // --- 3. Écouteurs sur les Paramètres ---
    energySlider.addEventListener('input', () => {
        resetTraining();
    });

    shakeSlider.addEventListener('input', () => {
        resetTraining();
    });

    radioAlgos.forEach(radio => {
        radio.addEventListener('change', () => {
            resetTraining();
        });
    });

    // --- 4. Fonction pour générer le nom de la vidéo ---
    function getVideoFilename(step) {
        // Récupérer l'algo sélectionné (PPO ou SAC, en minuscules)
        const algo = document.querySelector('input[name="algo"]:checked').value.toLowerCase();
        
        // Récupérer les valeurs des curseurs
        const energyVal = energySlider.value;
        const shakeVal = shakeSlider.value;

        // Traduire les chiffres (1, 2) en mots ("faible", "forte")
        const energyStr = valueMap[energyVal];
        const shakeStr = valueMap[shakeVal];

        // Construire le chemin final (ex: videos/pointeur_ppo_energie-faible_jitter-forte_phase-1.mp4)
        return `videos/pointeur_${algo}_energie-${energyStr}_jitter-${shakeStr}_phase-${step}.mp4`;
    }

    // --- 5. Logique du Bouton d'Entraînement ---
    function updateTrainButton() {
        trainBtn.innerText = `LANCER L'ENTRAÎNEMENT (${trainCount}/${MAX_TRAINS})`;
        if (trainCount >= MAX_TRAINS) {
            trainBtn.disabled = true;
            trainBtn.innerText = "ENTRAÎNEMENT MAXIMUM ATTEINT";
        } else {
            trainBtn.disabled = false;
        }
    }

    trainBtn.addEventListener('click', () => {
        if (trainCount < MAX_TRAINS) {
            
            // 1. Animation de chargement
            trainBtn.disabled = true;
            let dots = 0;
            trainStatus.style.color = "#fc3535";
            trainBtn.innerText = "CALCUL EN COURS...";
            
            const loadingInterval = setInterval(() => {
                dots = (dots + 1) % 4;
                trainStatus.innerText = "L'IA s'entraîne dans le moteur physique" + ".".repeat(dots);
            }, 500);

            // 2. On simule un temps de calcul de 2.5 secondes
            setTimeout(() => {
                clearInterval(loadingInterval);

                // 3. Incrémenter l'étape d'entraînement
                trainCount++;
                
                // 4. Générer le nom du fichier vidéo correspondant à la configuration actuelle
                const videoToLoad = getVideoFilename(trainCount);

                // 5. Mise à jour de l'interface
                updateTrainButton();
                trainStatus.style.color = "lightgreen";
                trainStatus.innerText = `Entraînement ${trainCount} terminé ! Voici le résultat.`;
                
                // 6. Chargement et lecture de la vidéo
                video.src = videoToLoad; 
                
                // Gestion d'erreur si la vidéo n'existe pas dans le dossier
                video.onerror = () => {
                    trainStatus.style.color = "#fc3535";
                    trainStatus.innerText = `Fichier introuvable : ${videoToLoad}`;
                };

                video.load();
                video.play();
                playPauseBtn.innerText = '⏸ PAUSE';

            }, 2500); 
        }
    });

    // Initialisation
    updateTrainButton();
}