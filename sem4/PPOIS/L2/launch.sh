#!/bin/bash
set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # Reset

# Logging functions
info()    { echo -e "${BLUE}[!]${NC} $*"; }
success() { echo -e "${GREEN}[✓]${NC} $*"; }
warn()    { echo -e "${YELLOW}[⚠]${NC} $*"; }
error()   { echo -e "${RED}[✗]${NC} $*" >&2; }

CONDA_ENV="base"  # Default value
SKIP_BUILD=0

while [[ $# -gt 0 ]]; do
    case $1 in
        --conda-env)
            [[ -z "${2:-}" || "$2" == --* ]] && { error "--conda-env requires a value"; exit 1; }
            CONDA_ENV="$2"
            shift 2
            ;;
        --conda-env=*)
            CONDA_ENV="${1#*=}"
            shift
            ;;
        --no-build|--skip-build)
            SKIP_BUILD=1
            shift
            ;;
        --help|-h)
            cat <<EOF
Usage: $0 [OPTIONS]

Build (regenerate UI/resources) and launch the application.

Options:
  --conda-env NAME    Conda environment to use (default: base)
  --no-build          Skip UI/resource regeneration, just activate env and run
                      (alias: --skip-build)
  -h, --help          Show this help message
EOF
            exit 0
            ;;
        *)
            error "Unknown option: $1"
            echo "Use --help for usage information" >&2
            exit 1
            ;;
    esac
done

# Error trap
trap 'error "Launch failed at line $LINENO"; exit 1' ERR

# Ensure we are in project root
cd "$(dirname "$0")"

# Check env
if [ "${CONDA_DEFAULT_ENV:-}" != "$CONDA_ENV" ]; then
    warn "Active env: '${CONDA_DEFAULT_ENV:-none}' | Required: '$CONDA_ENV'"

    # Check if running in interactive terminal
    if [[ -t 0 ]]; then
        read -p "$(echo -e "${YELLOW}Activate '$CONDA_ENV'? [y/N]: ${NC}")" -n 1 -r
        echo # newline
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            info "Activating conda env: $CONDA_ENV..."

            # Source conda.sh if needed (for conda activate to work in scripts)
            if [[ -f "$CONDA_PREFIX/etc/profile.d/conda.sh" ]]; then
                source "$CONDA_PREFIX/etc/profile.d/conda.sh"
            elif command -v conda >/dev/null 2>&1; then
                # Try to find conda.sh via conda info
                CONDA_SH="$(conda info --base)/etc/profile.d/conda.sh"
                [[ -f "$CONDA_SH" ]] && source "$CONDA_SH"
            fi

            # Activate the environment
            if ! conda activate "$CONDA_ENV" 2>/dev/null; then
                error "Failed to activate '$CONDA_ENV'. Please activate manually:"
                echo -e "  ${YELLOW}conda activate $CONDA_ENV${NC}"
                exit 1
            fi
            success "Environment '$CONDA_ENV' activated"
        else
            error "Aborted: '$CONDA_ENV' is required but not active."
            exit 1
        fi
    else
        # Non-interactive mode (CI, cron, pipe)
        error "Required env '$CONDA_ENV' is not active (non-interactive mode)."
        error "Run manually: ${YELLOW}conda activate $CONDA_ENV && $0${NC}"
        exit 1
    fi
else
  info "Conda environment $CONDA_ENV already activated. Skipped"
fi

# Build step (skippable)
if [[ $SKIP_BUILD -eq 1 ]]; then
    info "Skipping UI/resource build (--no-build)"
else
    # Generate UI and Resource files
    info "Generating UI and resource files..."
    pyside6-uic ./resources/main_window.ui  -o ./src/ui_mainwindow.py
    pyside6-uic ./resources/record_dialog.ui -o ./src/ui_record_dialog.py
    pyside6-rcc ./resources/resources.qrc   -o ./src/resources_rc.py

    # Patch imports
    info "Patching imports..."
    sed -i.bak 's/^import resources_rc$/from .resources_rc import */' ./src/ui_mainwindow.py
    sed -i.bak 's/^# -*- coding: utf-8 -*-$//' ./src/ui_mainwindow.py
    sed -i.bak 's/^# -*- coding: utf-8 -*-$//' ./src/ui_record_dialog.py
    rm -f ./src/*.bak

    success "UI Build complete!"
fi

# ——— Runtime ———

trap 'error "Runtime failed at line $LINENO"; exit 1' ERR # Relocate error for runtime

python -m src
