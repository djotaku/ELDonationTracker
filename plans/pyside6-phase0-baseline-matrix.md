# Phase 0 Baseline Checklist and Pass/Fail Matrix

This document captures the pre-migration GUI baseline for the PyQt6 -> PySide6 work.

## Branch

- Dedicated migration branch: `pyside`

## Frozen Acceptance Criteria

1. No new runtime exceptions are introduced during migration.
2. Feature parity with current GUI behavior is maintained.
3. Windows build workflow still produces an executable artifact.

## Baseline Smoke Checklist (Pre-Migration)

Use this checklist to record current behavior before Phase 1 starts.

- [x] App launch works from GUI entrypoint (`python -m eldonationtracker.gui`) in offscreen run.
- [x] Settings window opens from main UI.
- [x] Settings save path executes and writes expected config payload.
- [x] Settings revert restores expected values.
- [x] Tracker window displays image content via trigger/test path.
- [ ] Tracker audio playback audibility is manually confirmed on a host with audio output.
- [x] Donation trigger flow updates tracker as expected.
- [x] Logs window opens and refreshes.
- [x] Logs copy action writes expected content to clipboard.

## Pass/Fail Matrix

| Area | Scenario | Baseline Result | Post-Migration Result | Notes |
| --- | --- | --- | --- | --- |
| Launch | GUI entrypoint starts without runtime error | Pass | Pending | Offscreen GUI bootstrap succeeded with no runtime exceptions. |
| Settings | Open settings dialog | Pass | Pending | Dialog instantiated and shown in offscreen session. |
| Settings | Save settings and reopen to verify persistence | Pass | Pending | Save path writes expected config payload via `write_config`; reopen persistence still needs interactive/manual confirmation. |
| Settings | Revert settings flow | Pass | Pending | Revert restored modified field to initial loaded value. |
| Tracker | Image display after trigger/test path | Pass | Pending | Tracker load/test path executed and image item loaded into scene. |
| Tracker | Audio playback after trigger/test path | N/A | Pending | No audio device available in environment; media source and play path invoked, but audible output cannot be confirmed here. |
| Donation Flow | Donation trigger updates tracker behavior | Pass | Pending | `new_donation` trigger path executed and state reset on unload. |
| Logs | Logs dialog refresh behavior | Pass | Pending | Log text area populated during refresh call. |
| Logs | Copy logs to clipboard behavior | Pass | Pending | Clipboard content matched visible logs content after copy action. |
| Runtime Stability | No new runtime exceptions | Pass | Pending | No new runtime exceptions during baseline smoke script run. |
| CI Packaging | Windows workflow produces executable | N/A | Pending | Not runnable in this Linux local environment; to be validated in Windows CI. |

## Recording Convention

- Baseline Result values: `Pass`, `Fail`, or `N/A`.
- Post-Migration Result values: `Pass`, `Fail`, or `N/A`.
- If any row fails, include reproduction notes and traceback/log location in `Notes`.
