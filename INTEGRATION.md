# iOS 26 Adaptation — 使用说明

> 本仓库是**纯 AI 技能工具**，不参与任何项目编译。

---

## 核心定位

```
┌─────────────────────────────────────────────────────────────┐
│                    主项目（你的 iOS App）                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ AppDelegate │  │ SceneDelegate│  │ UIApplication+Ext   │  │
│  │ （手动修改） │  │ （手动添加） │  │ （手动添加）        │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│                                                             │
│  所有代码都是开发者手动复制/编写，和 skill 仓库无引用关系       │
└─────────────────────────────────────────────────────────────┘
                              ↑
                              │ AI 读取 skill 知识，指导开发
                              │
┌─────────────────────────────────────────────────────────────┐
│           ios26-adaptation-skill（本仓库）                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ SKILL.md │  │ templates│  │ scripts  │  │ docs     │    │
│  │ 知识文档  │  │ 代码模板  │  │ 扫描脚本  │  │ 参考文档  │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
│                                                             │
│  仅作为 AI 知识和开发者参考，不加入任何 Xcode 项目编译          │
└─────────────────────────────────────────────────────────────┘
```

---

## 使用方式

### 方式1：AI 助手驱动（推荐）

AI 读取本仓库的知识，直接在主项目中生成和修改代码。

**开发者只需要说：**

```
"帮我适配 iOS 26"
"扫描一下项目有哪些废弃 API"
"生成 SceneDelegate 代码"
```

**AI 的工作流程：**

1. 读取 `SKILL.md` 了解适配策略
2. 读取 `AGENTS.md` 了解检查清单
3. 运行 `scripts/ios26-scanner.py` 扫描主项目
4. 参考 `templates/` 中的代码模板
5. **直接在主项目中**生成/修改代码

### 方式2：开发者手动参考

```bash
# 1. 下载到本地任意位置（和主项目完全独立）
git clone https://github.com/luodeCoding/ios26-adaptation-skill.git

# 2. 查看需要的模板代码
cat ios26-adaptation-skill/templates/swift/SceneDelegate.swift

# 3. 手动复制粘贴到主项目，按需修改
# 直接复制代码，不是引用文件！

# 4. 运行扫描脚本检查遗漏
python3 ios26-adaptation-skill/scripts/ios26-scanner.py /path/to/your/ios/project
```

---

## 重要说明

### ❌ 不要做的事情

| 不要做 | 原因 |
|--------|------|
| 不要把 skill 仓库文件加入 Xcode 项目 | 这些文件只是参考模板，不需要编译 |
| 不要用 `#import` 或 `import` 引用 skill 文件 | skill 文件不在主项目中 |
| 不要把 skill 仓库作为 git submodule | 完全没必要，AI 直接读取本地文件即可 |
| 不要把 skill 仓库复制到主项目里 | 保持独立，方便更新和 AI 读取 |

### ✅ 正确的工作流

```
主项目遇到 iOS 26 适配问题
        ↓
AI 读取 skill 仓库知识（SKILL.md、模板、检查清单）
        ↓
AI 分析主项目代码，找出问题
        ↓
AI 参考模板，直接在主项目中生成修复代码
        ↓
开发者审阅、调整、编译验证
        ↓
发现问题 → 继续让 AI 调整（循环）
```

---

## 文件用途说明

| 文件/目录 | 用途 | 谁使用 |
|----------|------|--------|
| `SKILL.md` | 完整适配指南、决策流程、代码示例 | AI + 开发者 |
| `AGENTS.md` | Claude Code 工作流、触发条件 | AI |
| `templates/swift/` | Swift 代码模板 | AI 参考后生成代码 |
| `templates/objc/` | Objective-C 代码模板 | AI 参考后生成代码 |
| `scripts/ios26-scanner.py` | 废弃 API 扫描脚本 | AI / 开发者手动运行 |
| `docs/faq.md` | 常见问题解答 | 开发者参考 |
| `examples/` | 分阶段检查清单 | AI + 开发者 |

---

## 扫描脚本使用

```bash
# 基本用法
python3 /path/to/ios26-adaptation-skill/scripts/ios26-scanner.py /path/to/your/ios/project

# 生成 JSON 报告
python3 /path/to/ios26-adaptation-skill/scripts/ios26-scanner.py \
    /path/to/your/ios/project \
    --format json \
    --output report.json
```

扫描内容：
- `keyWindow` 使用
- `delegate.window` 使用
- `UNNotificationPresentationOptionAlert`
- `UNAuthorizationOptionAlert`
- SceneDelegate 配置状态
- AppDelegate `sharedInstance` 方法
