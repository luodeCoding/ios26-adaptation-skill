# iOS 26 / 27 时间线与适配范围总览

> **最后更新**: 2026-08-03
> **适用读者**: 需要向团队/老板解释"什么时候必须做什么"的开发者
> **信息来源**: Apple 官方公告、WWDC25/WWDC26、iOS 27 Beta Release Notes、TN3187

本文是整个技能库的**唯一时间线权威参考**。每个时间节点都明确标注：
苹果强制什么、你必须适配哪些范围、不做会怎样、对应哪份检查清单。

---

## 一图看懂

```
2025-06          2025-09           2026-04-28        ~2026-09          ~2027-04(预估)
  │                │                  │                 │                  │
  ▼                ▼                  ▼                 ▼                  ▼
WWDC25           iOS 26            App Store          Xcode 27 发布      App Store
iOS 26 SDK 发布   正式版发布          强制 iOS 26       iOS 27 正式版发布    强制 iOS 27
Liquid Glass     新 SDK 构建即       SDK 构建           Liquid Glass       SDK 构建
首次亮相          默认启用玻璃效果     （已生效❗）        强制、标志移除       （Phase 3 完成）
                  ──────────────    ──────────────    ──────────────    ──────────────
                  可选退出：          Phase 1           Phase 2           Phase 3
                  UIDesignRequires   必须完成           窗口关闭           必须完成
                  Compatibility
```

---

## 时间线节点详解

### 节点 1：2025-06（WWDC25）— iOS 26 SDK 发布

| 项目 | 内容 |
|------|------|
| 苹果动作 | 发布 Xcode 26 / iOS 26 SDK，推出 Liquid Glass 设计语言 |
| 强制要求 | 无（此阶段完全自愿） |
| 建议动作 | 在 beta 环境试编译，摸底项目适配工作量 |

### 节点 2：2025-09 — iOS 26 正式版发布

| 项目 | 内容 |
|------|------|
| 苹果动作 | iOS 26 推送到用户设备 |
| 强制要求 | 用 iOS 26 SDK 构建的 App 默认启用 Liquid Glass |
| 逃生通道 | `UIDesignRequiresCompatibility = YES` 可临时恢复旧外观（**有期限**，见节点 4） |
| 建议动作 | 开始 Phase 1 适配，不要等截止日 |

### 节点 3：**2026-04-28**（已生效❗）— App Store 强制 iOS 26 SDK 构建

| 项目 | 内容 |
|------|------|
| 苹果强制 | 所有新 App 和更新必须用 iOS 26 SDK（Xcode 26+）构建 |
| 不做的后果 | **提审直接被拒**，没有宽限期 |
| 必须完成的适配范围 | **Phase 1**（下表） |

**Phase 1 适配范围（iOS 26 SDK 构建达标）**：

| # | 适配项 | 性质 | 对应扫描规则 |
|---|--------|------|-------------|
| 1 | 废弃窗口访问替换：`keyWindow` / `delegate.window` / `windows` / `statusBarFrame` | 编译错误/警告 | WINDOW-001~008、STATUS-004 |
| 2 | SceneDelegate 架构迁移（Info.plist `UIApplicationSceneManifest` + SceneDelegate + AppDelegate 改造） | 架构必需（同时满足 iOS 27 强制项） | ARCH-001~003 |
| 3 | 通知选项：`UNNotificationPresentationOptionAlert` → `.banner \| .list` | 弃用警告 | NOTIF-001 |
| 4 | StoreKit 1 → StoreKit 2（Xcode 26 中 StoreKit 1 已**移除**） | 编译失败 | STOREKIT-001 |
| 5 | AssetsLibrary 移除、`UIWebView` 清除 | 编译失败/拒审 | ASSETSLIBRARY-*、WEB-001 |
| 6 | Privacy Manifest（`PrivacyInfo.xcprivacy`） | 拒审 | PRIVACY-001 |
| 7 | CoreData iCloud 同步 Key 移除、TLS 最低 1.2 | 运行时/连接失败 | COREDATA-001、TLS-001 |
| 8 | 临时禁用 Liquid Glass：`UIDesignRequiresCompatibility = YES` | 可选过渡手段 | PHASE2-001（提醒后续移除） |

> 📋 完整清单：[examples/phase1-checklist.zh.md](../examples/phase1-checklist.zh.md)

### 节点 4：**~2026-09** — Xcode 27 发布，Liquid Glass 强制（Phase 2 窗口关闭）

| 项目 | 内容 |
|------|------|
| 苹果动作 | 随 iPhone 18 发布 iOS 27 正式版 + Xcode 27 |
| 苹果强制 | `UIDesignRequiresCompatibility` 兼容标志**被移除**，Liquid Glass 无法再关闭 |
| 不做的后果 | 升级 Xcode 27 后 App 外观强制切换为 Liquid Glass，未适配的自定义 UI 会出现视觉错乱、布局错位 |
| 必须完成的适配范围 | **Phase 2**（下表） |
| 环境要求 | Xcode 27 仅支持 macOS Tahoe 26.4+、Apple Silicon |

**Phase 2 适配范围（Liquid Glass 视觉达标）**：

