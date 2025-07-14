# HasName Mixin

## Purpose
Provides name property with comparison and hashing capabilities for objects that need string-based identification.

## Features
- `name` property (str) with getter
- Comparable by name (sorting support)
- Printable string representation
- Hash function based on name
- Handles None names gracefully

## Usage

### Basic Usage
```python
class MyClass(HasName):
    def __init__(self, name: str = None):
        super().__init__(name)

obj = MyClass("example")
print(obj.name)  # "example"
print(str(obj))  # "example"
```

### Comparison and Sorting
```python
obj1 = MyClass("apple")
obj2 = MyClass("banana")
obj3 = MyClass(None)

# Sorting works automatically
items = [obj2, obj3, obj1]
sorted_items = sorted(items)  # [None, "apple", "banana"]
```

### Hash Support
```python
obj = MyClass("test")
hash_value = hash(obj)  # Based on name
obj_set = {obj}  # Can be used in sets/dict keys
```

## Key Methods
- `__init__(name: str = None)` - Initialize with optional name
- `name` property - Returns the object's name
- `key_comparison()` - Returns comparison key for sorting
- `__str__()` - String representation (name or 'None')
- `__hash__()` - Hash based on name

## Notes
- Empty/None names sort before named objects
- String representation shows 'None' for missing names
- Inherits from Comparable and Printable mixins