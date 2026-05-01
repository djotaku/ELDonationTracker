# PyQt6 to PySide6 Migration Checklist

Use this as an execution runbook alongside `plans/pyside6-migration-plan.md`.

## 0) Prep and Baseline

- [ ] Create migration branch.
- [ ] Confirm current app launches successfully.
- [ ] Record baseline behavior:
  - [ ] Main window loads.
  - [ ] Settings window open/save/revert works.
  - [ ] Tracker image loads and donation sound plays.
  - [ ] About and Logs dialogs open.
  - [ ] Logs refresh/copy works.
- [ ] Freeze acceptance criteria for parity.

## 1) Dependencies and Locks

- [ ] Update `pyproject.toml` dependency from `pyqt6` to `pyside6`.
- [ ] Regenerate dependency artifacts:
  - [ ] `requirements.txt`
  - [ ] `uv.lock`
- [ ] Verify no project-required `PyQt6` dependency remains.

## 2) Regenerate UI Python Files

- [ ] Keep `QTdesignerfiles/*.ui` as source of truth.
- [ ] Switch generation tool from `pyuic6` to `pyside6-uic`.
- [ ] Regenerate:
  - [ ] `eldonationtracker/ui/main_gui.py`
  - [ ] `eldonationtracker/ui/settings.py`
  - [ ] `eldonationtracker/ui/tracker.py`
  - [ ] `eldonationtracker/ui/about.py`
  - [ ] `eldonationtracker/ui/logs.py`
- [ ] Confirm generated imports point to `PySide6`.

## 3) Runtime Module Migration

- [ ] Update imports in:
  - [ ] `eldonationtracker/ui/call_main_gui.py`
  - [ ] `eldonationtracker/ui/call_settings.py`
  - [ ] `eldonationtracker/ui/call_tracker.py`
  - [ ] `eldonationtracker/ui/call_about.py`
  - [ ] `eldonationtracker/ui/call_logs.py`
- [ ] Validate compatibility points:
  - [ ] Dialog execution calls (`exec` behavior).
  - [ ] Enum access in runtime and generated code.
  - [ ] Signal/slot connections.
  - [ ] `QtMultimedia` behavior (`QMediaPlayer`, `QAudioOutput`, `setSource`, volume).

## 4) Packaging and CI

- [ ] Update `.github/workflows/windowsbuild.yml` Qt DLL copy paths from `PyQt6` layout to `PySide6` layout.
- [ ] Verify PyInstaller still bundles required Qt plugins/deps.
- [ ] Adjust PyInstaller config if plugin discovery fails.
- [ ] Run Windows build workflow and confirm artifact creation.

## 5) Validation

- [ ] Run test suite (`pytest`).
- [ ] Manual GUI verification:
  - [ ] Main window starts.
  - [ ] Settings actions (folder/file pickers, font/color/background) work.
  - [ ] ID validation message boxes work.
  - [ ] Tracker trigger shows image + plays sound + unloads after timer.
  - [ ] Logs polling and clipboard copy work.
- [ ] Cross-platform sanity:
  - [ ] Linux local run.
  - [ ] Windows artifact startup sanity (if available).

## 6) Docs and Release Notes

- [ ] Update docs that reference `PyQt6`.
- [ ] Add changelog entry for `PySide6` migration.
- [ ] Document known limitations discovered during testing.

## 7) Release Readiness Gate

- [ ] No regressions against baseline checklist.
- [ ] No unresolved migration blockers.
- [ ] CI green for targeted workflows.
- [ ] Migration PR is ready for review.
