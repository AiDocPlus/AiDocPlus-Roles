#!/usr/bin/env python3
"""
AiDocPlus-Roles 构建脚本
扫描 data/ 目录，生成 roles.generated.ts
"""
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(REPO_DIR, "data")
DIST_DIR = os.path.join(REPO_DIR, "dist")

os.makedirs(DIST_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(DIST_DIR, "roles.generated.ts")


def find_roles(data_dir: str):
    """递归查找所有角色目录（含 manifest.json 的目录，排除 _meta.json）"""
    roles = []
    for root, dirs, files in os.walk(data_dir):
        if "manifest.json" in files:
            manifest_path = os.path.join(root, "manifest.json")
            prompt_path = os.path.join(root, "system-prompt.md")
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = json.load(f)
            system_prompt = ""
            if os.path.isfile(prompt_path):
                with open(prompt_path, "r", encoding="utf-8") as f:
                    system_prompt = f.read().strip()
            roles.append((manifest, system_prompt))
    # 按 majorCategory order + order 排序
    roles.sort(key=lambda r: (r[0].get("majorCategory", ""), r[0].get("order", 0)))
    return roles


def ts_string(s: str) -> str:
    """将字符串转为 TypeScript 字面量，使用反引号处理多行"""
    if "\n" in s:
        escaped = s.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")
        return f"`{escaped}`"
    else:
        return json.dumps(s, ensure_ascii=False)


def ts_string_array(arr: list) -> str:
    items = ", ".join(json.dumps(x, ensure_ascii=False) for x in arr)
    return f"[{items}]"


def generate_role_entry(manifest: dict, system_prompt: str) -> str:
    lines = []
    lines.append("  {")
    lines.append(f"    id: {ts_string(manifest['id'])},")
    lines.append(f"    name: {ts_string(manifest['name'])},")
    lines.append(f"    icon: {ts_string(manifest['icon'])},")
    lines.append(f"    description: {ts_string(manifest['description'])},")
    lines.append(f"    isBuiltIn: true,")
    lines.append(f"    systemPrompt: {ts_string(system_prompt)},")

    if manifest.get("markdownModePrompt"):
        lines.append(f"    markdownModePrompt: {ts_string(manifest['markdownModePrompt'])},")
    if manifest.get("suggestedTemperature") is not None:
        lines.append(f"    suggestedTemperature: {manifest['suggestedTemperature']},")
    if manifest.get("suggestedMaxTokens") is not None:
        lines.append(f"    suggestedMaxTokens: {manifest['suggestedMaxTokens']},")
    if manifest.get("recommendedTemplateCategories"):
        lines.append(f"    recommendedTemplateCategories: {ts_string_array(manifest['recommendedTemplateCategories'])},")
    if manifest.get("recommendedPlugins"):
        lines.append(f"    recommendedPlugins: {ts_string_array(manifest['recommendedPlugins'])},")

    lines.append("  },")
    return "\n".join(lines)


def main():
    print("🔨 构建角色数据...")
    roles = find_roles(DATA_DIR)

    if not roles:
        print("⚠️  未找到任何角色数据")
        sys.exit(1)

    entries = []
    for manifest, system_prompt in roles:
        entries.append(generate_role_entry(manifest, system_prompt))

    output = f"""/**
 * 自动生成文件 — 请勿手动编辑
 * 由 AiDocPlus-Roles/scripts/build.py 生成
 */
import type {{ UserRole }} from '../index';

export const BUILT_IN_ROLES: UserRole[] = [
{chr(10).join(entries)}
];
"""

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"✅ 角色数据构建完成: {OUTPUT_FILE}")
    print(f"   共 {len(roles)} 个角色")


if __name__ == "__main__":
    main()
