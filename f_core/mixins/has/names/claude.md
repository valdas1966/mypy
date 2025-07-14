# HasNames Mixin

## Purpose
Container for managing collections of HasName objects with name-based access and utilities.

## Features
- Extends UserList for standard list operations
- Name-based object lookup and containment checks
- Extract all names as list
- Access objects by name or index
- Type-safe collection of HasName objects

## Usage

### Basic Usage
```python
from f_core.mixins.has.name import HasName

class Item(HasName):
    pass

items = HasNames([
    Item("apple"),
    Item("banana"), 
    Item("cherry")
])

print(len(items))  # 3
```

### Name-based Operations
```python
# Get all names
names = items.names()  # ["apple", "banana", "cherry"]

# Check if name exists
"apple" in items  # True
"grape" in items  # False

# Access by name
apple = items["apple"]  # Returns Item with name "apple"

# Access by index (standard list behavior)
first = items[0]     # First item
subset = items[0:2]  # First two items
```

### Iteration and Standard List Operations
```python
# Iterate over items
for item in items:
    print(item.name)

# Add/remove items
items.append(Item("grape"))
items.remove(items["banana"])
```

## Key Methods
- `__init__(items: list[HasName])` - Initialize with HasName objects
- `names()` - Returns list of all object names
- `__contains__(name: str)` - Check if name exists in collection
- `__getitem__(item: str|int|slice)` - Get by name, index, or slice
- All standard UserList methods (append, remove, etc.)

## Notes
- Raises ValueError if name not found during string lookup
- Maintains insertion order like regular lists
- Type hints ensure only HasName objects can be stored
- Supports both name-based and index-based access patterns