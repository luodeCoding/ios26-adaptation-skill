# 更新日志

本项目的所有重要变更都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)。

## [Unreleased]

## [1.9.1] - 2026-07-30

### 新增
- **新增检查清单 `examples/phase3-checklist.md` / `.zh.md`** — iOS 27 准备检查清单（第三阶段前瞻）：UIScene 强制、启动屏四键、`canOpenURL` 迁移、链接器/构建链检查、布局现代化，并标注对应扫描规则 ID
- **第二阶段检查清单（中英）**：新增 iOS 26 运行时坑检查项 — 无 `tabBar` 私有 KVC、无直接 `navigationBar addSubview`、`AlwaysOriginal` 着色、布局不依赖 `statusBarFrame`
- **测试指南 (`docs/testing-guide.md`)**：新增 iOS 26 实战坑测试用例（自定义 TabBar 闪退、导航栏叠加视图、右侧按钮顺序、图片按钮着色）及第三阶段前瞻测试章节

### 修复
- **README.md / README.zh.md**：从滞后的 v1.6.0 状态同步 — 版本号、v1.7-v1.9 更新日志行、iOS 27 截止日期行、第三阶段前瞻章节、当前项目结构（混编模板、docs 新文档、第三阶段清单、测试套件）、扫描器覆盖范围概述、资源链接
- **INTEGRATION.md**：文件用途表与扫描内容列表更新为实际的 v1.9 规则集（此前仅列出最初的 6 项检查）

## [1.9.0] - 2026-07-30

### 新增
- **新增文档 `docs/ios27-preview.md`** — iOS 27 / Xcode 27 适配前瞻（第三阶段），依据 WWDC26 Session 278 + Apple 官方文档及社区实战反馈整理。涵盖 UIScene 生命周期强制（未迁移直接 fail to launch）、启动屏强制、`canOpenURL` 弃用 + `LSApplicationQueriesSchemes` 上限 50→25、构建链移除项（`-ld_classic`、Clang module 去重、ODR、MetricKit）、布局 `resize` 变化，以及三阶段时间线。
- **扫描器新规则 (`scripts/ios26-scanner.py`)**
  - iOS 26 运行时实战坑：`TABBAR-001`（私有 KVC `setValue:forKey:@"tabBar"` 闪退，Error）、`NAVBAR-001`（直接 `navigationBar addSubview`，Warning）、`BARBUTTON-001`（`rightBarButtonItems` 顺序/间距，Info）
  - iOS 27 前瞻：`OPENURL-001`（`canOpenURL` 弃用，Info）、`ODR-001`（`NSBundleResourceRequest`，Warning）、`METRICKIT-001`（`MXMetricManager`，Warning）
  - 项目级：`LINKER-001`（`.xcconfig`/`.pbxproj` 中的 `-ld_classic`，Warning）、`OPENURL-002`（`LSApplicationQueriesSchemes` 超过 25 条上限，Warning）
  - 注释行过滤扩展到新的行为类规则，避免误报
- **SKILL.md**：新增 iOS 27 截止日期行 +“iOS 27 已在 WWDC26 确认”小节、第二阶段“iOS 26 运行时实战坑”表、三张新的扫描规则参考表，以及内部/外部资源链接（conorluddy/LiquidGlassReference、fatbobman、博客园 weicy）
- **FAQ**：新增 Q25b-Q25e（iOS 26 运行时坑：tabBar KVC 闪退、navigationBar addSubview、AlwaysOriginal 蓝色 tint、statusBarFrame 为 0），以及全新“iOS 27 前瞻”章节 Q36-Q39（UIScene 强制、启动屏、`canOpenURL` 迁移、构建链变更）
- **AGENTS.md**：新增 iOS 27 前瞻触发词
- **测试**：新增 12 个单元测试，覆盖新增的代码级与项目级规则（共 47 个，全部通过）

## [1.8.0] - 2026-07-30

### 新增
- **扫描器新规则 (`scripts/ios26-scanner.py`)**
  - `WINDOW-007/008` — 检测已弃用的 `UIApplication.shared.windows` / `[UIApplication sharedApplication].windows`（iOS 15 起弃用）
  - `STATUS-004` — 检测已弃用的 `statusBarFrame` 访问（自动跳过现代替代写法 `statusBarManager.statusBarFrame`）
  - `PHASE2-001` — 项目级提醒：Info.plist 中存在 `UIDesignRequiresCompatibility` 时提示第二阶段待办（Xcode 27 前必须完成）
  - 部署目标检测新增 `.pbxproj` 回退：无 Podfile 声明时解析 `IPHONEOS_DEPLOYMENT_TARGET`（取最低值）
