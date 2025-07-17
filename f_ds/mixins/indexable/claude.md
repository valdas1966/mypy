# Indexable Mixin

Adds positional indexing to collections.

## Inherits From

`Collectionable` - must implement `to_iterable()`

## Features

- `obj[index]` - get item by position
- `obj[start:end]` - slice support
- All collection features (len, in, iteration)

## Example Usage

```python
class MyIndexable(Indexable[str]):
    def __init__(self, items):
        self._items = items
    
    def to_iterable(self):
        return self._items

# Usage
obj = MyIndexable(['a', 'b', 'c'])
obj[0]          # 'a'
obj[1]          # 'b' 
obj[0:2]        # ['a', 'b']
obj[-1]         # 'c'
```

## Tests

```python
abc = Factory.abc()  # ['a', 'b', 'c']
abc[0] == 'a'
abc[1] == 'b'
abc[0:2] == ['a', 'b']
abc[1:3] == ['b', 'c']
```

## Error Handling

Raises `TypeError` for invalid index types (not int or slice).