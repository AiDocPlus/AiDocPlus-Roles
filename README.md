# AiDocPlus-Roles

AiDocPlus 内置角色资源仓库，包含 10 个预设用户角色及其 System Prompt。

## 资源内容

### 内置角色（10 个）

| ID | 名称 | 图标 | 说明 |
|----|------|------|------|
| general | 通用助手 | Bot | 通用文档写作助手 |
| lawyer | 法律顾问 | Scale | 法律文书和合同审查 |
| teacher | 教师 | GraduationCap | 教学设计和教育内容 |
| civil-servant | 公务员 | Building2 | 公文写作和政务报告 |
| programmer | 程序员 | Code | 技术文档和代码相关 |
| student | 学生 | BookOpen | 学术论文和学习笔记 |
| content-creator | 自媒体 | Pen | 新媒体内容创作 |
| product-manager | 产品经理 | LayoutDashboard | 产品文档和需求分析 |
| researcher | 学术研究 | Microscope | 学术研究和论文写作 |
| marketer | 市场营销 | TrendingUp | 营销方案和市场分析 |

## 目录结构

```
data/
└── {category}/{id}/
    ├── manifest.json         # 角色元数据（名称、图标、描述、推荐配置）
    └── system-prompt.md      # 角色 System Prompt
scripts/
├── build.sh / build.py       # 构建 → dist/roles.generated.ts
├── deploy.sh                  # 部署到 AiDocPlus 构建目标
└── extract_from_source.js     # 一次性提取脚本
```

## 构建和部署

```bash
bash scripts/build.sh      # 生成 roles.generated.ts
bash scripts/deploy.sh      # 部署到 AiDocPlus/packages/shared-types/src/generated/
```

## 角色数据格式

**manifest.json**：
```json
{
  "id": "role-id",
  "name": "角色名称",
  "icon": "LucideIconName",
  "description": "角色描述",
  "isBuiltIn": true,
  "suggestedTemperature": 0.7,
  "suggestedMaxTokens": 4000,
  "recommendedTemplateCategories": ["category1"],
  "recommendedPlugins": ["plugin-uuid"]
}
```

**system-prompt.md**：角色专属的 System Prompt，会拼接在用户自定义 prompt 之前。

## 生成文件

| 文件 | 部署位置 |
|------|----------|
| `roles.generated.ts` | `AiDocPlus/packages/shared-types/src/generated/` |
