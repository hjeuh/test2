from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>3D Object Playground</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
        <style>
            body {
                margin: 0;
                overflow: hidden;
                background: url('https://www.transparenttextures.com/patterns/asfalt-light.png');
            }
            #scene-container {
                width: 100vw;
                height: 100vh;
            }
        </style>
    </head>
    <body>
        <h1 style="text-align: center; color: white;">3D Object Playground</h1>
        <div id="scene-container"></div>
        <div id="controls" style="position: absolute; top: 10px; right: 10px; background: rgba(255, 255, 255, 0.8); padding: 10px; border-radius: 8px;">
            <label>Choose Object: 
                <select id="object-selector">
                    <option value="cube">Cube</option>
                    <option value="sphere">Sphere</option>
                    <option value="cylinder">Cylinder</option>
                    <option value="cone">Cone</option>
                    <option value="torus">Torus</option>
                    <option value="tetrahedron">Tetrahedron</option>
                    <option value="octahedron">Octahedron</option>
                    <option value="dodecahedron">Dodecahedron</option>
                    <option value="icosahedron">Icosahedron</option>
                    <option value="torusknot">Torus Knot</option>
                    <option value="nested_sphere_cube">Nested Sphere in Cube</option>
                    <option value="nested_tetra_octa">Nested Tetrahedron in Octahedron</option>
                    <option value="nested_cutout">Cut-out Sphere in Cube</option>
                </select>
            </label><br>
            <label>Size: <input type="range" id="size-slider" min="0.5" max="5" step="0.1" value="1"></label><br>
            <label>Rotation Speed: <input type="range" id="rotation-slider" min="0" max="5" step="0.1" value="1"></label><br>
            <label>Scale: <input type="range" id="scale-slider" min="0.5" max="3" step="0.1" value="1"></label><br>
            <label>Opacity: <input type="range" id="opacity-slider" min="0.1" max="1" step="0.1" value="1"></label><br>
            <label>Wireframe: <input type="checkbox" id="wireframe-toggle"></label><br>
            <label>Color: <input type="color" id="color-picker" value="#ffa500"></label>
        </div>
        <script>
            let currentObject;
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            document.getElementById('scene-container').appendChild(renderer.domElement);

            const controls = new THREE.OrbitControls(camera, renderer.domElement);
            camera.position.z = 10;

            const ambientLight = new THREE.AmbientLight(0x606060, 0.8);
            scene.add(ambientLight);

            const pointLight = new THREE.PointLight(0xffffff, 1, 100);
            pointLight.position.set(5, 5, 5);
            scene.add(pointLight);

            function createObject(type, size, color, opacity, wireframe) {
                if (currentObject) {
                    scene.remove(currentObject);
                }

                const material = new THREE.MeshPhongMaterial({
                    color: color,
                    opacity: opacity,
                    transparent: true,
                    wireframe: wireframe
                });

                let geometry;
                let group;

                switch (type) {
                    case 'cube':
                        geometry = new THREE.BoxGeometry(size, size, size);
                        break;
                    case 'sphere':
                        geometry = new THREE.SphereGeometry(size, 32, 32);
                        break;
                    case 'cylinder':
                        geometry = new THREE.CylinderGeometry(size, size, size * 2, 32);
                        break;
                    case 'cone':
                        geometry = new THREE.ConeGeometry(size, size * 2, 32);
                        break;
                    case 'torus':
                        geometry = new THREE.TorusGeometry(size, size / 3, 16, 100);
                        break;
                    case 'tetrahedron':
                        geometry = new THREE.TetrahedronGeometry(size, 0);
                        break;
                    case 'octahedron':
                        geometry = new THREE.OctahedronGeometry(size, 0);
                        break;
                    case 'dodecahedron':
                        geometry = new THREE.DodecahedronGeometry(size, 0);
                        break;
                    case 'icosahedron':
                        geometry = new THREE.IcosahedronGeometry(size, 0);
                        break;
                    case 'torusknot':
                        geometry = new THREE.TorusKnotGeometry(size, size / 4, 100, 16);
                        break;
                    case 'nested_sphere_cube':
                        group = new THREE.Group();
                        const outerCube = new THREE.Mesh(new THREE.BoxGeometry(size, size, size), material);
                        const innerSphere = new THREE.Mesh(new THREE.SphereGeometry(size / 2, 32, 32), material);
                        group.add(outerCube);
                        group.add(innerSphere);
                        currentObject = group;
                        scene.add(group);
                        return;
                    case 'nested_tetra_octa':
                        group = new THREE.Group();
                        const outerTetra = new THREE.Mesh(new THREE.TetrahedronGeometry(size, 0), material);
                        const innerOcta = new THREE.Mesh(new THREE.OctahedronGeometry(size / 2, 0), material);
                        group.add(outerTetra);
                        group.add(innerOcta);
                        currentObject = group;
                        scene.add(group);
                        return;
                    case 'nested_cutout':
                        group = new THREE.Group();
                        const cutCube = new THREE.Mesh(new THREE.BoxGeometry(size, size, size), material);
                        const cutSphere = new THREE.Mesh(new THREE.SphereGeometry(size / 1.5, 32, 32), new THREE.MeshBasicMaterial({ color: 0x000000, wireframe: true }));
                        group.add(cutCube);
                        group.add(cutSphere);
                        cutSphere.position.set(0, 0, 0);
                        currentObject = group;
                        scene.add(group);
                        return;
                    default:
                        geometry = new THREE.BoxGeometry(size, size, size);
                }

                currentObject = new THREE.Mesh(geometry, material);
                scene.add(currentObject);
            }

            let rotationSpeed = 1;
            createObject('cube', 1, '#ffa500', 1, false);

            const updateObject = () => {
                const type = document.getElementById('object-selector').value;
                const size = parseFloat(document.getElementById('size-slider').value);
                const rotation = parseFloat(document.getElementById('rotation-slider').value);
                const scale = parseFloat(document.getElementById('scale-slider').value);
                const opacity = parseFloat(document.getElementById('opacity-slider').value);
                const wireframe = document.getElementById('wireframe-toggle').checked;
                const color = document.getElementById('color-picker').value;

                rotationSpeed = rotation;

                if (currentObject) {
                    currentObject.scale.set(scale, scale, scale);
                }
                createObject(type, size, color, opacity, wireframe);
            };

            document.querySelectorAll('#controls input, #controls select').forEach((el) => {
                el.addEventListener('input', updateObject);
            });

            function animate() {
                requestAnimationFrame(animate);
                if (currentObject) {
                    currentObject.rotation.x += rotationSpeed * 0.01;
                    currentObject.rotation.y += rotationSpeed * 0.01;
                }
                renderer.render(scene, camera);
            }
            animate();
        </script>
    </body>
    </html>
    '''
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True)
