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

	// Grid roads
	ctx.strokeStyle = "#1a1a2e";
	ctx.lineWidth = 3;
	for (var gx = 0; gx < 2048; gx += 64) {
		ctx.beginPath();
		ctx.moveTo(gx, 0);
		ctx.lineTo(gx, 2048);
		ctx.stroke();
	}
	for (var gy = 0; gy < 2048; gy += 64) {
		ctx.beginPath();
		ctx.moveTo(0, gy);
		ctx.lineTo(2048, gy);
		ctx.stroke();
	}

	// Main avenues (brighter)
	ctx.strokeStyle = "#2a2a3e";
	ctx.lineWidth = 6;
	for (var mx = 0; mx < 2048; mx += 256) {
		ctx.beginPath();
		ctx.moveTo(mx, 0);
		ctx.lineTo(mx, 2048);
		ctx.stroke();
		ctx.beginPath();
		ctx.moveTo(0, mx);
		ctx.lineTo(2048, mx);
		ctx.stroke();
	}

	// Building blocks (dark rectangles between roads)
	for (var bx = 0; bx < 2048; bx += 64) {
		for (var by = 0; by < 2048; by += 64) {
			if (Math.random() > 0.3) {
				var pad = 6;
				var bw = 64 - pad * 2;
				ctx.fillStyle = "rgba(10, 10, 25, " + (0.5 + Math.random() * 0.5) + ")";
				ctx.fillRect(bx + pad, by + pad, bw, bw);
			}
		}
	}

	// Intersection lights
	ctx.fillStyle = "#ffcc00";
	for (var ix = 0; ix < 2048; ix += 256) {
		for (var iy = 0; iy < 2048; iy += 256) {
			ctx.beginPath();
			ctx.arc(ix, iy, 4, 0, Math.PI * 2);
			ctx.fill();
		}
	}

	var groundTex = new THREE.CanvasTexture(groundCanvas);
	groundTex.wrapS = THREE.RepeatWrapping;
	groundTex.wrapT = THREE.RepeatWrapping;

	var groundMat = new THREE.MeshBasicMaterial({
		map: groundTex,
		side: THREE.DoubleSide,
	});

	var ground = new THREE.Mesh(groundGeo, groundMat);
	ground.rotation.x = -Math.PI / 2;
	ground.position.y = -0.05;
	cityGroup.add(ground);

	// ─── 2. SUBJECT ROAD GLOW STRIPS ────────────────────────────────
	var subjectColors = {
		"Math": 0x3399ff,
		"Reasoning": 0x33ff66,
		"English": 0xff4444,
	};

	if (subjectObjects && subjectObjects.length > 0) {
		subjectObjects.forEach(function (obj) {
			var name = obj.data.name || "";
			var roadX = obj.road.position.x;
			var roadZ = obj.road.position.z;
			var roadLen = obj.road.geometry.parameters.depth || 10;
			var color = subjectColors[name] || 0x4488ff;

			// Glowing road strip along Z-axis
			var stripGeo = new THREE.PlaneGeometry(0.4, roadLen);
			var stripMat = new THREE.MeshBasicMaterial({
				color: color,
				transparent: true,
				opacity: 0.35,
				side: THREE.DoubleSide,
			});
			var strip = new THREE.Mesh(stripGeo, stripMat);
			strip.rotation.x = -Math.PI / 2;
			strip.position.set(roadX, 0.01, roadZ);
			cityGroup.add(strip);

			// Edge glow lines
			for (var side = -1; side <= 1; side += 2) {
				var edgeGeo = new THREE.PlaneGeometry(0.08, roadLen);
				var edgeMat = new THREE.MeshBasicMaterial({
					color: color,
					transparent: true,
					opacity: 0.6,
					side: THREE.DoubleSide,
				});
				var edge = new THREE.Mesh(edgeGeo, edgeMat);
				edge.rotation.x = -Math.PI / 2;
				edge.position.set(roadX + side * 0.9, 0.02, roadZ);
				cityGroup.add(edge);
			}
		});
	}

	// ─── 3. DESTINATION MONUMENT ─────────────────────────────────────
	var destPos = destination ? destination.position.clone() : new THREE.Vector3(0, 1.5, -12);

	// Tower base (cylinder)
	var towerBaseGeo = new THREE.CylinderGeometry(0.6, 0.8, 3, 8);
	var towerBaseMat = new THREE.MeshStandardMaterial({
		color: 0xffcc00,
		emissive: 0xffaa00,
		emissiveIntensity: 0.8,
	});
	var towerBase = new THREE.Mesh(towerBaseGeo, towerBaseMat);
	towerBase.position.set(destPos.x, 1.5, destPos.z);
	cityGroup.add(towerBase);

	// Tower top (box spire)
	var spireGeo = new THREE.BoxGeometry(0.3, 1.5, 0.3);
	var spireMat = new THREE.MeshStandardMaterial({
		color: 0xffff00,
		emissive: 0xffff00,
		emissiveIntensity: 1.5,
	});
	var spire = new THREE.Mesh(spireGeo, spireMat);
	spire.position.set(destPos.x, 3.5, destPos.z);
	cityGroup.add(spire);

	// Floating exam billboard
	var billboardCanvas = document.createElement("canvas");
	billboardCanvas.width = 512;
	billboardCanvas.height = 128;
	var bCtx = billboardCanvas.getContext("2d");

	bCtx.fillStyle = "rgba(0, 0, 0, 0.7)";
	bCtx.fillRect(0, 0, 512, 128);
	bCtx.strokeStyle = "#ffcc00";
	bCtx.lineWidth = 3;
	bCtx.strokeRect(4, 4, 504, 120);
	bCtx.fillStyle = "#ffffff";
	bCtx.font = "bold 36px Arial";
	bCtx.textAlign = "center";
	bCtx.fillText("DESTINATION", 256, 50);
	bCtx.font = "24px Arial";
	bCtx.fillStyle = "#ffcc00";
	bCtx.fillText("Your Goal Awaits", 256, 90);

	var billboardTex = new THREE.CanvasTexture(billboardCanvas);
	var billboardMat = new THREE.SpriteMaterial({
		map: billboardTex,
		transparent: true,
	});
	var billboard = new THREE.Sprite(billboardMat);
	billboard.scale.set(5, 1.25, 1);
	billboard.position.set(destPos.x, 5.5, destPos.z);
	cityGroup.add(billboard);

	// ─── 4. CITY LIGHTS (lightweight points) ─────────────────────────
	var lightCount = 120;
	var lightGeo = new THREE.BufferGeometry();
	var positions = new Float32Array(lightCount * 3);
	var colors = new Float32Array(lightCount * 3);

	var lightColors = [
		[1.0, 0.9, 0.4],   // warm yellow
		[0.4, 0.8, 1.0],   // cool blue
		[1.0, 0.5, 0.2],   // orange
		[0.3, 1.0, 0.5],   // green
	];

	for (var li = 0; li < lightCount; li++) {
		positions[li * 3] = (Math.random() - 0.5) * 80;
		positions[li * 3 + 1] = 0.1 + Math.random() * 0.3;
		positions[li * 3 + 2] = (Math.random() - 0.5) * 80;

		var lc = lightColors[Math.floor(Math.random() * lightColors.length)];
		colors[li * 3] = lc[0];
		colors[li * 3 + 1] = lc[1];
		colors[li * 3 + 2] = lc[2];
	}

	lightGeo.setAttribute("position", new THREE.BufferAttribute(positions, 3));
	lightGeo.setAttribute("color", new THREE.BufferAttribute(colors, 3));

	var lightMat = new THREE.PointsMaterial({
		size: 0.4,
		vertexColors: true,
		transparent: true,
		opacity: 0.8,
		sizeAttenuation: true,
	});

	var cityLights = new THREE.Points(lightGeo, lightMat);
	cityGroup.add(cityLights);

	// ─── 5. BOUNDARY GLOW RING ───────────────────────────────────────
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

	// ─── 6. ROTATE GROUP — Z movement appears LEFT → RIGHT ──────────
	cityGroup.rotation.y = -Math.PI / 2;

	scene.add(cityGroup);

	// ─── 7. LIGHT FLICKER UPDATE (call in animate loop) ──────────────
	function updateCityLights() {
		var time = Date.now() * 0.001;
		var posArr = cityLights.geometry.attributes.position.array;

		for (var ui = 0; ui < lightCount; ui++) {
			posArr[ui * 3 + 1] = 0.1 + Math.sin(time * 2 + ui * 0.7) * 0.08;
		}
		cityLights.geometry.attributes.position.needsUpdate = true;
		cityLights.material.opacity = 0.6 + Math.sin(time * 1.5) * 0.2;
	}

	console.log("City environment created");

	return {
		group: cityGroup,
		updateLights: updateCityLights,
	};
}
