# Independent review — Creative desktop design preview

Scope: the opt-in redesign experiment above desktop-foundation commit
439e486414070161d9fea58a6123644e8d0afdc3. The production entry point, installer,
license notices, file schema and measurement units remain inherited.

The first senior-reviewer pass inspected 439e486..c8859ed in a fresh ordinary
clone. Its verdict required changes. Findings and dispositions:

| Severity / finding | Fix / evidence |
| --- | --- |
| P0: every interactive launch replaced the sample, discarding Ctrl+S edits | Only create an absent interactive sample; captures use a separate path/account. Real launcher test saves a named tree and verifies it after restart and capture. |
| P1: inherited main-window strings use the subclass translation context | Forward tr to GardenPlannerApp; compiled-German menu and shared header-action assertions. |
| P1: launcher omits the saved translator | Call existing load_translator before constructing widgets; German restart test. |
| P1: launcher overwrites window/dock preferences | Deterministic showNormal/resize/reset only for capture; restart test checks real geometry and hidden docks. |
| P1: visible startup checkbox has no effect | Interactive launch uses inherited startup sequence and preference; no unconditional second welcome. Restart test checks disabled welcome. |
| P1: fullscreen leaves enabled sun toolbar/new label visible | Include sun toolbar in saved/hide/restore set; fullscreen restoration assertion. |
| P1: Windows download document link is broken | Link to existing docs/WINDOWS_DOWNLOAD.md. |

Review P2 follow-ups remain explicit: selected-language formatting of recent-file
dates and consolidation of global theme restyling. Neither is represented as
completed; styling performance is also an unresolved full-suite validation issue.

Clean re-review of the fixes is pending. This document is not a merge approval.
Full inherited-suite completion, native package checks, owner visual approval
and manual testing remain outstanding. No merge or production release is
authorized by this review.
