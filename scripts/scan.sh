#!/bin/bash
#
# Security Scan Runner for WhitePaper
#
# Runs applicable security-toolkit scans against this repository.
# Requires: brucedombrowski/security-toolkit installed at ~/Security
#
# Standards:
#   - NIST SP 800-53: SA-11 (Developer Testing), SI-12 (Information Retention)
#   - NIST SP 800-171: 3.14.1 (Flaw Remediation)
#
# Usage: ./scripts/scan.sh
#

set -eu

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TOOLKIT_DIR="${SECURITY_TOOLKIT_DIR:-$HOME/Security}"
SCANS_DIR="$REPO_DIR/.scans"
TIMESTAMP=$(date -u "+%Y-%m-%dT%H:%M:%SZ")

# Verify toolkit is available
if [ ! -d "$TOOLKIT_DIR/scripts" ]; then
    echo "ERROR: Security Verification Toolkit not found at $TOOLKIT_DIR"
    echo "Install from: https://github.com/brucedombrowski/security-toolkit"
    echo "Or set SECURITY_TOOLKIT_DIR environment variable."
    exit 1
fi

# Create output directory
mkdir -p "$SCANS_DIR"

echo "============================================="
echo "WhitePaper Security Scan"
echo "============================================="
echo "Timestamp: $TIMESTAMP"
echo "Target:    $REPO_DIR"
echo "Toolkit:   $TOOLKIT_DIR"
echo ""

# Track results
PASS=0
FAIL=0
REVIEW=0

run_scan() {
    local name="$1"
    local slug
    slug=$(echo "$name" | tr ' ' '-' | tr '[:upper:]' '[:lower:]')
    local script="$2"
    local log_file="$SCANS_DIR/${slug}-scan.log"

    echo "--- $name ---"
    "$TOOLKIT_DIR/scripts/$script" "$REPO_DIR" > "$log_file" 2>&1 || true
    local result
    result=$(tail -5 "$log_file" | grep -o "PASS\|FAIL\|REVIEW" | head -1)
    case "$result" in
        PASS)
            echo "  Result: PASS"
            PASS=$((PASS + 1))
            ;;
        REVIEW)
            echo "  Result: REVIEW (see .scans/${slug}-scan.log)"
            REVIEW=$((REVIEW + 1))
            ;;
        *)
            echo "  Result: FAIL (see .scans/${slug}-scan.log)"
            FAIL=$((FAIL + 1))
            ;;
    esac
    echo ""
}

# Run applicable scans
run_scan "PII Detection"       "check-pii.sh"
run_scan "Secrets Detection"   "check-secrets.sh"
run_scan "MAC Address"         "check-mac-addresses.sh"

# Host security (not target-specific, runs on the dev machine)
# Timeout after 30s to avoid hanging on softwareupdate checks
echo "--- Host Security ---"
timeout 30 "$TOOLKIT_DIR/scripts/check-host-security.sh" > "$SCANS_DIR/host-security-scan.log" 2>&1 || true
host_result=$(tail -5 "$SCANS_DIR/host-security-scan.log" | grep -o "PASS\|FAIL" | head -1)
case "$host_result" in
    PASS)
        echo "  Result: PASS"
        PASS=$((PASS + 1))
        ;;
    *)
        echo "  Result: FAIL (see .scans/host-security-scan.log)"
        FAIL=$((FAIL + 1))
        ;;
esac
echo ""

# Summary
TOTAL=$((PASS + FAIL + REVIEW))
echo "============================================="
echo "SCAN SUMMARY"
echo "============================================="
echo "Total:  $TOTAL"
echo "Pass:   $PASS"
echo "Fail:   $FAIL"
echo "Review: $REVIEW"
echo ""
echo "Results: $SCANS_DIR/"
echo "Timestamp: $TIMESTAMP"

if [ "$FAIL" -gt 0 ]; then
    echo ""
    echo "OVERALL: FAIL"
    exit 1
elif [ "$REVIEW" -gt 0 ]; then
    echo ""
    echo "OVERALL: REVIEW REQUIRED"
    exit 0
else
    echo ""
    echo "OVERALL: PASS"
    exit 0
fi
