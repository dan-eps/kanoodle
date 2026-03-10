# Kanoodle Solver

A solver for the board game [Kanoodle](https://www.educationalinsights.com/kanoodle), where 12 colored puzzle pieces must be placed to fill a 5×11 grid. Given a partially-filled board, this program finds all valid solutions using **Knuth's Algorithm X** with **Dancing Links** via an exact cover formulation.

---

## How It Works

Kanoodle is modeled as an **exact cover problem**. Each possible placement of each piece is encoded as a binary row with 67 columns — 55 columns for the board spaces (5×11) and 12 columns for the piece types. A valid solution is a set of rows where every column is covered exactly once, meaning every space is filled and every piece is used exactly once.

The solver uses the [`exact-cover`](https://pypi.org/project/exact-cover/) Python library, which implements Algorithm X with Dancing Links for efficient backtracking search.

### File Overview

| File | Description |
|---|---|
| `main.py` | Entry point. Initializes pieces, runs the menu, and invokes the solver. |
| `board.py` | Represents the 5×11 game board. Handles piece placement, removal, and isolation checks. |
| `piece.py` | Represents a single Kanoodle piece with support for rotation and flipping. |
| `menu.py` | Interactive terminal UI for setting up the starting board position using keyboard input. |
| `exact_cover_converter.py` | Converts piece placements into exact cover rows and decodes solutions back into boards. |

---

## Pieces

The game includes 12 uniquely shaped pieces, each identified by a color and display character:

| Character | Color | Size |
|---|---|---|
| `P` | Purple | 4 cells |
| `R` | Red | 5 cells |
| `p` | Light Pink | 5 cells |
| `W` | White | 3 cells |
| `g` | Light Green | 4 cells |
| `b` | Light Blue | 5 cells |
| `B` | Blue | 5 cells |
| `+` | Silver | 5 cells |
| `Y` | Yellow | 5 cells |
| `G` | Green | 5 cells |
| `M` | Magenta/Pink | 5 cells |
| `O` | Orange | 4 cells |

---

## Installation

**Requirements:** Python 3.10+

```bash
pip install numpy exact-cover keyboard
```

> **Note:** The `keyboard` library may require root/admin privileges on Linux/macOS.

---

## Usage

```bash
python main.py
```

### Setting Up the Board

When the program starts, an interactive menu lets you place any pieces that are already on your physical board:

| Key | Action |
|---|---|
| `P` | Select a new piece to place |
| `R` | Rotate the current piece 90° |
| `F` | Flip the current piece |
| `D` | Delete (undo) the last placed piece |
| `↑ ↓ ← →` | Move the current piece |
| `Q` | Solve with the current board state |

After pressing `Q`, the solver will print all valid solutions to the terminal, with each piece rendered in its corresponding color.

### Performance Note

On first run, the solver generates `all_placements.csv`, a precomputed file of all valid piece placements. This takes a moment but is cached for all future runs.

---

## Algorithm Details

The isolation check in `board.py` uses a flood-fill algorithm to ensure no group of open spaces is created that is too small to fit any remaining piece (fewer than 4 connected cells). This prunes invalid branches early and significantly reduces search time.

The exact cover matrix has one row per valid placement and 67 columns:
- Columns 0–54: the 55 board spaces (row-major order)
- Columns 55–66: the 12 piece types (one must be covered per piece)
