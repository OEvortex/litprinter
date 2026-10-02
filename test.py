"""Manual smoke test for litprinter.

Run it with no arguments::

    py test.py

Everything below works with **no imports**: `ic` is registered in builtins when
litprinter is installed. Run `py -m pytest` for the automated test suite
instead - this file exists so you can eyeball real terminal output.
"""


# ---------------------------------------------------------------------------
# Plain functions
# ---------------------------------------------------------------------------
def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


# ---------------------------------------------------------------------------
# Module level: calls and expressions get `file:line`, plain names stay clean
# ---------------------------------------------------------------------------
x = 42
name = "litprinter"
items = [1, 2, 3]

ic(x)                    # ic| x: 42                     <- no context needed
ic(name)                 # ic| name: 'litprinter'        <- no context needed
ic(add(5, 3))            # ic| [test.py:43] >>> add(5, 3): 8
ic(subtract(5, 3))       # ic| [test.py:44] >>> subtract(5, 3): 2
ic(multiply(5, 3))       # ic| [test.py:45] >>> multiply(5, 3): 15
ic(divide(5, 3))         # ic| [test.py:46] >>> divide(5, 3): 1.666...
ic(items[0])             # ic| [test.py:47] >>> items[0]: 1
ic(x * 2)                # ic| [test.py:48] >>> x * 2: 84
ic(f"{name}!")           # ic| 'litprinter!'              <- self-describing
ic(x + 1, includeContext=True)   # forced on:  ic| [test.py:50] >>> ...
ic()                    # ic| test.py:51 - HH:MM:SS.mmm  <- breadcrumb


# ---------------------------------------------------------------------------
# Inside a function: context also names the function
# ---------------------------------------------------------------------------
def compute():
    total = add(20, 22)
    ic(total)           # ic| total: 42                 <- still no context
    ic(total / 7)       # ic| [test.py:60 in compute()] >>> total / 7: 6.0
    return total


compute()


# ---------------------------------------------------------------------------
# ic.print: drop-in print() replacement
# ---------------------------------------------------------------------------
ic.print("plain print replacement")
ic.print("with", "sep", sep=" | ", end="!\n")
ic.print("[bold red]markup[/bold red] works")
ic.print("[on_blue] INFO [/on_blue] highlighted line")
ic.print({"port": 8080, "host": "0.0.0.0"}, highlight=True)
ic.print("[not markup]", markup=False)


# ---------------------------------------------------------------------------
# Logging without importing logging
# ---------------------------------------------------------------------------
ic.debug("cache miss", "user:42")
ic.info("server listening on :8080")
ic.success("build finished")
ic.warning("retrying in 5s", "attempt=2")
ic.error("request failed", "status=500")
ic.log("explicit level", level="info", timestamp=True)


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------
def safe_divide(a, b):
    try:
        return divide(a, b)
    except ValueError as exc:
        ic.error("caught", exc)
        return None


safe_divide(5, 0)
ic("safe_divide returned:", safe_divide(10, 2))
