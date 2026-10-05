# F1 Reflex Test

A desktop reaction-time trainer inspired by Formula 1's start-light sequence. Built with **Python**, **PyQt6**, and **SQLite**.

---

## Overview

The F1 Reflex Test measures how fast a player reacts to a visual stimulus. Five red lights turn on one at a time, then go out after a random delay. The player must press **SPACE** (or click **REACT**) as quickly as possible once the lights go out. The application records each reaction time in milliseconds, assigns a rating tier, and maintains a top-10 leaderboard.

---

## Features

- **User registration & login** — accounts stored in SQLite
- **F1-style lights sequence** — 5 lights, 800 ms apart
- **Randomized GO delay** — 1 to 3 seconds, so the timing can't be predicted
- **Jump-start detection** — pressing too early is flagged and saved separately
- **Reaction time measurement** — millisecond precision
- **Rating system** — from *F1 Racer* down to *Normal Driver, Slow*
- **Automatic leaderboard** — top 10 fastest valid reactions, rebuilt after every valid round
- **Persistent storage** — all data survives closing and reopening the app

---

## Rating Tiers

| Reaction Time | Rating |
|---|---|
| < 150 ms | F1 Racer |
| 150 – 199 ms | F2 Racer |
| 200 – 249 ms | F3 Racer |
| 250 – 349 ms | Karting Racer |
| ≥ 350 ms | Normal Driver, Slow |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| GUI | PyQt6 (Qt Designer `.ui` files) |
| Database | SQLite 3 (via Python's `sqlite3` module) |
| IDE | Visual Studio Code |

---

## Project Structure
