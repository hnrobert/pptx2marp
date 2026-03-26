"""Image extraction for slide pictures."""

from __future__ import annotations

import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


class ImageExtractor:
    """Extract image blobs from picture shapes into an assets directory."""

    def __init__(self, assets_dir: str):
        self.assets_dir = assets_dir

    def save_picture(self, shape, slide_index: int, image_index: int) -> str:
        """Persist a picture shape and return markdown-relative path.

        Returns an empty string when the picture has no embedded blob
        (for example linked images in some exported PPTX files).
        """
        try:
            image = shape.image
        except Exception as exc:  # pylint: disable=broad-except
            logger.warning(
                "Skipping picture on slide %s (index %s): %s",
                slide_index,
                image_index,
                exc,
            )
            return ""

        ext = image.ext or "png"
        filename = f"slide{slide_index:03d}_img{image_index:02d}.{ext}"

        os.makedirs(self.assets_dir, exist_ok=True)
        output_path = Path(self.assets_dir) / filename
        output_path.write_bytes(image.blob)

        return f"assets/{filename}"
