# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Xiaohongshu (小红书/Red Note) signature reverse engineering project. The core achievement is a complete Python reimplementation of the `seccore_signv2` function (found in `vendor-dynamic.77f9fe85.js`) that generates the `x-s` request parameter, along with cookie management and the `x-s-common` parameter.

## Language

All responses and documentation should be in **Chinese (中文)**.

## Running

```bash
# Main crawler
python crawlers/one_text_crawlers.py

# Add real browser cookies
python crawlers/add_real_cookie.py

# Test cookie manager
python test_data/test_cookie_manager.py
```

No build step. Pure Python 3 with standard library + `requests`. No requirements.txt — dependencies are minimal (just `requests`).

## Architecture

### Data flow

```
Crawler (crawlers/one_text_crawlers.py)
  ├── RealisticXHSSignatureGenerator → generates x-s header
  ├── XHSCommonGenerator → generates x-s-common header
  └── Cookie Manager (real or simulated) → generates cookie string
      → Complete HTTP request to XHS API
```

### generators/ — Core signature and cookie logic

- `realistic_xhs_signature_generator.py` — **Primary generator**. Produces 328-char signatures with `XYS_` prefix using multi-round hashing (MD5 → SHA1 → SHA256 → Base64) plus device fingerprint/environment simulation.
- `xhs_cookie_manager.py` — Simulated cookie manager. Handles three cookie tiers: static (`webId`, `a1`), semi-static (`web_session`, `gid`), dynamic (`acw_tc`, `loadts`). Auto-refresh on expiry.
- `real_cookie_manager.py` — Manages real browser-extracted cookies, persisted to `xhs_cookies.json`. Falls back to simulated cookies.
- `xhs_common_generator.py` — Generates the `x-s-common` request header.
- Other generators (`xhs_signature_generator.py`, `advanced_*`, `complete_*`, `final_*`, `xs_generator.py`) are earlier iterations kept for reference.

### crawlers/ — Scraper implementations

- `one_text_crawlers.py` — Main crawler. Imports generators via `sys.path.append` to `../generators`. Uses `generate_headers_with_signature(path, params)` as the central header-building function.
- `add_real_cookie.py` — CLI tool to inject real cookies from browser sessions.

### browser_files/ — Original JS source

Contains the original Xiaohongshu JavaScript bundles used for reverse engineering analysis. Key file: `vendor-dynamic.77f9fe85.js` (contains `seccore_signv2`).

### analysis_reports/ — Research artifacts

Analysis scripts and markdown reports documenting the reverse engineering process (cookie analysis, parameter patterns, etc.).

## Import Pattern

Generators are imported via `sys.path.append` rather than package imports:

```python
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "generators"))
from realistic_xhs_signature_generator import RealisticXHSSignatureGenerator
```

## Key Technical Details

- Signature algorithm: multi-round hash chain with environment payload, output is `XYS_` + Base64
- Cookie system has three refresh tiers with different TTLs
- The project prioritizes real cookies over simulated ones (controlled by `use_real_cookie=True` flag)
- Cookie data persists to `xhs_cookies.json` files in both `generators/` and `crawlers/` directories
