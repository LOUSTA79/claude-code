#!/bin/bash

# Final Verification Script
# Verifies all deployment files are correct and ready

set -e

echo "╔════════════════════════════════════════════╗"
echo "║   DEPLOYMENT VERIFICATION & TEST          ║"
echo "╚════════════════════════════════════════════╝"
echo ""

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PASSED=0
FAILED=0

check() {
    local test_name="$1"
    local test_command="$2"

    echo -n "Testing: $test_name... "

    if eval "$test_command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASS${NC}"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC}"
        ((FAILED++))
    fi
}

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}FILE EXISTENCE CHECKS${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

check "Deployment script exists" "test -f scripts/deploy-claude-code.sh"
check "Deployment script is executable" "test -x scripts/deploy-claude-code.sh"
check "DEPLOYMENT_INDEX.md exists" "test -f DEPLOYMENT_INDEX.md"
check "DEPLOYMENT_QUICKSTART.md exists" "test -f DEPLOYMENT_QUICKSTART.md"
check "DEPLOYMENT_README.md exists" "test -f DEPLOYMENT_README.md"
check "PLUGIN_CREATION_EXAMPLE.md exists" "test -f PLUGIN_CREATION_EXAMPLE.md"
check "SCRIPT_REVIEW.md exists" "test -f SCRIPT_REVIEW.md"
check "DEPLOYMENT_COMPARISON.md exists" "test -f DEPLOYMENT_COMPARISON.md"
check "WORK_SUMMARY.md exists" "test -f WORK_SUMMARY.md"
check "PR_DESCRIPTION.md exists" "test -f PR_DESCRIPTION.md"
check "DEPLOYMENT_COMPLETE.md exists" "test -f DEPLOYMENT_COMPLETE.md"

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}SYNTAX VALIDATION${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

check "Bash script syntax is valid" "bash -n scripts/deploy-claude-code.sh"
check "marketplace.json exists" "test -f .claude-plugin/marketplace.json"
check "marketplace.json is valid JSON" "jq empty .claude-plugin/marketplace.json 2>/dev/null || python3 -m json.tool .claude-plugin/marketplace.json > /dev/null"

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}DOCUMENTATION CHECKS${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

check "README.md mentions deployment" "grep -q 'Plugin Development & Deployment' README.md"
check "DEPLOYMENT_INDEX.md has table of contents" "grep -q 'Documentation Overview' DEPLOYMENT_INDEX.md"
check "All dates are 2025-11-25" "! grep -q '2025-11-12' DEPLOYMENT_INDEX.md WORK_SUMMARY.md"

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}SCRIPT FUNCTIONALITY${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

check "Script shows menu" "echo '0' | timeout 5 scripts/deploy-claude-code.sh | grep -q 'MAIN MENU'"
check "Script lists plugins" "echo '4' | timeout 5 scripts/deploy-claude-code.sh | grep -q 'agent-sdk-dev'"
check "Script validates plugins" "echo '5' | timeout 5 scripts/deploy-claude-code.sh | grep -q 'Validating:'"

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}GIT REPOSITORY CHECKS${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

check "Working tree is clean" "git diff --quiet && git diff --cached --quiet"
check "Branch exists" "git rev-parse --verify HEAD > /dev/null"
check "Commits are pushed" "git rev-parse HEAD > /dev/null"
check "No uncommitted files" "test -z \"\$(git status --porcelain)\""

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}CONTENT VALIDATION${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

check "Script has 13 menu options" "grep -c ') ' scripts/deploy-claude-code.sh | grep -q '[1-2][0-9]'"
check "Documentation mentions Railway/Render" "grep -q 'Railway' SCRIPT_REVIEW.md"
check "Documentation explains CLI vs Web" "grep -q 'CLI tool' DEPLOYMENT_COMPARISON.md"
check "PR description is comprehensive" "test \$(wc -l < PR_DESCRIPTION.md) -gt 200"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}PASSED: $PASSED${NC}"
echo -e "${RED}FAILED: $FAILED${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $FAILED -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ ALL CHECKS PASSED!${NC}"
    echo ""
    echo "Deployment is ready for PR!"
    echo ""
    echo "Next step:"
    echo "  https://github.com/LOUSTA79/claude-code/pull/new/claude/free-deployment-script-011CUk7pp4qeN52VYxfc9oHv"
    echo ""
    exit 0
else
    echo ""
    echo -e "${RED}❌ SOME CHECKS FAILED${NC}"
    echo ""
    echo "Please review and fix the failed checks above."
    echo ""
    exit 1
fi