| # | 适配项 | 性质 | 对应扫描规则 |
|---|--------|------|-------------|
| 1 | 移除 `UIDesignRequiresCompatibility` | 必需 | PHASE2-001 |
| 2 | 导航栏自定义审查：硬编码背景色、`navigationBar addSubview` 被合成层吞掉 | 视觉/功能异常 | NAVBAR-001 |
| 3 | `rightBarButtonItems` 顺序反转 + 共享玻璃背景间距修复 | 视觉异常 | BARBUTTON-001 |
| 4 | 自定义 TabBar：`setValue:forKey:@"tabBar"` 私有 KVC 闪退 | **闪退** | TABBAR-001 |
| 5 | 浮动 TabBar 引起的 safeArea 变化（底部布局改用 `additionalSafeAreaInsets`） | 布局错位 | — |
| 6 | 键盘玻璃工具栏（可选，按需清除 `inputAccessoryView`） | 视觉协调 | KEYBOARD-001~003 |
| 7 | `UIScrollView.allowsLiquidTransform` 边缘滚动变形处理 | 视觉异常 | — |
| 8 | 全量 UI 回归测试（Light/Dark/着色模式） | 质量门槛 | — |

> 📋 完整清单：[examples/phase2-checklist.zh.md](../examples/phase2-checklist.zh.md)

### 节点 5：2026-09 起 — 用 iOS 27 SDK 构建即触发 Phase 3 强制项

> ⚠️ 触发条件是**你构建所用的 SDK**，不是用户的系统版本。
> 已上架的 iOS 26 SDK 二进制在 iOS 27 上照常运行；一旦用 Xcode 27 重新构建，以下强制项立即生效。

**Phase 3 适配范围（iOS 27 达标，WWDC26 已确认）**：

| # | 适配项 | 级别 | 不做的后果 | 对应扫描规则 |
|---|--------|------|-----------|-------------|
| 1 | UIScene 生命周期强制（官方文档 + TN3187） | 🔴 P0 | **App 无法启动**（用户侧表现为闪退） | ARCH-001~002 |
| 2 | 启动屏四选一 Info.plist 键（`UILaunchStoryboardName` / `UILaunchStoryboards` / `UILaunchScreen` / `UILaunchScreens`） | 🔴 P0 | **提审被拒** | 手动审计（生成式 Info.plist 见 ios27-preview） |
| 3 | `-ld_classic` 残留链接器标志清理 | 🔴 P0 | **编译失败**，CI 中断 | LINKER-001 |
| 4 | Clang module 同名去重（重复 `module.modulemap`） | 🔴 P0 | 编译失败 | 手动排查 |
| 5 | `canOpenURL` 弃用 + `LSApplicationQueriesSchemes` 上限 50→25 | 🟡 P1 | 超出 25 条的 scheme 静默返回 false | OPENURL-001~002 |
| 6 | On Demand Resources（`NSBundleResourceRequest`）弃用 | 🟡 P1 | 后续版本可能移除 | ODR-001 |
| 7 | `MXMetricManager` → `MetricManager` | 🟡 P1 | MetricKit 框架级重构 | METRICKIT-001 |
| 8 | 代码级隐蔽变更：NSURL 双重编码修复、C++ `multimap/multiset::find()` 语义、`FilePath.stat()` 命名冲突 | 🟡 P1 | 隐蔽逻辑错误/编译错误 | 手动排查 |

> 📋 完整清单：[examples/phase3-checklist.zh.md](../examples/phase3-checklist.zh.md)
> 📖 详细解读：[docs/ios27-preview.md](ios27-preview.md)

### 节点 6：**~2027-04（预估）** — App Store 强制 iOS 27 SDK 构建

| 项目 | 内容 |
|------|------|
| 苹果强制（预估，按往年规律） | 所有新 App 和更新必须用 iOS 27 SDK（Xcode 27+）构建 |
| 不做的后果 | 提审被拒 |
| 必须完成 | Phase 1 + Phase 2 + Phase 3 全部 |

---

## 我应该在什么时间做什么？（按发版时间选择策略）

| 你的下一个发版时间 | 策略 | 必做范围 | 详情 |
|-------------------|------|---------|------|
| 2026-04-28 之前 | 策略 A：分支适配 | 当前版本不动，`feature/ios26-adaptation` 分支完成 Phase 1 | SKILL.md §Decision Framework |
| 2026-04-28 ~ 2026-09 | 策略 B | Phase 1 必须；Phase 2 视 Xcode 27 前的发版计划评估 | 同上 |
| 2026-09 之后 | 策略 C | Phase 1 + 2 + 3 一次到位（推荐，避免返工） | 同上 |

**核心建议**：无论哪种策略，**Phase 1 的 SceneDelegate 迁移一次做对**——
它同时满足 2026-04-28 的构建要求和 iOS 27 最致命的"无法启动"强制项，是整条时间线上回报最高的一项。

---

## 相关文档

| 文档 | 内容 |
|------|------|
| [SKILL.md](../SKILL.md) | 完整适配指南、决策流程、代码示例 |
| [docs/ios27-preview.md](ios27-preview.md) | iOS 27 / Xcode 27 详细前瞻（Phase 3） |
| [examples/](../examples/) | 三阶段检查清单（中英双语） |
| [INTEGRATION.md](../INTEGRATION.md) | 使用说明与适配影响声明 |
