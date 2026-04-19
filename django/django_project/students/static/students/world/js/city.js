/**
 * city.js — Cinematic aerial city environment for Performance World
 *
 * Creates a rotated city scene so Z-axis movement appears LEFT → RIGHT.
 * All elements are inside a single THREE.Group rotated -90° on Y.
 *
 * Usage: var city = createCity(scene, subjectObjects, destination);
 *        // In animate loop: city.updateLights();
 */

function createCity(scene, subjectObjects, destination) {
	var cityGroup = new THREE.Group();

	// ─── CITY NIGHT SKYLINE BACKGROUND ──────────────────────────────
	(function () {
		var skyCanvas = document.createElement("canvas");
		skyCanvas.width = 2048;
		skyCanvas.height = 1024;
		var ctx = skyCanvas.getContext("2d");

		var skyGrad = ctx.createLinearGradient(0, 0, 0, 1024);
		skyGrad.addColorStop(0, "#020010");
		skyGrad.addColorStop(0.3, "#050520");
		skyGrad.addColorStop(0.55, "#0a0a30");
		skyGrad.addColorStop(0.7, "#101845");
		skyGrad.addColorStop(0.85, "#1a2050");
		skyGrad.addColorStop(1, "#0d1225");
		ctx.fillStyle = skyGrad;
		ctx.fillRect(0, 0, 2048, 1024);

		for (var s = 0; s < 400; s++) {
			var sx = Math.random() * 2048;
			var sy = Math.random() * 600;
			var sr = 0.3 + Math.random() * 1.2;
			var brightness = 150 + Math.floor(Math.random() * 105);
			ctx.fillStyle = "rgba(" + brightness + "," + brightness + "," + (brightness + 30) + "," + (0.4 + Math.random() * 0.6) + ")";
			ctx.beginPath();
			ctx.arc(sx, sy, sr, 0, Math.PI * 2);
			ctx.fill();
		}

		var hazeGrad = ctx.createLinearGradient(0, 550, 0, 720);
		hazeGrad.addColorStop(0, "rgba(20,25,60,0)");
		hazeGrad.addColorStop(0.5, "rgba(30,40,80,0.3)");
		hazeGrad.addColorStop(1, "rgba(15,20,40,0)");
		ctx.fillStyle = hazeGrad;
		ctx.fillRect(0, 550, 2048, 170);

		var layers = [
			{ y: 680, minH: 40, maxH: 200, color: "#06060f", windowChance: 0.15, count: 60 },
			{ y: 700, minH: 30, maxH: 160, color: "#08081a", windowChance: 0.25, count: 50 },
			{ y: 720, minH: 20, maxH: 120, color: "#0c0c24", windowChance: 0.35, count: 45 },
		];

		layers.forEach(function (layer) {
			for (var b = 0; b < layer.count; b++) {
				var bx = Math.random() * 2048;
				var bw = 10 + Math.random() * 35;
				var bh = layer.minH + Math.random() * (layer.maxH - layer.minH);
				var by = layer.y - bh;
				ctx.fillStyle = layer.color;
				ctx.fillRect(bx, by, bw, bh);
				if (Math.random() > 0.6) {
					ctx.fillStyle = "rgba(255,100,50,0.4)";
					ctx.fillRect(bx + bw * 0.3, by - 2, bw * 0.4, 2);
				}
				if (bh > 120 && Math.random() > 0.5) {
					ctx.strokeStyle = "rgba(255,80,80,0.5)";
					ctx.lineWidth = 1;
					ctx.beginPath();
					ctx.moveTo(bx + bw / 2, by);
					ctx.lineTo(bx + bw / 2, by - 8 - Math.random() * 12);
					ctx.stroke();
					ctx.fillStyle = "rgba(255,50,50,0.8)";
					ctx.beginPath();
					ctx.arc(bx + bw / 2, by - 8 - Math.random() * 12, 1.5, 0, Math.PI * 2);
					ctx.fill();
				}
				for (var wx = bx + 2; wx < bx + bw - 3; wx += 5) {
					for (var wy = by + 4; wy < by + bh - 3; wy += 6) {
						if (Math.random() < layer.windowChance) {
							var warmth = Math.random();
							if (warmth > 0.7) {
								ctx.fillStyle = "rgba(255,220,100," + (0.5 + Math.random() * 0.5) + ")";
							} else if (warmth > 0.4) {
								ctx.fillStyle = "rgba(180,200,255," + (0.3 + Math.random() * 0.4) + ")";
							} else {
								ctx.fillStyle = "rgba(100,180,255," + (0.2 + Math.random() * 0.3) + ")";
							}
							ctx.fillRect(wx, wy, 3, 3);
						}
					}
				}
			}
		});

		var glowGrad = ctx.createLinearGradient(0, 650, 0, 1024);
		glowGrad.addColorStop(0, "rgba(30,25,60,0)");
		glowGrad.addColorStop(0.4, "rgba(40,35,70,0.2)");
		glowGrad.addColorStop(1, "rgba(10,10,20,0.9)");
		ctx.fillStyle = glowGrad;
		ctx.fillRect(0, 650, 2048, 374);

		var accents = [
			{ x: 300, color: "rgba(0,150,255,0.08)" },
			{ x: 900, color: "rgba(255,50,100,0.06)" },
			{ x: 1500, color: "rgba(0,255,150,0.06)" },
		];
		accents.forEach(function (a) {
			var aGrad = ctx.createRadialGradient(a.x, 720, 10, a.x, 720, 200);
			aGrad.addColorStop(0, a.color);
			aGrad.addColorStop(1, "rgba(0,0,0,0)");
			ctx.fillStyle = aGrad;
			ctx.fillRect(a.x - 200, 520, 400, 400);
		});

		var skyTexture = new THREE.CanvasTexture(skyCanvas);
		scene.background = skyTexture;
	})();

	// ─── 1. BASE LAYER — Procedural aerial city ground plane ────────
	var groundSize = 200;
	var groundGeo = new THREE.PlaneGeometry(groundSize, groundSize);

	// Procedural city texture (no external image needed)
	var groundCanvas = document.createElement("canvas");
	groundCanvas.width = 2048;
	groundCanvas.height = 2048;
	var ctx = groundCanvas.getContext("2d");

	// Dark base
	ctx.fillStyle = "#0a0a14";
	ctx.fillRect(0, 0, 2048, 2048);

	var groundTex = new THREE.CanvasTexture(groundCanvas);
	groundTex.wrapS = THREE.RepeatWrapping;
	groundTex.wrapT = THREE.RepeatWrapping;

	var groundMat = new THREE.MeshBasicMaterial({
		map: groundTex,
		side: THREE.DoubleSide,
		transparent: true,
		opacity: 0.9,
	});

	var ground = new THREE.Mesh(groundGeo, groundMat);
	ground.rotation.x = -Math.PI / 2;
	ground.position.y = -0.05;
	cityGroup.add(ground);

	// ─── 2. BOUNDARY GLOW RING ───────────────────────────────────────
	var ringGeo = new THREE.RingGeometry(38, 40, 32);
	var ringMat = new THREE.MeshBasicMaterial({
		color: 0x1a1a3e,
		transparent: true,
		opacity: 0.3,
		side: THREE.DoubleSide,
	});
	var ring = new THREE.Mesh(ringGeo, ringMat);
	ring.rotation.x = -Math.PI / 2;
	ring.position.y = 0.01;
	cityGroup.add(ring);

	// ─── 5. ROTATE GROUP — Z movement appears LEFT → RIGHT ──────────
	cityGroup.rotation.y = -Math.PI / 2;

	scene.add(cityGroup);

	// ─── 6. UPDATE (call in animate loop) ────────────────────────────
	function updateCityLights() {
		// no-op: roads and lights removed
	}

	console.log("City environment created");

	return {
		group: cityGroup,
		updateLights: updateCityLights,
		cameraConfig: { maxPolarAngle: Math.PI / 2.2, minDistance: 10, maxDistance: 80 },
	};
}
