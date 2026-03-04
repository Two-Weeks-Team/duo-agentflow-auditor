#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# Duo AgentFlow Auditor - E2E Demo Script
# =============================================================================
# This script automates the creation of a demo merge request with vulnerable
# code to trigger the duo-agentflow-auditor security scanning pipeline.
#
# Usage: scripts/demo.sh [--cleanup] [--gitlab-remote NAME]
# =============================================================================

# Colors
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Configuration
readonly DEFAULT_GITLAB_REMOTE="gitlab"
readonly MAX_WAIT_SECONDS=300  # 5 minutes
readonly POLL_INTERVAL=30
readonly DEMO_BRANCH_PREFIX="demo/security-audit"

# Global variables
GITLAB_REMOTE="${DEFAULT_GITLAB_REMOTE}"
CLEANUP_MODE=false
DEMO_BRANCH=""
MR_IID=""

# =============================================================================
# Helper Functions
# =============================================================================

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_wait() {
    echo -e "${YELLOW}[WAIT]${NC} $1"
}

# =============================================================================
# Cleanup Handler
# =============================================================================

cleanup() {
    local exit_code=$?
    if [[ $exit_code -ne 0 ]] && [[ "$CLEANUP_MODE" == "false" ]]; then
        log_warn "Script interrupted or failed. Run with --cleanup to remove demo artifacts."
        echo ""
        echo "To cleanup manually:"
        echo "  git checkout main 2>/dev/null || true"
        echo "  git branch -D \${DEMO_BRANCH:-'<branch>'} 2>/dev/null || true"
        echo "  git push \${GITLAB_REMOTE} --delete \${DEMO_BRANCH:-'<branch>'} 2>/dev/null || true"
    fi
    exit $exit_code
}

trap cleanup EXIT INT TERM

# =============================================================================
# Usage
# =============================================================================

show_help() {
    cat << 'EOF'
Duo AgentFlow Auditor - E2E Demo Script

Usage: scripts/demo.sh [--cleanup] [--gitlab-remote NAME]

Options:
  --cleanup          Clean up demo branches and MRs
  --gitlab-remote    GitLab remote name (default: gitlab)
  -h, --help         Show this help message

Examples:
  # Run the demo
  scripts/demo.sh

  # Use a different remote name
  scripts/demo.sh --gitlab-remote origin

  # Clean up demo artifacts
  scripts/demo.sh --cleanup

Description:
  This script automates the creation of a demo merge request with vulnerable
  code examples. It will:

  1. Check prerequisites (glab, git, GitLab remote)
  2. Create a test branch with timestamp
  3. Copy vulnerable example files from examples/vulnerable-mr/
  4. Commit and push the branch
  5. Create a merge request using glab
  6. Post a comment to trigger the auditor
  7. Poll for audit results
  8. Display the security findings

EOF
}

# =============================================================================
# Prerequisite Checks
# =============================================================================

check_prerequisites() {
    log_info "Checking prerequisites..."

    # Check glab CLI
    if ! command -v glab &> /dev/null; then
        log_error "glab CLI is not installed"
        echo ""
        echo "Install glab:"
        echo "  macOS:    brew install glab"
        echo "  Linux:    https://gitlab.com/gitlab-org/cli#installation"
        echo "  Windows:  winget install GitLab.Glab"
        echo ""
        echo "After installation, authenticate with:"
        echo "  glab auth login"
        exit 1
    fi
    log_success "glab CLI is installed"

    # Check glab authentication
    if ! glab auth status &> /dev/null; then
        log_error "glab is not authenticated"
        echo "Please run: glab auth login"
        exit 1
    fi
    log_success "glab is authenticated"

    # Check git
    if ! command -v git &> /dev/null; then
        log_error "git is not installed"
        exit 1
    fi
    log_success "git is installed"

    # Check if we're in a git repository
    if ! git rev-parse --git-dir &> /dev/null; then
        log_error "Not in a git repository"
        exit 1
    fi
    log_success "Inside a git repository"

    # Check GitLab remote
    if ! git remote get-url "$GITLAB_REMOTE" &> /dev/null; then
        log_error "GitLab remote '${GITLAB_REMOTE}' not found"
        echo ""
        echo "Available remotes:"
        git remote -v
        echo ""
        echo "To add a GitLab remote:"
        echo "  git remote add gitlab https://gitlab.com/YOUR_ORG/YOUR_REPO.git"
        exit 1
    fi
    log_success "GitLab remote '${GITLAB_REMOTE}' exists"

    # Check for vulnerable examples
    local examples_dir="examples/vulnerable-mr"
    if [[ ! -d "$examples_dir" ]]; then
        log_error "Vulnerable examples directory not found: $examples_dir"
        exit 1
    fi

    local required_files=("unsafe_script.py" "risky_config.yaml" "insecure_fetch.js")
    local missing=false
    for file in "${required_files[@]}"; do
        if [[ ! -f "$examples_dir/$file" ]]; then
            log_error "Missing required file: $examples_dir/$file"
            missing=true
        fi
    done

    if [[ "$missing" == "true" ]]; then
        exit 1
    fi
    log_success "All vulnerable example files present"
}

