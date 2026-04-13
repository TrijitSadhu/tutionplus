# Performance World — Visual Element Map

## Data Sources (3 API Calls)

| API Endpoint | Backend Source | Fallback |
|---|---|---|
| `GET /api/world-state/` | `SubjectPerformance` records | Dummy: Math (0.5), Reasoning (0.7), English (0.3) |
| `GET /api/topic-insights/` | `TopicPerformance` records | Demo: Time & Work, Probability, Grammar |
| `GET /api/cinematic-race/1/` | `MockTestAttempt` rankings | None (skipped if fails) |

---

## Roads (`createSubjects`)

- Each road = **one subject** (Math, Reasoning, English)
- **Length** = `10 - strength_score * 7` — weaker subjects get longer roads
- **Color**:
  - Dark red (`0x661111`) → strength < 0.4
  - Dark green (`0x116611`) → strength > 0.8
  - Default dark (`0x1a1a2e`) → otherwise
- **X position** = spaced evenly across lanes
- **Blue vehicle on road** = student's progress in that subject, Z position based on `strength_score`

---

## Topic Blocks (`createTopicBlocks`)

- Each block = **one chapter/topic** (e.g. "Time & Work", "Probability", "Grammar")
- **Color**:
  - Red (`0xff4d4d`) → strength < 0.4
  - Yellow (`0xffd633`) → strength < 0.7
  - Green (`0x00ff99`) → strength ≥ 0.7
- **X position** = mapped to subject lane (Math=-5, Reasoning=0, English=5)
- **Z position** = sorted by strength — weakest near start, strongest toward destination
- **Emissive glow** = stronger on weak topics (0.8) vs strong (0.3)
- **Animation speed** = weak (0.02), medium (0.04), strong (0.08)

---

## Other Elements

| Element | Visual | Represents |
|---|---|---|
| **Cyan cube** (studentVehicle) | Small cyan box | Overall student position based on mock test rank |
| **Yellow sphere** (destination) | Pulsing glowing sphere | Goal — positioned at end of longest road |
| **White cubes** (ghosts) | Semi-transparent boxes | Top 3 students from leaderboard |
| **Race track** | Thin dark strip | Central lane for rank-based movement |
| **City monument** | Tower + billboard | Destination landmark (from city.js) |
| **City ground** | Procedural grid texture | Aerial city environment |
| **City lights** | Flickering colored dots | Ambient city life |
| **Glow strips** | Colored transparent planes | Subject lane highlights (blue/green/red) |

---

## Current State

All data is **dummy/demo** — `subjects: Array(0)` falls back to hardcoded values, topic insights returns demo chapters.
Here's what each visual element represents based on the data flow:

Data Sources (3 API calls):

GET /api/world-state/ → SubjectPerformance records (or dummy data if empty)
GET /api/topic-insights/ → TopicPerformance records (or demo data if empty)
GET /api/cinematic-race/1/ → MockTestAttempt rankings
Roads (created in createSubjects):

Each road = one subject (Math, Reasoning, English)
Road length = 10 - strength_score * 7 — weaker subjects get longer roads (more ground to cover)
Road color: dark red (0x661111) if strength < 0.4, dark green (0x116611) if strength > 0.8, default dark (0x1a1a2e) otherwise
Road X position = spaced evenly across lanes
Blue vehicle on road = the student's progress in that subject, positioned along Z based on strength_score
Topic Blocks (created in createTopicBlocks):

Each block = one chapter/topic (e.g. "Time & Work", "Probability", "Grammar")
Block color: red (0xff4d4d) if strength < 0.4, yellow (0xffd633) if < 0.7, green (0x00ff99) if ≥ 0.7
Block X position = mapped to subject lane (Math=-5, Reasoning=0, English=5)
Block Z position = sorted by strength — weakest chapters near start, strongest further toward destination
Block emissive glow = stronger on weak topics (0.8 intensity vs 0.3)
Block animation speed = faster for stronger topics (0.08), slower for weak (0.02)
Other elements:

Cyan cube (studentVehicle) = overall student position based on mock test rank
Yellow sphere (destination) = the goal, positioned at the end of the longest road
White transparent cubes (ghosts) = top 3 students from leaderboard
Race track = the central lane for rank-based movement
City monument (tower + billboard) = destination landmark from city.js, at same position as the yellow sphere
Currently all data is dummy/demo — subjects: Array(0) falls back to hardcoded Math/Reasoning/English with fixed scores, and topic insights returns demo Time & Work, Probability, Grammar.