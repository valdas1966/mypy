from dataclasses import dataclass


@dataclass
class C:
    name: str


c = C(name='abc')
print(c)