# Usage Examples

## Basic Usage

### Export All Worlds

```bash
export WORLD_ANVIL_TOKEN='your_token_here'
python world_anvil_scraper.py
```

This will export all your worlds with all articles in JSON, Markdown, and PDF formats.

## Advanced Usage

### Custom Script: Export Only Specific World

Create a file `export_specific_world.py`:

```python
#!/usr/bin/env python3
from world_anvil_scraper import WorldAnvilAPI, WorldAnvilExporter
import os

# Your API token
API_TOKEN = os.environ.get('WORLD_ANVIL_TOKEN')

# Initialize
api = WorldAnvilAPI(API_TOKEN)
exporter = WorldAnvilExporter(output_dir="my_custom_export")

# Get all worlds
worlds = api.get_worlds()

# Find specific world by name
target_world_name = "My Campaign World"
target_world = next((w for w in worlds if w['title'] == target_world_name), None)

if target_world:
    world_id = target_world['id']
    print(f"Exporting: {target_world_name}")

    # Get articles
    articles = api.get_articles(world_id)

    # Export each article
    for article_summary in articles:
        article = api.get_article(article_summary['id'])
        exporter.export_to_pdf(article, f"{article['title']}.pdf")
else:
    print(f"World '{target_world_name}' not found")
```

### Export Only PDFs (Skip JSON/Markdown)

Modify the main loop in `world_anvil_scraper.py`:

```python
# Replace the export section with:
for i, article_summary in enumerate(articles):
    article_id = article_summary.get('id')
    article_title = article_summary.get('title', 'Untitled')

    print(f"  [{i+1}/{len(articles)}] Fetching: {article_title}")

    try:
        article = api.get_article(article_id)

        # Only export to PDF
        pdf_filename = f"{article_id}_{article_title[:50].replace('/', '_')}.pdf"
        exporter.export_to_pdf(article, world_dir / pdf_filename)
    except Exception as e:
        print(f"    ✗ Error: {e}")
```

### Export with Progress Bar

Install tqdm: `pip install tqdm`

Then modify the scraper:

```python
from tqdm import tqdm

# In the article loop, replace:
for i, article_summary in enumerate(articles):

# With:
for article_summary in tqdm(articles, desc="Exporting articles"):
```

### Create a Combined PDF for Each World

Create a file `export_combined_pdf.py`:

```python
#!/usr/bin/env python3
from world_anvil_scraper import WorldAnvilAPI
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

API_TOKEN = os.environ.get('WORLD_ANVIL_TOKEN')
api = WorldAnvilAPI(API_TOKEN)

worlds = api.get_worlds()

for world in worlds:
    world_id = world['id']
    world_name = world['title']

    print(f"Creating combined PDF for: {world_name}")

    # Create PDF
    pdf_path = f"{world_name}_complete.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Add world title
    elements.append(Paragraph(world_name, styles['Title']))
    elements.append(PageBreak())

    # Get and add all articles
    articles = api.get_articles(world_id)

    for article_summary in articles:
        article = api.get_article(article_summary['id'])

        # Add article title
        elements.append(Paragraph(article['title'], styles['Heading1']))
        elements.append(Spacer(1, 12))

        # Add article content
        if article.get('content'):
            elements.append(Paragraph(article['content'], styles['BodyText']))

        elements.append(PageBreak())

    # Build PDF
    doc.build(elements)
    print(f"✓ Created: {pdf_path}")
```

### Export Articles by Category/Tag

```python
#!/usr/bin/env python3
from world_anvil_scraper import WorldAnvilAPI, WorldAnvilExporter
import os

API_TOKEN = os.environ.get('WORLD_ANVIL_TOKEN')
api = WorldAnvilAPI(API_TOKEN)
exporter = WorldAnvilExporter()

# Target tag
TARGET_TAG = "Characters"

worlds = api.get_worlds()

for world in worlds:
    articles = api.get_articles(world['id'])

    for article_summary in articles:
        article = api.get_article(article_summary['id'])

        # Check if article has the target tag
        if article.get('tags') and TARGET_TAG in article['tags']:
            print(f"Exporting: {article['title']}")
            exporter.export_to_pdf(article, f"{article['title']}.pdf")
```

### Schedule Regular Backups (Linux/Mac)

Create a cron job to backup daily at 2 AM:

```bash
# Edit crontab
crontab -e

# Add this line:
0 2 * * * cd /path/to/ragingapathy && /usr/bin/python3 world_anvil_scraper.py
```

### Schedule Regular Backups (Windows)

Use Task Scheduler:

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., Daily at 2 AM)
4. Action: Start a program
5. Program: `python`
6. Arguments: `C:\path\to\world_anvil_scraper.py`
7. Set environment variable in batch file wrapper

## Integration Examples

### Import to Obsidian

1. Export to Markdown
2. Copy `world_anvil_export/world_*/` folders to your Obsidian vault
3. Use Obsidian's link features to connect articles

### Import to Notion

1. Export to Markdown
2. In Notion, use Import > Markdown
3. Select all .md files from export directory

### Create Static Website

Use a static site generator (e.g., Hugo, Jekyll):

1. Export to Markdown
2. Place files in content directory
3. Generate site

### Analyze Your Worldbuilding Stats

```python
#!/usr/bin/env python3
from world_anvil_scraper import WorldAnvilAPI
import os
from collections import Counter

API_TOKEN = os.environ.get('WORLD_ANVIL_TOKEN')
api = WorldAnvilAPI(API_TOKEN)

worlds = api.get_worlds()

for world in worlds:
    print(f"\nStatistics for: {world['title']}")
    print("-" * 50)

    articles = api.get_articles(world['id'])
    print(f"Total Articles: {len(articles)}")

    # Count word total
    total_words = 0
    all_tags = []

    for article_summary in articles:
        article = api.get_article(article_summary['id'])
        if article.get('content'):
            total_words += len(article['content'].split())
        if article.get('tags'):
            all_tags.extend(article['tags'])

    print(f"Total Words: {total_words:,}")
    print(f"Average Words per Article: {total_words // len(articles) if articles else 0}")

    # Most common tags
    tag_counts = Counter(all_tags)
    print(f"\nTop 5 Tags:")
    for tag, count in tag_counts.most_common(5):
        print(f"  - {tag}: {count}")
```

## Tips and Tricks

### Rate Limiting

If you have many articles, add delays to avoid rate limiting:

```python
import time

# In your article loop:
for article_summary in articles:
    # ... fetch and export ...
    time.sleep(1)  # Wait 1 second between requests
```

### Retry Failed Downloads

```python
import time

max_retries = 3
for article_summary in articles:
    for attempt in range(max_retries):
        try:
            article = api.get_article(article_summary['id'])
            # ... export ...
            break
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Retry {attempt + 1}/{max_retries}")
                time.sleep(2)
            else:
                print(f"Failed after {max_retries} attempts: {e}")
```

### Custom PDF Styling

Modify the `export_to_pdf` method to customize colors, fonts, margins, etc.:

```python
# In world_anvil_scraper.py, modify the ParagraphStyle:
title_style = ParagraphStyle(
    name='CustomTitle',
    parent=styles['Heading1'],
    fontSize=28,                    # Larger title
    textColor='#8B0000',           # Dark red
    spaceAfter=20,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)
```
