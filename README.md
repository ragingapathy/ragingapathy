# World Anvil Data Exporter

Tools to export and convert your World Anvil worldbuilding data to portable formats (JSON, Markdown, PDF).

## ⚠️ Important: Two Methods Available

### Method 1: Export Converter (Recommended - Works Now!)
Use World Anvil's built-in export feature. **This works immediately with just your Guild membership.**

See: `EXPORT_METHOD.md` for detailed instructions.

### Method 2: Direct API Access (Requires Application Key)
Direct API access requires both a user token AND an application key from World Anvil.

## Features

- 🔐 Secure authentication using your World Anvil API token
- 🌍 Fetch all your worlds and their content
- 📝 Export articles to JSON, Markdown, and PDF formats
- 📄 Beautiful PDF exports with proper formatting
- 📱 Better data portability for your worldbuilding content
- 💾 Offline access to your worlds

## Requirements

- Python 3.7+
- World Anvil Guild membership (for API access)
- World Anvil API token

## Quick Start (Export Converter)

1. Install dependencies:
```bash
pip3 install -r requirements.txt
```

2. Export your world from World Anvil:
   - Go to https://www.worldanvil.com/your-worlds
   - Export your world (Guild feature)
   - Download the ZIP file

3. Convert the export:
```bash
python3 world_anvil_export_converter.py ~/Downloads/your_world_export.zip
```

4. Find your files in `world_anvil_converted/` directory!

## Alternative: Direct API Method

**Note:** Requires both user token AND application key from World Anvil.

1. Get your API token from: https://www.worldanvil.com/api/auth/key

2. Apply for an application key (Grandmaster+ Guild members)

3. Set your tokens:
```bash
export WORLD_ANVIL_TOKEN='your_token_here'
export WORLD_ANVIL_APP_KEY='your_app_key_here'
```

4. Run the scraper:
```bash
python3 world_anvil_scraper.py
```

## Output

Data is exported to the `world_anvil_export/` directory:

```
world_anvil_export/
├── worlds.json                    # List of all your worlds
├── world_{id}.json                # Details for each world
└── world_{id}/                    # Directory for each world
    ├── article_{id}.json          # Article data in JSON
    ├── {id}_{title}.md            # Article in Markdown format
    └── {id}_{title}.pdf           # Article in PDF format
```

## Use Cases

- **Better Mobile Reading**: Export to Markdown and use your favorite mobile reader
- **Offline Access**: Keep local copies of your worlds
- **Data Backup**: Regular backups of your worldbuilding content
- **Cross-Platform**: Use your worlds with other tools (Obsidian, Notion, etc.)
- **Custom Apps**: Build your own reader with better UX

## API Information

This tool uses the World Anvil API v.2 (Boromir):
- Documentation: https://www.worldanvil.com/api/external/boromir/documentation
- API Tokens: https://www.worldanvil.com/api/auth/key

## Legal & Usage

- This tool uses the official World Anvil API
- You must have a Guild membership to access the API
- You retain full ownership of your content
- Respect World Anvil's Terms of Service
- For personal use only (commercial use requires authorization from World Anvil)

## Troubleshooting

**403 Error**: Make sure your API token is correct and your Guild membership is active

**Connection Error**: Check your internet connection and World Anvil API status

**Missing Data**: Some content may be restricted based on your membership level

## Contributing

Feel free to submit issues or pull requests to improve this tool!

## License

MIT License - Use freely for your own worldbuilding needs
