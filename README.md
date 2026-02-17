# Ableton Track Renamer

Strips auto-numbered prefixes from Ableton Live track names using PyLive and AbletonOSC.

Ableton replaces `#` in track names with the track's position number (e.g. `# 04_DRUMS` becomes `3 04_DRUMS`). This script detects that pattern and renames the tracks back.

## Prerequisites

1. **Ableton Live 11+** installed and running
2. **AbletonOSC** control surface installed

## Installing AbletonOSC

1. Download [AbletonOSC](https://github.com/ideoforms/AbletonOSC)
2. Copy the `AbletonOSC` folder to:
   - **macOS**: `~/Music/Ableton/User Library/Remote Scripts/`
   - **Windows**: `~\Documents\Ableton\User Library\Remote Scripts\`
3. Restart Ableton Live
4. Go to **Preferences > Link/Tempo/MIDI**
5. Set **Control Surface** to "AbletonOSC"
6. You should see: "AbletonOSC: Listening for OSC on port 11000"

## Usage

```bash
# Preview what would be renamed (no changes applied)
uv run python rename_tracks.py --dry-run

# Rename tracks
uv run python rename_tracks.py

# Show help
uv run python rename_tracks.py --help
```
