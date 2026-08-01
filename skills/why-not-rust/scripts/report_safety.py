#!/usr/bin/env python3
"""Escaping helpers for self-contained why-not-rust HTML reports."""

from __future__ import annotations

import html
import json
from typing import Any
from urllib.parse import urlsplit


def html_text(value: object) -> str:
    """Escape untrusted text for an HTML text or quoted-attribute context."""
    return html.escape(str(value), quote=True)


def safe_href(value: str) -> str:
    """Return an escaped absolute HTTP(S) URL; reject executable/relative schemes."""
    parsed = urlsplit(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("report links must be absolute http:// or https:// URLs")
    return html_text(value)


def json_for_html(value: Any) -> str:
    """Serialize strict JSON that cannot terminate an HTML script-data block."""
    rendered = json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)
    return (
        rendered.replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )
