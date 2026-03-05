# Project Notes

## Running Scripts

Always use `uv run python <script>` instead of `python <script>` directly.

Example:
```
uv run python rename_tracks.py --dry-run
```

## Known Issues

### PyLive bug: UnboundLocalError when groups have devices (issue #42)

PyLive 0.4.0 has a bug in `_scan_via_file` (the default scan mode on macOS): when a
Group track is processed, the object is stored in a local variable named `group` instead
of `track`. The clips/devices code that runs immediately after assumes `track` is always
set, so if the first or any group has a device attached (e.g., a group-level compressor),
the scan crashes with:

```
UnboundLocalError: local variable 'track' referenced before assignment
```

- Bug report: https://github.com/ideoforms/pylive/issues/42
- Fix pending (not yet merged): https://github.com/ideoforms/pylive/pull/43
  - The PR fix is trivial: rename the local variable from `group` to `track` in
    `_scan_via_file`. Three lines changed.

**Our approach:** We call `set.scan(mode="network")` instead of the default
`set.scan()`. The network scan mode looks up tracks by index from `self.tracks` rather
than relying on the local variable, so it is unaffected by the bug.

We considered two alternatives and rejected both:
1. **Patching the installed venv file** — works, but `uv sync` would silently overwrite
   the fix and reintroduce the bug.
2. **Falling back to network scan on error** — adds try/except complexity and still
   runs the broken file scan first.

The network scan is slightly slower (one OSC round-trip per track vs. a single JSON
file read), but the difference is imperceptible for typical set sizes. If PR #43 is ever
merged and we update the pylive dependency, we can remove the `mode="network"` argument
and this note.
