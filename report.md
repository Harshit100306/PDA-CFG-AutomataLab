# StackLab — Case-Study-Based Analysis and Design Using PDA and CFG

**Course:** 21CSC301T — Formal Language and Automata  
**Assessment Task 3 | Term Work | Semester V | AY 2026–2027**  
**Student:** Harshit Parmar | **Registration Number:** RA2411026050026  
**Faculty:** Dr. C. Gunasundari (AP)  
**SDG:** 9 — Industry, Innovation and Infrastructure

## Abstract
This case-study report examines three context-free language problems: balanced-parenthesis recognition, arithmetic-expression syntax validation, and palindrome recognition over a two-symbol alphabet. Each problem is specified by an alphabet and target language, modelled using a context-free grammar (CFG), and related to a pushdown automaton (PDA). The report includes derivations, stack behaviour, accepted and rejected strings, ambiguity and determinism analysis, and a discussion of why finite automata are insufficient. An accompanying browser-based demonstration and Python test suite make the designs observable and repeatable.

## 1. Introduction
Finite automata recognize regular languages using a fixed set of states. They cannot store an unbounded number of unmatched delimiters or an arbitrarily long prefix for later comparison. A pushdown automaton extends finite-state control with a last-in, first-out stack. A CFG describes recursive structure through productions. These models are fundamental in syntax analysis, compiler construction and structured-input validation.

## 2. Objectives and assumptions
- Define the alphabet and language of each selected case study.
- Provide standard CFG productions and explain their role.
- Describe PDA states, stack symbols and transitions.
- Show successful derivations and stack-processing examples.
- Analyse ambiguity, determinism and limitations.
- Validate at least five accepted and five rejected strings per application.
- Distinguish syntactic recognition from semantic processing.

The arithmetic grammar supports identifiers, integer/decimal numbers, `+`, `-`, `*`, `/` and parentheses. Unary operators, exponentiation and implicit multiplication are outside scope. The palindrome alphabet is `{a,b}`. The balanced-parenthesis alphabet is `{(,)}`.

# Case Study 1 — Balanced Parentheses

## 3. Language definition
Alphabet: `Σ = { (, ) }`

`L_BAL = { w ∈ Σ* | every prefix has at least as many '(' as ')', and the total counts are equal }`.

The empty string belongs to the language.

## 3.1 CFG
Start symbol: `S`

```text
S → (S)S | ε
```

`(S)S` generates one matched outer pair containing a balanced string, followed by another balanced string. `ε` represents the empty balanced sequence.

## 3.2 Successful derivations
For `()()`:
```text
S ⇒ (S)S
  ⇒ ()S
  ⇒ ()(S)S
  ⇒ ()()
```
For `(())`:
```text
S ⇒ (S)S
  ⇒ ((S)S)S
  ⇒ (())S
  ⇒ (())
```

## 3.3 PDA definition
The PDA has a scanning state `q` and stack bottom marker `Z0`. For each `(`, push marker `X`. For each `)`, pop one `X`. If a closing parenthesis is read while the stack top is `Z0`, reject immediately. At end of input, accept only if the stack contains `Z0` alone.

| Input | Stack action | Result |
|---|---|---|
| `(` | Push `X` | Continue |
| `)` with top `X` | Pop `X` | Continue |
| `)` with top `Z0` | Underflow | Reject |
| End with only `Z0` | No unmatched opening | Accept |
| End with one or more `X` | Unmatched opening remains | Reject |

### Stack trace for `(()())`
Top of stack is at the right.

| Step | Read | Stack after move | Meaning |
|---|---|---|---|
| 0 | — | `Z0` | Initial stack |
| 1 | `(` | `Z0 X` | Push |
| 2 | `(` | `Z0 X X` | Push |
| 3 | `)` | `Z0 X` | Pop |
| 4 | `(` | `Z0 X X` | Push |
| 5 | `)` | `Z0 X` | Pop |
| 6 | `)` | `Z0` | Pop |
| 7 | End | `Z0` | Accept |

## 3.4 Test strings
| Accepted strings | Reason |
|---|---|
| `ε` | Empty string is balanced |
| `()` | One matched pair |
| `(())` | One nested pair |
| `()()` | Two consecutive pairs |
| `(()())` | Nested and sequential pairs |
| `((()()))` | Deeper nesting |

| Rejected strings | Reason |
|---|---|
| `)(` | Closing symbol appears first |
| `(` | Opening symbol remains unmatched |
| `)` | Stack underflow |
| `(()` | Missing closing symbol |
| `())` | Extra closing symbol |
| `(a)` | `a` is outside the alphabet |

## 3.5 Determinism and finite-automaton limitation
The PDA is deterministic for one delimiter type because each input symbol uniquely determines whether to push or pop. The language is non-regular: a finite automaton has no unbounded memory for the number of unmatched opening parentheses. The CFG is unambiguous because a balanced string has a unique decomposition into its first matched outer group and the suffix following that group.

# Case Study 2 — Arithmetic Expression Syntax

