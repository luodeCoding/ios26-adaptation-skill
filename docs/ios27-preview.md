# iOS 27 / Xcode 27 适配前瞻（Phase 3 预告）

> **最后更新**: 2026-07-30
> **信息来源**: WWDC26 (2026-06)、Apple 官方文档、iOS 27 Beta Release Notes
> **状态**: iOS 27 处于 Beta 阶段，正式版预计 2026-09 随 Xcode 27 发布

本文档梳理 WWDC26 已**官方确认**的 iOS 27 / Xcode 27 强制要求与高风险变更。
如果你正在做 iOS 26 适配（本技能库的 Phase 1/2），**强烈建议同时读完本文**——
iOS 26 的 SceneDelegate 迁移与 iOS 27 的强制要求是同一条演进线，一次做对可以避免明年返工。

---

## ⚠️ 一句话总结

| 变更 | 级别 | 后果 | 与本技能库的关系 |
|------|------|------|----------------|
| UIScene 生命周期**强制** | 🔴 P0 | iOS 27 SDK 构建且未迁移 → **App 直接无法启动** | Phase 1 的 SceneDelegate 迁移就是为此做准备 |
| 启动屏四选一 Info.plist 键**强制** | 🔴 P0 | 缺失 → **App Store 提审被拒** | 新增检查项 |
| `-ld_classic` / ld64 链接器**移除** | 🔴 P0 | 引用未清 → **编译失败**，CI 中断 | 新增检查项（LINKER-001） |
| Clang module 同名去重**强制** | 🔴 P0 | 重复 `module.modulemap` → 编译失败 | 手动排查 |
| `canOpenURL(_:)` **废弃** + allowlist 上限 50→25 | 🟡 P1 | 链接 iOS 27 SDK 后超出 25 条的 scheme 静默返回 false | 新增检查项（OPENURL-001/002） |
| On Demand Resources（`NSBundleResourceRequest`）**废弃** | 🟡 P1 | 后续版本可能移除 | 新增检查项（ODR-001） |
| `MXMetricManager` → `MetricManager` | 🟡 P1 | MetricKit 框架级重构 | 新增检查项（METRICKIT-001） |
| idiom / orientation 不再适合布局判断 | 🟡 P1 | iPhone App 在 iPad 上全尺寸可调，须改用 size classes | 手动 Review |

---

## 1. UIScene 生命周期强制（最高优先级）

