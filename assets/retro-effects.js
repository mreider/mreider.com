// Funky Retro JavaScript Effects
(function() {
    'use strict';

    // Initialize retro effects when DOM is loaded
    document.addEventListener('DOMContentLoaded', function() {
        initRetroEffects();
    });

    function initRetroEffects() {
        addRetroModeClass();
        createMatrixRain();
        addGlitchEffect();
        addTypingEffect();
        addSoundEffects();
        addParticleSystem();
        addRetroConsoleLog();
    }

    // Add retro mode class to body
    function addRetroModeClass() {
        document.body.classList.add('retro-mode');
    }

    // Matrix-style digital rain effect
    function createMatrixRain() {
        const canvas = document.createElement('canvas');
        canvas.id = 'matrix-rain';
        canvas.style.position = 'fixed';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100%';
        canvas.style.height = '100%';
        canvas.style.pointerEvents = 'none';
        canvas.style.zIndex = '-2';
        canvas.style.opacity = '0.1';
        document.body.appendChild(canvas);

        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        const matrix = "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789@#$%^&*()*&^%+-/~{[|`]}";
        const matrixArray = matrix.split("");

        const fontSize = 10;
        const columns = canvas.width / fontSize;
        const drops = [];

        for (let x = 0; x < columns; x++) {
            drops[x] = 1;
        }

        function drawMatrix() {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.04)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = '#00ff00';
            ctx.font = fontSize + 'px monospace';

            for (let i = 0; i < drops.length; i++) {
                const text = matrixArray[Math.floor(Math.random() * matrixArray.length)];
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);

                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                    drops[i] = 0;
                }
                drops[i]++;
            }
        }

        setInterval(drawMatrix, 35);

        // Resize canvas on window resize
        window.addEventListener('resize', function() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        });
    }

    // Add glitch effect to headers
    function addGlitchEffect() {
        const headers = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
        headers.forEach(header => {
            header.setAttribute('data-text', header.textContent);
            
            // Random glitch trigger
            setInterval(() => {
                if (Math.random() < 0.1) {
                    header.style.animation = 'none';
                    setTimeout(() => {
                        header.style.animation = 'textGlow 2s ease-in-out infinite alternate';
                    }, 100);
                }
            }, 3000);
        });
    }

    // Typing effect for paragraphs
    function addTypingEffect() {
        const paragraphs = document.querySelectorAll('p');
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.classList.contains('typed')) {
                    typeText(entry.target);
                }
            });
        });

        paragraphs.forEach(p => {
            if (p.textContent.length > 0) {
                observer.observe(p);
            }
        });
    }

    function typeText(element) {
        element.classList.add('typed');
        const text = element.textContent;
        element.textContent = '';
        element.style.borderRight = '2px solid #00ffff';
        
        let i = 0;
        const timer = setInterval(() => {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
            } else {
                clearInterval(timer);
                setTimeout(() => {
                    element.style.borderRight = 'none';
                }, 500);
            }
        }, 20);
    }

    // Add retro sound effects (using Web Audio API)
    function addSoundEffects() {
        let audioContext;
        
        // Initialize audio context on first user interaction
        document.addEventListener('click', function initAudio() {
            if (!audioContext) {
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
                document.removeEventListener('click', initAudio);
            }
        });

        // Add click sounds to links and buttons
        document.addEventListener('click', function(e) {
            if (audioContext && (e.target.tagName === 'A' || e.target.tagName === 'BUTTON')) {
                playBeep(audioContext, 800, 0.1);
            }
        });

        // Add hover sounds to navigation
        const navLinks = document.querySelectorAll('nav a');
        navLinks.forEach(link => {
            link.addEventListener('mouseenter', function() {
                if (audioContext) {
                    playBeep(audioContext, 600, 0.05);
                }
            });
        });
    }

    function playBeep(audioContext, frequency, duration) {
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.value = frequency;
        oscillator.type = 'square';
        
        gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + duration);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + duration);
    }

    // Particle system for extra retro flair
    function addParticleSystem() {
        const canvas = document.createElement('canvas');
        canvas.id = 'particles';
        canvas.style.position = 'fixed';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100%';
        canvas.style.height = '100%';
        canvas.style.pointerEvents = 'none';
        canvas.style.zIndex = '-1';
        document.body.appendChild(canvas);

        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        const particles = [];
        const particleCount = 50;

        class Particle {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.vx = (Math.random() - 0.5) * 0.5;
                this.vy = (Math.random() - 0.5) * 0.5;
                this.size = Math.random() * 2 + 1;
                this.color = this.getRandomColor();
                this.opacity = Math.random() * 0.5 + 0.2;
            }

            getRandomColor() {
                const colors = ['#ff00ff', '#00ffff', '#39ff14', '#ff6600', '#ffff00'];
                return colors[Math.floor(Math.random() * colors.length)];
            }

            update() {
                this.x += this.vx;
                this.y += this.vy;

                if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
                if (this.y < 0 || this.y > canvas.height) this.vy *= -1;

                this.opacity += (Math.random() - 0.5) * 0.02;
                this.opacity = Math.max(0.1, Math.min(0.8, this.opacity));
            }

            draw() {
                ctx.save();
                ctx.globalAlpha = this.opacity;
                ctx.fillStyle = this.color;
                ctx.shadowBlur = 10;
                ctx.shadowColor = this.color;
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fill();
                ctx.restore();
            }
        }

        // Initialize particles
        for (let i = 0; i < particleCount; i++) {
            particles.push(new Particle());
        }

        function animateParticles() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            particles.forEach(particle => {
                particle.update();
                particle.draw();
            });

            requestAnimationFrame(animateParticles);
        }

        animateParticles();

        // Resize canvas on window resize
        window.addEventListener('resize', function() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        });
    }

    // Add retro console messages
    function addRetroConsoleLog() {
        const messages = [
            '🚀 RETRO MODE ACTIVATED',
            '💾 Loading cyberpunk aesthetics...',
            '🌈 Neon colors initialized',
            '⚡ Glitch effects online',
            '🎵 8-bit vibes enabled',
            '🔮 Welcome to the digital realm!'
        ];

        console.log('%c' + messages[0], 'color: #ff00ff; font-size: 20px; font-weight: bold;');
        
        messages.slice(1).forEach((message, index) => {
            setTimeout(() => {
                console.log('%c' + message, 'color: #00ffff; font-size: 14px;');
            }, (index + 1) * 500);
        });

        // Easter egg: Konami code
        let konamiCode = [];
        const konamiSequence = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65]; // ↑↑↓↓←→←→BA

        document.addEventListener('keydown', function(e) {
            konamiCode.push(e.keyCode);
            if (konamiCode.length > konamiSequence.length) {
                konamiCode.shift();
            }
            
            if (konamiCode.length === konamiSequence.length && 
                konamiCode.every((code, index) => code === konamiSequence[index])) {
                activateUltraRetroMode();
                konamiCode = [];
            }
        });
    }

    function activateUltraRetroMode() {
        console.log('%c🎮 ULTRA RETRO MODE ACTIVATED! 🎮', 'color: #ffff00; font-size: 24px; font-weight: bold; text-shadow: 2px 2px 4px #ff00ff;');
        
        // Add extra visual effects
        document.body.style.filter = 'hue-rotate(180deg) saturate(1.5)';
        
        setTimeout(() => {
            document.body.style.filter = '';
        }, 3000);

        // Create temporary rainbow border
        const rainbowBorder = document.createElement('div');
        rainbowBorder.style.position = 'fixed';
        rainbowBorder.style.top = '0';
        rainbowBorder.style.left = '0';
        rainbowBorder.style.right = '0';
        rainbowBorder.style.bottom = '0';
        rainbowBorder.style.border = '5px solid';
        rainbowBorder.style.borderImage = 'linear-gradient(45deg, #ff00ff, #00ffff, #39ff14, #ff6600, #ffff00, #ff00ff) 1';
        rainbowBorder.style.pointerEvents = 'none';
        rainbowBorder.style.zIndex = '9999';
        rainbowBorder.style.animation = 'borderGlow 1s linear infinite';
        
        document.body.appendChild(rainbowBorder);
        
        setTimeout(() => {
            document.body.removeChild(rainbowBorder);
        }, 5000);
    }

    // Add some retro cursor effects
    function addCursorEffects() {
        let mouseX = 0, mouseY = 0;
        const trail = [];
        const trailLength = 10;

        document.addEventListener('mousemove', function(e) {
            mouseX = e.clientX;
            mouseY = e.clientY;
            
            trail.push({x: mouseX, y: mouseY, time: Date.now()});
            if (trail.length > trailLength) {
                trail.shift();
            }
        });

        function drawCursorTrail() {
            const existingTrail = document.getElementById('cursor-trail');
            if (existingTrail) {
                existingTrail.remove();
            }

            const canvas = document.createElement('canvas');
            canvas.id = 'cursor-trail';
            canvas.style.position = 'fixed';
            canvas.style.top = '0';
            canvas.style.left = '0';
            canvas.style.width = '100%';
            canvas.style.height = '100%';
            canvas.style.pointerEvents = 'none';
            canvas.style.zIndex = '9998';
            document.body.appendChild(canvas);

            const ctx = canvas.getContext('2d');
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;

            function animate() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                
                const now = Date.now();
                trail.forEach((point, index) => {
                    const age = now - point.time;
                    const opacity = Math.max(0, 1 - age / 500);
                    const size = 5 * opacity;
                    
                    ctx.save();
                    ctx.globalAlpha = opacity;
                    ctx.fillStyle = '#00ffff';
                    ctx.shadowBlur = 10;
                    ctx.shadowColor = '#00ffff';
                    ctx.beginPath();
                    ctx.arc(point.x, point.y, size, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.restore();
                });

                requestAnimationFrame(animate);
            }
            animate();
        }

        // Only add cursor effects on non-touch devices
        if (!('ontouchstart' in window)) {
            drawCursorTrail();
        }
    }

    // Initialize cursor effects after a short delay
    setTimeout(addCursorEffects, 1000);

})();
