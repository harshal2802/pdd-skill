#!/usr/bin/env bash
set -euo pipefail

python3 scripts/render_workflow_tables.py --check
python3 scripts/verify_structure.py
python3 tests/test_metadata_model.py
python3 tests/test_provider_packaging.py