Apple 官方原文（[Transitioning to the UIKit scene-based life cycle](https://developer.apple.com/documentation/UIKit/transitioning-to-the-uikit-scene-based-life-cycle)）：

> "Beginning in iOS 27, iPadOS 27, Mac Catalyst 27, tvOS 27, and visionOS 27,
> apps built with the latest SDK must adopt the scene-based life cycle
> **or they fail to launch**."

WWDC26 Session 278《Modernize your UIKit app》(2:36) 措辞同样直接：

> "UIScene lifecycle is now required when building with the latest SDKs.
> Without it, your application will no longer launch."

### 关键事实

- **不是废弃，不是警告，是无法启动**（用户看到的是闪退）。
- 触发条件是**你构建所用的 SDK**，不是用户的系统版本：已上架的 iOS 26 SDK 构建的二进制在 iOS 27 上照常运行；一旦用 Xcode 27 重新构建，强制要求随之生效。
- 警告早已开始：iOS 18.4 起 UIKit 就为未迁移的 App 输出迁移日志，iOS 26 中日志措辞升级，iOS 27 中日志变成启动失败。

### 两条件判定法（满足任一即需迁移）

1. `Info.plist` 中**没有** `UIApplicationSceneManifest` 键（或键存在但无有效 configuration）；
2. AppDelegate **没有**实现 scene-configuration 方法
   （`application(_:configurationForConnecting:options:)`）。

本技能库扫描器的 `ARCH-001` / `ARCH-002` 规则即对应这两个条件。

### 最小迁移路径

- **静态路由**（推荐）：在 Info.plist 添加 `UIApplicationSceneManifest` 配置（Xcode 中位于 target General → Deployment Info → Scene manifest）。
- **动态路由**：在 AppDelegate 中实现 scene-configuration 方法，按 `session.role` 返回不同配置。
- 注意配置时应指定 **`UIWindowScene`** 而不是 `UIScene`；CarPlay 场景使用专属的 template-application scene type。
- **多窗口/多 Scene 支持仍然是可选的**——强制的只是生命周期本身，不要求你的数据模型 scene 化。

👉 直接复用本技能库的模板即可满足要求：
`templates/swift/SceneDelegate.swift`、`templates/objc/SceneDelegate.h/.m`、
`templates/swift/AppDelegate+Setup.swift`（含生命周期转发）。

### Xcode 27 的官方迁移工具

Xcode 27 内置 **app modernization agent skill**：可自动把 App 转换到 scene 生命周期、
把 `UIScreen.main` 调用改写为 trait collection / scene bounds、把 orientation 判断改写为
size classes；复杂场景会提问，未完成的部分留注释。可通过
`xcrun agent skills export` 导出为 markdown 供其他 AI 工具使用。
（照例：Review 它产出的 diff，尤其是状态恢复和 window 初始化部分。）

---

## 2. 启动屏四选一强制（提审门槛）

iOS 27 Release Notes 原文：

> "iOS and iPadOS apps built with the 27.0 SDK or later are required to include
> a launch screen. Your app's Info.plist must contain one of the following keys:
> `UILaunchStoryboardName`, `UILaunchStoryboards`, `UILaunchScreen`, or
> `UILaunchScreens`. Apps that don't include a launch screen are **rejected**."

### 关键事实

- 后果是**提审被拒**（发生在 App Store Connect），不是运行时失败。
- 范围仅 **iOS / iPadOS**，未提及 tvOS、visionOS、Mac Catalyst。
- 四个键怎么选：有 LaunchScreen.storyboard → `UILaunchStoryboardName`（唯一的字符串型键）；
  没有 storyboard → `UILaunchScreen` 字典（空字典也合规）；
  复数形式（`UILaunchScreens`/`UILaunchStoryboards`）仅用于按 URL scheme 显示不同启动屏的少见场景。
- **高危人群**：仍在用 `UILaunchImages`（iOS 13 已废弃）的老项目——它不在四键之列，
  十年的 Xcode 升级也不会自动帮你补一个。

### ⚠️ grep 查不到不等于没配置

Xcode 13+ 模板默认使用**生成式 Info.plist**（`GENERATE_INFOPLIST_FILE = YES`），
启动屏由构建设置 `INFOPLIST_KEY_UILaunchScreen_Generation = YES` 在构建时写入，
**仓库里任何文件都搜不到这四个键**。正确的审计方法是问构建系统：

```bash
xcodebuild -showBuildSettings \
  -project YourApp.xcodeproj -target YourApp \
  -configuration Release -sdk iphoneos 2>/dev/null \
  | grep -E "^ +(GENERATE_INFOPLIST_FILE|INFOPLIST_FILE|INFOPLIST_KEY_UILaunch)"
```

- `GENERATE_INFOPLIST_FILE = YES` 且 `INFOPLIST_KEY_UILaunchScreen_Generation = YES` → 合规；
- `GENERATE_INFOPLIST_FILE = NO` → 打开 `INFOPLIST_FILE` 指向的文件确认四键之一存在。

`-configuration Release` 和 `-sdk iphoneos` 都不能省：审核看的是 Release 产物，
且多平台 target 的这些设置按 SDK 分别声明。

---

## 3. canOpenURL 废弃 + allowlist 上限减半

iOS 27 Beta Release Notes 原文：

> "canOpenURL: is deprecated. Attempt to open the URL and handle any failure
> instead of validating it first."

### 关键事实

- `canOpenURL(_:)` 在 27.0 标记废弃（iOS/iPadOS/Mac Catalyst/tvOS/visionOS 全平台），
  暂无移除版本，参考 `openURL(_:)` 的先例（废弃十年后变成"调用无效果"而非移除）。
- **真正有牙齿的是数字**：`LSApplicationQueriesSchemes` 上限从 50 条降到 **25 条**，
  触发条件是**链接 iOS 27 SDK**。超出部分的行为未见文档说明，最可能是静默返回 false
  ——与"目标 App 未安装"无法区分。
- 替代模式是 **attempt-and-handle**：`open(_:options:completionHandler:)`
  **不受 allowlist 约束**，完全迁移后可直接删掉 `LSApplicationQueriesSchemes` 键。

```swift
// Before: 先验证再打开（需要 Info.plist 声明）
if UIApplication.shared.canOpenURL(url) {
    UIApplication.shared.open(url)
} else {
    presentWebFallback()
}

// After: 直接尝试，失败兜底（无需声明）
let opened = await UIApplication.shared.open(url)
if !opened {
    presentWebFallback()
}
```

### 两个结构性差异（迁移前必读）

1. **同步 → 异步 + 主线程**：`canOpenURL` 是 `nonisolated` 的同步 Boolean，可在任意线程
   渲染前做判断；`open` 是 `@MainActor` 异步方法。模型层/后台队列里的"先验证再决定 UI"
   逻辑需要重构。
2. **无法私下询问**：attempt 成功的副作用是**对方 App 被拉到前台**。
   "只在装了某 App 时才显示入口"这类模式失去了直接等价物。
   幸存的存在性检查是 `universalLinksOnly` 选项（iOS 10 起，未废弃，仅限 Universal Link）：

```swift
// 存在性检查，App 未安装时无任何可见副作用
let installed = await UIApplication.shared.open(
    url, options: [.universalLinksOnly: true]
)
```

### 行动建议

- 清点 `LSApplicationQueriesSchemes` 条目数：> 25 条的 App **必须**在链接 iOS 27 SDK 前裁剪或迁移。
- 逐步把 `canOpenURL` + `open` 的组合改为 attempt-and-handle。
- App 安装检测类需求评估迁移到 Universal Link + `universalLinksOnly`。

---

## 4. 构建链 P0 风险

### 4.1 -ld_classic / ld64 链接器完全移除

Xcode 27 中 ld64 被彻底移除，`-ld_classic` 选项不再支持——引用未清理会**直接编译失败**。
这个 flag 常见于 Xcode 15 时代为绕过新链接器 bug 而添加的 workaround。

```bash
# 快速检查
grep -r "ld_classic" --include="*.xcconfig" --include="*.pbxproj" .
```

依赖旧链接器行为的三方库（常见于闭源 .a/.framework）需升级到兼容版本。

### 4.2 Clang module 同名去重强制

Swift 依赖扫描器要求单次 scan action 中所有可达的 Clang module 名称唯一，
重复声明（常见于三方源码自带的 `module.modulemap` 重新声明了 SDK 模块）会导致编译失败。

```bash
find . -name "module.modulemap" -not -path "*/build/*" | sort
```

### 4.3 On Demand Resources 废弃

`NSBundleResourceRequest` / ODR 已废弃，迁移目标是 **Background Assets** 框架
（支持路径通配、文件排除、自定义子路径、本地化资源包）。

```bash
grep -r "NSBundleResourceRequest" --include="*.swift" --include="*.m" .
```

### 4.4 MetricKit 框架级重构

`MXMetricManager` → `MetricManager`（异步序列接收指标）、`MetricReport`（Codable + Sendable）、
`DiagnosticReport`、`MetricResult`。旧 API 全面替换，性能监控 SDK 需同步升级。

---

## 5. 布局层：一切皆可 resize

iOS 27 中 iPhone Mirroring 窗口在 Mac 上自由缩放、iPhone-only App 在 iPad 上
"像任何 iPad App 一样完全可调大小"。Session 278 给出的排查清单：

| 旧写法 | 问题 | 新写法 |
|--------|------|--------|
| `UIScreen.main`（任何引用） | scene 可能在别的显示器上，返回错误信息 | 通过 window 的 windowScene 动态获取，或彻底移除 |
| `UIScreen.main.scale` | 同上 | `traitCollection.displayScale` |
| `UIScreen.main.bounds` | 同上 | windowScene 的 effective geometry 或父视图 size |
| `userInterfaceIdiom` 做布局判断 | iPhone App 在 iPad 上全尺寸可调但 idiom 仍报 phone | **size classes** |
| supported interface orientation | 可 resize 环境中系统忽略该偏好 | **size classes** |
| `UIRequiresFullscreen`（游戏） | iOS 27 起行为变为**离散 resize** | 每次 resize 过渡到匹配的屏幕配置 |

本技能库扫描器的 `SCREEN-001` / `SCREEN-002` 规则已覆盖 `UIScreen.main` 检测。
自动 trait 追踪（layoutSubviews 等方法内读取的 trait 变化时自动重调）可减轻迁移负担。
测试方面 Device Hub 与 Xcode Previews 新增 "enter resize mode" 可自由拖拽设备边缘。

---

## 6. 时间线与三阶段策略

```
2026-04-28          2026-09 (Xcode 27)              2027-04 (预估)
    │                     │                              │
    ▼                     ▼                              ▼
 Phase 1              Phase 2                        Phase 3
 iOS 26 SDK 构建      Liquid Glass 完整适配           iOS 27 SDK 构建强制
 SceneDelegate 迁移   移除 UIDesignRequires-          UIScene 强制生效
 弃用 API 替换        Compatibility                   启动屏四键强制
                                                     canOpenURL 迁移
                                                     构建链清理
```

**核心建议**：Phase 1 做 SceneDelegate 迁移时，直接按 iOS 27 的两条件判定法验收
（manifest + scene-configuration 方法齐备），Phase 3 的最大风险项就已提前消除。
参考历史规律，App Store 对 iOS 27 SDK 的强制期限预计在 **2027 年 4 月前后**。

---

## 7. 参考资源

### Apple 官方
- [Transitioning to the UIKit scene-based life cycle](https://developer.apple.com/documentation/UIKit/transitioning-to-the-uikit-scene-based-life-cycle) — UIScene 强制要求与迁移指南
- [Upcoming requirements — Apple Developer](https://developer.apple.com/news/upcoming-requirements/) — 官方截止日期权威来源
- WWDC26 Session 278 "Modernize your UIKit app" — UIScene 强制 + resize 适配
- [UILaunchScreen / UILaunchStoryboardName 文档](https://developer.apple.com/documentation/bundleresources/information-property-list/uilaunchscreen)

### 社区文章与开源项目
- [WWDC26 / iOS27 API 更新适配风险总结（lrdcq）](https://lrdcq.com/me/read.php/169.htm) — 中文，含 P0/P1/P2 分级与快速检查命令
- [conorluddy/LiquidGlassReference](https://github.com/conorluddy/LiquidGlassReference) — iOS 26 Liquid Glass Swift/SwiftUI 综合参考项目
- [记录我适配 iOS 26 遇到的一些问题（cnblogs weicy）](https://www.cnblogs.com/weicyNo-1/p/19157486) — tabBar KVC 闪退、导航栏 addSubview 失效等一线经验（详见 FAQ）
- [UIKit + SwiftUI 混合架构下的 Liquid Glass 适配实战（fatbobman）](https://fatbobman.com/zh/posts/grow-on-ios26/) — 18 万五星应用 Grow 的 Phase 2 实战经验

---

*本文档属于 iOS 26 Adaptation Skill 的一部分。iOS 27 正式版发布后本文将升级为完整的 Phase 3 适配指南。*
