# iOS 26 适配指南

<div align="right">
  <b>🌐 语言:</b> <a href="./README.md">English</a> | 中文
</div>

---

> **语言**: Objective-C / Swift  
> **平台**: iOS  
> **最低 iOS 版本**: 12.0+  
> **最后更新**: 2026-04-14

全面适配 iOS 26 SDK 和 Liquid Glass 设计语言的技能指南。

## 概览

Apple 要求所有在 **2026年4月28日** 之后提交的应用必须使用 iOS 26 SDK 构建。本指南提供：

- 📋 **两阶段适配策略** - SDK 构建适配 和 Liquid Glass 完整适配
- 🔍 **项目扫描规则** - 识别废弃 API 和需要的改动
- 📊 **决策流程图** - 根据你的时间安排选择合适的适配策略
- ✅ **检查清单** - 跟踪每个阶段的进度

## 关键时间节点

| 日期 | 要求 | 影响 |
|------|------|------|
| **2026-04-28** | 必须使用 iOS 26 SDK 构建 | 不合规将无法提交应用更新 |
| **~2026-09** | Xcode 27 发布，Liquid Glass 强制启用 | `UIDesignRequiresCompatibility` 将被移除 |

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

## 快速开始

### 1. 通过 CocoaPods 安装

在你的项目 `Podfile` 中添加：

```ruby
pod 'iOS26Adaptation', '~> 1.0'
```

然后运行：

```bash
pod install
```

> **为什么选择 CocoaPods？** 本包仅包含文档、代码模板和扫描脚本 —— **不会编译任何代码**到你的应用中。完成 iOS 26 适配并通过 bug 验证后，你可以安全地移除该 pod，对项目没有任何影响。

安装后，所有资源位于：

```
Pods/iOS26Adaptation/iOS26Adaptation.bundle/
├── templates/       # Swift 和 Objective-C 代码模板
├── scripts/         # ios26-scanner.py 扫描脚本
├── docs/            # FAQ 和测试指南
├── examples/        # 分阶段检查清单
└── *.md             # 文档
```

### 2. 确定你的策略

根据你的应用发布日期：

| 发布日期 | 推荐策略 |
|---------|---------|
| 2026-04-28 之前 | **策略 A**: 在新分支中适配，截止日期后合并 |
| 2026-04-28 ~ Xcode 27 | **策略 B**: 完成第一阶段，评估第二阶段 |
| Xcode 27 之后 | **策略 C**: 两个阶段的适配一起完成 |

### 3. 扫描你的项目

使用内置扫描脚本自动生成报告：

```bash
# 如果通过 CocoaPods 安装，从 bundle 中运行
python3 Pods/iOS26Adaptation/iOS26Adaptation.bundle/scripts/ios26-scanner.py /path/to/your/ios/project

# 或直接使用本仓库
python3 scripts/ios26-scanner.py /path/to/your/ios/project

# 生成 JSON 报告以供后续处理
python3 Pods/iOS26Adaptation/iOS26Adaptation.bundle/scripts/ios26-scanner.py /path/to/your/ios/project --format json --output report.json
```

扫描器会检查：
- 废弃 API（`keyWindow`、`delegate.window`、通知选项等）
- 是否缺少 `SceneDelegate` 或 `UIApplicationSceneManifest`
- `AppDelegate` 是否缺少 `sharedInstance` 方法

或手动搜索常见的废弃 API 模式：

```bash
# 常用搜索模式
grep -r "keyWindow" --include="*.swift" --include="*.m" --include="*.mm"
grep -r "delegate\.window" --include="*.swift" --include="*.m" --include="*.mm"
grep -r "UNNotificationPresentationOptionAlert" --include="*.swift" --include="*.m"
grep -r "UNAuthorizationOptionAlert" --include="*.swift" --include="*.m"
```

### 4. 应用代码模板

参考已安装 bundle 中的模板（或直接从本仓库 `templates/` 目录），复制到你的 Xcode 项目并根据需要调整类名：

