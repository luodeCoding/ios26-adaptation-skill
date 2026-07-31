# 第三阶段检查清单：iOS 27 准备（前瞻）

> **截止时间**: iOS 27 SDK 构建强制前（**预估 ~2027-04**）  
> **目标**: 提前满足 WWDC26 已确认的 iOS 27 强制要求  
> **参考**: [docs/ios27-preview.md](../docs/ios27-preview.md)

以下所有条目均为**已确认要求**（WWDC26 / Apple 官方文档），不是猜测。大部分条目今天就可以用 iOS 26 工具链验证。

---

## P0 — 应用无法启动 / 编译失败

### UIScene 生命周期（强制）
- [ ] `Info.plist` 包含 `UIApplicationSceneManifest`
- [ ] AppDelegate 实现了 `application(_:configurationForConnecting:options:)`
- [ ] SceneDelegate 存在且所有生命周期事件转发到 AppDelegate
- [ ] iOS 13+ 上应用通过 scene 路径正常启动和运行
- [ ] 运行扫描器：无 `ARCH-001` / `ARCH-002` 问题

> 用 iOS 27 SDK 构建但未迁移 scene 生命周期的应用**无法启动**。完成本技能库第一阶段即已满足此要求。

### 链接器标志
- [ ] 所有 `.xcconfig`、`.pbxproj`、Podfile `post_install` 钩子中无 `-ld_classic` / `-ld64`（扫描规则 `LINKER-001`）
- [ ] 项目用现代链接器可正常链接（今天就去掉标志构建一次验证）

---

## P0 — App Store 拒审

### 启动屏（强制）
- [ ] `Info.plist` 包含以下四键之一：`UILaunchStoryboardName` / `UILaunchStoryboards` / `UILaunchScreen` / `UILaunchScreens`
- [ ] 若使用生成式 Info.plist：`xcodebuild -showBuildSettings | grep -i launch` 确认 `INFOPLIST_KEY_UILaunchScreen_Generation = YES`
- [ ] 无遗留 `UILaunchImages` 用法（已移除；迁移到 storyboard / `UILaunchScreen`）

---

## P1 — 需要迁移的弃用项

### canOpenURL → 直接尝试打开并处理失败
- [ ] 已盘点所有 `canOpenURL` 调用点（扫描规则 `OPENURL-001`）
- [ ] 尽可能迁移到 `open(_:options:completionHandler:)` 并处理失败回调
- [ ] `LSApplicationQueriesSchemes` 精简至 ≤ 25 条（扫描规则 `OPENURL-002`）
- [ ] 仅需检查 Universal Link 的场景考虑 `universalLinksOnly` 选项

### On Demand Resources
- [ ] 已盘点 `NSBundleResourceRequest` 用法（扫描规则 `ODR-001`）
- [ ] 已规划迁移到 Background Assets 框架

### MetricKit
- [ ] 已盘点 `MXMetricManager` 用法（扫描规则 `METRICKIT-001`）
- [ ] 已规划迁移到 `MetricManager`

---

## P1 — 构建链

### Clang Modules
- [ ] 依赖之间无同名 module（Xcode 27 强制去重）
- [ ] 所有第三方 SDK 已升级到可用 Xcode 26+ 构建的版本（见 [docs/sdk-compatibility.md](../docs/sdk-compatibility.md)）

---

## P2 — 布局现代化

- [ ] 布局逻辑基于 size classes，而非设备 idiom / 方向判断
- [ ] `UIScreen.main.scale` 替换为 `traitCollection.displayScale`
- [ ] 已评估 `UIRequiresFullscreen` 变为离散 resize 行为的影响
- [ ] 已在 iPadOS 上测试窗口缩放场景

---

## 验证

- [ ] `python3 scripts/ios26-scanner.py <project>` 无 iOS 27 前瞻类问题（`OPENURL-001/002`、`ODR-001`、`METRICKIT-001`、`LINKER-001`）
- [ ] 当前发布版本完整回归通过
- [ ] 定期复查 [Apple 即将生效的要求](https://developer.apple.com/news/upcoming-requirements/) 确认最新时间点

---

**作者**: roder
