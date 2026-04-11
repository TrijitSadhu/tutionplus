let subjectObjects = [];
let studentVehicle;
let targetZ = 0;
let currentZ = 0;
let ghostVehicles = [];
let success = false;

async function loadWorldState() {
	try {
		var response = await fetch("/api/world-state/");

		if (!response.ok) {
			throw new Error("Failed to fetch world state");
		}

		var data = await response.json();

		console.log("World State:", data);

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

	console.log("World JS Loaded");

	if (!canvas) {
		console.error("Canvas not found");
		return;
	}

	console.log("Canvas found:", canvas);

	var scene = new THREE.Scene();
	scene.background = new THREE.Color(0x000011);
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

	camera.position.set(0, 4, 8);
	camera.lookAt(0, 1.5, 0);

	var light = new THREE.AmbientLight(0xffffff, 1);
	scene.add(light);

	const raceGeometry = new THREE.BoxGeometry(2, 0.1, 12);
	const raceMaterial = new THREE.MeshBasicMaterial({
		color: 0x222222,
	});
	const raceTrack = new THREE.Mesh(raceGeometry, raceMaterial);
	raceTrack.position.set(0, -1, -7);
	scene.add(raceTrack);

	studentVehicle = new THREE.Mesh(
		new THREE.BoxGeometry(0.6, 0.6, 0.6),
		new THREE.MeshBasicMaterial({ color: 0x00ffff })
	);
	scene.add(studentVehicle);

	var geometry = new THREE.SphereGeometry(1, 32, 32);
	var material = new THREE.MeshBasicMaterial({
		color: 0xffff00,
	});
	var destination = new THREE.Mesh(geometry, material);
	destination.position.set(0, 1, -12);
	scene.add(destination);

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

			var geometry = new THREE.BoxGeometry(1.5, 0.2, length);
			var color = new THREE.Color();
			color.setRGB(confusion, 1 - confusion, 0);

			var material = new THREE.MeshBasicMaterial({
				color: color,
			});
			var road = new THREE.Mesh(geometry, material);
			var vehicleGeometry = new THREE.BoxGeometry(0.5, 0.5, 0.5);
			var vehicleMaterial = new THREE.MeshBasicMaterial({
				color: 0x0000ff,
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
			});
		});

		console.log("Subjects created:", subjectObjects.length);
	}

    console.log("Three.js initialized");
	function animate() {
		requestAnimationFrame(animate);
		destination.rotation.y += 0.01;
		const scale = 1 + Math.sin(Date.now() * 0.003) * 0.1;
		destination.scale.set(scale, scale, scale);
		studentVehicle.position.z += (targetZ - studentVehicle.position.z) * 0.08;
		camera.position.z += (studentVehicle.position.z + 8 - camera.position.z) * 0.05;

		if (Math.abs(targetZ - studentVehicle.position.z) > 0.1) {
			studentVehicle.material.color.set(0x00ffcc);
		} else {
			studentVehicle.material.color.set(0x00ffff);
		}

		subjectObjects.forEach(function (obj) {
			obj.vehicle.position.y = 0.4 + Math.sin(Date.now() * 0.002) * 0.05;
            obj.vehicle.position.z +=(obj.targetZ - obj.vehicle.position.z) * 0.05;
		});
		ghostVehicles.forEach(function (ghost) {
			ghost.position.y = 0.5 + Math.sin(Date.now() * 0.002) * 0.03;
		});

		if (success) {
			destination.material.color.set(0x00ff00);
		}
        
		renderer.render(scene, camera);
	}

	animate();

	window.addEventListener("resize", function () {
		camera.aspect = window.innerWidth / window.innerHeight;
		camera.updateProjectionMatrix();
		renderer.setSize(window.innerWidth, window.innerHeight);
	});

	var worldState = await loadWorldState();
	if (!worldState) {
		return;
	}

	if (!Array.isArray(worldState.subjects) || worldState.subjects.length === 0) {
		console.warn("No subjects found. Using dummy data.");

		worldState.subjects = [
			{
				name: "Math",
				strength_score: 0.5,
				previous_strength_score: 0.4,
				average_confusion_index: 0.2,
			},
			{
				name: "Reasoning",
				strength_score: 0.7,
				previous_strength_score: 0.6,
				average_confusion_index: 0.3,
			},
			{
				name: "English",
				strength_score: 0.3,
				previous_strength_score: 0.35,
				average_confusion_index: 0.5,
			},
		];
	}

	let maxLength = 0;

	worldState.subjects.forEach(function (subject) {
		const strength = subject.strength_score || 0;
		const length = 10 - strength * 7;

		if (length > maxLength) {
			maxLength = length;
		}
	});

	destination.position.set(0, 1, -maxLength - 2);
	destination.position.y = 1.5;

	createSubjects(worldState);

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
				new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.4 })
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
