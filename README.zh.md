# iOS 26 适配技能

<div align="right">
  <b>🌐 语言:</b> <a href="./README.md">English</a> | 中文
</div>

---

> **语言**: Objective-C / Swift  
> **平台**: iOS  
> **最低 iOS 版本**: 12.0+  
> **最后更新**: 2026-08-03  
> **版本**: [v1.12.0](https://github.com/luodeCoding/ios26-adaptation-skill/blob/main/CHANGELOG.zh.md)

**本仓库是 AI 适配技能工具，不参与任何项目编译。**

提供 iOS 26 SDK 适配的方案、模板、扫描脚本和检查清单，供 AI 助手和开发者参考使用。

## 这是什么？

本仓库是一个**独立的技能知识库**，用于：

- 🤖 **AI 助手** — 读取 SKILL.md、模板代码、检查清单，指导开发者完成适配
- 👨‍💻 **开发者参考** — 查看代码模板、复制需要的代码到主项目
- 🔍 **项目扫描** — 运行脚本检查主项目的废弃 API

**本仓库的文件不会被主项目引用或编译。** 所有模板代码需要开发者**手动复制**到主项目中使用。

### 适配影响承诺（低冲击保证）

把本技能应用到你的项目（AI 自动执行或手动参考）时，改动是**外科手术式**的：

- ✅ **只动 iOS 26/27 相关代码** — 废弃 API 调用点、SceneDelegate 生命周期架构、Info.plist 适配键、新增适配器文件
- ✅ **不改 Deployment Target**；保留 iOS 13 之前的兼容路径；所有版本差异用 `#available` / `@available` 包裹
- ✅ **不顺手重构** — 业务逻辑、无关文件、第三方 SDK 源码（`Pods/`）一律不碰
- ✅ **对齐苹果官方标准** — 每一项要求均可追溯到苹果官方来源（Upcoming Requirements、Release Notes、WWDC、TN3187）
- ✅ **可审计流程** — 扫描 → 列出文件清单与理由 → 执行 → 重扫直到 Error 清零

完整声明见：[INTEGRATION.md](INTEGRATION.md) § 适配影响声明。

### 零遗漏保证（覆盖总账）

AI 适配最经典的痛点："一会儿漏这样、一会儿漏那样"。v1.12.0 把这个洞堵死：

- 📋 **50 项覆盖总账**（`scripts/adaptation-ledger.json`）— Phase 1/2/3 的完整任务清单唯一事实源；AI 必须逐项对照执行，不允许凭记忆取子集（[docs/coverage.zh.md](docs/coverage.zh.md)）
- 🔍 **扫描报告末尾自带人工核对清单 + 上线门禁（SHIP-01~05）** — 无法静态检测的项逐条列出；"完成"的定义是门禁全绿，而不是"代码能编译"
- 🛡️ **CI 一致性测试** — 总账中每个自动检测项必须对应真实存在的扫描规则；未来漏项会直接测试失败

目标：用本技能改完后，再修一轮 bug，基本就能上线。

## 关键时间节点

| 日期 | 要求 | 影响 |
|------|------|------|
| **2026-04-28**（已生效） | 必须使用 iOS 26 SDK 构建 | 不合规将无法提交应用更新 |
| **~2026-09** | Xcode 27 发布，Liquid Glass 强制启用 | `UIDesignRequiresCompatibility` 将被移除，Phase 2 窗口正在关闭 |
| **~2027-04（预估）** | iOS 27 SDK 构建强制（WWDC26 已确认） | 未迁移 UIScene 生命周期的应用**无法启动**；启动屏强制 |

> iOS 27 要求已确认 — 详见 [docs/ios27-preview.md](docs/ios27-preview.md)（第三阶段前瞻）。
>
> 📅 **每个时间节点该适配什么，一页看全**：[docs/timeline.zh.md](docs/timeline.zh.md)（[English](docs/timeline.md)）

## 更新日志

| 版本 | 日期 | 主要更新 |
|------|------|---------|
| **[v1.12.0](CHANGELOG.zh.md)** | 2026-08-03 | 零遗漏引擎：50 项覆盖总账、启动屏/扩展/第三方 SDK 扫描规则、报告内置人工核对清单与上线门禁、覆盖矩阵文档 |
| **[v1.11.0](CHANGELOG.zh.md)** | 2026-08-03 | 推广版发布：适配影响声明（低冲击承诺）、时间线与适配范围总览文档、技能安装指南 |
| **[v1.10.0](CHANGELOG.zh.md)** | 2026-08-03 | iOS 27 前瞻大更新：Xcode 27 环境要求、代码级 P1 风险、Beta 已知问题、TN3187；SKILL.md 断链修复 |
| **[v1.9.2](CHANGELOG.zh.md)** | 2026-08-03 | README 补齐 INTEGRATION.md 引用（结构树/链接/文档表） |
| **[v1.9.1](CHANGELOG.zh.md)** | 2026-07-30 | 第三阶段检查清单（中英）、iOS 26 实战坑测试用例、README/INTEGRATION 文档同步 |
| **[v1.9.0](CHANGELOG.zh.md)** | 2026-07-30 | iOS 27 前瞻文档（第三阶段）、iOS 26 运行时坑 + iOS 27 前瞻扫描规则、FAQ iOS 27 章节 |
| **[v1.8.0](CHANGELOG.zh.md)** | 2026-07-30 | `windows`/`statusBarFrame` 扫描规则、第二阶段待办提醒、扫描器崩溃/误报修复 |
| **[v1.7.0](CHANGELOG.zh.md)** | 2026-06-02 | 纯 Swift 项目支持、AssetsLibrary 规则、项目类型自动检测 |
| **[v1.6.0](CHANGELOG.zh.md)** | 2026-05-12 | Liquid Glass 键盘工具栏适配器、键盘扫描规则、第二阶段检查清单更新 |
| **[v1.5.0](CHANGELOG.zh.md)** | 2026-05-06 | Privacy Manifest 模板、Swift 6 并发适配模板、第三方 SDK 兼容性速查表、单元测试、CI |
| **[v1.4.0](CHANGELOG.zh.md)** | 2026-05-06 | StoreKit 2、SiriKit→App Intents、SwiftUI 现代 API、Photos 扫描规则 |
| **[v1.3.0](CHANGELOG.zh.md)** | 2026-05-06 | Swift 6 并发、TLS 1.2、CoreData、Liquid Glass 结构影响扫描规则 |
| **[v1.1.0](CHANGELOG.zh.md)** | 2026-04-14 | 生产模板、扫描脚本、FAQ、AGENTS.md |
| **[v1.0.0](CHANGELOG.zh.md)** | 2026-04-10 | 初始发布 — 两阶段策略、双语文档、检查清单 |

> [查看完整更新日志 →](CHANGELOG.zh.md)

## 两阶段适配（+ 第三阶段前瞻）

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

### 第三阶段前瞻：iOS 27 强制要求（WWDC26 已确认）

**目标**: 在 iOS 27 SDK 构建强制前（预估 ~2027-04）完成准备

**关键要求**（详见 [docs/ios27-preview.md](docs/ios27-preview.md)）:
- UIScene 生命周期强制 — 未迁移的应用用 iOS 27 SDK 构建后**无法启动**
- 启动屏强制 — 缺少启动屏配置将被 App Store 拒审
- `canOpenURL` 弃用；`LSApplicationQueriesSchemes` 上限减半至 25 条
- Xcode 27 移除 `-ld_classic` 链接器

> 完成第一阶段的 SceneDelegate 迁移，就已满足 iOS 27 最大的强制要求。

## 使用方式

### 方式1：安装为 AI 技能（推荐）

一次安装，之后只需对 AI 说“帮我适配 iOS 26/27”——它会扫描、规划，并在[低冲击承诺](#适配影响承诺低冲击保证)下直接修改你的主项目。

**Claude Code**（本仓库本身就是 SKILL.md 格式的原生技能）：

```bash
# 安装到用户技能目录
git clone https://github.com/luodeCoding/ios26-adaptation-skill.git ~/.claude/skills/ios26-adaptation

# 然后在你的 iOS 项目里直接说：
#   “帮我适配 iOS 26”
```

**Qoder / 其他 Agent 工具**：从本仓库的 GitHub 地址安装为插件/技能；
或者克隆到任意位置后让 Agent 指向该目录——`SKILL.md` + `AGENTS.md` 包含 Agent 所需的全部知识。

```
开发者: "帮我适配 iOS 26"
AI: 读取 SKILL.md → 扫描主项目 → 列出文件改动清单 → 修改主项目文件 → 重扫验证
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

> 两种方式的详细工作流、注意事项和文件用途表见 [INTEGRATION.md](INTEGRATION.md)。

## 项目结构

```
ios26-adaptation-skill/
├── README.md              # 英文版
├── README.zh.md           # 本文件（中文版）
├── SKILL.md               # 📘 AI 核心技能文档（详细适配指南）
├── AGENTS.md              # 🤖 Claude Code Agent 使用指南
├── INTEGRATION.md         # 🔗 使用说明（本仓库与主项目的关系）
├── CHANGELOG.md           # 版本历史（英文）
├── CHANGELOG.zh.md        # 版本历史（中文）
├── LICENSE                # MIT 许可证
│
├── docs/                  # 📚 文档
│   ├── faq.md             # 常见问题
│   ├── coverage.md / .zh.md # 50 项覆盖矩阵（零遗漏总账镜像）
│   ├── timeline.md / .zh.md # iOS 26/27 时间线与各阶段适配范围
│   ├── testing-guide.md   # 测试指南
│   ├── sdk-compatibility.md # 第三方 SDK 兼容性速查表
│   └── ios27-preview.md   # iOS 27 / Xcode 27 适配前瞻（第三阶段）
│
├── .claude/               # 🎯 Claude 专用指南
│   └── iOS26-适配框架指南.md
│
├── examples/              # ✅ 检查清单
│   ├── phase1-checklist.md / .zh.md
│   ├── phase2-checklist.md / .zh.md
│   └── phase3-checklist.md / .zh.md
│
├── scripts/               # 🔍 扫描脚本
│   ├── ios26-scanner.py   # 废弃 API 扫描器（50+ 条规则，三层检测）
│   ├── adaptation-ledger.json # 覆盖总账：50 项适配项（唯一事实源）
│   └── test_scanner.py    # 扫描器单元测试 + 总账一致性测试
│
└── templates/             # 📋 代码模板（仅参考，不编译）
    ├── PrivacyInfo.xcprivacy  # Privacy Manifest 模板
    ├── swift/             # Swift 模板（窗口访问、SceneDelegate、
    │                      #   Swift 6 并发、Liquid Glass 适配器等）
    ├── objc/              # Objective-C 模板（覆盖范围相同）
    └── mixed/             # 混编项目桥接方案
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
# 扫描主项目的废弃 API（50+ 条规则：iOS 26 + iOS 27 前瞻）
python3 scripts/ios26-scanner.py /path/to/your/ios/project

# 输出 JSON 报告
python3 scripts/ios26-scanner.py /path/to/your/ios/project --format json --output report.json
```

覆盖范围：窗口访问（`keyWindow` / `windows` / `statusBarFrame`）、SceneDelegate 架构、通知选项、iOS 26 运行时坑（`tabBar` KVC 闪退、`navigationBar addSubview`），以及 iOS 27 前瞻检查（`canOpenURL`、`-ld_classic`、`LSApplicationQueriesSchemes` 上限、ODR、MetricKit）。项目级检查新增**启动屏强制项（含生成式 Info.plist）**、App 扩展、第三方 SDK 清单；每份报告末尾附**人工核对清单**与**上线门禁（SHIP-01~05）**。完整规则参考见 [SKILL.md](SKILL.md)，全量适配项矩阵见 [docs/coverage.zh.md](docs/coverage.zh.md)。

### AI 技能文档

| 文档 | 用途 |
|------|------|
| `SKILL.md` | 完整适配指南、决策流程、代码示例、AI 影响边界规则 |
| `AGENTS.md` | Claude Code 工作流、触发条件、检查清单、最小冲击规则 |
| `INTEGRATION.md` | 使用说明、适配影响声明、文件用途表 |
| `docs/timeline.md` / `.zh.md` | iOS 26/27 每个时间节点及对应的适配范围 |
| `docs/coverage.md` / `.zh.md` + `scripts/adaptation-ledger.json` | 50 项覆盖矩阵 — AI 必须逐项执行的零遗漏任务清单 |
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
- [App Store 即将生效的要求](https://developer.apple.com/news/upcoming-requirements/)
- [迁移到 UIKit 场景生命周期](https://developer.apple.com/documentation/uikit/transitioning-to-the-uikit-scene-based-life-cycle)

## 许可证

MIT 许可证 - 详见 LICENSE 文件

---

**作者**: roder
