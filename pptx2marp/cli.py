"""Command line interface for PPTX to Marp markdown converter."""

from __future__ import annotations

import argparse
import logging
import os
import sys
from glob import glob
from pathlib import Path

from .converter import PptxToMarpConverter

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Convert PPTX files to Marp markdown format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example usage:
  %(prog)s input.pptx                     # Output to stdout
  %(prog)s input.pptx -o output.md        # Output to file
  %(prog)s *.pptx -o output_dir/          # Batch conversion
        """,
    )

    parser.add_argument(
        "input_files",
        nargs="+",
        help="Input PowerPoint file paths (.pptx; supports wildcards)",
    )
    parser.add_argument("-o", "--output", help="Output file or directory path")
    parser.add_argument("-t", "--title", help="Override Marp frontmatter title")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show verbose logs")

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    converter = PptxToMarpConverter()

    try:
        for input_pattern in args.input_files:
            matching_files = glob(input_pattern)
            if not matching_files:
                logger.warning("No matching files found: %s", input_pattern)
                continue

            for file_path in matching_files:
                if not file_path.lower().endswith(".pptx"):
                    logger.warning("Skipping non-PPTX file: %s", file_path)
                    continue

                output_path = None
                if args.output:
                    if os.path.isdir(args.output) or args.output.endswith("/"):
                        output_path = os.path.join(args.output, f"{Path(file_path).stem}.md")
                    else:
                        output_path = args.output

                markdown_content = converter.convert_file(
                    file_path,
                    output_path=output_path,
                    title=args.title,
                )

                if not output_path:
                    print(f"\n=== {file_path} ===\n")
                    print(markdown_content)
    except KeyboardInterrupt:
        logger.info("Conversion interrupted by user")
        sys.exit(1)
    except Exception as exc:  # pylint: disable=broad-except
        logger.error("Program execution failed: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
