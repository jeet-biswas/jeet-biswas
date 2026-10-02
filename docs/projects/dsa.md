# Data structures and algorithms practice

[Repository](https://github.com/jeet-biswas/DSA) |
[Implementations](https://github.com/jeet-biswas/DSA/tree/master/algorithms) |
[Tests](https://github.com/jeet-biswas/DSA/tree/master/tests)

The repository keeps the original array notebooks and adds reusable Python
implementations with executable tests. It is a place to make reasoning visible:
input assumptions, invariants, boundary cases, and time/space costs.

## Reading path

| Start with | Then ask |
|---|---|
| Traversal | Which values or indices must be retained? |
| Binary search | What does each boundary mean, including duplicates? |
| Prefix sums | What work can be precomputed for repeated range queries? |
| Hashing | Is membership, frequency, or an index lookup needed? |
| Two pointers | What property permits moving one endpoint? |
| Sliding windows | When is a window valid, and when should it shrink? |
| Stacks and queues | Does the problem need last-in-first-out or first-in-first-out order? |
| Sorting | What tradeoff is made between implementation cost and complexity? |

## Run the checks

From the DSA repository root, with Python 3.11 or newer:

```sh
python -m unittest discover -s tests -v
```

The reusable modules and tests use the Python standard library. Jupyter is only
needed to run the original notebooks. The exercises document sorted-input and
mutation assumptions rather than hiding them in examples.

For a useful study session, choose one algorithm, trace a small case by hand,
compare it with a straightforward reference solution, and then change a boundary
condition. Empty inputs, repeated values, and negative numbers often expose the
assumption that matters.

[Back to profile](../../README.md)
