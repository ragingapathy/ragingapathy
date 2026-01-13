# World Anvil Data Export Guide

## The API Issue

The World Anvil API requires **two** authentication keys:
1. **User Auth Token** (you have this) ✓
2. **Application Key** (requires applying to World Anvil) ✗

Unfortunately, to get an Application Key, you need to:
- Be a Grandmaster+ Guild member
- Fill out an application form to create an official app

## Alternative Solution: Use World Anvil's Built-in Export

Since you have a Guild membership, you can use World Anvil's built-in export feature!

### Step-by-Step Guide:

#### 1. Export Your World from World Anvil

1. Log in to World Anvil
2. Go to: https://www.worldanvil.com/your-worlds
3. Find your world
4. Click on the world settings/options
5. Look for "Export World" or similar option
6. Download the export ZIP file
7. Save it somewhere easy to find (like your Downloads folder)

#### 2. Convert the Export to Readable Formats

Run the converter script I created:

```bash
python3 world_anvil_export_converter.py ~/Downloads/your_world_export.zip
```

Replace `~/Downloads/your_world_export.zip` with the actual path to your downloaded file.

#### 3. Find Your Converted Files

Look in the `world_anvil_converted/` directory. You'll find:
- `.md` files (Markdown - great for Obsidian, reading in text editors)
- `.pdf` files (PDF - readable on any device, great for mobile)

## What Gets Exported

The World Anvil export includes:
- All your articles
- Metadata (tags, creation dates, etc.)
- Content (converted from HTML to readable text)

## Benefits of This Method

✅ **Works without Application Key** - Just use your Guild membership
✅ **Official Feature** - Supported by World Anvil
✅ **Complete Data** - Gets everything from your world
✅ **Offline Forever** - Once exported, it's yours

## Need the API Method?

If you really need real-time API access, you have two options:

### Option 1: Apply for Application Key
1. Make sure you're a Grandmaster+ Guild member
2. Contact World Anvil support or check their documentation for the application form
3. Explain your use case (personal mobile app, backup tool, etc.)

### Option 2: Use Community Tools
Check out existing tools that might already have Application Keys:
- [pywaclient](https://pypi.org/project/pywaclient/) - Python World Anvil client
- [World Anvil API Python Client](https://gitlab.com/SoulLink/world-anvil-api-client) - GitLab project

## Questions?

- **How often can I export?** Guild members can export daily (depending on membership level)
- **Does this violate ToS?** No! It's an official feature
- **Can I automate this?** Yes, but you'd need to manually download the export each time (or look into the API with proper keys)

---

**Sources:**
- [World Anvil API Documentation - v.2 (Boromir)](https://www.worldanvil.com/api/external/boromir/documentation)
- [User API Tokens | World Anvil](https://www.worldanvil.com/api/auth/key)
- [pywaclient · PyPI](https://pypi.org/project/pywaclient/)
