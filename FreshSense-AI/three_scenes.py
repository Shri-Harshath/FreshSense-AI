"""
FreshSense AI - 3D WebGL Immersive Visualizations
=================================================
High-performance Three.js WebGL scenes for FreshSense AI:
1. Smart Glass Container 3D Hero Scene on Multi-Tiered Pedestal with realistic 3D food,
   IoT sensor module, floating HUD indicators, dynamic particle fields, and smooth mouse parallax.
2. 3D AI Cognitive Pipeline (Sensors -> Neural Core -> Predictive Verdict).
3. 3D Interactive Environmental Chamber for Simulation Mode.
"""

def get_3d_smart_container_hero_html(
    temp_c: float = 24.8,
    humidity_pct: float = 68.0,
    gas_ppm: float = 420.0,
    freshness_score: float = 72.0,
    food_name: str = "Tomatoes",
    food_status: str = "AT RISK",
    est_time_str: str = "~8 hours remaining",
    height: int = 360
) -> str:
    """
    Generates the hardware-accelerated 3D WebGL Hero Scene matching the reference image:
    - Multi-tiered glowing iridescent pedestal.
    - Transparent rectangular smart glass container with teal latches and FreshSense logo.
    - Inside: Bed of fresh salad greens and ripe glossy red tomatoes with green calyx and stems.
    - Top Lid: Smart IoT sensor module with glowing screen and pulsing radar ring.
    - Surrounding: Floating leaves, sparkles, and ambient HUD telemetry.
    """
    if freshness_score >= 80:
        theme_hex = "#10b981"
        status_color_num = "0x10b981"
    elif freshness_score >= 60:
        theme_hex = "#f59e0b"
        status_color_num = "0xf59e0b"
    else:
        theme_hex = "#f43f5e"
        status_color_num = "0xf43f5e"

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800;900&family=JetBrains+Mono:wght@700;800&family=Outfit:wght@700;800;900&display=swap');
    
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        user-select: none;
    }}
    
    body {{
        background: transparent;
        overflow: hidden;
        font-family: 'Plus Jakarta Sans', sans-serif;
        width: 100vw;
        height: {height}px;
    }}
    
    #canvas-container {{
        width: 100%;
        height: 100%;
        position: relative;
        border-radius: 28px;
        overflow: hidden;
        background: radial-gradient(circle at 50% 35%, rgba(224, 242, 254, 0.95) 0%, rgba(240, 253, 250, 0.9) 45%, rgba(245, 243, 255, 0.95) 100%);
        border: 1.5px solid rgba(255, 255, 255, 0.95);
        box-shadow: 0 16px 36px rgba(0, 210, 255, 0.12), 0 6px 16px rgba(0, 0, 0, 0.04);
    }}
    
    /* HUD Overlays */
    .hud-overlay {{
        position: absolute;
        inset: 0;
        pointer-events: none;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 14px 18px;
    }}
    
    .hud-top {{
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
    }}
    
    .hud-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 0.72rem;
        font-weight: 800;
        padding: 4px 12px;
        border-radius: 999px;
        backdrop-filter: blur(12px);
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.95);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }}
    
    .hud-live-tag {{
        color: #047857;
        border-color: rgba(16, 185, 129, 0.35);
    }}
    
    .hud-dot {{
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #10b981;
        box-shadow: 0 0 8px #10b981;
        animation: pulse-dot 1.8s infinite ease-in-out;
    }}
    
    @keyframes pulse-dot {{
        0%, 100% {{ transform: scale(1); opacity: 0.8; }}
        50% {{ transform: scale(1.3); opacity: 1; }}
    }}
    
    .hud-caption {{
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 800;
        color: #475569;
        background: rgba(255, 255, 255, 0.85);
        padding: 4px 12px;
        border-radius: 999px;
        border: 1px solid rgba(255, 255, 255, 0.85);
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        backdrop-filter: blur(8px);
        margin: 0 auto;
    }}