# =============================================================================
# Demo Creation Functions
# =============================================================================

create_demo_branch() {
    log_info "Creating demo branch..."

    DEMO_BRANCH="${DEMO_BRANCH_PREFIX}-$(date +%s)"

    # Ensure we're on main/master
    local default_branch
    default_branch=$(git remote show "$GITLAB_REMOTE" 2>/dev/null | grep 'HEAD branch' | awk '{print $NF}') || default_branch="main"

    log_info "Fetching latest ${default_branch}..."
    git fetch "$GITLAB_REMOTE" "$default_branch" --quiet

    log_info "Creating branch: $DEMO_BRANCH"
    git checkout -b "$DEMO_BRANCH" "$GITLAB_REMOTE/$default_branch"

    log_success "Created branch: $DEMO_BRANCH"
}

copy_vulnerable_files() {
    log_info "Copying vulnerable example files..."

    local source_dir="examples/vulnerable-mr"
    local files=("unsafe_script.py" "risky_config.yaml" "insecure_fetch.js")

    for file in "${files[@]}"; do
        if [[ -f "$source_dir/$file" ]]; then
            cp "$source_dir/$file" .
            log_info "Copied: $file"
        fi
    done

    log_success "Vulnerable files copied to project root"
}

commit_changes() {
    log_info "Committing vulnerable files..."

    git add -A
    git commit -m "Demo: Add intentionally vulnerable code for security audit

This commit introduces vulnerable code patterns for demonstration:
- unsafe_script.py: Uses os.system() with user input
- risky_config.yaml: Contains hardcoded credentials
- insecure_fetch.js: Uses eval() on untrusted data

DO NOT MERGE - This is for audit demo only." --quiet

    log_success "Changes committed"
}

push_branch() {
    log_info "Pushing branch to ${GITLAB_REMOTE}..."

    git push -u "$GITLAB_REMOTE" "$DEMO_BRANCH"

    log_success "Branch pushed: $DEMO_BRANCH"
}

create_merge_request() {
    log_info "Creating merge request..."

    local mr_desc="This MR contains intentionally vulnerable code for demonstrating the duo-agentflow-auditor security scanning capabilities.

## Vulnerable Files Added

- **unsafe_script.py**: Uses os.system() with user input (command injection risk)
- **risky_config.yaml**: Contains hardcoded credentials
- **insecure_fetch.js**: Uses eval() on untrusted data (code injection risk)

## Expected Audit Findings

The auditor should identify:
1. High severity: Command injection in os.system() calls
2. High severity: Hardcoded credentials/secrets
3. High severity: Unsafe eval() usage

---
*This is an automated demo MR. Do not merge.*"

    # Create MR and capture output
    local mr_output
    mr_output=$(glab mr create \
        --source-branch "$DEMO_BRANCH" \
        --title "Demo: Security Audit Test" \
        --description "$mr_desc" \
        --target-branch main \
        --yes 2>&1)

    # Extract MR IID from output
    MR_IID=$(echo "$mr_output" | grep -oE '!([0-9]+)' | head -1 | tr -d '!')

    if [[ -z "$MR_IID" ]]; then
        log_error "Failed to create merge request"
        echo "$mr_output"
        exit 1
    fi

    log_success "Created MR !${MR_IID}"
    echo ""
    echo "MR URL: $(echo "$mr_output" | grep -E '^https?://' | head -1)"
}

trigger_audit() {
    log_info "Triggering security audit..."

    glab mr note "$MR_IID" --message "@duo-agentflow-auditor please review this MR"

    log_success "Audit triggered"
}

