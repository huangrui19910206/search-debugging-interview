#!/usr/bin/env bash
# Runs the candidate test suite. Expect the 5 baseline tests to pass and the
# 4 test_level_* tests to fail (that is the exercise).
set -euo pipefail
cd "$(dirname "$0")/.."
python -m pytest -v