</style>
</head>
<body>

<div id="canvas-container">
    <div class="hud-overlay">
        <div class="hud-top">
            <div class="hud-badge hud-live-tag">
                <span class="hud-dot"></span>
                <span>3D SMART CONTAINER 01</span>
            </div>
            <div class="hud-badge" style="color: #0284c7;">
                <span>IoT Node Active</span>
            </div>
        </div>
        
        <div style="text-align: center;">
            <div class="hud-caption">
                ✨ Move cursor to interactively inspect container & sensor optics
            </div>
        </div>
    </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
(function() {{
    const container = document.getElementById('canvas-container');
    const width = container.clientWidth || window.innerWidth;
    const height = container.clientHeight || {height};
    
    // Scene & Camera
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 100);
    camera.position.set(0, 1.2, 5.8);
    
    // WebGL Renderer
    const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true, powerPreference: "high-performance" }});
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    container.appendChild(renderer.domElement);
    
    // Lighting Setup
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.85);
    scene.add(ambientLight);
    
    const keyLight = new THREE.DirectionalLight(0x00d2ff, 1.4);
    keyLight.position.set(4, 6, 4);
    scene.add(keyLight);
    
    const fillLight = new THREE.DirectionalLight(0xff758c, 0.9);
    fillLight.position.set(-4, 4, -3);
    scene.add(fillLight);
    
    const rimLight = new THREE.DirectionalLight(0x10b981, 1.0);
    rimLight.position.set(0, 5, -4);
    scene.add(rimLight);
    
    const statusLight = new THREE.PointLight({status_color_num}, 1.8, 6);
    statusLight.position.set(0, 0.4, 0);
    scene.add(statusLight);
    
    // Root Parallax Group
    const mainGroup = new THREE.Group();
    scene.add(mainGroup);
    
    // -------------------------------------------------------------------------
    // 1. Multi-Tiered Glowing Iridescent Pedestal (Matching Reference)
    // -------------------------------------------------------------------------
    const podiumGroup = new THREE.Group();
    podiumGroup.position.y = -1.15;
    mainGroup.add(podiumGroup);
    
    // Bottom Tier Disc
    const tier1Geo = new THREE.CylinderGeometry(2.3, 2.4, 0.14, 64);
    const tier1Mat = new THREE.MeshStandardMaterial({{
        color: 0xffffff,
        roughness: 0.15,
        metalness: 0.2
    }});
    const tier1 = new THREE.Mesh(tier1Geo, tier1Mat);
    podiumGroup.add(tier1);
    
    // Glowing cyan/teal rim ring on bottom tier
    const rim1Geo = new THREE.TorusGeometry(2.35, 0.035, 16, 64);
    const rim1Mat = new THREE.MeshStandardMaterial({{
        color: 0x00d2ff,
        emissive: 0x00d2ff,
        emissiveIntensity: 1.2
    }});
    const rim1 = new THREE.Mesh(rim1Geo, rim1Mat);
    rim1.rotation.x = Math.PI / 2;
    podiumGroup.add(rim1);
    
    // Middle Tier Disc
    const tier2Geo = new THREE.CylinderGeometry(2.0, 2.1, 0.12, 64);
    const tier2Mat = new THREE.MeshStandardMaterial({{
        color: 0xf0fdfa,
        roughness: 0.1,
        metalness: 0.3
    }});
    const tier2 = new THREE.Mesh(tier2Geo, tier2Mat);
    tier2.position.y = 0.13;
    podiumGroup.add(tier2);
    
    // Top Tier Disc with mint/emerald glowing edge
    const tier3Geo = new THREE.CylinderGeometry(1.75, 1.8, 0.1, 64);
    const tier3Mat = new THREE.MeshStandardMaterial({{
        color: 0xffffff,
        roughness: 0.1,
        metalness: 0.4
    }});
    const tier3 = new THREE.Mesh(tier3Geo, tier3Mat);
    tier3.position.y = 0.24;
    podiumGroup.add(tier3);
    
    const rim3Geo = new THREE.TorusGeometry(1.78, 0.03, 16, 64);
    const rim3Mat = new THREE.MeshStandardMaterial({{
        color: 0x10b981,
        emissive: 0x10b981,
        emissiveIntensity: 1.4
    }});
    const rim3 = new THREE.Mesh(rim3Geo, rim3Mat);
    rim3.rotation.x = Math.PI / 2;
    rim3.position.y = 0.29;
    podiumGroup.add(rim3);

    // -------------------------------------------------------------------------
    // 2. Rectangular Smart Glass Container
    // -------------------------------------------------------------------------
    const containerGroup = new THREE.Group();
    containerGroup.position.y = -0.15;
    mainGroup.add(containerGroup);
    
    const glassMaterial = new THREE.MeshPhysicalMaterial({{
        color: 0xffffff,
        transparent: true,
        opacity: 0.42,
        roughness: 0.05,
        metalness: 0.05,
        transmission: 0.9,
        ior: 1.5,
        reflectivity: 0.9,
        clearcoat: 1.0,
        clearcoatRoughness: 0.05,
        side: THREE.DoubleSide
    }});
    
    // Glass Body (Rounded Box Shape)
    const boxGeo = new THREE.BoxGeometry(2.2, 1.4, 1.7, 10, 10, 10);
    const boxMesh = new THREE.Mesh(boxGeo, glassMaterial);
    containerGroup.add(boxMesh);
    
    // Teal/Cyan Container Rim Frame
    const frameMat = new THREE.MeshStandardMaterial({{
        color: 0x06b6d4,
        roughness: 0.2,
        metalness: 0.6
    }});
    
    // Top Lid Glass & Seal
    const lidGeo = new THREE.BoxGeometry(2.32, 0.14, 1.82);
    const lidMesh = new THREE.Mesh(lidGeo, frameMat);
    lidMesh.position.y = 0.76;
    containerGroup.add(lidMesh);
    
    // Side Latches / Clips (Teal)
    const latchGeo = new THREE.BoxGeometry(0.12, 0.35, 0.45);
    const latchL = new THREE.Mesh(latchGeo, frameMat);
    latchL.position.set(-1.18, 0.58, 0);
    containerGroup.add(latchL);
    
    const latchR = new THREE.Mesh(latchGeo, frameMat);
    latchR.position.set(1.18, 0.58, 0);
    containerGroup.add(latchR);
    
    // FreshSense AI Front Label Badge
    const badgeGeo = new THREE.PlaneGeometry(0.85, 0.22);
    const badgeMat = new THREE.MeshBasicMaterial({{
        color: 0x0f172a,
        side: THREE.DoubleSide
    }});
    const badgeMesh = new THREE.Mesh(badgeGeo, badgeMat);
    badgeMesh.position.set(0, 0.48, 0.86);
    containerGroup.add(badgeMesh);
    
    // -------------------------------------------------------------------------
    // 3. IoT Sensor Puck on Lid
    // -------------------------------------------------------------------------
    const puckGroup = new THREE.Group();
    puckGroup.position.set(0, 0.95, 0);
    containerGroup.add(puckGroup);
    
    const puckBaseGeo = new THREE.CylinderGeometry(0.48, 0.52, 0.2, 32);
    const puckBaseMat = new THREE.MeshStandardMaterial({{
        color: 0xffffff,
        roughness: 0.2,
        metalness: 0.7
    }});
    const puckBase = new THREE.Mesh(puckBaseGeo, puckBaseMat);
    puckGroup.add(puckBase);
    
    // Puck Glowing Screen
    const puckScreenGeo = new THREE.CylinderGeometry(0.38, 0.38, 0.02, 32);
    const puckScreenMat = new THREE.MeshBasicMaterial({{
        color: 0x00d2ff
    }});
    const puckScreen = new THREE.Mesh(puckScreenGeo, puckScreenMat);
    puckScreen.position.y = 0.11;
    puckGroup.add(puckScreen);
    
    // Pulsing radar ring
    const radarGeo = new THREE.TorusGeometry(0.42, 0.025, 16, 32);
    const radarMat = new THREE.MeshBasicMaterial({{
        color: 0x10b981
    }});
    const radarRing = new THREE.Mesh(radarGeo, radarMat);
    radarRing.rotation.x = Math.PI / 2;
    radarRing.position.y = 0.12;
    puckGroup.add(radarRing);

    // -------------------------------------------------------------------------
    // 4. Food Contents: Fresh Salad Greens Bed + Ripe Tomatoes
    // -------------------------------------------------------------------------
    const contentsGroup = new THREE.Group();
    contentsGroup.position.y = -0.15;
    containerGroup.add(contentsGroup);
    
    // Salad Greens Bed (Clusters of green leaves)
    const leafMat = new THREE.MeshStandardMaterial({{
        color: 0x22c55e,
        roughness: 0.4,
        metalness: 0.1,
        side: THREE.DoubleSide
    }});
    
    const leafGeo = new THREE.SphereGeometry(0.35, 12, 12);
    leafGeo.scale(1.2, 0.15, 0.8);
    
    for (let i = 0; i < 9; i++) {{
        const leafMesh = new THREE.Mesh(leafGeo, leafMat);
        const ang = (i / 9) * Math.PI * 2;
        leafMesh.position.set(Math.cos(ang) * 0.7, -0.48, Math.sin(ang) * 0.5);
        leafMesh.rotation.set(0.2, ang + Math.random(), 0.15);
        contentsGroup.add(leafMesh);
    }}
    
    // 3D Realistic Glossy Tomatoes with Calyx Sepals & Stem
    function createTomato(scale, posX, posY, posZ, rotY) {{
        const tGroup = new THREE.Group();
        
        const tomatoGeo = new THREE.SphereGeometry(scale, 32, 32);
        tomatoGeo.scale(1.0, 0.88, 1.0);
        
        const tomatoMat = new THREE.MeshStandardMaterial({{
            color: 0xe11d48,
            roughness: 0.18,
            metalness: 0.08,
            emissive: 0x881337,
            emissiveIntensity: 0.2
        }});
        const tMesh = new THREE.Mesh(tomatoGeo, tomatoMat);
        tGroup.add(tMesh);
        
        // Green Calyx / Sepals
        const calyxGeo = new THREE.ConeGeometry(scale * 0.26, scale * 0.14, 5);
        const calyxMat = new THREE.MeshStandardMaterial({{
            color: 0x10b981,
            roughness: 0.4,
            metalness: 0.1
        }});
        
        for (let i = 0; i < 5; i++) {{
            const sep = new THREE.Mesh(calyxGeo, calyxMat);
            const angle = (i / 5) * Math.PI * 2;
            sep.position.set(Math.cos(angle) * (scale * 0.2), scale * 0.84, Math.sin(angle) * (scale * 0.2));
            sep.rotation.set(0.35, angle, 0.4);
            sep.scale.set(0.6, 1.2, 0.2);
            tGroup.add(sep);
        }}
        
        const stemGeo = new THREE.CylinderGeometry(scale * 0.035, scale * 0.045, scale * 0.32, 8);
        const stemMesh = new THREE.Mesh(stemGeo, calyxMat);
        stemMesh.position.set(0, scale * 0.95, 0);
        stemMesh.rotation.z = 0.2;
        tGroup.add(stemMesh);
        
        tGroup.position.set(posX, posY, posZ);
        tGroup.rotation.y = rotY;
        return tGroup;
    }}
    
    // Front Hero Tomato
    const tom1 = createTomato(0.56, -0.32, -0.15, 0.2, 0.3);
    contentsGroup.add(tom1);
    
    // Right Hero Tomato
    const tom2 = createTomato(0.48, 0.42, -0.22, 0.15, 1.4);
    contentsGroup.add(tom2);
    
    // Center-Back Small Tomato
    const tom3 = createTomato(0.38, 0.08, -0.08, -0.35, -0.6);
    contentsGroup.add(tom3);

    // -------------------------------------------------------------------------
    // 5. Floating Ambient 3D Leaves & Sparkle Particles (Matching Reference)
    // -------------------------------------------------------------------------
    const floatingLeavesGroup = new THREE.Group();
    mainGroup.add(floatingLeavesGroup);
    
    const floatLeafGeo = new THREE.SphereGeometry(0.18, 8, 8);
    floatLeafGeo.scale(1.3, 0.1, 0.7);
    
    const floatLeafMat = new THREE.MeshStandardMaterial({{
        color: 0x10b981,
        roughness: 0.3,
        side: THREE.DoubleSide
    }});
    
    const floatLeaves = [];
    for (let i = 0; i < 7; i++) {{
        const fl = new THREE.Mesh(floatLeafGeo, floatLeafMat);
        const rad = 2.2 + Math.random() * 0.8;
        const theta = (i / 7) * Math.PI * 2;
        fl.position.set(Math.cos(theta) * rad, -0.5 + Math.random() * 1.6, Math.sin(theta) * rad);
        fl.rotation.set(Math.random() * Math.PI, Math.random() * Math.PI, Math.random() * Math.PI);
        floatingLeavesGroup.add(fl);
        floatLeaves.push({{ mesh: fl, rad: rad, speed: 0.008 + Math.random() * 0.01, theta: theta }});
    }}

    // Ambient Sparkle Particles
    const pCount = 80;
    const pGeo = new THREE.BufferGeometry();
    const pPos = new Float32Array(pCount * 3);
    for (let i = 0; i < pCount; i++) {{
        pPos[i * 3] = (Math.random() - 0.5) * 6;
        pPos[i * 3 + 1] = (Math.random() - 0.5) * 4;
        pPos[i * 3 + 2] = (Math.random() - 0.5) * 5;
    }}
    pGeo.setAttribute('position', new THREE.BufferAttribute(pPos, 3));
    const pMat = new THREE.PointsMaterial({{
        color: 0x00d2ff,
        size: 0.05,
        transparent: true,
        opacity: 0.65,
        blending: THREE.AdditiveBlending
    }});
    const sparkles = new THREE.Points(pGeo, pMat);
    mainGroup.add(sparkles);

    // -------------------------------------------------------------------------
    // 6. Interactive Mouse Parallax & Animation Loop
    // -------------------------------------------------------------------------
    let targetRotX = 0;
    let targetRotY = 0;
    let clock = new THREE.Clock();
    
    window.addEventListener('mousemove', (e) => {{
        const rect = container.getBoundingClientRect();
        const x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
        const y = -(((e.clientY - rect.top) / rect.height) * 2 - 1);
        targetRotY = x * 0.35;
        targetRotX = -y * 0.2;
    }});
    
    function animate() {{
        requestAnimationFrame(animate);
        const t = clock.getElapsedTime();
        
        // Smooth Parallax Lerp
        mainGroup.rotation.y += (targetRotY - mainGroup.rotation.y) * 0.06;
        mainGroup.rotation.x += (targetRotX - mainGroup.rotation.x) * 0.06;
        
        // Gentle Floating Bobbing Motion
        containerGroup.position.y = -0.15 + Math.sin(t * 1.5) * 0.03;
        
        // Radar Pulse Scale
        const scalePulse = 1.0 + Math.sin(t * 4) * 0.08;
        radarRing.scale.set(scalePulse, scalePulse, scalePulse);
        
        // Floating Leaves Orbit
        floatLeaves.forEach((fl) => {{
            fl.theta += fl.speed;
            fl.mesh.position.x = Math.cos(fl.theta) * fl.rad;
            fl.mesh.position.z = Math.sin(fl.theta) * fl.rad;
            fl.mesh.position.y += Math.sin(t * 2 + fl.theta) * 0.003;
            fl.mesh.rotation.y += 0.015;
            fl.mesh.rotation.x += 0.01;
        }});
        
        sparkles.rotation.y = t * 0.04;
        
        renderer.render(scene, camera);
    }}
    animate();
    
    // Resize Handler
    window.addEventListener('resize', () => {{
        const newW = container.clientWidth || window.innerWidth;
        const newH = container.clientHeight || {height};
        camera.aspect = newW / newH;
        camera.updateProjectionMatrix();
        renderer.setSize(newW, newH);
    }});
}})();
</script>
</body>
</html>
"""


def get_3d_ai_flow_html(height: int = 180) -> str:
    """
    Renders the 3D Hologram AI Orb with orbiting particle rings.
    """
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; overflow: hidden; }}
    body {{ background: transparent; width: 100vw; height: {height}px; display: flex; align-items: center; justify-content: center; }}
    #orb-canvas {{ width: 100%; height: 100%; }}
</style>
</head>
<body>
<div id="orb-canvas"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
(function() {{
    const container = document.getElementById('orb-canvas');
    const width = container.clientWidth || 240;
    const height = container.clientHeight || {height};
    
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
    camera.position.z = 4.2;
    
    const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);
    
    const orbGroup = new THREE.Group();
    scene.add(orbGroup);
    
    // Core Glowing Sphere
    const coreGeo = new THREE.SphereGeometry(0.85, 32, 32);
    const coreMat = new THREE.MeshBasicMaterial({{
        color: 0x00d2ff,
        wireframe: true,
        transparent: true,
        opacity: 0.65
    }});
    const coreMesh = new THREE.Mesh(coreGeo, coreMat);
    orbGroup.add(coreMesh);
    
    // Inner Sphere
    const inGeo = new THREE.SphereGeometry(0.65, 24, 24);
    const inMat = new THREE.MeshBasicMaterial({{
        color: 0x9333ea,
        wireframe: false,
        transparent: true,
        opacity: 0.75
    }});
    const inMesh = new THREE.Mesh(inGeo, inMat);
    orbGroup.add(inMesh);
    
    // Orbiting Ring 1
    const r1Geo = new THREE.TorusGeometry(1.2, 0.02, 16, 64);
    const r1Mat = new THREE.MeshBasicMaterial({{ color: 0x00d2ff }});
    const r1 = new THREE.Mesh(r1Geo, r1Mat);
    orbGroup.add(r1);
    
    // Orbiting Ring 2
    const r2Geo = new THREE.TorusGeometry(1.35, 0.02, 16, 64);
    const r2Mat = new THREE.MeshBasicMaterial({{ color: 0x10b981 }});
    const r2 = new THREE.Mesh(r2Geo, r2Mat);
    r2.rotation.x = Math.PI / 3;
    orbGroup.add(r2);
    
    let clock = new THREE.Clock();
    function animate() {{
        requestAnimationFrame(animate);
        const t = clock.getElapsedTime();
        coreMesh.rotation.y = t * 0.4;
        coreMesh.rotation.x = t * 0.2;
        inMesh.rotation.y = -t * 0.3;
        r1.rotation.y = t * 0.6;
        r1.rotation.x = t * 0.3;
        r2.rotation.y = -t * 0.5;
        r2.rotation.z = t * 0.4;
        
        const pulse = 1.0 + Math.sin(t * 3) * 0.06;
        orbGroup.scale.set(pulse, pulse, pulse);
        
        renderer.render(scene, camera);
    }}
    animate();
}})();
</script>
</body>
</html>
"""
