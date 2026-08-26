# Workshop tools

Tools in this directory are intentionally small and dependency-free. Each tool
must state its input, output, failure conditions, and acceptance command.

Current tool:

- [`workshop_lint.py`](workshop_lint.py) checks skill-card metadata, allowed
  status values, required limits, and obvious secret-like strings.

The linter checks workshop hygiene. It does not prove that a skill is correct,
safe for every environment, or adopted by the city.
