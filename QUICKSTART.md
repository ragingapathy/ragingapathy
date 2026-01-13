# Quick Start Guide

Get your World Anvil data exported in minutes!

## Prerequisites

- Python 3.7 or higher installed
- World Anvil Guild membership
- Your World Anvil API token

## Step-by-Step Setup

### 1. Install Dependencies

Open a terminal in this directory and run:

```bash
pip install -r requirements.txt
```

Or if you're using Python 3 specifically:

```bash
pip3 install -r requirements.txt
```

### 2. Get Your API Token

1. Log in to World Anvil
2. Go to: https://www.worldanvil.com/api/auth/key
3. Copy your API token (it should be a long string)

### 3. Set Your API Token

**Option A: Environment Variable (Recommended)**

On Linux/Mac:
```bash
export WORLD_ANVIL_TOKEN='your_token_here'
```

On Windows (Command Prompt):
```cmd
set WORLD_ANVIL_TOKEN=your_token_here
```

On Windows (PowerShell):
```powershell
$env:WORLD_ANVIL_TOKEN="your_token_here"
```

**Option B: Create a .env file**

Create a file named `.env` in this directory:
```
WORLD_ANVIL_TOKEN=your_token_here
```

Then modify `world_anvil_scraper.py` to load from .env:
```python
# Add at the top after imports:
from dotenv import load_dotenv
load_dotenv()
```

And install python-dotenv:
```bash
pip install python-dotenv
```

### 4. Run the Scraper

```bash
python world_anvil_scraper.py
```

Or:
```bash
python3 world_anvil_scraper.py
```

### 5. Find Your Exported Data

Check the `world_anvil_export/` directory. You'll find:

- `worlds.json` - List of all your worlds
- `world_<id>/` - Directories for each world containing:
  - JSON files with raw article data
  - Markdown files for easy reading
  - PDF files for offline viewing

## Troubleshooting

### "Please set the WORLD_ANVIL_TOKEN environment variable"

You forgot to set your API token. See Step 3 above.

### "HTTP Error 403"

Your API token might be incorrect or expired. Get a fresh token from:
https://www.worldanvil.com/api/auth/key

### "HTTP Error 401"

Authentication failed. Double-check:
1. Your token is correct (no extra spaces)
2. Your Guild membership is active
3. You're using the correct API endpoint

### "Connection Error"

Check your internet connection and try again.

## What's Next?

### View Your Content

- **Markdown**: Use any text editor, Obsidian, Notion, etc.
- **PDF**: Open with any PDF reader
- **JSON**: Parse programmatically or import into other tools

### Automate Regular Exports

Create a shell script (Linux/Mac) or batch file (Windows) to automate exports:

**backup_world_anvil.sh** (Linux/Mac):
```bash
#!/bin/bash
export WORLD_ANVIL_TOKEN='your_token_here'
python3 world_anvil_scraper.py
```

Make it executable: `chmod +x backup_world_anvil.sh`
Run it: `./backup_world_anvil.sh`

**backup_world_anvil.bat** (Windows):
```batch
@echo off
set WORLD_ANVIL_TOKEN=your_token_here
python world_anvil_scraper.py
pause
```

Run it: Double-click the file

### Customize the Export

Edit `world_anvil_scraper.py` to:
- Change export directory
- Skip certain export formats
- Filter specific worlds or articles
- Add custom formatting

## Need Help?

- Check the main README.md for detailed information
- Review the World Anvil API docs: https://www.worldanvil.com/api/external/boromir/documentation
- Check your API token page: https://www.worldanvil.com/api/auth/key

## Security Note

**NEVER** commit your API token to git! It's in the .gitignore file for your protection.
