# Change 04 — Publish AI conversation log to GitHub

## Why

The course requires submitting the AI-collaboration log (`與AI的對話紀錄`).
Originally we kept `ai_record.md` local (gitignored) so the user could upload
it themselves. The user has now decided to publish it directly in the repo
so everything lives in one place.

## What changes

- **MODIFIED** `.gitignore`: remove `ai_record.md`.
- **MODIFIED** `ai_record.md`: rewrite as a detailed turn-by-turn transcript
  of the entire assignment session (user requests + assistant responses +
  key decisions + intermediate results).

## Impact

- No code changes, no spec changes. Pure documentation artifact.
- `ai_record.md` becomes publicly visible in the repo (it was already local).

## Acceptance criteria

- `ai_record.md` is tracked by git.
- The file captures all major user messages and assistant replies in the
  session in chronological order.
- Running `git check-ignore ai_record.md` returns a non-match (i.e. not ignored).
