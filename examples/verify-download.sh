#!/bin/bash

# Verification script for downloaded deployment packages
# Run this after downloading to verify integrity

set -e

echo "🔒 Verifying S25 Ultra Coding Agent Suite Download"
echo ""

# Expected checksums
EXPECTED_TARBALL="5d0951d6b434f78ae92282e40498e474db79385bf2c38ff40bc337fc6e83c195"
EXPECTED_ZIP="eeb6d09c4a855551fc03a45f80c2c501cb4b841cb4b288aadab0da102a456c8d"

# Find the downloaded file
TARBALL=$(find . -maxdepth 1 -name "coding-agents-s25-ultra-*.tar.gz" 2>/dev/null | head -1)
ZIPFILE=$(find . -maxdepth 1 -name "coding-agents-s25-ultra-*.zip" 2>/dev/null | head -1)

if [ -z "$TARBALL" ] && [ -z "$ZIPFILE" ]; then
    echo "❌ No deployment package found in current directory"
    echo ""
    echo "Please download one of:"
    echo "  • coding-agents-s25-ultra-20251030_201750.tar.gz"
    echo "  • coding-agents-s25-ultra-20251030_201750.zip"
    echo ""
    exit 1
fi

# Verify tarball
if [ -n "$TARBALL" ]; then
    echo "📦 Found: $TARBALL"
    echo "🔍 Computing checksum..."

    ACTUAL=$(sha256sum "$TARBALL" | awk '{print $1}')

    if [ "$ACTUAL" = "$EXPECTED_TARBALL" ]; then
        echo "✅ Checksum verified: tar.gz package is authentic"
    else
        echo "❌ Checksum mismatch!"
        echo "   Expected: $EXPECTED_TARBALL"
        echo "   Got:      $ACTUAL"
        echo ""
        echo "⚠️  WARNING: Package may be corrupted or tampered with!"
        exit 1
    fi
fi

# Verify zip
if [ -n "$ZIPFILE" ]; then
    echo "📦 Found: $ZIPFILE"
    echo "🔍 Computing checksum..."

    ACTUAL=$(sha256sum "$ZIPFILE" | awk '{print $1}')

    if [ "$ACTUAL" = "$EXPECTED_ZIP" ]; then
        echo "✅ Checksum verified: zip package is authentic"
    else
        echo "❌ Checksum mismatch!"
        echo "   Expected: $EXPECTED_ZIP"
        echo "   Got:      $ACTUAL"
        echo ""
        echo "⚠️  WARNING: Package may be corrupted or tampered with!"
        exit 1
    fi
fi

echo ""
echo "🎉 Verification complete! Your download is safe to install."
echo ""
echo "Next steps:"
if [ -n "$TARBALL" ]; then
    echo "  tar -xzf $TARBALL"
    echo "  cd coding-agents-s25-ultra-20251030_201750"
elif [ -n "$ZIPFILE" ]; then
    echo "  unzip $ZIPFILE"
    echo "  cd coding-agents-s25-ultra-20251030_201750"
fi
echo "  bash install.sh"
echo ""
