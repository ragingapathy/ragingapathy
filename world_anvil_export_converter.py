#!/usr/bin/env python3
"""
World Anvil Export Converter - Converts World Anvil exports to readable formats
Since the API requires an application key (not just user token), this tool works
with the built-in export feature that World Anvil provides to Guild members.
"""

import json
import zipfile
import os
from pathlib import Path
from typing import Dict, List
import html2text
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER


class WorldAnvilExportConverter:
    """Convert World Anvil export files to various formats"""

    def __init__(self, export_file: str, output_dir: str = "world_anvil_converted"):
        """
        Initialize the converter.

        Args:
            export_file: Path to the World Anvil export ZIP file
            output_dir: Directory to save converted files
        """
        self.export_file = Path(export_file)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir = self.output_dir / "temp"
        self.temp_dir.mkdir(exist_ok=True)

    def extract_export(self):
        """Extract the World Anvil export ZIP file"""
        print(f"Extracting {self.export_file}...")
        with zipfile.ZipFile(self.export_file, 'r') as zip_ref:
            zip_ref.extractall(self.temp_dir)
        print("✓ Extraction complete")

    def find_json_files(self) -> List[Path]:
        """Find all JSON files in the extracted export"""
        json_files = list(self.temp_dir.rglob("*.json"))
        print(f"✓ Found {len(json_files)} JSON files")
        return json_files

    def convert_to_markdown(self, article: Dict, output_path: Path):
        """
        Convert an article to Markdown format.

        Args:
            article: Article data dictionary
            output_path: Output file path
        """
        # Build markdown content
        md_content = f"# {article.get('title', 'Untitled')}\n\n"

        if article.get('subtitle'):
            md_content += f"*{article['subtitle']}*\n\n"

        # Handle content - might be HTML
        if article.get('content'):
            h = html2text.HTML2Text()
            h.ignore_links = False
            h.body_width = 0
            try:
                content_text = h.handle(article['content'])
                md_content += f"{content_text}\n\n"
            except:
                md_content += f"{article['content']}\n\n"

        # Add metadata
        md_content += "---\n\n"
        md_content += "## Metadata\n\n"

        if article.get('tags'):
            tags = article['tags'] if isinstance(article['tags'], list) else [article['tags']]
            md_content += f"**Tags:** {', '.join(tags)}\n\n"

        if article.get('state'):
            md_content += f"**State:** {article['state']}\n\n"

        if article.get('created_at'):
            md_content += f"**Created:** {article['created_at']}\n\n"

        if article.get('updated_at'):
            md_content += f"**Updated:** {article['updated_at']}\n\n"

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

    def convert_to_pdf(self, article: Dict, output_path: Path):
        """
        Convert an article to PDF format.

        Args:
            article: Article data dictionary
            output_path: Output file path
        """
        # Create PDF document
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )

        elements = []
        styles = getSampleStyleSheet()

        # Custom styles
        title_style = ParagraphStyle(
            name='CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor='#2c3e50',
            spaceAfter=12,
            alignment=TA_CENTER
        )

        # Add title
        title = article.get('title', 'Untitled')
        elements.append(Paragraph(title, title_style))
        elements.append(Spacer(1, 0.2 * inch))

        # Add subtitle if exists
        if article.get('subtitle'):
            subtitle_style = ParagraphStyle(
                name='Subtitle',
                parent=styles['Heading2'],
                fontSize=14,
                textColor='#7f8c8d',
                alignment=TA_CENTER,
                fontName='Helvetica-Oblique'
            )
            elements.append(Paragraph(article['subtitle'], subtitle_style))
            elements.append(Spacer(1, 0.2 * inch))

        # Add content
        if article.get('content'):
            h = html2text.HTML2Text()
            h.ignore_links = False
            h.body_width = 0

            try:
                content_text = h.handle(article['content'])
            except:
                content_text = article['content']

            # Split into paragraphs
            paragraphs = content_text.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    para = para.replace('\n', ' ').strip()
                    if para:
                        try:
                            elements.append(Paragraph(para, styles['BodyText']))
                            elements.append(Spacer(1, 0.15 * inch))
                        except:
                            # Skip paragraphs that cause issues
                            pass

        # Build PDF
        try:
            doc.build(elements)
        except Exception as e:
            print(f"  Warning: PDF creation had issues: {e}")

    def process_export(self):
        """Process the entire export"""
        # Extract the ZIP
        self.extract_export()

        # Find all JSON files
        json_files = self.find_json_files()

        print(f"\nConverting {len(json_files)} articles...")
        print("-" * 60)

        converted_count = 0
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    article = json.load(f)

                # Get article title for filename
                title = article.get('title', 'untitled')
                safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
                safe_title = safe_title[:50]  # Limit length

                # Create output files
                md_path = self.output_dir / f"{safe_title}.md"
                pdf_path = self.output_dir / f"{safe_title}.pdf"

                print(f"Converting: {title}")

                # Convert to Markdown
                self.convert_to_markdown(article, md_path)
                print(f"  ✓ Markdown: {md_path}")

                # Convert to PDF
                self.convert_to_pdf(article, pdf_path)
                print(f"  ✓ PDF: {pdf_path}")

                converted_count += 1

            except Exception as e:
                print(f"  ✗ Error converting {json_file.name}: {e}")

        print()
        print("=" * 60)
        print(f"✓ Converted {converted_count}/{len(json_files)} articles")
        print(f"✓ Output saved to: {self.output_dir}")


def main():
    """Main function"""
    print("World Anvil Export Converter")
    print("=" * 60)
    print()
    print("This tool converts World Anvil export files to Markdown and PDF.")
    print()
    print("HOW TO USE:")
    print("1. Go to World Anvil and export your world:")
    print("   https://www.worldanvil.com/your-worlds")
    print("2. Download the export ZIP file")
    print("3. Run this script with the ZIP file path")
    print()

    # Check for export file
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 world_anvil_export_converter.py <export_file.zip>")
        print()
        print("Example:")
        print("  python3 world_anvil_export_converter.py my_world_export.zip")
        return

    export_file = sys.argv[1]

    if not os.path.exists(export_file):
        print(f"✗ Error: File not found: {export_file}")
        return

    # Process the export
    converter = WorldAnvilExportConverter(export_file)
    converter.process_export()


if __name__ == "__main__":
    main()