## 4. Language definition
The expression language contains identifiers, numeric literals, the binary operators `+`, `-`, `*`, `/`, and grouping parentheses. Whitespace may appear between tokens.

The grammar defines syntax, not numerical meaning. It does not evaluate expressions or check variable types.

## 4.1 Precedence-aware CFG
Start symbol: `E`

```text
E  → T E′
E′ → + T E′ | - T E′ | ε
T  → F T′
T′ → * F T′ | / F T′ | ε
F  → (E) | id | number
```

`E` handles addition and subtraction. `T` handles multiplication and division. `F` handles parenthesized expressions, identifiers and numbers. This separation gives multiplication and division higher precedence than addition and subtraction. The repeated operator structure is interpreted left-associatively by the implementation.

## 4.2 Successful derivation
For `id + id * id`:
```text
E
⇒ T E′
⇒ F T′ E′
⇒ id E′
⇒ id + T E′
⇒ id + F T′ E′
⇒ id + id * F T′ E′
⇒ id + id * id T′ E′
⇒ id + id * id E′
⇒ id + id * id
```
The multiplication is derived inside `T`, so it binds more tightly than the addition.

For `(id + id) * id`, the first factor expands as `(E)`, ensuring that the addition is grouped before multiplication.

## 4.3 PDA construction from CFG
A standard CFG-to-NPDA construction uses the grammar symbols on the stack:
1. Initialize the stack with bottom marker `Z0` and start variable `E`.
2. If a nonterminal is on top, replace it with the right-hand side of one of its productions. Push the right-hand side in reverse order so its leftmost symbol is processed first.
3. If a terminal is on top and matches the next input token, pop it and consume that token.
4. Accept when the input is exhausted and the stack has returned to `Z0`.

For this particular grammar, the implementation uses a deterministic recursive-descent parser with `expression`, `term`, and `factor` procedures. This is a practical deterministic parser for the selected grammar, while the CFG-to-NPDA method illustrates the general PDA construction.

## 4.4 Accepted and rejected strings
| Accepted | Explanation |
|---|---|
| `x` | Single identifier |
| `42` | Single numeric literal |
| `x + y` | Addition |
| `a + b * c` | Multiplication has higher precedence |
| `(a + b) * c` | Parenthesized subexpression |
| `x / (y - 2)` | Nested expression |
| `alpha_1 + 12.5` | Identifier and decimal literal |

| Rejected | Explanation |
|---|---|
| Empty input | No expression supplied |
| `+a` | Expression begins with binary operator |
| `a+` | Right operand is missing |
| `a**b` | Repeated operator |
| `(a+b` | Missing closing parenthesis |
| `a+b)` | Extra closing parenthesis |
| `a @ b` | Unsupported character |
| `a b` | Two adjacent operands without operator |

## 4.5 Ambiguity and grammar revision
The simple grammar `E → E+E | E*E | (E) | id` is ambiguous. For `id + id * id`, it allows more than one parse tree, including `(id+id)*id` and `id+(id*id)`. The revised grammar in Section 4.1 separates expressions, terms and factors, encoding precedence and the intended associativity. The grammar therefore removes the specific ambiguity caused by mixing all binary operators at one level.

## 4.6 Syntax versus semantics
The parser validates token order and grouping. Semantic processing is still needed to evaluate the expression, resolve identifiers, enforce types, detect division by zero and report runtime errors.

# Case Study 3 — Palindrome Recognition over {a,b}

## 5. Language definition
Alphabet: `Σ = {a,b}`

`L_PAL = { w ∈ Σ* | w = wᴿ }`, where `wᴿ` is the reverse of `w`.

The empty string and every one-symbol string are palindromes.

## 5.1 CFG
Start symbol: `S`

```text
S → aSa | bSb | a | b | ε
```
The recursive rules add the same symbol at both ends. The base cases handle odd-length strings and the empty string.

## 5.2 Successful derivations
For `aba`:
```text
S ⇒ aSa
  ⇒ aba
```
For `abba`:
```text
S ⇒ aSa
  ⇒ abSba
  ⇒ abba
```

## 5.3 Nondeterministic PDA
Without a marked centre, the PDA cannot know where the first half ends. It nondeterministically guesses a midpoint:
1. In push mode, read the first part and push each symbol.
2. Guess the midpoint. For an odd-length string, consume one centre symbol during the switch; for an even-length string, switch between the two central symbols.
3. In matching mode, compare each remaining input symbol with the stack top.
4. If equal, pop and continue. If unequal, that computation branch rejects.
5. Accept if the input ends with the stack returned to its bottom marker.

The Python implementation tries all possible midpoint branches. This simulates the nondeterministic choice; it does not claim that a deterministic PDA can identify the midpoint in advance.

## 5.4 Example trace for `abba`
| Stage | Action | Stack (top at right) |
|---|---|---|
| Start | Bottom marker | `Z0` |
| Push | Read `a`, push | `Z0 a` |
| Push | Read `b`, push | `Z0 a b` |
| Guess midpoint | Switch to matching | `Z0 a b` |
| Match | Read `b`, match and pop | `Z0 a` |
| Match | Read `a`, match and pop | `Z0` |
| End | Input consumed | Accept |

