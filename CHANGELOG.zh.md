# 更新日志

本项目的所有重要变更都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)。

## [1.5.0] - 2026-05-06

### 新增
- **`templates/PrivacyInfo.xcprivacy`** — Privacy Manifest 模板，包含 Required Reason API 声明和数据收集示例
- **`templates/swift/Swift6ConcurrencyAdapter.swift`** — Swift 6 严格并发迁移模式（@MainActor、@Sendable、async/await、全局 Actor）
- **`docs/sdk-compatibility.md`** — 第三方 SDK iOS 26 兼容性速查表（Firebase、Facebook、RevenueCat、Branch 等）
- **`scripts/test_scanner.py`** — 单元测试套件，覆盖全部 19 条扫描规则 + 架构检查 + 完整项目扫描
- **`.github/workflows/ci.yml`** — GitHub Actions CI 流水线（扫描器测试、Python 代码检查、Markdown 链接验证）

## [1.4.0] - 2026-05-06

### 新增（第二轮 QA 差距分析）
- **Privacy Manifest 覆盖**：`PRIVACY-001` 扫描规则检测缺失的 `PrivacyInfo.xcprivacy`；文档说明 Required Reason API 和第三方 SDK 声明
- **StoreKit 1 → StoreKit 2**：`STOREKIT-001` 扫描规则检测已移除的 StoreKit 1 API；SKILL.md 和 FAQ 包含迁移表和双路径指导
- **SiriKit → App Intents**：`SIRIKIT-001` 扫描规则检测废弃的 SiriKit intent domain；FAQ 涵盖 Xcode 自动转换
- **SwiftUI 现代 API**：`SWIFTUI-001/002/003` 扫描规则检测 `NavigationView`、`.cornerRadius()`、`.foregroundColor()`；SKILL.md 包含完整替换表
- **Photos 迁移**：`PHOTOS-001` 扫描规则检测 `UIImagePickerController`；FAQ 提供 `PHPickerViewController` 示例代码
- 新增 FAQ 条目（Q26-Q30）：Privacy Manifest、StoreKit 2、SiriKit、SwiftUI 废弃 API、PHPicker

## [1.3.0] - 2026-05-06

### 新增（第一轮 QA 差距分析）
- **QA 差距分析**：对照最新 iOS 26 SDK 文档和社区迁移指南进行扫描
- `scripts/ios26-scanner.py` 新增扫描规则：
  - `SCREEN-001/002` — `UIScreen.main` 废弃检测
  - `WEB-001` — 已移除的 `UIWebView` 检测
  - `TLS-001` — 旧版 TLS 1.0/1.1 检测
  - `COREDATA-001` — 已移除的 CoreData iCloud 同步 key 检测
  - `SWIFT6-001` — Swift 6 严格并发信息标记
- `docs/faq.md` 新增 FAQ 条目（Q19-Q25）：Swift 6 并发、TLS 1.2、CoreData key、TabBar safeArea、UIDropShadowView、背景色冲突
- `SKILL.md` 新增章节："Additional iOS 26 SDK Changes"，涵盖 Swift 6、TLS、CoreData、Liquid Glass 结构影响
- 更新 `docs/testing-guide.md`，增加 TabBar safeArea、UIDropShadowView 和背景冲突测试用例

### 修复
- **自引用废弃 API**：`SKILL.md` 和 `templates/swift/AppDelegate+Setup.swift` 示例中标注 iOS 12 fallback 路径的 `UIScreen.main` 使用
- **关键修正**：`UNNotificationPresentationOptionAlert` 在 **iOS 14.0** 就已废弃，而非 iOS 26.0 — 更新所有模板和文档
- **关键修正**：`UNAuthorizationOptionAlert` 在 iOS 26 SDK 中**未被废弃** — 从所有模板中移除替换逻辑
- 移除 `NOTIF-002` 扫描规则（曾误将 `UNAuthorizationOptionAlert` 标记为废弃）
- 更新 `AGENTS.md` 语言特定说明，提供更清晰的混合项目指导
- 修复 `AGENTS.md` 中的模板文件名引用（`UIApplication+MainWindow`、`UNNotificationOptions+Adapter`）

## [1.1.0] - 2026-04-14

### 新增
- `templates/` 目录，包含可用于生产的 Swift 和 Objective-C 代码模板：
  - `UIApplication+Extension`（统一窗口/导航访问）
  - `SceneDelegate`（完整生命周期和 URL 转发实现）
  - `AppDelegate+Setup`（双路径重构示例）
  - `NotificationAdapter`（集中式通知选项适配器，用于废弃 API 变更）
- `scripts/ios26-scanner.py` — 自动化项目扫描器，检测废弃 API 和架构缺陷
- `docs/faq.md` — 全面 FAQ，涵盖策略、构建错误和 Liquid Glass
- `AGENTS.md` — Claude Code 集成的 Agent 使用指南
- `SKILL.md` 中完整的 Swift 实现示例（AppDelegate + SceneDelegate + UIApplication Extension）
- `SKILL.md` 中的 `UNAuthorizationOptionAlert` 代码替换示例

### 修复
- `README.zh.md` 中的树形结构格式
- `SKILL.md` 中的 Objective-C 代码示例，使用实例方法语法（`[[UIApplication sharedApplication] mainWindow]`）

## [1.0.0] - 2026-04-10

### 新增
- iOS 26 适配 Skill 初始发布
- 全面的两阶段适配策略（SDK 构建 & Liquid Glass）
- 废弃 API 项目扫描规则
- 基于发布时间线的决策流程图
- 双语文档（英文 & 中文）
- 第一阶段 & 第二阶段检查清单
- 用于 Claude Code 集成的 SKILL.md

### 功能
- 📋 两阶段适配策略指南
- 🔍 废弃 API 扫描规则（keyWindow、通知选项等）
- 📊 基于发布时间线的决策流程图
- ✅ 两个适配阶段的详细检查清单
- 🌐 完整双语支持（英/中）

### 文档
- README.md - 快速入门指南（英文）
- README.zh.md - 快速入门指南（中文）
- SKILL.md - 详细技能文档
- .claude/iOS26-适配框架指南.md - 完整适配框架（中文）
- docs/testing-guide.md - QA 团队测试指南
- examples/phase1-checklist.md - 第一阶段执行检查清单（英文）
- examples/phase1-checklist.zh.md - 第一阶段执行检查清单（中文）
- examples/phase2-checklist.md - 第二阶段执行检查清单（英文）
- examples/phase2-checklist.zh.md - 第二阶段执行检查清单（中文）

---

**作者**: roder
