"""Slide to markdown conversion logic."""

from __future__ import annotations

from .text_formatter import format_paragraph
from .utils import escape_markdown


class SlideProcessor:
    """Convert one slide into Marp-friendly markdown."""

    def __init__(self, image_extractor):
        self.image_extractor = image_extractor

    def process_slide(self, slide, slide_index: int) -> str:
        lines = []
        title_shape = getattr(slide.shapes, "title", None)

        if title_shape is not None and getattr(title_shape, "text", "").strip():
            title = escape_markdown(title_shape.text.strip())
            lines.append(f"# {title}")
            lines.append("")

        image_count = 0
        for shape in slide.shapes:
            if title_shape is not None and shape == title_shape:
                continue

            if getattr(shape, "shape_type", None) == 13:
                next_image_index = image_count + 1
                image_path = self.image_extractor.save_picture(shape, slide_index, next_image_index)
                if image_path:
                    image_count = next_image_index
                    lines.append(f"![slide-{slide_index}-image-{image_count}]({image_path})")
                    lines.append("")
                continue

            if getattr(shape, "has_text_frame", False):
                for paragraph in shape.text_frame.paragraphs:
                    paragraph_md = format_paragraph(paragraph)
                    if paragraph_md:
                        lines.append(paragraph_md)
                if lines and lines[-1] != "":
                    lines.append("")

            if getattr(shape, "has_table", False):
                lines.extend(self._format_table(shape.table))
                lines.append("")

        while lines and lines[-1] == "":
            lines.pop()

        if not lines:
            return "<!-- empty slide -->"

        return "\n".join(lines)

    def _format_table(self, table) -> list[str]:
        rows = []
        for row in table.rows:
            cells = []
            for cell in row.cells:
                text = " ".join(cell.text.split())
                cells.append(escape_markdown(text))
            rows.append(cells)

        if not rows:
            return []

        header = rows[0]
        divider = ["---"] * len(header)
        lines = [
            "| " + " | ".join(header) + " |",
            "| " + " | ".join(divider) + " |",
        ]

        for row in rows[1:]:
            if len(row) < len(header):
                row += [""] * (len(header) - len(row))
            elif len(row) > len(header):
                row = row[: len(header)]
            lines.append("| " + " | ".join(row) + " |")

        return lines
