# Stellar — Data-Driven Academic Universe

## Overview

Stellar is a Three.js 3D visualization at `/api/stellar/` that turns a student's real academic performance data into a living, interactive solar system. Every object in the scene is generated from actual API data — nothing is decorative or hardcoded (except a starfield background). If your Math strength score is 70%, your Math planet is literally sized at 70% of maximum.

---

## URL

```
http://127.0.0.1:8000/api/stellar/
```

---

## Files

| File | Purpose |
|---|---|
| `students/urls.py` | Registers the `stellar/` path |
| `students/views.py` | `stellar(request)` — `@login_required`, renders the template |
| `students/templates/students/world/stellar.html` | Complete self-contained Three.js page |

---

## APIs Used

Stellar fetches two endpoints in parallel on page load:

### 1. `/api/world-state/`
Provides subject-level performance data for the active exam.

**Fields used:**
| Field | Used for |
|---|---|
| `exam` | HUD exam label |
| `level` | Sun color, size, and corona intensity |
| `mastery_streak` | Shooting star frequency |
| `recommendation` | Floating holographic label above the sun |
| `subjects[].name` | Planet label sprite |
| `subjects[].strength_score` | Planet size and brightness |
| `subjects[].previous_strength_score` | Second (ghost) orbit ring radius |
| `subjects[].average_confusion_index` | Particle cloud density and color |
| `subjects[].total_confused_questions` | Shown in the side info panel |

### 2. `/api/topic-insights/`
Provides chapter-level weak and strong topic data.

**Fields used:**
| Field | Used for |
|---|---|
| `weak_topics[]` | Red icosahedra (asteroid rocks) near the subject's planet |
| `strong_topics[]` | Teal moons orbiting the subject's planet |
| `weak_topics[].subject` | Matched to the planet by subject name |
| `strong_topics[].subject` | Matched to the planet by subject name |

**Fallback:** If either API returns no data, the scene renders with built-in demo data (Math 50%, Reasoning 70%, English 30%) so the page is never blank.

---

## Scene Anatomy

### The Sun (Center)
The sun represents your overall academic level. Its color, size, and bloom glow intensity change based on the `level` field from `world-state`.

| Level | Sun Color | Size | Glow |
|---|---|---|---|
| Beginner | Orange `#ff8c00` | Small | Soft |
| Intermediate | Yellow `#ffcc00` | Medium | Moderate |
| Advanced | Blue-white `#00bfff` | Large | Strong |
| Expert | Near-white `#e0f0ff` | XL | Intense |
| Master | Pink `#ff6ec7` | XXL | Maximum |

The sun also gently pulses (scale oscillates by ±2.5%) and slowly rotates on its Y axis every frame.

A `THREE.PointLight` is attached to the sun, casting colored light across all nearby planets.

### Planets (One per subject)
Each subject from `world-state` becomes a planet.

**Size formula:**
```
planetRadius = 0.38 + (strength_score × 1.05)
```
A subject with `strength_score = 1.0` (100%) has radius `1.43`.
A subject with `strength_score = 0.0` has radius `0.38`.

**Brightness:**
```
emissiveIntensity = 0.55 + (strength_score × 0.85)
```
Stronger subjects literally glow brighter.

**Orbit radius:** Fixed radii at `[7, 11.5, 16, 20.5, 25, 30]` units — first subject orbits closest to the sun.

**Orbit speed:** Closer planets orbit faster, matching planetary physics intuitively:
```
speeds = [0.28, 0.20, 0.15, 0.11, 0.08, 0.06]  rad/sec
```

**Colors:** 6 distinct colors cycling through subjects:
`#4fc3f7` (blue), `#ce93d8` (purple), `#4db6ac` (teal), `#ffcc80` (amber), `#ef9a9a` (red), `#90caf9` (light blue)

### Orbit Rings (Two per planet)
Each planet has two orbit rings drawn in its subject color:

1. **Full ring** — the current orbit path (always at full radius)
2. **Ghost ring** — sized proportionally to `previous_strength_score`, showing where the student was before. The gap between the two rings is a visual representation of growth or regression.

### Confusion Particle Cloud
If `average_confusion_index > 0.04`, a particle cloud is generated around the planet.

**Particle count:**
```
count = max(12, confusion_index × 200)
```
A subject at 50% confusion index spawns ~100 particles; at 100% ~200 particles.

**Cloud radius:** Spawns between `1.5×` and `2.6×` the planet's radius — tight enough to look atmospheric but distinct from the planet surface.

**Color:**
| Confusion Level | Color |
|---|---|
| ≤ 25% | Teal `#00d4aa` |
| 26–50% | Amber `#ffb344` |
| > 50% | Red `#ff4d6d` |

The cloud slowly rotates on its Y axis (0.014 rad/frame), giving a swirling atmospheric effect.

### Strong Topic Moons (Teal)
For each subject, up to **2 strong topics** (from `topic-insights`) become small teal moons that orbit the planet. They are `MeshStandardMaterial` spheres with teal emissive glow. Each moon orbits at a slightly different speed and distance, creating a layered satellite system.

### Weak Topic Asteroids (Red)
For each subject, up to **4 weak topics** become small red `IcosahedronGeometry` rocks placed around the planet at varied positions. They are static (do not orbit) but their jagged shape and red emissive color makes them visually distinct as "problem areas."

### Recommendation Sprite
If the API returns a non-default recommendation (anything other than "Continue current practice"), a holographic floating text label appears above the sun. It gently bobs up and down using a sine wave. Built with a `THREE.Sprite` from a `CanvasTexture` with a rounded-rectangle glass-morphism style background.

