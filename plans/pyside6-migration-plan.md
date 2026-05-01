# PyQt6 to PySide6 Migration Plan

## Goal

Migrate the GUI stack from `PyQt6` to `PySide6` with no behavior regressions across the main window, settings window, tracker window (including audio), and logs/about dialogs.

This project cannot safely be migrated with a regex-only replacement because it includes:

- generated UI modules that should be regenerated with a different toolchain,
- enum/API usage that can differ subtly between bindings,
- multimedia and packaging paths that are binding-specific,
- lock/build files and CI steps that require coordinated updates.

## Current Migration Surface

### Runtime GUI code

- `eldonationtracker/ui/call_main_gui.py`
- `eldonationtracker/ui/call_settings.py`
- `eldonationtracker/ui/call_tracker.py`
- `eldonationtracker/ui/call_about.py`
- `eldonationtracker/ui/call_logs.py`

### Generated UI modules (from Qt Designer `.ui`)

- `eldonationtracker/ui/main_gui.py`
- `eldonationtracker/ui/settings.py`
- `eldonationtracker/ui/tracker.py`
- `eldonationtracker/ui/about.py`
- `eldonationtracker/ui/logs.py`

### Dependency + packaging + release surface

- `pyproject.toml`
- `requirements.txt`
- `uv.lock`
- `.github/workflows/windowsbuild.yml`
- `changelog.md` (release note history and new release notes)

## Migration Strategy (Phased)

## Phase 0: Branch, baseline, and acceptance criteria

1. Create a dedicated branch for the migration.
2. Capture baseline behavior with manual smoke checks:
   - app launch,
   - settings open/save/revert,
   - tracker image + audio playback,
   - donation trigger flow,
   - logs window refresh/copy.
3. Freeze acceptance criteria:
   - no new runtime exceptions,
   - feature parity with current GUI behavior,
   - Windows build workflow still produces an executable.

Deliverable: baseline checklist and pass/fail matrix to compare after migration.

## Phase 1: Dependency and toolchain migration

1. Replace runtime dependency in `pyproject.toml`:
   - remove `pyqt6`,
   - add `pyside6` (pin/range policy consistent with existing dependency style).
2. Regenerate lock artifacts:
   - refresh `requirements.txt` from the dependency source of truth,
   - refresh `uv.lock`.
3. Confirm no transitive `PyQt6` packages remain required by this project.

Why this is not regex-only: lockfiles and resolver outputs are structural and must be regenerated, not text-edited.

## Phase 2: Regenerate generated UI modules from `.ui` files

1. Keep `QTdesignerfiles/*.ui` as the source of truth.
2. Replace `pyuic6` generation path with `pyside6-uic`.
3. Regenerate:
   - `main_gui.py`, `settings.py`, `tracker.py`, `about.py`, `logs.py`.
4. Review generated code headers/imports to ensure they now import from `PySide6`.

Important: generated files should not be manually hand-edited except for project-required customizations (prefer none).

## Phase 3: Manual runtime import/API migration

Update runtime modules to `PySide6` imports intentionally (file-by-file), then validate API compatibility.

### 3.1 Import namespace migration

For each runtime file listed above:

- move `from PyQt6...` imports to equivalent `from PySide6...` imports,
- keep module boundaries (`QtCore`, `QtGui`, `QtWidgets`, `QtMultimedia`) consistent.

### 3.2 API compatibility checkpoints

Validate these known risk points after import migration:

- dialog execution methods (`exec` / `exec_` compatibility),
- enum access patterns used by generated code and runtime code,
- multimedia calls in tracker (`QMediaPlayer`, `QAudioOutput`, `setSource`, volume units),
- signal/slot connection signatures where overload handling may differ.

Why this is not regex-only: API names may match while behavior/signature expectations can still differ.

## Phase 4: Packaging and CI adjustments

1. Update `.github/workflows/windowsbuild.yml` hardcoded Qt DLL copy paths from `PyQt6` site-packages layout to `PySide6` layout.
2. Confirm PyInstaller still captures Qt plugins and multimedia dependencies for `PySide6`.
3. If needed, adjust PyInstaller spec/options for Qt plugin discovery.
4. Re-run Windows build workflow to verify artifact creation.

## Phase 5: Validation matrix

### 5.1 Automated checks

- run existing tests (`pytest`) to catch non-GUI regressions.

### 5.2 Manual GUI smoke tests

1. Launch GUI entrypoint.
2. Open each dialog/window (`main`, `settings`, `tracker`, `about`, `logs`).
3. Exercise settings actions:
   - choose folder/file,
   - choose font/color/background,
   - validate IDs and message boxes.
4. Trigger tracker test path and verify:
   - image displays,
   - sound plays,
   - unload timer clears as expected.
5. Confirm log polling window updates and clipboard copy still works.

### 5.3 Cross-platform sanity (minimum)

- Linux local run (current environment),
- Windows CI build artifact startup sanity (if possible in test environment).

## Phase 6: Documentation and release notes

1. Update user/developer docs where dependency name is mentioned.
2. Add changelog entry describing migration from `PyQt6` to `PySide6`.
3. Include known limitations (if any) discovered during validation.

## Risk Register

- **High:** Multimedia behavior changes in `QtMultimedia` backend between bindings.
- **High:** Windows packaging path/plugins may fail if old `PyQt6` paths remain.
- **Medium:** Generated UI code deltas may alter enum usage/constructor signatures.
- **Low-Medium:** Runtime dialog behavior edge cases (`exec` and modal flow).

## Rollback Plan

1. Keep migration in isolated branch until full validation passes.
2. If regressions appear, revert the migration branch or selectively revert:
   - dependency changes,
   - generated UI regeneration,
   - runtime import changes,
   - workflow packaging changes.
3. Re-run baseline smoke checks after rollback to confirm restored behavior.

## Suggested Execution Order (Concrete)

1. Baseline smoke checks and branch creation.
2. Dependency + lock update.
3. Regenerate all UI Python files with `pyside6-uic`.
4. Migrate runtime imports and fix binding-specific API mismatches.
5. Update Windows build packaging paths and PyInstaller behavior.
6. Run tests + manual GUI matrix.
7. Update docs/changelog and prepare PR.
