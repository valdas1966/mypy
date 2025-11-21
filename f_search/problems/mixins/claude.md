# mixins - Compositional Problem Features

## Purpose
Provides reusable mixin classes that add specific features to problem definitions. Mixins enable compositional design, allowing problems to combine features (start, goal, goals) without deep inheritance hierarchies.

## Structure

- **has_start/** - `HasStart` - Provides single start state
- **has_goal/** - `HasGoal` - Provides single goal state
- **has_goals/** - `HasGoals` - Provides multiple goal states (set)

## Mixin Pattern

### Design Philosophy
Instead of creating deep inheritance hierarchies, use **horizontal composition**:
- Each mixin adds one specific feature
- Problems mix and match features as needed
- Clean separation of concerns
- Reusable components

### Traditional vs Mixin Approach

**Traditional (Deep Inheritance):**
```
Problem
  ├─ ProblemWithStart
  │   ├─ ProblemWithStartAndGoal (SPP)
  │   └─ ProblemWithStartAndGoals (OMSPP)
```

**Mixin (Composition):**
```
Problem + HasStart + HasGoal → SPP
Problem + HasStart + HasGoals → OMSPP
```

## Available Mixins

### HasStart
**Purpose:** Adds a single start state to a problem

**Provides:**
- `start` property → `StateBase`
- Constructor: `__init__(start: StateBase)`

**Used by:**
- ProblemSPP
- ProblemOMSPP

**Semantics:** The initial configuration/position

### HasGoal
**Purpose:** Adds a single goal state to a problem

**Provides:**
- `goal` property → `StateBase`
- Constructor: `__init__(goal: StateBase)`

**Used by:**
- ProblemSPP

**Semantics:** The single target configuration/position

### HasGoals
**Purpose:** Adds multiple goal states to a problem

**Provides:**
- `goals` property → `set[StateBase]`
- Constructor: `__init__(goals: Iterable[StateBase])`

**Used by:**
- ProblemOMSPP

**Semantics:** Multiple target configurations/positions

**Note:** Stores goals as a set (no duplicates, no order)

## Mixin Composition Examples

### One-to-One (SPP)
```python
class ProblemSPP(ProblemSearch, HasStart, HasGoal):
    def __init__(self, grid, start, goal):
        ProblemSearch.__init__(self, grid=grid)
        HasStart.__init__(self, start=start)
        HasGoal.__init__(self, goal=goal)
```

Result: Problem with grid + start + goal

### One-to-Many (OMSPP)
```python
class ProblemOMSPP(ProblemSearch, HasStart, HasGoals):
    def __init__(self, grid, start, goals):
        ProblemSearch.__init__(self, grid=grid)
        HasStart.__init__(self, start=start)
        HasGoals.__init__(self, goals=goals)
```

Result: Problem with grid + start + goals (set)

## Benefits of Mixin Design

### 1. Reusability
Each mixin is self-contained and reusable:
- HasStart used by both SPP and OMSPP
- Can be reused in future problem types

### 2. Single Responsibility
Each mixin has exactly one responsibility:
- HasStart: manages start state
- HasGoal: manages goal state
- HasGoals: manages goal set

### 3. Flexibility
Easy to create new combinations:
- Many-to-One: HasStarts + HasGoal
- Many-to-Many: HasStarts + HasGoals
- Constrained: HasStart + HasGoal + HasConstraints

### 4. Explicitness
Problem class signature clearly shows features:
- `ProblemSPP(ProblemSearch, HasStart, HasGoal)` → obviously has start and goal
- `ProblemOMSPP(ProblemSearch, HasStart, HasGoals)` → obviously has start and goals

### 5. Type Safety
Mixins provide type-safe property access:
- `problem.start` guaranteed to exist (via HasStart)
- `problem.goal` or `problem.goals` depending on mixin

## Mixin Constructor Pattern

All mixins follow the same pattern:

```python
class HasFeature:
    def __init__(self, feature):
        self._feature = feature

    @property
    def feature(self):
        return self._feature
```

This provides:
- Private storage (`_feature`)
- Public read-only access (`feature` property)
- Immutability (no setter)

## Future Mixin Opportunities

Potential new mixins for extended problem types:

- **HasStarts**: Multiple start states
- **HasConstraints**: Resource/time constraints
- **HasCosts**: Non-uniform edge costs
- **HasDynamics**: Time-varying obstacles
- **HasRegions**: Zone-based restrictions
- **HasPreferences**: Soft constraints

## Multiple Inheritance Considerations

### Constructor Chaining
Problems must call all mixin constructors:
```python
def __init__(self, grid, start, goal):
    ProblemSearch.__init__(self, grid=grid)
    HasStart.__init__(self, start=start)
    HasGoal.__init__(self, goal=goal)
```

### Method Resolution Order (MRO)
Python resolves multiple inheritance using C3 linearization:
- Mixins should not overlap in methods
- Each mixin provides unique properties/methods
- No diamond problem (mixins are independent)

### Mixin Independence
Mixins are designed to be independent:
- No dependencies between mixins
- Each can be used standalone
- No shared state or methods

## Design Guidelines

When creating new mixins:

1. **Single Feature**: Each mixin adds exactly one feature
2. **No Dependencies**: Don't depend on other mixins
3. **Immutable**: Provide read-only properties
4. **Explicit Init**: Require feature in constructor
5. **Property Access**: Use @property for public interface
6. **Private Storage**: Use `_name` for internal attributes

## Relationship to Problems

```
Mixin (feature provider)
    ↓ composed by
Problem (feature consumer)
    ↓ used by
Algorithm (feature user)
```

Algorithms access mixin features through problem interface:
```python
start = problem.start  # From HasStart
goal = problem.goal    # From HasGoal
goals = problem.goals  # From HasGoals
```

## Type Hierarchy

Mixins don't form a hierarchy, they're flat:
```
HasStart  (independent)
HasGoal   (independent)
HasGoals  (independent)
```

Problems combine them horizontally:
```
ProblemSPP = ProblemSearch + HasStart + HasGoal
ProblemOMSPP = ProblemSearch + HasStart + HasGoals
```