- **SKILL.md**：扫描规则参考与实际规则集同步 — 补充 `WINDOW-007/008`、`STATUS-003/004`、`ASSETSLIBRARY-001/002/003`，并新增“项目级检查”表（`PRIVACY-001`、`ARCH-001/002/003`、`PHASE2-001`）
- **FAQ**：新增 Q19a（`UIApplication.shared.windows` / `statusBarFrame` 弃用说明）
- **测试**：新增 8 个单元测试，覆盖新规则、`.pbxproj` 部署目标解析和误报过滤（共 35 个）

### 修复
- **扫描器崩溃**：纯 Swift 项目无 Podfile/pbxproj 部署目标时，架构严重级判断中 `None >= 13.0` 比较导致 `TypeError`
- **扫描器误报**：`WINDOW-003` 跳过过滤器仅匹配旧的 `UIApplication+Extension` 文件名 — 现已同时匹配实际模板名 `UIApplication+MainWindow`
- **FAQ 编号重复**：两个 Q25、测试/策略章节重复使用 Q19-Q23 — 重新编号为 Q25a 和 Q31-Q35
- **FAQ 模板路径错误**：`templates/*/UIApplication+Extension.*` 修正为实际的 `UIApplication+MainWindow.*` 文件名
- **SKILL.md**：Swift 示例标题由 `UIApplication+Extension.swift` 改为 `UIApplication+MainWindow.swift`，与实际模板一致
- **CHANGELOG.zh.md**：补齐缺失的 1.7.0 版本记录

## [1.7.0] - 2026-06-02

### 新增
- **纯 Swift 项目适配支持**
  - `templates/swift/SceneDelegate+SwiftOnly.swift` — 简化版 SceneDelegate，无 @objc 注解，带 @MainActor 适配 Swift 6
  - `templates/swift/AppDelegate+SwiftOnly.swift` — 纯 Swift AppDelegate，使用 `static let shared` 替代 `@objc static let shared` / `sharedInstance`
  - 更新 `templates/swift/UIApplication+MainWindow.swift`，增加 `@MainActor` 和跨语言使用注释
- **扫描器改进 (`scripts/ios26-scanner.py`)**
  - `ASSETSLIBRARY-001/002/003` — 检测 `import AssetsLibrary`、`#import <AssetsLibrary/AssetsLibrary.h>` 和 `ALAssetsLibrary` 使用（Error 级别）
  - `detect_project_type()` — 自动检测纯 Swift / 混合 / Objective-C 项目及部署目标
  - ARCH-001/002 严重级根据项目类型自适应：纯 Swift iOS 13+ 项目无 SceneDelegate 时从 Error 降级为 Warning（向后兼容仍可用，但 iOS 27 将强制迁移）
  - SCREEN-001/002 误报过滤：跳过 `Pods/`、`Vender/`、`vendor/`、`ThirdParty/` 目录
  - ARCH-003 建议文案更新，针对 Swift 项目提及 `static let shared`
- **文档更新**
  - SKILL.md：Swift Projects 章节新增“Pure Swift Project Notes (iOS 26+)”
  - FAQ：新增 Q5a（纯 Swift SceneDelegate 迁移）、Q14a（ALAssetsLibrary 编译错误）

## [1.6.0] - 2026-05-12

### 新增
- **Keyboard Liquid Glass 工具栏适配器**: `templates/swift/UITextInput+LiquidGlassAdapter.swift` 和 `templates/objc/UITextInput+LiquidGlassAdapter.h/.m`
  - 可选的 `lg_clearLiquidGlassAccessoryIfNeeded()` 扩展，用于 `UITextField` / `UITextView`
  - 在 iOS 26+ 上清除默认的 `inputAccessoryView`，当玻璃拟态键盘工具栏在视觉上具有干扰性时
  - 在 SKILL.md 第二阶段中记录了按控件 / 子类 / 全局扫描的策略表
- **键盘适配扫描规则**:
  - `KEYBOARD-001` — 检测自定义 `UITextField` 子类
  - `KEYBOARD-002` — 检测自定义 `UITextView` 子类
  - `KEYBOARD-003` — 检测 `inputAccessoryView` 赋值
- **AGENTS.md 更新**: 在标准工作流中增加了 `inputAccessoryView`、自定义文本输入扫描；在必查项中增加了自定义文本输入检查
- **第二阶段检查清单** (中英文): 增加了 Liquid Glass 工具栏决策和自定义文本输入扫描项

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
