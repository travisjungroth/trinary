![License](https://img.shields.io/github/license/travisjungroth/trinary?color=blue)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
# trinary - A Python implementation of three-valued logic
trinary is a Python library for working with three-valued logic. It allows you to represent and manipulate statements with three possible truth values: true, false, and unknown. Unknown represents the possibility of true and false.

# Usage
To use trinary, import `Unknown` into your Python project. You can then use `Unknown` alongside `True` and `False`.
```python
from trinary import Unknown

# Logical AND
print(Unknown & True)      # Unknown
print(Unknown & False)     # False
print(Unknown & Unknown)   # Unknown

# Logical OR
print(Unknown | True)      # True
print(Unknown | False)     # Unknown
print(Unknown | Unknown)   # Unknown

# Logical XOR
print(Unknown ^ True)      # Unknown
print(Unknown ^ False)     # Unknown
print(Unknown | Unknown)   # Unknown

# Logical NOT
print(~Unknown)            # Unknown

# Comparisons
print(Unknown == True)     # Unknown
print(Unknown == False)    # Unknown
print(Unknown == Unknown)  # Unknown   
print(Unknown != True)     # Unknown
print(Unknown != False)    # Unknown
print(Unknown != Unknown)  # Unknown
print(Unknown < True)      # Unknown
print(Unknown < False)     # False
print(Unknown < Unknown)   # Unknown   
print(Unknown <= True)     # True
print(Unknown <= False)    # Unknown
print(Unknown <= Unknown)  # Unknown   
print(Unknown > True)      # False
print(Unknown > False)     # Unknown
print(Unknown > Unknown)   # Unknown   
print(Unknown >= True)     # Unknown
print(Unknown >= False)    # True
print(Unknown >= Unknown)  # Unknown
```
To cast to a `bool`, use strictly or weakly to decide how `Unknown` is cast.

```python
from trinary import Unknown, strictly, weakly

correct = Unknown
print(strictly(correct))  # False
print(weakly(correct))    # True
# anything else is the same as calling bool()
print(weakly(''))         # False
```

# Examples

Use trinary to represent the truth value of a statement with uncertain information.

```python
from trinary import Trinary, Unknown, strictly, weakly

test_a = Unknown
test_b = True

passed_both = test_a & test_b
print(passed_both)            # Unknown
print(strictly(passed_both))  # False
passed_at_least_one = test_a | test_b
print(passed_at_least_one)    # True
maybe_failed_both = weakly(~test_a & ~test_b)
print(maybe_failed_both)      # True


# Example with functions and type hints
def hot_out(weather: str) -> Trinary:
    if weather == "sunny":
        return True
    elif weather == "cloudy":
        return Unknown
    else:
        return False


def going_to_the_beach(weather: str, off_work: Trinary) -> Trinary:
    return hot_out(weather) & off_work


monday_beach = going_to_the_beach(weather="cloudy", off_work=False)
print(monday_beach)              # False
saturday_beach = going_to_the_beach(weather="cloudy", off_work=True)
print(saturday_beach)            # Unknown
definitely_free_saturday = strictly(~saturday_beach)
print(definitely_free_saturday)  # False
```
# Theory
trinary implements Stephen Cole Kleene's ["strong logic of indeterminacy"](https://en.wikipedia.org/wiki/Three-valued_logic#Kleene_and_Priest_logics), also called K3. This is equivalent to SQL logic with `NULL`.

### Truth Table
|p|q|p&q|p^q|p⇒q|¬p|
|-|-|---|---|---|--|
|T|T|T  |F  |T  |F |
|F|F|F  |F  |T  |T |
|F|?|F  |?  |?  |T |
|?|T|?  |?  |T  |? |
|?|F|F  |?  |?  |? |
|?|?|?  |?  |?  |? |

# License
trinary is licensed under the [MIT License](license.md).