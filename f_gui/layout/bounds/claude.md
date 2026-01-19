# Bounds Module

> **Quick Recap**: GUI layout utility that converts relative (percentage-based) positions to absolute (pixel-based) positions within a parent container.

---

## 📊 Visual Concept

```
┌─────────────────────────────────────────────┐
│ Parent Container (100x100 pixels)          │
│ Absolute: (0, 0, 100, 100)                 │
│                                             │
│   ┌─────────────────────┐                  │
│   │ Child Component     │                  │
│   │ Relative: (25%, 25%, 50%, 50%)        │
│   │ ↓ Bounds converts ↓                   │
│   │ Absolute: (25, 25, 50, 50)            │
│   └─────────────────────┘                  │
│                                             │
└─────────────────────────────────────────────┘

Parent resizes to 200x200:
┌─────────────────────────────────────────────────────────────────┐
│ Parent Container (200x200 pixels)                               │
│ Absolute: (0, 0, 200, 200)                                      │
│                                                                  │
│   ┌─────────────────────────────────────────────┐              │
│   │ Child Component                              │              │
│   │ Relative: (25%, 25%, 50%, 50%) UNCHANGED    │              │
│   │ ↓ Bounds auto-updates ↓                     │              │
│   │ Absolute: (50, 50, 100, 100) AUTO-UPDATED   │              │
│   └─────────────────────────────────────────────┘              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Purpose

The `Bounds` class solves the **responsive layout problem** by:

1. **Storing relative positions as percentages** (0-100)
2. **Auto-calculating absolute pixel positions** based on parent dimensions
3. **Auto-updating when parent changes** (reactive behavior)
4. **Decoupling component logic from container sizes**

### Key Formula

```python
absolute_top    = parent.top + (parent.height × relative.top / 100)
absolute_left   = parent.left + (parent.width × relative.left / 100)
absolute_width  = parent.width × relative.width / 100
absolute_height = parent.height × relative.height / 100
```

---

## 🔧 Core Components

### 1. **Bounds Class** (`main.py`)

```
Properties:
  .relative  → Rect (percentage-based: 0-100)
  .parent    → Rect (absolute pixel values)
  .absolute  → Rect (computed pixel values, read-only)

Methods:
  update_absolute()  → Recalculates absolute from relative × parent
```

### 2. **Factory Pattern** (`_factory.py`)

Pre-configured common layouts:

```python
Factory.full()     → (0, 0, 100, 100)   # Fills entire parent
Factory.half()     → (25, 25, 50, 50)   # Centered, half-size
Factory.quarter()  → (37.5, 37.5, 25, 25) # Centered, quarter-size
```

---

## 💼 Use Cases

### Use Case 1: Responsive UI Components

**Problem**: Button should always be centered and occupy 30% of window width

```python
# Window is 800x600
window = Rect(0, 0, 800, 600)
button_bounds = Bounds(
    relative=(35, 35, 30, 10),  # 30% wide, 10% tall, centered-ish
    parent=window
)

print(button_bounds.absolute)  # (210, 280, 240, 60)

# Window resizes to 1920x1080
button_bounds.parent = Rect(0, 0, 1920, 1080)
print(button_bounds.absolute)  # (378, 672, 576, 108) - auto-updated!
```

### Use Case 2: Nested Layouts

**Problem**: Panel inside a sidebar, sidebar inside main window

```python
# Main window
main_window = Rect(0, 0, 1200, 800)

# Sidebar (left 20% of window)
sidebar_bounds = Bounds(
    relative=(0, 0, 20, 100),
    parent=main_window
)

# Panel (top 50% of sidebar)
panel_bounds = Bounds(
    relative=(0, 0, 100, 50),
    parent=sidebar_bounds.absolute  # Nested!
)

print(sidebar_bounds.absolute)  # (0, 0, 240, 800)
print(panel_bounds.absolute)    # (0, 0, 240, 400)
```

### Use Case 3: Grid Layouts

**Problem**: Create 2×2 grid of equal cells

```python
parent = Rect(0, 0, 400, 400)

# Top-left cell
cell_tl = Bounds(relative=(0, 0, 50, 50), parent=parent)