### Shooting Stars
Shooting stars streak across the scene. Their frequency is controlled by `mastery_streak`:

| Streak | Frequency |
|---|---|
| 0 | Every 3.5 seconds |
| 1–5 | Every 1.4 seconds |
| > 5 | Every 0.45 seconds (rapid burst effect) |

If streak > 3, there's a 50% chance a second star fires 120ms after the first, creating a "double streak" burst.

### Static Starfield
- **14,000 small white stars** scattered in a sphere of radius 120–400 units — the deep background
- **6,000 blue-tinted stars** arranged in a disk/band pattern (radius 90–220 units) to simulate a galactic plane

---

## UI Elements

### Top Navigation Bar
Frosted glass bar (backdrop-filter blur) with links back to Performance Dashboard, World, and Space. Sticky at the top.

### HUD Strip (Bottom)
A floating pill at the bottom of the screen showing:
- **Exam name** (from `world-state`)
- **Level** (colored purple)
- **Mastery Streak** with fire emoji
- **Recommendation tip** (smaller text)

Animates in from below on load with a spring-easing keyframe.

### Hover Label
When the mouse hovers over a planet, a small tooltip appears near the cursor showing the subject name, strength %, and confusion %. Built entirely in CSS/JS — no Three.js sprites involved.

### Click → Side Info Panel
Clicking any planet slides in a detail panel from the right edge with:
- Subject name (colored in the planet's color)
- Strength bar (current)
- Previous strength bar (comparison)
- Confusion index bar (colored by severity)
- Confused question count
- Legend explaining moons/asteroids

On mobile, the panel slides up from the bottom instead.

### Loading Screen
Full-screen black overlay with:
- Spinning star icon
- Animated gradient-filled "STELLAR" title
- Progress bar (CSS animation, 2 seconds)
- "MAPPING YOUR UNIVERSE" subtitle
Fades out with opacity transition once the scene is ready.

---

## Post-Processing

Uses the same CDN version (`three@0.146`) and the same post-processing pipeline as the existing `world/`, `space/`, and `experiment/` pages:

```
EffectComposer
  └── RenderPass
  └── UnrealBloomPass
        strength:   1.4
        radius:     0.55
        threshold:  0.22  ← only emissive objects bloom
```

All planet materials and the sun use `emissive` + `emissiveIntensity` specifically to trigger the bloom pass, giving them a realistic glow without affecting non-emissive geometry.

Renderer settings:
- `ACESFilmicToneMapping` — cinematic color response
- `toneMappingExposure: 1.1`
- `antialias: true`
- Pixel ratio capped at 2 for performance on high-DPI screens

---

## Camera & Controls

`OrbitControls` with:
- **Auto-rotate** at `0.4` RPM until the user first interacts (then stops)
- **Damping** (`dampingFactor: 0.04`) — smooth momentum on drag release
- **Min distance:** 5 units (can't go inside the sun)
- **Max distance:** 80 units (can't leave the solar system)
- Camera starts at `(0, 22, 40)` — slightly above and in front for a dramatic downward angle

---

## Animation Loop

Every frame (`requestAnimationFrame`):

1. Sun pulses (sine wave scale) and rotates
2. Each planet advances its orbit angle by `orbitSpeed × deltaTime`
3. Each planet's group position is recalculated: `(cos(angle) × orbitRadius, 0, sin(angle) × orbitRadius)`
4. Each planet rotates on its own Y axis
5. Confusion clouds rotate on Y axis
6. Moons orbit around their planet
7. Recommendation sprite floats (sine wave Y)
8. Shooting stars advance, fade, and are removed when opacity hits 0
9. Raycasting runs for hover detection
10. `controls.update()` applies damping
11. `composer.render()` — renders through the bloom post-process pipeline

Delta time is capped at 50ms to prevent physics jumps on tab-blur/resume.

---

## Mobile Support

- Canvas fills 100vw × 100vh at all times
- HUD wraps to 2-column grid on screens < 600px
- Side info panel becomes a bottom sheet (slides up) on mobile
- Touch tap triggers the click handler via `touchend` event
- OrbitControls natively supports pinch-zoom and touch-drag

---

## Fallback Data

If `world-state` or `topic-insights` APIs return errors or empty data, the scene renders with built-in demo values:

```json
[
  { "name": "Math",      "strength_score": 0.5,  "previous": 0.40, "confusion": 0.2 },
  { "name": "Reasoning", "strength_score": 0.7,  "previous": 0.60, "confusion": 0.3 },
  { "name": "English",   "strength_score": 0.3,  "previous": 0.35, "confusion": 0.5 }
]
```

This ensures the page always renders something meaningful and never shows a broken/empty Three.js canvas.

---

## Relationship to Other Pages

| Page | URL | Type | Data |
|---|---|---|---|
| `world/` | `/api/world/` | Three.js city scene | Static art, stats panel via `world-state` |
| `space/` | `/api/space/` | Three.js space scene | Static art |
| `experiment/` | `/api/experiment/` | Three.js lab scene | Static art |
| **`stellar/`** | `/api/stellar/` | Three.js solar system | **Geometry generated from API data** |
| `performance-dashboard/` | `/api/performance-dashboard/` | Chart.js HTML dashboard | All API data, 2D charts |

Stellar is the only page where the 3D geometry itself (planet size, cloud density, moon count) is a direct mathematical function of the student's performance numbers.
