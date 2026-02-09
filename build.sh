#!/bin/bash
#
# Build Script for WhitePaper
#
# Compiles whitepaper.tex to whitepaper.pdf with full reference resolution.
# Runs pdflatex → bibtex → pdflatex → pdflatex (standard LaTeX build cycle).
#
# Standards:
#   - NIST SP 800-53 CM-3: Reproducible build from version-controlled source
#
# Usage: ./build.sh
#

set -eu

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEX_FILE="$SCRIPT_DIR/whitepaper.tex"
BASE_NAME="whitepaper"

if [ ! -f "$TEX_FILE" ]; then
    echo "ERROR: $TEX_FILE not found"
    exit 1
fi

echo "Building $BASE_NAME.pdf ..."

# Step 1: Initial compile (generates .aux for bibtex)
echo "  [1/4] pdflatex (initial)"
pdflatex -interaction=nonstopmode -output-directory="$SCRIPT_DIR" "$TEX_FILE" > /dev/null 2>&1

# Step 2: Process bibliography
echo "  [2/4] bibtex"
(cd "$SCRIPT_DIR" && bibtex "$BASE_NAME") > /dev/null 2>&1

# Step 3: Second compile (incorporates bibliography)
echo "  [3/4] pdflatex (bibliography)"
pdflatex -interaction=nonstopmode -output-directory="$SCRIPT_DIR" "$TEX_FILE" > /dev/null 2>&1

# Step 4: Third compile (resolves all cross-references)
echo "  [4/4] pdflatex (cross-references)"
pdflatex -interaction=nonstopmode -output-directory="$SCRIPT_DIR" "$TEX_FILE" > /dev/null 2>&1

# Generate reviewable Markdown (GitHub-flavored, selectable text)
if command -v pandoc &> /dev/null; then
    echo "  [5/5] pandoc (markdown for review)"
    pandoc "$TEX_FILE" -f latex -t gfm --wrap=auto -o "$SCRIPT_DIR/${BASE_NAME}-review.md" 2>/dev/null
fi

# Verify output
if [ -f "$SCRIPT_DIR/$BASE_NAME.pdf" ]; then
    PAGES=$(pdfinfo "$SCRIPT_DIR/$BASE_NAME.pdf" 2>/dev/null | grep "Pages:" | awk '{print $2}' || echo "?")
    SIZE=$(ls -lh "$SCRIPT_DIR/$BASE_NAME.pdf" | awk '{print $5}')
    echo ""
    echo "SUCCESS: $BASE_NAME.pdf ($PAGES pages, $SIZE)"
else
    echo ""
    echo "FAIL: $BASE_NAME.pdf not generated. Check $BASE_NAME.log for errors."
    exit 1
fi