# Top-right cell
cell_tr = Bounds(relative=(0, 50, 50, 50), parent=parent)

# Bottom-left cell
cell_bl = Bounds(relative=(50, 0, 50, 50), parent=parent)

# Bottom-right cell
cell_br = Bounds(relative=(50, 50, 50, 50), parent=parent)

print(cell_tl.absolute)  # (0, 0, 200, 200)
print(cell_tr.absolute)  # (0, 200, 200, 200)
print(cell_bl.absolute)  # (200, 0, 200, 200)
print(cell_br.absolute)  # (200, 200, 200, 200)
```

### Use Case 4: Dynamic Padding

**Problem**: Component should have 10% padding on all sides

```python
container = Rect(0, 0, 500, 300)

# Content area (90% of container, centered with 5% margins)
content = Bounds(
    relative=(5, 5, 90, 90),
    parent=container
)

print(content.absolute)  # (15, 25, 450, 270)
# Actual padding: 15px top, 25px left, 15px bottom, 25px right
```

---

## 📝 Code Examples

### Example 1: Basic Usage

```python
from f_gui.layout.bounds import Bounds
from f_math.shapes.rect import Rect

# Create a bounds with default full layout
bounds = Bounds()
print(bounds)  # (0, 0, 100, 100) X (0, 0, 100, 100) -> (0, 0, 100, 100)

# Create custom relative bounds
custom = Bounds(
    relative=(10, 20, 50, 30),  # top, left, width, height (%)
    parent=(0, 0, 800, 600)     # Tuple gets auto-converted to Rect
)
print(custom.absolute)  # (60, 160, 400, 180)
```

### Example 2: Using Factory

```python
from f_gui.layout.bounds import Bounds

# Create centered half-size layout
half = Bounds.Factory.half()
print(half.absolute)  # (25, 25, 50, 50)

# Create centered quarter-size layout
quarter = Bounds.Factory.quarter()
print(quarter.absolute)  # (37.5, 37.5, 25, 25)
```

### Example 3: Reactive Updates

```python
from f_gui.layout.bounds import Bounds
from f_math.shapes.rect import Rect

# Component at 50% width/height, centered
component = Bounds(
    relative=(25, 25, 50, 50),
    parent=Rect(0, 0, 400, 300)
)

print(component.absolute)  # (75, 100, 200, 150)

# Parent resizes
component.parent = Rect(0, 0, 800, 600)
print(component.absolute)  # (150, 200, 400, 300) - auto-calculated!
```

### Example 4: Offsetted Parents

```python
from f_gui.layout.bounds import Bounds
from f_math.shapes.rect import Rect

# Parent is NOT at (0,0) - it's offset in the screen
parent = Rect(top=100, left=50, width=600, height=400)

# Child takes upper-left quarter
child = Bounds(
    relative=(0, 0, 50, 50),
    parent=parent
)

print(child.absolute)  # (100, 50, 300, 200)
# Notice: top/left inherited parent's offset (100, 50)
```

### Example 5: String Representation

```python
from f_gui.layout.bounds import Bounds

bounds = Bounds(
    relative=(20, 30, 40, 50),
    parent=(0, 0, 800, 800)
)

print(str(bounds))
# Output: (20, 30, 40, 50) X (0, 0, 800, 800) -> (160, 240, 320, 400)
#         └─ relative ─┘   └─── parent ───┘    └───── absolute ─────┘
```

---

## 🏗️ Architecture

### Data Flow

```
User Sets             Bounds Manages           Auto-Computes
─────────────         ──────────────           ─────────────

relative (%)    →     _relative                     ↓
parent (px)     →     _parent          →       _absolute (px)
                           ↓
                   update_absolute()
```

### Dependencies

```
Bounds
  ├── Rect (from f_math.shapes.rect)
  ├── Printable (from f_core.mixins.printable)
  └── Comparable (from f_core.mixins.comparable)
```

### Comparison Behavior

Objects are compared by their **absolute bounds**:

```python
b1 = Bounds(relative=(0, 0, 50, 50), parent=(0, 0, 100, 100))
b2 = Bounds(relative=(0, 0, 100, 100), parent=(0, 0, 50, 50))

