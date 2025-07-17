# Collectionable Mixin

Adds collection behavior to classes.

## Core Method

Must implement `to_iterable()` that returns items.

## Features

- `len()` - get size
- `in` operator - check membership  
- iteration support
- string representation

## Example Usage

```python
class MyCollection(Collectionable[str]):
    def __init__(self, items):
        self._items = items
    
    def to_iterable(self):
        return self._items

# Usage
obj = MyCollection(['a', 'b', 'c'])
len(obj)        # 3
'a' in obj      # True
list(obj)       # ['a', 'b', 'c']
```

## Tests

```python
abc = Factory.abc()  # ['a', 'b', 'c']
len(abc) == 3
'a' in abc
'd' not in abc
```