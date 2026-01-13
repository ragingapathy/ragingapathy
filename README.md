# World Anvil Scraper

A Python tool to fetch and export your World Anvil worldbuilding data using the official World Anvil API.

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

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Get your API token from: https://www.worldanvil.com/api/auth/key

3. Set your API token as an environment variable:
```bash
export WORLD_ANVIL_TOKEN='your_token_here'
```

## Usage

Run the scraper:
```bash
python world_anvil_scraper.py
```

The tool will:
1. Connect to the World Anvil API
2. Fetch all your worlds
3. Download all articles from each world
4. Export data to JSON, Markdown, and PDF formats

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
