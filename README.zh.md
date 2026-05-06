# iOS 26 适配技能

<div align="right">
  <b>🌐 语言:</b> <a href="./README.md">English</a> | 中文
</div>

---

> **语言**: Objective-C / Swift  
> **平台**: iOS  
> **最低 iOS 版本**: 12.0+  
> **最后更新**: 2026-05-06  
> **版本**: [v1.5.0](https://github.com/luodeCoding/ios26-adaptation-skill/blob/main/CHANGELOG.md)

**本仓库是 AI 适配技能工具，不参与任何项目编译。**

提供 iOS 26 SDK 适配的方案、模板、扫描脚本和检查清单，供 AI 助手和开发者参考使用。

## 这是什么？

本仓库是一个**独立的技能知识库**，用于：

- 🤖 **AI 助手** — 读取 SKILL.md、模板代码、检查清单，指导开发者完成适配
- 👨‍💻 **开发者参考** — 查看代码模板、复制需要的代码到主项目
- 🔍 **项目扫描** — 运行脚本检查主项目的废弃 API

**本仓库的文件不会被主项目引用或编译。** 所有模板代码需要开发者**手动复制**到主项目中使用。

## 关键时间节点

| 日期 | 要求 | 影响 |
|------|------|------|
| **2026-04-28** | 必须使用 iOS 26 SDK 构建 | 不合规将无法提交应用更新 |
| **~2026-09** | Xcode 27 发布，Liquid Glass 强制启用 | `UIDesignRequiresCompatibility` 将被移除 |

## 更新日志

| 版本 | 日期 | 主要更新 |
|------|------|---------|
| **[v1.5.0](CHANGELOG.zh.md)** | 2026-05-06 | Privacy Manifest 模板、Swift 6 并发适配模板、第三方 SDK 兼容性速查表、单元测试、CI |
| **[v1.4.0](CHANGELOG.zh.md)** | 2026-05-06 | StoreKit 2、SiriKit→App Intents、SwiftUI 现代 API、Photos 扫描规则 |
| **[v1.3.0](CHANGELOG.zh.md)** | 2026-05-06 | Swift 6 并发、TLS 1.2、CoreData、Liquid Glass 结构影响扫描规则 |
| **[v1.1.0](CHANGELOG.zh.md)** | 2026-04-14 | 生产模板、扫描脚本、FAQ、AGENTS.md |
| **[v1.0.0](CHANGELOG.zh.md)** | 2026-04-10 | 初始发布 — 两阶段策略、双语文档、检查清单 |

> [查看完整更新日志 →](CHANGELOG.zh.md)

## 两阶段适配

### 第一阶段：SDK 构建适配（2026-04-28 前）

**目标**: 使用 iOS 26 SDK 构建，同时保持现有 UI 不变

**关键任务**:
- 升级到 Xcode 26.0+
- 修复废弃 API 调用（keyWindow 等）
- 暂时禁用 Liquid Glass
- 完成 SceneDelegate 架构迁移

### 第二阶段：Liquid Glass 完整适配（Xcode 27 前）

**目标**: 完整适配 Liquid Glass 设计语言

**关键任务**:
- 移除 `UIDesignRequiresCompatibility` 标记
- 验证所有 UI 控件在 Liquid Glass 下的表现
- 调整自定义 UI 以达到视觉协调

## 使用方式

### 方式1：AI 助手使用（推荐）

将本仓库作为 AI 技能加载，AI 读取文档和模板后，直接在主项目中生成/修改代码。

```
开发者: "帮我适配 iOS 26"
AI: 读取 SKILL.md → 扫描主项目 → 生成适配代码 → 直接修改主项目文件
```

### 方式2：开发者手动参考

```bash
# 1. 下载到本地（任意位置，和主项目无关）
git clone https://github.com/luodeCoding/ios26-adaptation-skill.git

# 2. 查看需要的模板
cat ios26-adaptation-skill/templates/swift/SceneDelegate.swift

# 3. 手动复制需要的代码到主项目
# 直接复制粘贴，按需修改

# 4. 运行扫描脚本检查遗漏
python3 ios26-adaptation-skill/scripts/ios26-scanner.py /path/to/your/ios/project
```

## 项目结构

```
ios26-adaptation-skill/
├── README.md              # 本文件
├── README.zh.md           # 中文版
├── SKILL.md               # 📘 AI 核心技能文档（详细适配指南）
├── AGENTS.md              # 🤖 Claude Code Agent 使用指南
├── CHANGELOG.md           # 版本历史
├── LICENSE                # MIT 许可证
│
├── docs/                  # 📚 文档
│   ├── faq.md             # 常见问题
│   └── testing-guide.md   # 测试指南
│
├── .claude/               # 🎯 Claude 专用指南
│   └── iOS26-适配框架指南.md
│
├── examples/              # ✅ 检查清单
│   ├── phase1-checklist.md
│   ├── phase1-checklist.zh.md
│   ├── phase2-checklist.md
│   └── phase2-checklist.zh.md
│
├── scripts/               # 🔍 扫描脚本
│   └── ios26-scanner.py   # 废弃 API 扫描器
│
└── templates/             # 📋 代码模板（仅参考，不编译）
    ├── swift/             # Swift 模板
    │   ├── UIApplication+MainWindow.swift
    │   ├── SceneDelegate.swift
    │   ├── AppDelegate+Setup.swift
    │   └── UNNotificationOptions+Adapter.swift
    └── objc/              # Objective-C 模板
        ├── UIApplication+MainWindow.h/.m
        ├── SceneDelegate.h/.m
        ├── AppDelegate+Setup.h/.m
        └── UNNotificationOptionsAdapter.h/.m
```

## 核心内容速览

### 废弃 API 替换

| 废弃 API | 替代方案 | 模板位置 |
|---------|---------|---------|
| `keyWindow` | `UIApplication.mainWindow` | `templates/swift/UIApplication+MainWindow.swift` |
| `delegate.window` | `UIApplication.mainWindow` | 同上 |
| `UNNotificationPresentationOptionAlert` | `.banner \| .list` | `templates/swift/UNNotificationOptions+Adapter.swift` |
| `UNAuthorizationOptionAlert` | 仍然有效，无需替换 | 同上 |

### 扫描脚本

```bash
# 扫描主项目的废弃 API
python3 scripts/ios26-scanner.py /path/to/your/ios/project

# 输出 JSON 报告
python3 scripts/ios26-scanner.py /path/to/your/ios/project --format json --output report.json
```

### AI 技能文档

| 文档 | 用途 |
|------|------|
| `SKILL.md` | 完整适配指南、决策流程、代码示例 |
| `AGENTS.md` | Claude Code 工作流、触发条件、检查清单 |
| `.claude/iOS26-适配框架指南.md` | 中文完整框架指南 |

## 常见误区

| 误区 | 事实 |
|-----|------|
| 必须将 Deployment Target 改为 iOS 26 | ❌ 不需要。保持你当前的最低版本 |
| 用户必须升级到 iOS 26 | ❌ 不需要。运行时要求由 Deployment Target 决定 |
| 现有应用版本将被下架 | ❌ 不会。仅影响新提交和更新包 |
| 有宽限期 | ❌ 没有。2026年4月28日是硬性截止日期 |

## 资源

- [Apple Developer 新闻](https://developer.apple.com/news/)
- [iOS 26 发布说明](https://developer.apple.com/documentation/ios-release-notes)
- [Liquid Glass 设计指南](https://developer.apple.com/design/)

## 许可证

MIT 许可证 - 详见 LICENSE 文件

---

**作者**: roder
