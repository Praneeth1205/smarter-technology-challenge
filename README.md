# 📦 Package Sorter — Smarter Technology Robotic Automation Challenge

A Python solution for dispatching packages to the correct stack based on volume and mass, written for Smarter Technology's robotic arm factory system.

---

## Problem Summary

Each package needs to be routed to one of three stacks:

| Stack | Condition |
|---|---|
| `STANDARD` | Not bulky and not heavy |
| `SPECIAL` | Bulky **or** heavy (but not both) |
| `REJECTED` | Bulky **and** heavy |

**Bulky** = volume ≥ 1,000,000 cm³ OR any single dimension ≥ 150 cm  
**Heavy** = mass ≥ 20 kg

---

## How to Run

No dependencies. Just Python 3.

```bash
python sort_packages.py
```

Expected output:
```
Ran 17 tests in 0.001s

OK
```

---

## Solution

```python
def sort(width: float, height: float, length: float, mass: float) -> str:
    if any(v < 0 for v in (width, height, length, mass)):
        raise ValueError("Dimensions and mass must be non-negative.")

    volume = width * height * length
    is_bulky = volume >= 1_000_000 or max(width, height, length) >= 150
    is_heavy = mass >= 20

    if is_bulky and is_heavy:
        return "REJECTED"
    if is_bulky or is_heavy:
        return "SPECIAL"
    return "STANDARD"
```

The logic uses two boolean flags to keep the branching clean and readable. The three return paths map directly to the three stacks — no nested conditions, no ambiguity.

---

## Design Decisions

**Why two boolean flags instead of inline conditions?**  
`is_bulky` and `is_heavy` make the intent readable at a glance. The three `if` branches then read almost like the spec itself.

**Why `max(width, height, length)` for the dimension check?**  
It avoids repeating `>= 150` three times and makes it obvious we're checking any single dimension, not all of them.

**Why raise `ValueError` for negatives?**  
A package can't have negative dimensions or mass. Silently accepting bad input would produce meaningless results. Failing loudly is safer in a physical automation context.

**Why `float` types?**  
Real-world measurements aren't always whole numbers. Using `float` handles both integer and decimal inputs without any type-casting.

---

## Test Coverage

17 tests across all branches and boundaries:

| Category | Tests |
|---|---|
| STANDARD cases | Normal package, zero mass, just-below volume boundary |
| SPECIAL (bulky) | Volume exactly 1,000,000; over 1,000,000; dimension exactly 150; dimension over 150 |
| SPECIAL (heavy) | Mass exactly 20 kg; mass over 20 kg |
| REJECTED | Bulky + heavy, large dimension + heavy, all extreme values |
| Edge cases | Zero dimensions, negative dimension (raises), negative mass (raises), float dimensions, mass at 19.9999 kg |

Key boundary tests:
```python
# Exactly at the volume limit → SPECIAL
sort(100, 100, 100, 5)  # volume = 1,000,000 → "SPECIAL"

# Just below → STANDARD
sort(99.9999, 10, 10, 19)  # volume = 999,999 → "STANDARD"

# Exactly at mass limit → SPECIAL
sort(10, 10, 10, 20)  # → "SPECIAL"

# Both triggered → REJECTED
sort(100, 100, 100, 20)  # → "REJECTED"
```

---

## Author

**Praneeth Reddy Elugoti**  
Senior Software Engineer | Java · Python · Spring Boot · AWS  
[LinkedIn](https://linkedin.com/in/praneethreddy) · Chicago, IL
