# iOS 26/27 适配覆盖矩阵（Coverage Ledger）

> **单一事实源**：[`scripts/adaptation-ledger.json`](../scripts/adaptation-ledger.json)（v1.12.0，50 项）。
> 本文档由总账生成口径。若两者不一致，以 JSON 总账为准。
> CI 一致性测试保证：总账中每个 `auto` 项的规则 ID 必须在扫描器中真实存在——**未来漏项会直接测试失败**。

## 零遗漏适配是如何保证的

AI 适配最常见的失败模式是"一会儿漏这样、一会儿漏那样"。本技能库用三层机制堵死遗漏：

| 层 | 机制 | 覆盖范围 |
|---|---|---|
| 1. 自动检测 | `scripts/ios26-scanner.py` 37 条行级规则 + 14 条项目级规则 | 所有 `detection: auto` 项 |
| 2. 人工核对 | 扫描报告末尾 **Manual Audit Checklist** | 所有 `detection: manual` 项（无法静态检测） |
| 3. 上线门禁 | 扫描报告末尾 **Completion Gate**（SHIP-01~05） | 定义"改完即可上线"的完成标准 |

**使用方式**：在项目根目录运行扫描器，报告自带清单与门禁；AI 代理按 `SKILL.md` 的"零遗漏适配循环"逐项推进，直到门禁全绿。

```bash
python3 scripts/ios26-scanner.py /path/to/YourProject --format markdown
```

检测方式图例：

- **auto** — 扫描器自动检测，附规则 ID
- **manual** — 无法静态检测，报告人工核对清单逐项列出
- **test** — 通过构建/运行/测试矩阵验证（见 [testing-guide.md](testing-guide.md)）

---

## Phase 1：iOS 26 SDK 构建适配（截止 **2026-04-28**）

| ID | 适配项 | 检测 | 规则 ID | 验收方式 |
|---|---|---|---|---|
| P1-01 | 废弃窗口访问替换（keyWindow / delegate.window / windows） | auto | WINDOW-001~008 | 替换为 `UIApplication.mainWindow` 统一访问，编译无警告 |
| P1-02 | 状态栏 API 替换（statusBarStyle / statusBarFrame） | auto | STATUS-001~004 | 改用 safeAreaLayoutGuide / statusBarManager |
| P1-03 | UIScreen.main 替换 | auto | SCREEN-001~002 | 改用 UIWindowScene.screen（iOS 12 路径保留并注释） |
| P1-04 | 通知前台展示选项替换（Alert → Banner\|List） | auto | NOTIF-001 | `#available(iOS 14)` 分支包裹 |
| P1-05 | SceneDelegate 文件存在 | auto | ARCH-001 | iOS 13+ 路径经 SceneDelegate 创建窗口 |
| P1-06 | Info.plist UIApplicationSceneManifest 配置 | auto | ARCH-002 / ARCH-004 | 静态路由或动态 scene-configuration |
| P1-07 | AppDelegate sharedInstance / 生命周期转发结构 | auto | ARCH-003 | setupApplication / setupSceneUI 抽取完成 |
| P1-08 | 生命周期事件转发完整性（前后台/活跃状态） | test | — | 测试指南关键场景 3：埋点与状态保存正常 |
| P1-09 | StoreKit 1 → StoreKit 2（Xcode 26 已移除 StoreKit 1） | auto | STOREKIT-001 | iOS 15+ 走 StoreKit 2，低版本双路径 |
| P1-10 | AssetsLibrary 框架移除 | auto | ASSETSLIBRARY-001~003 | 迁移至 Photos 框架 |
| P1-11 | UIWebView 清除 | auto | WEB-001 | 迁移至 WKWebView（拒审项） |
| P1-12 | Privacy Manifest（PrivacyInfo.xcprivacy） | auto | PRIVACY-001 | Required Reason APIs 与数据收集声明完整 |
| P1-13 | CoreData iCloud Ubiquitous 同步 Key 移除 | auto | COREDATA-001 | 迁移 NSPersistentCloudKitContainer / SwiftData |
| P1-14 | TLS 最低版本 1.2 | auto | TLS-001 | 移除 TLS 例外，验证内网服务 |
| P1-15 | SiriKit 废弃 intent domains → App Intents | auto | SIRIKIT-001 | Xcode 自动转换 + 回归 |
| P1-16 | SwiftUI 废弃 API（NavigationView 等） | auto | SWIFTUI-001~003 | 按部署目标选择现代替代 |
| P1-17 | UIImagePickerController → PHPickerViewController | auto | PHOTOS-001 | PhotosUI 选择器回归 |
| P1-18 | Swift 6 严格并发新警告评估 | auto | SWIFT6-001 | 仅处理新 SDK 引入的警告（低冲击边界） |
| P1-19 | 临时禁用 Liquid Glass（UIDesignRequiresCompatibility） | auto | PHASE2-001 | Phase 1 可加；Phase 2 必须移除 |
| P1-20 | iOS 26 SDK 构建成功且无弃用警告 | test | — | Xcode 26 clean build，warning 清零 |

## Phase 2：Liquid Glass 全量适配（Xcode 27 之前，约 **2026-09**）

