# State - Search State Representation

## Main Class
`State(HasKey[Key])`

## Inheritance
- **Base Classes:** `HasKey[Key]` (from f_core.mixins.has.key)
- **Generic Parameter:** `Key` - the type of identifier for this state (typically a cell/coordinate)

## Purpose
Represents a single configuration or node in the search space. In the context of grid-based pathfinding, a State typically wraps a cell/coordinate on the grid, representing a position that can be occupied and explored.

## Functionality from Base Classes
From `HasKey[Key]`:
- **`key` property:** Provides access to the underlying key/identifier
- **Key abstraction:** Separates the state concept from its concrete representation

## Specialized Functionality

### Core Functionality

#### Constructor (`__init__(key: Key)`)
- **Purpose:** Creates a state wrapping a specific key
- **Parameters:**
  - `key`: The identifier for this state (e.g., cell coordinates)
- **Storage:** Stores the key internally for later access

### State Identity
- States are identified and compared by their keys
- Two states with the same key represent the same configuration
- Used in sets and dictionaries for efficient lookup

## Design Philosophy

### Wrapper Pattern
State acts as a **wrapper** around the key:
- Provides semantic meaning (this is a "state" not just a "key")
- Allows for future extension of state properties
- Maintains clean separation between state abstraction and concrete representation

### Type Safety
By using generic type parameter `Key`:
- Ensures type consistency throughout the codebase
- Allows different key types (coordinates, indices, etc.)
- Provides compile-time type checking

## Usage Context

### In Search Algorithms
States are used throughout the search process:
- **Start/Goal:** Initial and target states
- **Generated:** States in the open queue awaiting exploration
- **Explored:** States that have been fully processed
- **Parent Tracking:** States used as keys in parent dictionary
- **Path:** Sequences of states forming the solution

### In Grid Pathfinding
For 2D grid search:
- Key typically represents a cell (x, y coordinate)
- State wraps this coordinate with semantic meaning
- Enables pathfinding algorithms to operate on "states" abstractly

## Relationship to Other Classes

- **Cost:** Associates cost values with states
- **Path:** Ordered sequences of states
- **Generated:** Priority queue of states
- **Problem:** Generates successor states
- **Solution:** Contains path of states

## Class Attribute
- **Factory**: Type reference for factory pattern (set in `__init__.py`)

## Simplicity by Design
This class is intentionally minimal:
- Focuses on wrapping a key with semantic meaning
- Delegates complexity to other classes (Cost, Path, etc.)
- Provides clean interface via HasKey mixin
- Extensible for future state properties (cached values, flags, etc.)
