"""Text and paragraph formatting helpers."""

from __future__ import annotations

from .utils import escape_markdown


def _is_bullet_paragraph(paragraph) -> bool:
    p_pr = paragraph._p.pPr  # pylint: disable=protected-access
    if p_pr is None:
        return False

    for child in p_pr.iterchildren():
        if child.tag.endswith("}buChar") or child.tag.endswith("}buAutoNum"):
            return True
    return False


def format_run_text(run) -> str:
    text = escape_markdown(run.text or "")
    if not text:
        return ""

    if run.font.bold:
        text = f"**{text}**"
    if run.font.italic:
        text = f"*{text}*"
    if run.font.underline:
        text = f"<u>{text}</u>"

    return text


def format_paragraph(paragraph) -> str:
    raw = paragraph.text or ""
    if not raw.strip():
        return ""

    body = "".join(format_run_text(run) for run in paragraph.runs) or escape_markdown(raw.strip())
    level = int(getattr(paragraph, "level", 0) or 0)

    if _is_bullet_paragraph(paragraph):
        indent = "  " * max(level, 0)
        return f"{indent}- {body.strip()}"

    return body.strip()
