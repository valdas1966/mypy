# Instruction to AI Agent (Claude Code): Generate CLAUDE.md for a python folder (class \ module \ package)

Create a `CLAUDE.md` for the given folder. Keep it concise, concrete, and accurate to the code. Do not invent behavior.

## Output rules
- Use Markdown with clear section headers.
- If something is unclear from the file alone, ask clarification questions from the user (do not guess).

## Mandatory sections (in this order):
### 1) Purpose - What the class is responsible for.

### 2) Public API
List only public methods/properties (including dunder methods).
For each API item include a signature with full type hints and behavior / guarantee.

### 3) Inheritance (Hierarchy)
- Show the class inheritance chain (bases in order).
- What responsibilities come from each base.

### 4) Dependencies - Summarize imports as core dependencies (classes this class relies on)

### 5) Usage example (concise + classic)
Provide a minimal example that a user would actually write
You can use _factory.py and _tester.py files from the folder for practical examples.
