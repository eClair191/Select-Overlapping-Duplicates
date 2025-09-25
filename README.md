# Select Overlapping Duplicates

A Blender addon to compare two collections and automatically select overlapping duplicate objects based on vertex count and proximity.

> **⚠️ Note on "Duplicates":** The term "duplicates" is used loosely in this addon. Objects are matched based on identical vertex counts and proximity of bounding box centers, not exact geometry comparison. This method meets the creator's specific workflow needs but may not catch all types of duplicates or may flag objects that aren't true duplicates.

## Features

- **Compare Collections**: Analyze objects between two different collections
- **Smart Duplicate Detection**: Matches objects with identical vertex counts and nearby centers
- **Flexible Selection**: Choose which collection to select duplicates from
- **Adjustable Threshold**: Set custom distance threshold for proximity detection
- **Detailed Console Output**: See all matches with vertex counts and distances

## Installation

1. Download `select_overlapping_duplicates.py`
2. Open Blender
3. Go to `Edit` → `Preferences` → `Add-ons`
4. Click `Install...` button
5. Select the downloaded `.py` file
6. Enable the checkbox next to "Select Overlapping Duplicates"

## Usage

### Method 1: F3 Search Menu
1. Press `F3` to open the search menu
2. Type "Select Overlapping Duplicates"
3. Press Enter

### Method 2: Select Menu
1. In Object Mode, go to the top menu bar
2. Click `Select` → `Select Overlapping Duplicates`

### Dialog Options

- **First Collection**: Choose the first collection to compare
- **Second Collection**: Choose the second collection to compare
- **Select Duplicates From**: Choose which collection's duplicates to select
  - First Collection: Select matches from the first collection
  - Second Collection: Select matches from the second collection
- **Distance Threshold**: Maximum distance between object centers (default: 0.1)

## How It Works

The addon compares objects between two collections using:

1. **Vertex Count Matching**: Only compares objects with identical vertex counts
2. **Bounding Box Centers**: Calculates the center of each object's bounding box in world space
3. **Distance Check**: Measures distance between centers
4. **Threshold Filter**: Marks objects as duplicates if distance < threshold

Objects matching these criteria from the selected collection are automatically selected in the viewport.

## Use Cases

- Finding duplicate imported meshes across collections
- Cleaning up scenes with redundant geometry
- Identifying overlapping objects from different sources
- Quality control for asset libraries

## Requirements

- Blender 4.5.0 or higher
- Works only with mesh objects (cameras, lights, empties are skipped)

## Console Output

The addon provides detailed terminal output:
```
======================================================================
Comparing Collections for Duplicates
First: 'col_a' | Second: 'col_b'
Selecting from: 'col_b' | Threshold: 0.1000
======================================================================
Match: 'Cube.001' ↔ 'Cube.005' | Verts: 8 | Distance: 0.0523
Match: 'Sphere' ↔ 'Sphere.002' | Verts: 482 | Distance: 0.0891
======================================================================
Total duplicates found: 2
Selected: ['Cube.005', 'Sphere.002']
======================================================================
```

**Development Note:** This addon was developed with the assistance of AI.
