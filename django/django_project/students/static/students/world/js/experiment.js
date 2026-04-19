/**
 * experiment.js — Experimental environment for Performance World
 *
 * Same interface as city.js: createCity(scene, subjectObjects, destination)
 * Returns { group, updateLights, cameraConfig }
 */

function createCity(scene, subjectObjects, destination) {
	var spaceGroup = new THREE.Group();

	// ─── DEEP SPACE BACKGROUND ──────────────────────────────────────
	(function () {
		var skyCanvas = document.createElement("canvas");
		skyCanvas.width = 2048;
		skyCanvas.height = 1024;
		var ctx = skyCanvas.getContext("2d");

		// Deep space gradient
		var skyGrad = ctx.createLinearGradient(0, 0, 0, 1024);
		skyGrad.addColorStop(0, "#000005");
		skyGrad.addColorStop(0.3, "#020012");
		skyGrad.addColorStop(0.5, "#050018");
		skyGrad.addColorStop(0.7, "#080020");
		skyGrad.addColorStop(1, "#030010");
		ctx.fillStyle = skyGrad;
		ctx.fillRect(0, 0, 2048, 1024);

		// Nebula clouds (purple/blue/pink)
		var nebulae = [
			{ x: 400, y: 300, r: 250, color: [80, 20, 120] },
			{ x: 1200, y: 500, r: 300, color: [20, 40, 100] },
			{ x: 1700, y: 200, r: 180, color: [100, 20, 60] },
			{ x: 800, y: 700, r: 200, color: [30, 60, 90] },
		];
		nebulae.forEach(function (n) {
			var nebGrad = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, n.r);
			nebGrad.addColorStop(0, "rgba(" + n.color[0] + "," + n.color[1] + "," + n.color[2] + ",0.15)");
			nebGrad.addColorStop(0.5, "rgba(" + n.color[0] + "," + n.color[1] + "," + n.color[2] + ",0.06)");
			nebGrad.addColorStop(1, "rgba(0,0,0,0)");
			ctx.fillStyle = nebGrad;
			ctx.fillRect(n.x - n.r, n.y - n.r, n.r * 2, n.r * 2);
		});

		// Milky Way band (diagonal glow)
		ctx.save();
		ctx.translate(1024, 400);
		ctx.rotate(-0.3);
		var milkyGrad = ctx.createLinearGradient(-800, -60, 800, 60);
		milkyGrad.addColorStop(0, "rgba(0,0,0,0)");
		milkyGrad.addColorStop(0.3, "rgba(60,50,80,0.06)");
		milkyGrad.addColorStop(0.5, "rgba(80,70,100,0.08)");
		milkyGrad.addColorStop(0.7, "rgba(60,50,80,0.06)");
		milkyGrad.addColorStop(1, "rgba(0,0,0,0)");
		ctx.fillStyle = milkyGrad;
		ctx.fillRect(-800, -80, 1600, 160);
		ctx.restore();

		var skyTexture = new THREE.CanvasTexture(skyCanvas);
		scene.background = skyTexture;
	})();

	// ─── 1. FLOATING PLATFORM (transparent glass deck) ──────────────
	var platformSize = 60;
	var platformGeo = new THREE.PlaneGeometry(platformSize, platformSize);
	var platformTex = new THREE.TextureLoader().load("/static/students/world/images/experiment_ground.png");
	platformTex.encoding = THREE.sRGBEncoding;
	platformTex.wrapS = THREE.ClampToEdgeWrapping;
	platformTex.wrapT = THREE.ClampToEdgeWrapping;
	platformTex.minFilter = THREE.LinearMipmapLinearFilter;
	platformTex.magFilter = THREE.LinearFilter;

	var platformMat = new THREE.MeshStandardMaterial({
		map: platformTex,
		side: THREE.DoubleSide,
		roughness: 1.0,
		metalness: 0.0,
	});

	var platform = new THREE.Mesh(platformGeo, platformMat);
	platform.rotation.x = -Math.PI / 2;
	platform.position.y = -0.05;
	spaceGroup.add(platform);

	// ─── DESTINATION FLAG (replaces yellow sphere visually) ─────────
	var destinationFlag = new THREE.Group();

	var poleGeo = new THREE.CylinderGeometry(0.08, 0.08, 3.5, 12);
	var poleMat = new THREE.MeshStandardMaterial({
		color: 0xd9d9d9,
		roughness: 0.4,
		metalness: 0.5,
	});
	var flagPole = new THREE.Mesh(poleGeo, poleMat);
	flagPole.position.y = 1.75;
	destinationFlag.add(flagPole);

	var flagTex = new THREE.TextureLoader().load("/static/students/world/images/destiny.png");
	flagTex.encoding = THREE.sRGBEncoding;
	flagTex.minFilter = THREE.LinearMipmapLinearFilter;
	flagTex.magFilter = THREE.LinearFilter;

	var flagGeo = new THREE.PlaneGeometry(2.0, 1.0);
	var flagMat = new THREE.MeshStandardMaterial({
		map: flagTex,
		transparent: true,
		side: THREE.DoubleSide,
		roughness: 0.7,
		metalness: 0.0,
	});
	var flagCloth = new THREE.Mesh(flagGeo, flagMat);
	flagCloth.position.set(1.0, 2.7, 0);
	destinationFlag.add(flagCloth);

	// Keep world.js destination logic intact, only hide the yellow sphere visuals.
	destination.material.transparent = true;
	destination.material.opacity = 0;
	destination.material.depthWrite = false;
	destination.scale.set(1, 1, 1);

	scene.add(destinationFlag);

	// Platform edge glow ring
	var edgeGeo = new THREE.RingGeometry(29, 30, 64);
	var edgeMat = new THREE.MeshBasicMaterial({
		color: 0x2244aa,
		transparent: true,
		opacity: 0.25,
		side: THREE.DoubleSide,
	});
	var edgeRing = new THREE.Mesh(edgeGeo, edgeMat);
	edgeRing.rotation.x = -Math.PI / 2;
	edgeRing.position.y = 0.01;
	spaceGroup.add(edgeRing);

	// ─── 2. DISTANT PLANET ──────────────────────────────────────────
	var planetGeo = new THREE.SphereGeometry(8, 32, 32);
	var planetMat = new THREE.MeshStandardMaterial({
		color: 0x334488,
		emissive: 0x112244,
		emissiveIntensity: 0.3,
	});
	var planet = new THREE.Mesh(planetGeo, planetMat);
	planet.position.set(-60, 15, -80);
	spaceGroup.add(planet);

	// Planet atmosphere glow
	var atmosGeo = new THREE.SphereGeometry(8.5, 32, 32);
	var atmosMat = new THREE.MeshBasicMaterial({
		color: 0x4466cc,
		transparent: true,
		opacity: 0.12,
		side: THREE.BackSide,
	});
	var atmosphere = new THREE.Mesh(atmosGeo, atmosMat);
	atmosphere.position.copy(planet.position);
	spaceGroup.add(atmosphere);

	// ─── 4. FLOATING PARTICLES (space dust) ─────────────────────────
	var dustCount = 200;
	var dustGeo = new THREE.BufferGeometry();
	var dustPositions = new Float32Array(dustCount * 3);
	var dustColors = new Float32Array(dustCount * 3);

	for (var di = 0; di < dustCount; di++) {
		dustPositions[di * 3] = (Math.random() - 0.5) * 100;
		dustPositions[di * 3 + 1] = -3 + Math.random() * 10;
		dustPositions[di * 3 + 2] = (Math.random() - 0.5) * 100;

		var dc = Math.random();
		if (dc > 0.7) {
			dustColors[di * 3] = 0.3; dustColors[di * 3 + 1] = 0.5; dustColors[di * 3 + 2] = 1.0;
		} else if (dc > 0.4) {
			dustColors[di * 3] = 0.6; dustColors[di * 3 + 1] = 0.4; dustColors[di * 3 + 2] = 0.8;
		} else {
			dustColors[di * 3] = 0.8; dustColors[di * 3 + 1] = 0.8; dustColors[di * 3 + 2] = 0.9;
		}
	}

	dustGeo.setAttribute("position", new THREE.BufferAttribute(dustPositions, 3));
	dustGeo.setAttribute("color", new THREE.BufferAttribute(dustColors, 3));

	var dustMat = new THREE.PointsMaterial({
		size: 0.2,
		vertexColors: true,
		transparent: true,
		opacity: 0.6,
		sizeAttenuation: true,
	});

	var spaceDust = new THREE.Points(dustGeo, dustMat);
	spaceGroup.add(spaceDust);

	// ─── 5. ROTATE GROUP ────────────────────────────────────────────
	spaceGroup.rotation.y = -Math.PI / 2;

	scene.add(spaceGroup);

	// ─── 6. ANIMATE (call in animate loop) ──────────────────────────
	function updateCityLights() {
		var time = Date.now() * 0.001;

		// Keep flag anchored to destination position without inheriting sphere spin.
		destinationFlag.position.copy(destination.position);

		// Drift space dust
		var posArr = spaceDust.geometry.attributes.position.array;
		for (var ui = 0; ui < dustCount; ui++) {
			posArr[ui * 3 + 1] += Math.sin(time + ui * 0.3) * 0.003;
		}
		spaceDust.geometry.attributes.position.needsUpdate = true;
		spaceDust.material.opacity = 0.4 + Math.sin(time * 0.8) * 0.15;

		// Planet rotation
		planet.rotation.y += 0.001;
	}

	console.log("Space environment created");

	return {
		group: spaceGroup,
		updateLights: updateCityLights,
		cameraConfig: { maxPolarAngle: Math.PI, minDistance: 0.5, maxDistance: 500 },
	};
}