## 5.5 Accepted and rejected strings
| Accepted | Explanation |
|---|---|
| `ε` | Empty string |
| `a` | Single symbol |
| `b` | Single symbol |
| `aa` | Same forwards and backwards |
| `aba` | Reverse is `aba` |
| `abba` | Reverse is `abba` |
| `baab` | Reverse is `baab` |
| `aabbaa` | Reverse is `aabbaa` |

| Rejected | Explanation |
|---|---|
| `ab` | Reverse is `ba` |
| `aab` | Reverse is `baa` |
| `abb` | Reverse is `bba` |
| `abab` | Reverse is `baba` |
| `ba` | Reverse is `ab` |
| `abc` | `c` is outside the alphabet |

## 5.6 Determinism and limitations
The midpoint is not marked, so the PDA uses nondeterminism to choose it. The palindrome language over `{a,b}` is context-free but not regular. A finite automaton cannot store an arbitrarily long first half and compare it with the later suffix in reverse order.

# 6. Comparative Analysis

| Feature | Balanced parentheses | Arithmetic expressions | Palindromes |
|---|---|---|---|
| Main memory requirement | Unmatched opening delimiters | Recursive/nested syntax | Prefix for reverse matching |
| Formal model | CFG + DPDA | CFG + PDA construction | CFG + NPDA |
| Stack operation | Push and pop marker | Expand nonterminals, match terminals | Push prefix, pop matching suffix |
| Determinism | Deterministic | Selected grammar parsed deterministically | Nondeterministic midpoint |
| Key edge case | Stack underflow or leftover marker | Missing operand / unmatched grouping | Wrong midpoint / symbol mismatch |

## 7. Why Finite Automata Are Insufficient
A finite automaton has a fixed number of states and cannot maintain an unbounded stack:
- Balanced parentheses require remembering unmatched opening symbols.
- Arithmetic expressions allow arbitrarily nested parentheses.
- Palindromes require comparing an arbitrarily long prefix against a later suffix in reverse order.

A PDA adds a stack and can recognize these context-free structures. It does not solve every programming-language problem: type checking, symbol-table lookup, context-sensitive constraints and runtime semantics require additional mechanisms.

## 8. Implementation and Validation
The repository contains a browser-based interactive showcase, Python recognizers, trace helpers, Mermaid diagrams and automated tests. The browser page supports live input for all three case studies. The Python implementation can be run as follows:

```bash
python demo.py
python -m unittest discover -s tests -v
```

The arithmetic parser checks the stated grammar only. The balanced-parentheses recognizer uses a deterministic stack. The palindrome recognizer tests possible midpoint branches to simulate an NPDA.

## 9. SDG 9 — Design Alignment
The project has a design-level connection to SDG 9: Industry, Innovation and Infrastructure. Formal grammar and stack-based parsing are foundational methods used in compilers, interpreters and structured-data processing. They help software systems identify malformed structures before later processing. This is an educational prototype and does not claim infrastructure-scale impact.

## 10. Five-Minute Demonstration Plan
| Time | Activity |
|---|---|
| 0:00–0:30 | Introduce CFG, PDA and the need for stack memory. |
| 0:30–1:30 | Test `(()())` and `())`; explain push/pop and stack underflow. |
| 1:30–2:45 | Test `a+b*c`, `(a+b)*c`, and `a+*b`; explain precedence and ambiguity. |
| 2:45–4:00 | Test `abba`, `aba` and `aab`; explain midpoint guessing. |
| 4:00–4:40 | Run the Python tests and show the results. |
| 4:40–5:00 | Summarize determinism, limitations and SDG 9. |

## 11. Conclusion
The case studies demonstrate how CFGs describe recursive language structure and how PDAs recognize context-free patterns with a stack. Balanced parentheses use a deterministic stack discipline. Arithmetic syntax uses a precedence-aware CFG and can be parsed deterministically with the selected grammar. Palindrome recognition without a centre marker naturally uses nondeterministic midpoint choice. The comparison shows why finite automata are insufficient for these unbounded structures and why syntax recognition remains distinct from semantic analysis.

## 12. GitHub and Evidence
GitHub profile: https://github.com/Harshit100306/

Task 3 repository URL: **Add the repository URL after pushing this project.**

Add screenshots from your own execution:
- Figure 1 — Balanced-parentheses PDA: valid nested input and invalid underflow.
- Figure 2 — Arithmetic parser: valid precedence expression and malformed expression.
- Figure 3 — Palindrome PDA: accepting and rejecting midpoint branches.
- Figure 4 — Terminal output showing the unit tests passing.

## Academic Integrity Note
This report is written specifically for the stated case studies and accompanying implementation. A similarity percentage cannot be guaranteed in advance because results depend on the institution's checker, its databases and settings. Review the report, add your own screenshots and observations, cite any external sources you consult, and verify the below-15% requirement using the institution-approved similarity checker.
