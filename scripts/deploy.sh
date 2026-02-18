#!/bin/bash
# AiDocPlus-Roles deploy.sh
# 将构建产物部署到 AiDocPlus/ 构建目标
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
PARENT_DIR="$(dirname "$REPO_DIR")"
TARGET_DIR="${PARENT_DIR}/AiDocPlus"
DIST_DIR="${REPO_DIR}/dist"
DATA_DIR="${REPO_DIR}/data"

echo "[deploy] AiDocPlus-Roles -> ${TARGET_DIR}"

# 1. 部署 generated TypeScript 文件
GENERATED_DIR="${TARGET_DIR}/packages/shared-types/src/generated"
mkdir -p "$GENERATED_DIR"

if [ -f "${DIST_DIR}/roles.generated.ts" ]; then
  cp "${DIST_DIR}/roles.generated.ts" "${GENERATED_DIR}/"
  echo "   [ok] roles.generated.ts -> generated/"
else
  echo "   [warn] dist/roles.generated.ts 不存在，请先运行 build.sh"
fi

# 2. 部署角色数据到 bundled-resources（供 Rust 后端 + SQLite 索引）
BUNDLED_DIR="${TARGET_DIR}/apps/desktop/src-tauri/bundled-resources/roles"
mkdir -p "$BUNDLED_DIR"

# 复制 _meta.json
if [ -f "${DATA_DIR}/_meta.json" ]; then
  cp "${DATA_DIR}/_meta.json" "${BUNDLED_DIR}/"
fi

# 复制所有角色目录
find "$DATA_DIR" -name "manifest.json" -not -path "*/_meta.json" | while read -r manifest_file; do
  role_dir="$(dirname "$manifest_file")"
  role_id=$(grep -o '"id"[[:space:]]*:[[:space:]]*"[^"]*"' "$manifest_file" | head -1 | sed 's/.*"\([^"]*\)"$/\1/')
  
  target_role_dir="${BUNDLED_DIR}/${role_id}"
  mkdir -p "$target_role_dir"
  cp -r "${role_dir}/"* "$target_role_dir/"
  echo "   ${role_id}"
done

echo "   [ok] 角色数据 -> bundled-resources/roles/"
echo "[done] AiDocPlus-Roles 部署完成"
