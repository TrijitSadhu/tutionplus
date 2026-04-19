let subjectObjects = [];
let studentVehicle;
let targetZ = 0;
let currentZ = 0;
let ghostVehicles = [];
let success = false;
let particles = [];
let explosionTriggered = false;
let weakestObj = null;
let topicBlocks = [];
let topicLabels = [];
let bestTopicObj = null;
let insightsVisible = false;

function toggleInsights(show) {
	topicBlocks.forEach(function (block) {
		block.mesh.visible = show;
	});
	topicLabels.forEach(function (label) {
		label.visible = show;
	});
	var panel = document.getElementById("stats-panel");
	if (panel) {
		panel.style.display = show ? "block" : "none";
	}
}

function updateUI(data) {
	var insights = data.insights || [];
	var recommendation = data.recommendation || "";
	var level = data.level || "";

	var statsPanel = document.getElementById("stats-content");
	var html = "";
	html += '<h3 style="color:#00ffff;">Level: ' + level + "</h3>";
	if (insights.length > 0) {
		html += "<h4>Insights</h4>";
		insights.forEach(function (i) {
			html += '<p style="margin:5px 0;">\u2022 ' + i + "</p>";
		});
	}
	if (recommendation) {
		html += '<hr><p style="color:yellow;"><b>Next Step:</b><br>' + recommendation + "</p>";
	}
	statsPanel.innerHTML = html;
}

async function loadWorldState() {
	try {
		var response = await fetch("/api/world-state/");

		if (!response.ok) {
			throw new Error("Failed to fetch world state");
		}

		var data = await response.json();

		console.log("World State:", data);

		updateUI(data);

		return data;
	} catch (error) {
		console.error("Error loading world state:", error);
		return null;
	}
}

async function loadRaceData() {
	try {
		const response = await fetch("/api/cinematic-race/1/");

		if (!response.ok) throw new Error("Race API failed");

		const data = await response.json();

		console.log("Race Data:", data);

		return data;
	} catch (err) {
		console.error(err);
		return null;
	}
}

async function loadTopicInsights() {
	try {
		var response = await fetch("/api/topic-insights/");
		if (!response.ok) throw new Error("Topic insights API failed");
		var data = await response.json();
		console.log("Topic Insights:", data);
		return data;
	} catch (err) {
		console.error(err);
		return null;
	}
}

function createTextSprite(text) {
	var canvas = document.createElement("canvas");
	var context = canvas.getContext("2d");

	canvas.width = 256;
	canvas.height = 128;

	context.fillStyle = "white";
	context.font = "24px Arial";
	context.textAlign = "center";

	context.fillText(text, canvas.width / 2, canvas.height / 2);

	var texture = new THREE.CanvasTexture(canvas);

	var material = new THREE.SpriteMaterial({
		map: texture,
		transparent: true,
	});

	var sprite = new THREE.Sprite(material);

	sprite.scale.set(2, 1, 1);

	return sprite;
}

