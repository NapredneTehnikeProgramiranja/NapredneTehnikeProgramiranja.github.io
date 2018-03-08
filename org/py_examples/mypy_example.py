def loud_greetings(name: str) -> str:
    return 1
# ^^^ Incompatible return value type (got "int", expected "str")

def loud_greetings_two(name: str) -> str:
    return "Hello World!"

def mypy_example() -> None:
    # Ovako override-ujemo type inference
    a = 2 #type: float

### Kinds

from typing import Tuple
def mypy_k1(a: int) -> Tuple[str, int]:
    return 'prvi', a

def mypy_k2(a: int) -> Tuple[str, int]:
    return a, a
# ^^^ Incompatible return value type (got "Tuple[int, int]", expected "Tuple[str, int]")

from typing import Iterator
def mypy_iterator() -> Iterator[int]:
    i = 0
    while True:
        yield i
        i += 1
