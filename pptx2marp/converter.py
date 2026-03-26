"""Core converter module for PPTX to Marp Markdown conversion."""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Optional

try:
    from pptx import Presentation  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover - dependency check is handled at runtime
    Presentation = None  # type: ignore[assignment]

from .image_extractor import ImageExtractor
from .slide_processor import SlideProcessor
from .utils import clean_markdown_content

logger = logging.getLogger(__name__)


class PptxToMarpConverter:
    """PPTX to Marp markdown converter."""

    def __init__(self):
        self.output_folder: str = ""
        self.assets_dir: str = ""

    def convert_file(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        title: Optional[str] = None,
    ) -> str:
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file does not exist: {input_path}")

        if not input_path.lower().endswith(".pptx"):
            raise ValueError(f"Only .pptx is supported: {input_path}")

        if Presentation is None:
            raise RuntimeError(
                "Missing required dependency 'python-pptx'. Please run: pip install python-pptx"
            )

        self._setup_output_structure(input_path, output_path)
        presentation = Presentation(input_path)
        image_extractor = ImageExtractor(self.assets_dir)
        slide_processor = SlideProcessor(image_extractor)

        output_lines = [
            "---",
            "marp: true",
            "theme: default",
            "paginate: true",
        ]
        if title:
            output_lines.append(f'title: "{title}"')
        output_lines.extend(["---", ""])

        for idx, slide in enumerate(presentation.slides, start=1):
            if idx > 1:
                output_lines.extend(["", "---", ""])
            output_lines.append(slide_processor.process_slide(slide, idx))

        markdown_content = clean_markdown_content(output_lines)
        final_output_path = self._get_final_output_path(input_path, output_path)
        self._write_output(markdown_content, final_output_path)
        self._cleanup_empty_assets_dir()

        logger.info("Conversion completed, output file: %s", final_output_path)
        return markdown_content

    def _setup_output_structure(self, input_path: str, output_path: Optional[str]):
        input_stem = Path(input_path).stem

        if output_path:
            if os.path.isdir(output_path) or output_path.endswith("/"):
                self.output_folder = os.path.join(output_path, input_stem)
            else:
                self.output_folder = os.path.dirname(output_path)
                if not self.output_folder:
                    self.output_folder = input_stem
        else:
            self.output_folder = input_stem

        os.makedirs(self.output_folder, exist_ok=True)
        self.assets_dir = os.path.join(self.output_folder, "assets")
        os.makedirs(self.assets_dir, exist_ok=True)

    def _get_final_output_path(self, input_path: str, output_path: Optional[str]) -> str:
        input_stem = Path(input_path).stem

        if output_path:
            if os.path.isdir(output_path) or output_path.endswith("/"):
                return os.path.join(self.output_folder, f"{input_stem}.md")
            return output_path

        return os.path.join(self.output_folder, f"{input_stem}.md")

    def _write_output(self, content: str, output_path: str):
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

    def _cleanup_empty_assets_dir(self):
        if self.assets_dir and os.path.exists(self.assets_dir) and not os.listdir(self.assets_dir):
            os.rmdir(self.assets_dir)
