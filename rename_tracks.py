"""
Rename Ableton Live tracks by stripping auto-numbered prefixes.

Ableton replaces '#' in track names with the track's position number,
turning '# 04_DRUMS' into something like '3 04_DRUMS'. This script
detects that pattern and renames tracks back to '# ...' form.

Requirements:
    - Ableton Live 11+ running
    - AbletonOSC installed and enabled in Live
      (Preferences > Link/Tempo/MIDI > Control Surface: AbletonOSC)
"""

import argparse
import re
import sys

import live
from pythonosc import udp_client

ABLETONOSC_INSTALL_HELP = """\
Could not connect to Ableton Live.

Make sure Ableton Live is running with AbletonOSC installed:

  1. Download AbletonOSC from https://github.com/ideoforms/AbletonOSC
  2. Copy the 'AbletonOSC' folder to:
       macOS:   ~/Music/Ableton/User Library/Remote Scripts/
       Windows: ~\\Documents\\Ableton\\User Library\\Remote Scripts\\
  3. Restart Ableton Live
  4. Go to Preferences > Link/Tempo/MIDI
  5. Set Control Surface to "AbletonOSC"
  6. You should see: "AbletonOSC: Listening for OSC on port 11000"
"""


def rename_track(osc_client: udp_client.SimpleUDPClient, track_index: int, name: str):
    """Rename a track using OSC (not exposed in PyLive API)."""
    osc_client.send_message("/live/track/set/name", [track_index, name])


def strip_track_number(name: str) -> str | None:
    """Remove the auto-numbered prefix that Ableton generates from '#' in track names.

    Ableton replaces '#' with the track's position number and spaces become
    dashes, so '#_D Stab' becomes '6-02_D Stab' via the API. This detects
    that pattern (number, dash, zero-padded index, underscore, rest) and
    returns '#' + '_rest', e.g. '#_D Stab'.
    """
    m = re.match(r"^\d+-\d+(_.*)", name)
    if m:
        return "#" + m.group(1)
    return None


def print_all_track_names(set: live.Set):
    """Print all track names, showing group hierarchy."""
    print("Current track names:")
    for track in set.tracks:
        if track is None:
            continue
        indent = "    " if track.group is not None else "  "
        label = " [GROUP]" if track.is_group else ""
        print(f"{indent}Track {track.index}{label}: '{track.name}'")


def main():
    parser = argparse.ArgumentParser(
        description="Strip auto-numbered prefixes from Ableton Live track names.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview renames without applying them.",
    )
    args = parser.parse_args()

    print("Connecting to Ableton Live...")

    try:
        set = live.Set()
        # Use network scan mode to work around a bug in PyLive 0.4.0's
        # _scan_via_file: when a Group track is encountered, the local variable
        # is named 'group' instead of 'track', so the subsequent clips/devices
        # code raises UnboundLocalError if any group has a device attached.
        # See: https://github.com/ideoforms/pylive/issues/42
        # Fix pending in: https://github.com/ideoforms/pylive/pull/43
        # The network scan avoids the bug by looking up tracks via index rather
        # than relying on the local variable. It is slightly slower but correct.
        set.scan(mode="network")
    except (ConnectionError, OSError) as e:
        print(ABLETONOSC_INSTALL_HELP, file=sys.stderr)
        print(f"(Error details: {e})", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(set.tracks)} tracks.")
    print_all_track_names(set)

    # Collect renames
    renames = []
    for track in set.tracks:
        new_name = strip_track_number(track.name)
        if new_name is not None:
            renames.append((track.index, track.name, new_name))

    if not renames:
        print("\nNo tracks need renaming.")
        return

    if args.dry_run:
        print("\n[DRY RUN] The following tracks would be renamed:")
        for i, old, new in renames:
            print(f"  Track {i}: '{old}' -> '{new}'")
        return

    print("\nRenaming tracks...")
    osc_client = udp_client.SimpleUDPClient("127.0.0.1", 11000)
    for i, old, new in renames:
        rename_track(osc_client, i, new)
        print(f"  Track {i}: '{old}' -> '{new}'")

    print("Done.")


if __name__ == "__main__":
    main()