| 模板 | Swift | Objective-C | 用途 |
|------|-------|-------------|------|
| `UIApplication+Extension` | [Swift](./templates/swift/UIApplication+Extension.swift) | [OC](./templates/objc/UIApplication+Extension.h) | 统一窗口/导航访问 |
| `SceneDelegate` | [Swift](./templates/swift/SceneDelegate.swift) | [OC](./templates/objc/SceneDelegate.h) | 窗口创建与生命周期转发 |
| `AppDelegate+Setup` | [Swift](./templates/swift/AppDelegate+Setup.swift) | [OC](./templates/objc/AppDelegate+Setup.h) | 双路径启动改造 |
| `NotificationAdapter` | [Swift](./templates/swift/NotificationAdapter.swift) | [OC](./templates/objc/NotificationAdapter.h) | iOS 26 通知选项适配 |

详细的集成说明请见 `Pods/iOS26Adaptation/iOS26Adaptation.bundle/templates/README.md`（或本仓库的 [`templates/README.md`](./templates/README.md)）。

### 5. 遵循检查清单

详见 [SKILL.md](./SKILL.md) 获取：
- 决策流程图
- 实施指南
- 分阶段检查清单
- 测试框架

### 6. 查看常见问题

遇到常见疑问？请参阅 [docs/faq.md](./docs/faq.md)，其中解答了：
- 是否需要修改 Deployment Target？
- CocoaPods 中包含废弃 API 怎么办？
- 是否只需在模拟器上测试？

## 项目结构

```
ios26-adaptation-skill/
├── README.md              # 本文件 - 快速入门指南
├── README.zh.md           # 中文版 README
├── SKILL.md               # 详细技能文档
├── CHANGELOG.md           # 版本历史
├── LICENSE                # MIT 许可证
├── AGENTS.md              # Claude Code Agent 使用指南
├── docs/
│   ├── testing-guide.md   # 测试团队测试指南
│   └── faq.md             # 常见问题解答
├── .claude/
│   └── iOS26-适配框架指南.md  # 完整适配框架指南（中文）
├── examples/
│   ├── phase1-checklist.md    # 第一阶段执行检查清单（英文）
│   ├── phase1-checklist.zh.md # 第一阶段执行检查清单（中文）
│   ├── phase2-checklist.md    # 第二阶段执行检查清单（英文）
│   └── phase2-checklist.zh.md # 第二阶段执行检查清单（中文）
├── scripts/
│   └── ios26-scanner.py   # 自动化项目扫描脚本
└── templates/
    ├── swift/                 # Swift 代码模板
    └── objc/                  # Objective-C 代码模板
```

## 常见误区

| 误区 | 事实 |
|-----|------|
| 必须将 Deployment Target 改为 iOS 26 | ❌ 不需要。保持你当前的最低版本（iOS 12/13 等） |
| 用户必须升级到 iOS 26 | ❌ 不需要。运行时要求由 Deployment Target 决定 |
| 现有应用版本将被下架 | ❌ 不会。仅影响新提交和更新 |
| 有宽限期 | ❌ 没有。2026年4月28日是硬性截止日期 |

## 核心概念

### SceneDelegate 架构（iOS 13+）

- **问题**: `UIApplication.keyWindow` 和 `AppDelegate.window` 在 iOS 13+ 中不可靠
- **解决方案**: 通过 `UIApplication` 扩展使用统一访问接口
- **影响**: 所有窗口访问必须通过新接口进行

### 废弃 API（iOS 26）

| 废弃 API | 替代方案 |
|---------|---------|
| `keyWindow` | 基于 SceneDelegate 的窗口访问 |
| `UNNotificationPresentationOptionAlert` | `UNNotificationPresentationOptionBanner \| List` |
| `UNAuthorizationOptionAlert` | `UNAuthorizationOptionBanner` |

### Liquid Glass 设计

- **是什么**: iOS 26 的新视觉语言
- **自动适配**: 标准 UIKit 控件自动获得新外观
- **自定义**: 自定义 UI 需要手动调整
- **时间线**: 第一阶段可选，第二阶段强制

## 决策检查清单

开始适配前，请回答以下问题：

- [ ] 下次应用发布计划是什么时候？
- [ ] 现在是否有可用的开发资源？
- [ ] SceneDelegate 是否已经配置？
- [ ] 项目中有多少废弃 API 调用？
- [ ] 是否使用了大量自定义 UI 组件？

## 资源

- [Apple Developer 新闻](https://developer.apple.com/news/)
- [iOS 26 发布说明](https://developer.apple.com/documentation/ios-release-notes)
- [Liquid Glass 设计指南](https://developer.apple.com/design/)

## 许可证

MIT 许可证 - 详见 LICENSE 文件

---

**作者**: roder
