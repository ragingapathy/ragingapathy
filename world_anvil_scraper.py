#!/usr/bin/env python3
"""
World Anvil Scraper - A tool to fetch and export your World Anvil data
"""

import requests
import json
import os
from typing import Dict, List, Optional
from pathlib import Path
import html2text
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER


class WorldAnvilAPI:
    """Client for interacting with the World Anvil API (Boromir v2)"""

    BASE_URL = "https://www.worldanvil.com/api/external/boromir"

    def __init__(self, api_token: str):
        """
        Initialize the World Anvil API client.

        Args:
            api_token: Your World Anvil API token
        """
        self.api_token = api_token
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'x-auth-token': self.api_token
        })

    def _make_request(self, endpoint: str, method: str = 'GET', params: Optional[Dict] = None) -> Dict:
        """
        Make a request to the World Anvil API.

        Args:
            endpoint: API endpoint (without base URL)
            method: HTTP method (GET, POST, etc.)
            params: Query parameters

        Returns:
            JSON response as dictionary
        """
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"

        try:
            if method == 'GET':
                response = self.session.get(url, params=params)
            elif method == 'POST':
                response = self.session.post(url, json=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            print(f"Response: {response.text}")
            raise
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            raise

    def test_connection(self) -> bool:
        """
        Test the API connection and authentication.

        Returns:
            True if connection is successful, False otherwise
        """
        try:
            # Try to fetch user info or worlds list
            result = self._make_request('user')
            print("✓ API connection successful!")
            print(f"User data: {json.dumps(result, indent=2)}")
            return True
        except Exception as e:
            print(f"✗ API connection failed: {e}")
            return False

    def get_worlds(self) -> List[Dict]:
        """
        Fetch all worlds accessible to the user.

        Returns:
            List of world objects
        """
        return self._make_request('worlds')

    def get_world(self, world_id: str) -> Dict:
        """
        Fetch details for a specific world.

        Args:
            world_id: The ID of the world

        Returns:
            World object with details
        """
        return self._make_request(f'world/{world_id}')

    def get_articles(self, world_id: str) -> List[Dict]:
        """
        Fetch all articles from a specific world.

        Args:
            world_id: The ID of the world

        Returns:
            List of article objects
        """
        return self._make_request(f'world/{world_id}/articles')

    def get_article(self, article_id: str) -> Dict:
        """
        Fetch a specific article.

        Args:
            article_id: The ID of the article

        Returns:
            Article object with full content
        """
        return self._make_request(f'article/{article_id}')


class WorldAnvilExporter:
    """Export World Anvil data to various formats"""

    def __init__(self, output_dir: str = "world_anvil_export"):
        """
        Initialize the exporter.

        Args:
            output_dir: Directory to save exported data
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def export_to_json(self, data: Dict, filename: str):
        """
        Export data to JSON file.

        Args:
            data: Data to export
            filename: Output filename
        """
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✓ Exported to {output_path}")

    def export_to_markdown(self, article: Dict, filename: str):
        """
        Export an article to Markdown format.

        Args:
            article: Article data
            filename: Output filename
        """
        output_path = self.output_dir / filename

        # Build markdown content
        md_content = f"# {article.get('title', 'Untitled')}\n\n"

        if article.get('subtitle'):
            md_content += f"*{article['subtitle']}*\n\n"

        if article.get('content'):
            md_content += f"{article['content']}\n\n"

        # Add metadata
        md_content += "---\n\n"
        md_content += "## Metadata\n\n"

        if article.get('tags'):
            md_content += f"**Tags:** {', '.join(article['tags'])}\n\n"

        if article.get('created_at'):
            md_content += f"**Created:** {article['created_at']}\n\n"

        if article.get('updated_at'):
            md_content += f"**Updated:** {article['updated_at']}\n\n"

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

        print(f"✓ Exported to {output_path}")

    def export_to_pdf(self, article: Dict, filename: str):
        """
        Export an article to PDF format.

        Args:
            article: Article data
            filename: Output filename
        """
        output_path = self.output_dir / filename

        # Create PDF document
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )

        # Container for the 'Flowable' objects
        elements = []

        # Define styles
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name='Justify',
            parent=styles['BodyText'],
            alignment=TA_JUSTIFY,
            fontSize=11,
            leading=14
        ))

        title_style = ParagraphStyle(
            name='CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor='#2c3e50',
            spaceAfter=12,
            alignment=TA_CENTER
        )

        subtitle_style = ParagraphStyle(
            name='CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=14,
            textColor='#7f8c8d',
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Oblique'
        )

        # Add title
        title = article.get('title', 'Untitled')
        elements.append(Paragraph(title, title_style))
        elements.append(Spacer(1, 0.2 * inch))

        # Add subtitle if exists
        if article.get('subtitle'):
            elements.append(Paragraph(article['subtitle'], subtitle_style))
            elements.append(Spacer(1, 0.2 * inch))

        # Add content
        if article.get('content'):
            # Convert HTML to plain text if needed
            h = html2text.HTML2Text()
            h.ignore_links = False
            h.ignore_images = False
            h.body_width = 0  # Don't wrap text

            content = article['content']

            # Try to convert HTML to text while preserving some formatting
            try:
                content_text = h.handle(content)
            except:
                content_text = content

            # Split into paragraphs and add to PDF
            paragraphs = content_text.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    # Clean up the text
                    para = para.replace('\n', ' ').strip()
                    if para:
                        elements.append(Paragraph(para, styles['Justify']))
                        elements.append(Spacer(1, 0.15 * inch))

        # Add metadata section
        elements.append(Spacer(1, 0.3 * inch))
        elements.append(Paragraph("Metadata", styles['Heading2']))
        elements.append(Spacer(1, 0.1 * inch))

        metadata_style = styles['Normal']

        if article.get('tags') and isinstance(article['tags'], list):
            tags_text = f"<b>Tags:</b> {', '.join(article['tags'])}"
            elements.append(Paragraph(tags_text, metadata_style))
            elements.append(Spacer(1, 0.05 * inch))

        if article.get('created_at'):
            created_text = f"<b>Created:</b> {article['created_at']}"
            elements.append(Paragraph(created_text, metadata_style))
            elements.append(Spacer(1, 0.05 * inch))

        if article.get('updated_at'):
            updated_text = f"<b>Updated:</b> {article['updated_at']}"
            elements.append(Paragraph(updated_text, metadata_style))

        # Build PDF
        try:
            doc.build(elements)
            print(f"✓ Exported to {output_path}")
        except Exception as e:
            print(f"✗ Error creating PDF: {e}")


def main():
    """Main function to run the scraper"""

    # Load API token from environment variable or config
    api_token = os.environ.get('WORLD_ANVIL_TOKEN')

    if not api_token:
        print("Please set the WORLD_ANVIL_TOKEN environment variable")
        print("Example: export WORLD_ANVIL_TOKEN='your_token_here'")
        return

    print("World Anvil Scraper")
    print("=" * 50)
    print()

    # Initialize API client
    api = WorldAnvilAPI(api_token)

    # Test connection
    print("Testing API connection...")
    if not api.test_connection():
        return

    print()

    # Fetch worlds
    print("Fetching your worlds...")
    try:
        worlds = api.get_worlds()
        print(f"✓ Found {len(worlds)} world(s)")
        print()

        # Initialize exporter
        exporter = WorldAnvilExporter()

        # Export worlds list
        exporter.export_to_json(worlds, "worlds.json")

        # For each world, fetch and export articles
        for world in worlds:
            world_id = world.get('id')
            world_name = world.get('title', 'Unknown')

            print(f"\nProcessing world: {world_name} (ID: {world_id})")
            print("-" * 50)

            # Fetch world details
            world_details = api.get_world(world_id)
            exporter.export_to_json(world_details, f"world_{world_id}.json")

            # Fetch articles
            print("Fetching articles...")
            articles = api.get_articles(world_id)
            print(f"✓ Found {len(articles)} article(s)")

            # Create directory for this world
            world_dir = exporter.output_dir / f"world_{world_id}"
            world_dir.mkdir(exist_ok=True)

            # Fetch and export each article
            for i, article_summary in enumerate(articles):
                article_id = article_summary.get('id')
                article_title = article_summary.get('title', 'Untitled')

                print(f"  [{i+1}/{len(articles)}] Fetching: {article_title}")

                try:
                    article = api.get_article(article_id)

                    # Export to JSON
                    json_filename = f"article_{article_id}.json"
                    with open(world_dir / json_filename, 'w', encoding='utf-8') as f:
                        json.dump(article, f, indent=2, ensure_ascii=False)

                    # Export to Markdown
                    md_filename = f"{article_id}_{article_title[:50].replace('/', '_')}.md"
                    exporter.export_to_markdown(article, world_dir / md_filename)

                    # Export to PDF
                    pdf_filename = f"{article_id}_{article_title[:50].replace('/', '_')}.pdf"
                    exporter.export_to_pdf(article, world_dir / pdf_filename)

                except Exception as e:
                    print(f"    ✗ Error fetching article {article_id}: {e}")

        print()
        print("=" * 50)
        print(f"✓ Export complete! Data saved to: {exporter.output_dir}")

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
