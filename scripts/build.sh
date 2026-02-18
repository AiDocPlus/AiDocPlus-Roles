#!/bin/bash
# AiDocPlus-Roles build.sh
# 扫描 data/ 目录，生成 roles.generated.ts
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "${SCRIPT_DIR}/build.py"