document.addEventListener("DOMContentLoaded", async function () {
	var canvas = document.getElementById("worldCanvas");
	var cityEnv = null;

	console.log("World JS Loaded");

	var toggleBtn = document.getElementById("toggleInsightsBtn");
	if (toggleBtn) {
		toggleBtn.addEventListener("click", function () {
			insightsVisible = !insightsVisible;
			toggleBtn.innerText = insightsVisible ? "Hide Insights" : "Show Insights";
			toggleInsights(insightsVisible);
		});
	}

	// Hide insights initially
	toggleInsights(false);

	if (!canvas) {
		console.error("Canvas not found");
		return;
	}

	console.log("Canvas found:", canvas);

	var scene = new THREE.Scene();

	var camera = new THREE.PerspectiveCamera(
		70,
		window.innerWidth / window.innerHeight,
		0.1,
		1000
	);

	var renderer = new THREE.WebGLRenderer({
		canvas: canvas,
		antialias: true,
	});

	renderer.setSize(window.innerWidth, window.innerHeight);

	const composer = new THREE.EffectComposer(renderer);
	const renderPass = new THREE.RenderPass(scene, camera);
	composer.addPass(renderPass);

	const bloomPass = new THREE.UnrealBloomPass(
		new THREE.Vector2(window.innerWidth, window.innerHeight),
		1.5,
		0.4,
		0.85
	);

	composer.addPass(bloomPass);

	bloomPass.threshold = 0.4;
	bloomPass.strength = 1.2;
	bloomPass.radius = 0.5;

	camera.position.set(0, 25, 30);
	camera.lookAt(0, 0, -6);

	// OrbitControls for zoom/rotate/pan
	var controls = new THREE.OrbitControls(camera, renderer.domElement);
	controls.enableDamping = true;
	controls.dampingFactor = 0.08;
	controls.minDistance = 10;
	controls.maxDistance = 80;
	controls.maxPolarAngle = Math.PI / 2.2;
	controls.target.set(0, 0, -4);

	var light = new THREE.AmbientLight(0xffffff, 0.3);
	scene.add(light);

	const raceGeometry = new THREE.BoxGeometry(2, 0.02, 12);
	const raceMaterial = new THREE.MeshBasicMaterial({
		color: 0x1a1a2e,
		transparent: true,
		opacity: 0.3,
	});
	const raceTrack = new THREE.Mesh(raceGeometry, raceMaterial);
	raceTrack.position.set(0, -0.5, -7);
	scene.add(raceTrack);

	studentVehicle = new THREE.Mesh(
		new THREE.BoxGeometry(0.6, 0.6, 0.6),
		new THREE.MeshBasicMaterial({ color: 0x00ffff })
	);
	scene.add(studentVehicle);

	var geometry = new THREE.SphereGeometry(1, 32, 32);
	var material = new THREE.MeshStandardMaterial({
		color: 0xffff00,
		emissive: 0xffff00,
		emissiveIntensity: 2,
	});
	var destination = new THREE.Mesh(geometry, material);
	destination.position.set(0, 1, -12);
	scene.add(destination);

	var destLabel = createTextSprite("DESTINATION");
	destLabel.position.set(0, 3, -12);
	scene.add(destLabel);

	const destLight = new THREE.PointLight(0xffff00, 2, 20);
	destLight.position.copy(destination.position);
	scene.add(destLight);

	function createSubjects(worldState) {
		subjectObjects = [];
		var total = worldState.subjects.length;
		var offset = (total - 1) / 2;

		worldState.subjects.forEach(function (subject, index) {
			var strength = subject.strength_score || 0;
			var prev = subject.previous_strength_score || strength;
			var confusion = subject.average_confusion_index || 0;
			var length = 10 - strength * 7;
			var startZ;
			var endZ;

			var geometry = new THREE.BoxGeometry(1.5, 0.05, length);
			var color = new THREE.Color();
			color.setRGB(confusion, 1 - confusion, 0);

			var material = new THREE.MeshBasicMaterial({
				color: 0x1a1a2e,
				transparent: true,
				opacity: 0.4,
			});
			var road = new THREE.Mesh(geometry, material);

			if (strength < 0.4) {
				road.material.color.set(0x661111);
				road.material.opacity = 0.5;
			}
			if (strength > 0.8) {
				road.material.color.set(0x116611);
				road.material.opacity = 0.5;
			}

			var vehicleGeometry = new THREE.BoxGeometry(0.5, 0.5, 0.5);
			var vehicleMaterial = new THREE.MeshBasicMaterial({
				color: 0x0044ff,
			});
			var vehicle = new THREE.Mesh(vehicleGeometry, vehicleMaterial);

			road.position.x = (index - offset) * 3;
			road.position.y = 0;
			road.position.z = -length / 2;

			startZ = road.position.z + length / 2 - prev * length;
			endZ = road.position.z + length / 2 - strength * length;

			vehicle.position.x = road.position.x;
			vehicle.position.y = 0.4;
			vehicle.position.z = startZ;

			console.log(subject.name, "Strength:", strength, "Confusion:", confusion);

			scene.add(road);
			scene.add(vehicle);

			var label = createTextSprite(subject.name);
			label.position.x = road.position.x;
			label.position.set(
				label.position.x,
				0.8,
				road.position.z
			);
			scene.add(label);

			subjectObjects.push({
				road: road,
				vehicle: vehicle,
				targetZ: endZ,
				data: subject,
			});
		});

		console.log("Subjects created:", subjectObjects.length);
	}

	function createTopicBlocks(topicData, scene) {
		var allTopics = Array.isArray(topicData) ? topicData : [];

		// Step 1 — Group by subject (backend provides subject explicitly)
		var topicsBySubject = {};
		allTopics.forEach(function (topic) {
			var subject = topic.subject || "General";

			if (!topicsBySubject[subject]) {
				topicsBySubject[subject] = [];
			}
			topicsBySubject[subject].push(topic);
		});

		// Step 2 — Sort by strength (weak near start, strong near destination)
		Object.keys(topicsBySubject).forEach(function (subject) {
			topicsBySubject[subject].sort(function (a, b) {
				return (a.strength || 0) - (b.strength || 0);
			});
		});

		// Step 3 — Map subject to lane X position
		var subjectLaneMap = {
			"Math": -5,
			"Reasoning": 0,
			"English": 5,
			"General": 0,
		};

		var bestStrength = -1;

		// Step 4 — Place topics along path
		Object.keys(topicsBySubject).forEach(function (subject) {
			var laneX = subjectLaneMap[subject] || 0;
			var topics = topicsBySubject[subject];

			var laneLabel = createTextSprite(subject);
			laneLabel.position.set(laneX, 2.5, 0);
			scene.add(laneLabel);
			topicLabels.push(laneLabel);

			topics.forEach(function (topic, index) {
				var strength = topic.strength || 0;

				var color;
				if (strength < 0.4) {
					color = 0xff4d4d;
				} else if (strength < 0.7) {
					color = 0xffd633;
				} else {
					color = 0x00ff99;
				}

				var geometry = new THREE.BoxGeometry(1, 1, 1);
				var material = new THREE.MeshStandardMaterial({
					color: color,
					emissive: color,
					emissiveIntensity: strength < 0.4 ? 0.8 : 0.3,
				});

				var cube = new THREE.Mesh(geometry, material);

				// Z = progression path (weak near start, strong further)
				var zPos = -2 - index * 3;
				cube.position.set(laneX, 1, zPos);

				scene.add(cube);

				var chapterLabel = createTextSprite(topic.chapter || "");
				chapterLabel.position.set(laneX, 2.2, zPos);
				scene.add(chapterLabel);
				topicLabels.push(chapterLabel);

				var speed = strength < 0.4 ? 0.02 : strength < 0.7 ? 0.04 : 0.08;

				var blockObj = {
					mesh: cube,
					speed: speed,
					targetZ: zPos - 1,
					data: topic,
				};

				topicBlocks.push(blockObj);

				if (strength > bestStrength) {
					bestStrength = strength;
					bestTopicObj = blockObj;
				}
			});
		});

		console.log("Topic blocks created:", topicBlocks.length);
	}

    console.log("Three.js initialized");
	function createExplosion() {
		for (let i = 0; i < 50; i++) {
			const geometry = new THREE.SphereGeometry(0.1, 8, 8);
			const material = new THREE.MeshBasicMaterial({
				color: 0xffff00,
			});
			const particle = new THREE.Mesh(geometry, material);
			particle.position.copy(destination.position);
			particle.userData.velocity = {
				x: (Math.random() - 0.5) * 0.2,
				y: Math.random() * 0.2,
				z: (Math.random() - 0.5) * 0.2,
			};
			scene.add(particle);
			particles.push(particle);
		}
	}

	function animate() {
		requestAnimationFrame(animate);
		controls.update();
		destination.rotation.y += 0.01;
		const pulse = 1 + Math.sin(Date.now() * 0.003) * 0.15;
		destination.material.emissiveIntensity = pulse;
		destination.scale.set(pulse, pulse, pulse);
		studentVehicle.position.z += (targetZ - studentVehicle.position.z) * 0.08;
		camera.position.z += (studentVehicle.position.z + 18 - camera.position.z) * 0.05;

		if (weakestObj) {
			camera.position.x += (weakestObj.road.position.x - camera.position.x) * 0.02;
		}

		if (Math.abs(targetZ - studentVehicle.position.z) > 0.1) {
			studentVehicle.material.color.set(0x00ffcc);
		} else {
			studentVehicle.material.color.set(0x00ffff);
		}

		subjectObjects.forEach(function (obj) {
			obj.vehicle.position.y = 0.4 + Math.sin(Date.now() * 0.002) * 0.05;
            obj.vehicle.position.z +=(obj.targetZ - obj.vehicle.position.z) * 0.05;
		});

		topicBlocks.forEach(function (tb) {
			tb.mesh.position.z += (tb.targetZ - tb.mesh.position.z) * tb.speed;
			tb.mesh.position.y = 0.2 + Math.sin(Date.now() * 0.002) * 0.02;
		});

		if (bestTopicObj) {
			var glow = 1 + Math.sin(Date.now() * 0.004) * 0.15;
			bestTopicObj.mesh.scale.set(glow, glow, glow);
		}

		ghostVehicles.forEach(function (ghost) {
			ghost.position.y = 0.5 + Math.sin(Date.now() * 0.002) * 0.03;
		});

		if (success) {
			destination.material.color.set(0x00ff00);
			if (!explosionTriggered) {
				createExplosion();
				explosionTriggered = true;
			}
		}

		particles.forEach(function (p) {
			p.position.x += p.userData.velocity.x;
			p.position.y += p.userData.velocity.y;
			p.position.z += p.userData.velocity.z;
			p.userData.velocity.y -= 0.005;
		});

		if (cityEnv) {
			cityEnv.updateLights();
		}
        
		composer.render();
	}

	animate();

	window.addEventListener("resize", function () {
		camera.aspect = window.innerWidth / window.innerHeight;
		camera.updateProjectionMatrix();
		renderer.setSize(window.innerWidth, window.innerHeight);
		composer.setSize(window.innerWidth, window.innerHeight);
	});

	var worldState = await loadWorldState();
	if (!worldState) {
		return;
	}

	if (!Array.isArray(worldState.subjects) || worldState.subjects.length === 0) {
		console.warn("No subjects returned from API");
		return;
	}

	let maxLength = 0;

	worldState.subjects.forEach(function (subject) {
		const strength = subject.strength_score || 0;
		const length = 10 - strength * 7;

		if (length > maxLength) {
			maxLength = length;
		}
	});

	destination.position.set(0, 1.5, -maxLength - 2);
	destLabel.position.set(0, 3.5, -maxLength - 2);

	createSubjects(worldState);

	// Create cinematic city environment
	cityEnv = createCity(scene, subjectObjects, destination);

	// Apply environment-specific camera config
	if (cityEnv.cameraConfig) {
		controls.maxPolarAngle = cityEnv.cameraConfig.maxPolarAngle;
		controls.minDistance = cityEnv.cameraConfig.minDistance;
		controls.maxDistance = cityEnv.cameraConfig.maxDistance;
	}

	let minScore = 1;
	subjectObjects.forEach(function (obj) {
		if (obj.data.strength_score < minScore) {
			minScore = obj.data.strength_score;
			weakestObj = obj;
		}
	});

	setInterval(loadWorldState, 10000);

	var topicData = await loadTopicInsights();
	if (topicData) {
		var allTopics = [].concat(topicData.weak_topics || [], topicData.strong_topics || []);
		createTopicBlocks(allTopics, scene);
	}

	const raceData = await loadRaceData();
	if (raceData) {
		success =
			(raceData.student_rank && raceData.student_rank <= 10) ||
			(worldState.mastery_streak >= 3);

		const rank = raceData.student_rank || 50;
		const total = raceData.total_participants || 100;
		const progress = 1 - rank / total;
		studentVehicle.position.z = -progress * 12;
		studentVehicle.position.y = 0.5;

		currentZ = studentVehicle.position.z;
		targetZ = currentZ;

		setTimeout(function () {
			targetZ = currentZ - 2;
			console.log("Rank improved → moving forward");
		}, 2000);

		const leaderboard = raceData.top_three || raceData.leaderboard_top || [];

		leaderboard.forEach(function (entry, i) {
			const ghost = new THREE.Mesh(
				new THREE.BoxGeometry(0.5, 0.5, 0.5),
				new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.3 })
			);

			const ghostProgress = 1 - entry.rank / raceData.total_participants;

			ghost.position.z = -ghostProgress * 12;
			ghost.position.x = (i - 2) * 0.8;
			ghost.position.y = 0.5;

			scene.add(ghost);

			ghostVehicles.push(ghost);
		});
	}
});