poll_for_results() {
    log_wait "Waiting for audit results (max ${MAX_WAIT_SECONDS}s)..."
    echo ""

    local elapsed=0
    local spinner=('|' '/' '-' "\\")
    local spinner_idx=0

    while [[ $elapsed -lt $MAX_WAIT_SECONDS ]]; do
        # Update spinner
        printf "\r${YELLOW}%s${NC} Polling for audit comments... (%ds/%ds)" \
            "${spinner[$spinner_idx]}" "$elapsed" "$MAX_WAIT_SECONDS"
        spinner_idx=$(( (spinner_idx + 1) % 4 ))

        # Check for audit comments
        local comments
        comments=$(glab mr note "$MR_IID" --list 2>/dev/null || true)

        # Look for auditor response (not our trigger message)
        if echo "$comments" | grep -qv "please review this MR"; then
            # Check if there's a comment from the auditor (contains security findings)
            if echo "$comments" | grep -qE "(Security Audit|Risk|Severity|vulnerability)"; then
                printf "\n\n"
                log_success "Audit complete! Found security findings."
                echo ""
                display_results "$comments"
                return 0
            fi
        fi

        sleep 1
        elapsed=$((elapsed + 1))

        # Only show poll message every 30 seconds
        if [[ $((elapsed % POLL_INTERVAL)) -eq 0 ]] && [[ $elapsed -lt $MAX_WAIT_SECONDS ]]; then
            printf "\n"
            log_info "Still waiting... (${elapsed}s elapsed)"
        fi
    done

    printf "\n\n"
    log_warn "Timeout reached. Audit may still be in progress."
    echo ""
    echo "Check the MR manually:"
    glab mr view "$MR_IID" --web 2>/dev/null || echo "MR !${MR_IID}"
    return 1
}

display_results() {
    local comments="$1"

    echo "========================================"
    echo "         AUDIT RESULTS"
    echo "========================================"
    echo ""

    # Display the auditor's comment (not the trigger message)
    echo "$comments" | grep -A 100 -E "(Security Audit|Risk|Severity|vulnerability)" | head -50

    echo ""
    echo "========================================"
    log_success "Demo complete!"
    echo ""
    echo "MR Details:"
    glab mr view "$MR_IID" 2>/dev/null || echo "MR !${MR_IID}"
}

# =============================================================================
# Cleanup Functions
# =============================================================================

cleanup_demo() {
    log_info "Cleanup mode - removing demo artifacts..."

    # Find demo branches
    local demo_branches
    demo_branches=$(git branch -r --list "${GITLAB_REMOTE}/${DEMO_BRANCH_PREFIX}-*" 2>/dev/null | sed 's/.*\///' || true)

    if [[ -z "$demo_branches" ]]; then
        log_warn "No demo branches found on remote"
    else
        echo "Found demo branches:"
        echo "$demo_branches"
        echo ""

        for branch in $demo_branches; do
            log_info "Deleting remote branch: $branch"
            git push "$GITLAB_REMOTE" --delete "$branch" 2>/dev/null || log_warn "Failed to delete $branch"
        done
    fi

    # Find demo MRs
    log_info "Searching for demo MRs..."
    local demo_mrs
    demo_mrs=$(glab mr list --search "Demo: Security Audit Test" --state all 2>/dev/null | grep -E '^!' || true)

    if [[ -z "$demo_mrs" ]]; then
        log_warn "No demo MRs found"
    else
        echo "Found demo MRs:"
        echo "$demo_mrs"
        echo ""

        # Extract MR numbers and close them
        echo "$demo_mrs" | while read -r line; do
            local mr_num
            mr_num=$(echo "$line" | grep -oE '^![0-9]+' | tr -d '!')
            if [[ -n "$mr_num" ]]; then
                log_info "Closing MR !${mr_num}..."
                glab mr close "$mr_num" 2>/dev/null || log_warn "Failed to close MR !${mr_num}"
            fi
        done
    fi

    # Clean local branches
    local local_branches
    local_branches=$(git branch --list "${DEMO_BRANCH_PREFIX}-*" 2>/dev/null | sed 's/^[\* ]*//' || true)

    if [[ -n "$local_branches" ]]; then
        for branch in $local_branches; do
            log_info "Deleting local branch: $branch"
            git branch -D "$branch" 2>/dev/null || true
        done
    fi

    log_success "Cleanup complete"
}

# =============================================================================
# Main
# =============================================================================

main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --cleanup)
                CLEANUP_MODE=true
                shift
                ;;
            --gitlab-remote)
                if [[ -n "${2:-}" ]]; then
                    GITLAB_REMOTE="$2"
                    shift 2
                else
                    log_error "--gitlab-remote requires an argument"
                    exit 1
                fi
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                echo "Use --help for usage information"
                exit 1
                ;;
        esac
    done

    # Run cleanup if requested
    if [[ "$CLEANUP_MODE" == "true" ]]; then
        check_prerequisites
        cleanup_demo
        exit 0
    fi

    # Run the demo
    log_info "Starting Duo AgentFlow Auditor Demo"
    echo ""

    check_prerequisites
    create_demo_branch
    copy_vulnerable_files
    commit_changes
    push_branch
    create_merge_request
    trigger_audit
    poll_for_results

    echo ""
    log_success "Demo completed successfully!"
    echo ""
    echo "To clean up demo artifacts, run:"
    echo "  scripts/demo.sh --cleanup"
}

main "$@"
