# Ableton Track Renamer

Strips auto-numbered prefixes from Ableton Live track names using PyLive and AbletonOSC.

Ableton replaces `#` in track names with the track's position number (e.g. `# 04_DRUMS` becomes `3 04_DRUMS`). This script detects that pattern and renames the tracks back.

---

## Setup Guide

Follow these steps in order. Each step must be completed before moving to the next.

### Step 1 — Install Homebrew

Homebrew is a package manager for macOS that makes installing developer tools easy.

Open **Terminal** (press `Cmd + Space`, type "Terminal", press Enter) and paste this command:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Follow the on-screen prompts. When it finishes, close and reopen Terminal.

> If you already have Homebrew, skip this step.

### Step 2 — Install Python

```bash
brew install python
```

Verify it worked:

```bash
python3 --version
```

You should see something like `Python 3.x.x`.

### Step 3 — Install uv

`uv` is a fast Python project manager that handles dependencies for this project.

```bash
brew install uv
```

Verify it worked:

```bash
uv --version
```

### Step 4 — Install AbletonOSC

AbletonOSC lets this script communicate with Ableton Live.

1. Download the latest release from [AbletonOSC on GitHub](https://github.com/ideoforms/AbletonOSC/releases)
2. Unzip the downloaded file
3. Copy the `AbletonOSC` folder to your Ableton User Library Remote Scripts folder:
   - **macOS**: `~/Music/Ableton/User Library/Remote Scripts/`

   To open this folder quickly, press `Cmd + Space`, type "Finder", press Enter, then in the menu bar choose **Go > Go to Folder...** and paste the path above.

4. Open **Ableton Live**
5. Go to **Live > Settings** (or press `Cmd + ,`)
6. Click the **Link / Tempo / MIDI** tab
7. In the **Control Surface** dropdown, select **AbletonOSC**
8. At the bottom of the screen you should see: `AbletonOSC: Listening for OSC on port 11000`

### Step 5 — Install Git

Git is used to download this project and keep it up to date.

```bash
brew install git
```

Verify it worked:

```bash
git --version
```

You should see something like `git version 2.x.x`.

> If you already have git, skip this step.

### Step 6 — Download This Project

```bash
git clone https://github.com/CraftBrewzMusic/AbletonAutomations.git
cd AbletonAutomations
```

Or download the ZIP from GitHub: click the green **Code** button on the repo page, then **Download ZIP**. Unzip it and open Terminal in that folder.

### Step 7 — Install Project Dependencies

From inside the project folder, run:

```bash
uv sync
```

This installs all required Python packages automatically.

---

## Usage

Make sure Ableton Live is open with a project loaded before running these commands.

```bash
# Preview what would be renamed (no changes applied)
uv run python rename_tracks.py --dry-run

# Rename tracks
uv run python rename_tracks.py

# Show help
uv run python rename_tracks.py --help
```
