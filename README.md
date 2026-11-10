# StackLab — PDA & CFG Case-Study Studio

**21CSC301T | Assessment Task 3 | B.Tech AIML | Semester V | AY 2026–2027**

A polished interactive showcase and Python test suite for three context-free language case studies:
1. Balanced parentheses — CFG and deterministic stack recognizer.
2. Arithmetic expression syntax — precedence-aware CFG and recursive-descent parser.
3. Palindromes over `{a,b}` — CFG and nondeterministic midpoint PDA simulation.

## Open the showcase
Open `web/index.html` in a modern browser. It runs locally with no external packages or server.

## Run the Python implementation
Python 3.10+:
```bash
python demo.py
python -m unittest discover -s tests -v
```

## Structure
- `web/index.html` — interactive dark-mode StackLab dashboard
- `src/` — three recognizers/parsers and trace helpers
- `tests/` — accepted/rejected test cases
- `diagrams/` — Mermaid diagrams
- `report.md` — detailed academic design note

## Model notes
- Balanced parentheses uses a deterministic stack.
- Arithmetic syntax is specified by a precedence-aware CFG. The Python recursive-descent parser is a deterministic implementation for this grammar; the standard CFG-to-NPDA construction is also explained in the report.
- Palindrome recognition uses nondeterministic midpoint choice. The Python code tries all possible midpoint branches to simulate that nondeterminism.

## SDG 9
Design-level alignment through formal syntax checking as a foundational component of dependable software infrastructure.
