# OpenSpec Agent Instructions

This project uses **OpenSpec** (spec-driven development) for AI-assisted iteration.

## Directory layout

```
openspec/
├── project.md          Project-level context & tech stack
├── AGENTS.md           This file — how an AI agent should work here
├── changes/            Proposed / in-progress changes (numbered 01-, 02-, ...)
│   └── NN-<slug>/
│       ├── proposal.md     Why this change exists (problem → approach)
│       ├── tasks.md        Checklist of concrete sub-tasks
│       ├── design.md       (optional) Notes on non-obvious technical decisions
│       └── specs/          Delta specs — ADDED / MODIFIED / REMOVED requirements
│           └── <capability>/spec.md
└── specs/              Current (archived) specifications — source of truth
    └── <capability>/spec.md
```

## Workflow

1. **Propose.** Create a new directory under `changes/` with the next `NN-` number.
   Write `proposal.md` (problem + approach), `tasks.md` (checklist), and delta specs.
2. **Implement.** Work through `tasks.md`, ticking items as you complete them.
3. **Validate.** Ensure `tasks.md` is fully ticked and specs match the code.
4. **Archive.** Merge the change's delta specs into `openspec/specs/` and remove the
   change folder (or mark it archived). Update `HANDOVER.md` for the next iteration.

## Spec format

Each requirement in `specs/<capability>/spec.md` is written as:

```markdown
## Requirement: <Short imperative title>

The <component> SHALL <behaviour>.

### Scenario: <name>

- **GIVEN** <pre-condition>
- **WHEN** <action>
- **THEN** <expected outcome>
```

Keep requirements testable. Every `SHALL` must be verifiable from code + outputs.

## Change numbering rule

Change IDs start at `01-` and increase monotonically. Never skip numbers; never
re-use a retired number. The current highest number is recorded in `HANDOVER.md`.