# Both have absolute (0, 0, 50, 50)
assert b1 == b2  # True - compared by absolute, not relative!
```

---

## ⚙️ API Reference

### Constructor

```python
Bounds(
    relative: RectLike = Rect.Factory.full(),  # (top%, left%, width%, height%)
    parent: RectLike = Rect.Factory.full()     # (top_px, left_px, width_px, height_px)
)
```

**RectLike** = `Rect` object or `tuple[float, float, float, float]`

### Properties

| Property   | Type | Access | Description                              |
|-----------|------|--------|------------------------------------------|
| `relative` | Rect | R/W    | Percentage-based bounds (0-100)         |
| `parent`   | Rect | R/W    | Parent's absolute bounds (triggers update) |
| `absolute` | Rect | R/O    | Computed absolute bounds                |

### Methods

| Method              | Returns | Description                          |
|--------------------|---------|--------------------------------------|
| `update_absolute()` | None    | Recalculates absolute from relative × parent |
| `key_comparison()`  | tuple   | Returns absolute bounds as tuple (for Comparable) |

### Factory Methods

| Method      | Returns | Description                          |
|------------|---------|--------------------------------------|
| `full()`    | Bounds  | Full parent coverage (0, 0, 100, 100) |
| `half()`    | Bounds  | Centered half-size (25, 25, 50, 50)  |
| `quarter()` | Bounds  | Centered quarter-size (37.5, 37.5, 25, 25) |

---

## 🧪 Testing

Located in `_tester.py`:

```python
from f_gui.layout.bounds import Bounds

def test_full():
    bounds = Bounds()
    assert bounds.absolute == (0, 0, 100, 100)

def test_half():
    bounds = Bounds.Factory.half()
    assert bounds.absolute == Rect.Factory.half()

def test_quarter():
    bounds = Bounds.Factory.quarter()
    assert bounds.absolute == Rect.Factory.quarter()
```

---

## 📐 Rect Format

All Rect objects use the format:

```
(top, left, width, height)
 └─┬─┘ └──┬──┘ └───┬────┘
   │      │        └─ Size dimensions
   └──────┴────────── Position coordinates
```

**NOT** (x, y, width, height) - it's **(top, left, width, height)**!

---

## 🚀 Quick Start

```python
# 1. Import
from f_gui.layout.bounds import Bounds

# 2. Create bounds for a button (centered, 40% wide, 10% tall)
button = Bounds(
    relative=(45, 30, 40, 10),
    parent=(0, 0, 1024, 768)
)

# 3. Get absolute position for rendering
x, y, w, h = button.absolute.to_tuple()
draw_button(x, y, w, h)

# 4. Handle window resize
def on_resize(new_width, new_height):
    button.parent = Rect(0, 0, new_width, new_height)
    # button.absolute is now automatically updated!
```

---

## 🎨 Common Patterns

### Centered Element

```python
# 60% width, 40% height, centered
centered = Bounds(relative=(30, 20, 60, 40), parent=window)
```

### Full-Screen Overlay

```python
overlay = Bounds.Factory.full()  # Covers entire parent
```

### Split Screen (Vertical)

```python
left_pane = Bounds(relative=(0, 0, 50, 100), parent=window)
right_pane = Bounds(relative=(0, 50, 50, 100), parent=window)
```

### Toolbar (Top 10%)

```python
toolbar = Bounds(relative=(0, 0, 100, 10), parent=window)
content = Bounds(relative=(10, 0, 100, 90), parent=window)
```

---

## ⚠️ Important Notes

1. **Relative values are percentages (0-100)**, not decimals (0-1)
2. **Setting `.parent` triggers automatic `update_absolute()`**
3. **`.absolute` is read-only** - modify via `.relative` or `.parent`
4. **Tuples are auto-converted to Rect objects**
5. **Comparison uses absolute bounds**, not relative

---

## 📚 Related Modules

- `f_math.shapes.rect` - Rectangle primitive used by Bounds
- `f_gui.layout` - Parent module with master test runner
- `f_core.mixins.printable` - Provides `__str__()` functionality
- `f_core.mixins.comparable` - Provides comparison operators

---

**Last Updated**: 2026-01-18
**Module Path**: `f_gui.layout.bounds`
**Main Class**: `Bounds`