| ID | 适配项 | 检测 | 规则 ID | 验收方式 |
|---|---|---|---|---|
| P2-01 | 移除 UIDesignRequiresCompatibility | auto | PHASE2-001 | clean build 后 iOS 26 设备呈现玻璃效果 |
| P2-02 | 自定义 TabBar 私有 KVC（tabBar setValue）闪退排查 | auto | TABBAR-001 | 改用 UITabBarAppearance / 自定义容器 |
| P2-03 | navigationBar addSubview 叠加视图失效排查 | auto | NAVBAR-001 | 改用 titleView / navigationController.view |
| P2-04 | rightBarButtonItems 顺序反转与共享背景间距 | auto | BARBUTTON-001 | 应用 LiquidGlassAdapter 并视觉回归 |
| P2-05 | 键盘玻璃工具栏（inputAccessoryView）按需处理 | auto | KEYBOARD-001~003 | 仅对视觉冲突的输入框处理 |
| P2-06 | 浮动 TabBar safeArea 变化（底部布局） | manual | — | 审查硬编码 bottom 常量，改用 additionalSafeAreaInsets |
| P2-07 | UIScrollView.allowsLiquidTransform 边缘变形 | manual | — | 长列表边缘滚动目视检查 |
| P2-08 | UIDropShadowView 自动插入导致的视图遍历假设 | manual | — | 审查依赖 subviews 索引的系统栏代码 |
| P2-09 | 转场动画可中断性（completion 幂等） | manual | — | 审查自定义转场的 completion 双触发 |
| P2-10 | 全量 UI 回归（Light / Dark / 着色模式） | test | — | 测试指南视觉回归矩阵逐项通过 |

## Phase 3：iOS 27 SDK 构建适配（约 **2027-04** 强制）

| ID | 适配项 | 检测 | 规则 ID | 验收方式 |
|---|---|---|---|---|
| P3-01 | UIScene 生命周期强制（未迁移 App 无法启动） | auto | ARCH-001~002 | iOS 27 设备/模拟器启动验证 |
| P3-02 | 启动屏四选一 Info.plist 键强制 | auto | LAUNCH-001~003 | 四键之一存在；生成式 plist 查构建键 |
| P3-03 | -ld_classic 残留链接器标志清理 | auto | LINKER-001 | xcconfig / pbxproj / Podfile 全清 |
| P3-04 | Clang module 同名去重 | manual | — | `find . -name module.modulemap` 排查重名 |
| P3-05 | canOpenURL 弃用 + LSApplicationQueriesSchemes 上限 25 | auto | OPENURL-001~002 | 迁移 attempt-and-handle；清单 ≤25 条 |
| P3-06 | On Demand Resources 弃用 | auto | ODR-001 | 评估替代方案 |
| P3-07 | MXMetricManager → MetricManager | auto | METRICKIT-001 | MetricKit 上报回归 |
| P3-08 | NSURL URLWithString 双重编码修复影响审查 | manual | — | 搜索 URL 编码 workaround 逐一复核 |
| P3-09 | C++ multimap/multiset::find() 语义变化 | manual | — | C++ 层改用 lower_bound/equal_range |
| P3-10 | FilePath.stat() 命名冲突 | manual | — | 自定义 stat() 扩展限定 Darwin.stat() |
| P3-11 | idiom/orientation 布局判断 → size classes | manual | — | iPad 全尺寸可调场景审查 |
| P3-12 | App Extension / 多 target 同步适配 | auto | EXT-001 | 每个 extension 单独构建验证 |

## 环境项

| ID | 适配项 | 检测 | 规则 ID | 验收方式 |
|---|---|---|---|---|
| ENV-01 | Xcode 26.0+（推荐 26.3+）与 macOS Sequoia 15.3+ | manual | — | `xcodebuild -version` 确认 |
| ENV-02 | Xcode 27 环境：macOS Tahoe 26.4+、Apple Silicon、真机 iOS 17+ | manual | — | 升级前核对设备与 CI 机器 |
| ENV-03 | 第三方 SDK 兼容性核对 | auto | SDK-001~002 | 对照 [sdk-compatibility.md](sdk-compatibility.md) 升级 |

## 上线门禁（完成定义，全绿才可提审）

| ID | 门禁项 | 验收方式 |
|---|---|---|
| SHIP-01 | 扫描器 Error 清零 | 重跑扫描，errors == 0 |
| SHIP-02 | Warning 逐条 triage | 修复或记录豁免理由，无未处理 warning |
| SHIP-03 | 人工核对清单逐项勾选 | 扫描报告 Manual Audit Checklist 全勾 |
| SHIP-04 | 测试矩阵通过 | 最低版本 / iOS 13+ / iOS 26 设备 P0 全过 |
| SHIP-05 | 低冲击边界确认 | git diff 仅含 iOS 26/27 适配文件，Deployment Target 未变 |

---

**相关文档**：[timeline.zh.md](timeline.zh.md)（时间节点） · [testing-guide.md](testing-guide.md)（测试矩阵） · [sdk-compatibility.md](sdk-compatibility.md)（SDK 速查） · [faq.md](faq.md)
