# 🚀 iOS 26/27 适配完全指南：自动化扫描 + 零遗漏总账 + 踩坑实录

> **TL;DR**：4 月 28 日 App Store 强制 iOS 26 SDK，9 月 Xcode 27 强制 Liquid Glass，明年 4 月强制 iOS 27 SDK（未迁 UIScene 直接无法启动）。本文分享一套开源适配方案：Python 扫描脚本（50+ 规则）+ 50 项覆盖总账（AI 适配零遗漏）、Swift/OC 双语言模板、可一键安装到 Claude Code/Qoder 的 AI 技能，承诺只改 iOS 26/27 相关代码、不冲击主项目。GitHub 已开源，可直接用于生产。

<!--
【图1：封面头图 / 文章头图】
使用方式：上传到掘金封面图设置
内容：iOS 26 主题视觉，深色科技风，中央大号发光"26"
尺寸：1280×720（掘金建议）
已有提示词：platforms/images/prompts/01-cover.md
-->

---

## 📌 为什么写这篇文章

上周团队收到苹果邮件：**4 月 28 日之后，所有新提交和更新必须使用 iOS 26 SDK 构建**。deadline 就在眼前，但网上资料分散，缺乏系统性方案。

于是我们做了两轮深度 QA 排查，整理出了这套**开源适配框架**。本文把项目背景、扫描工具实现、以及排查过程中发现的坑一次性讲清楚。

> GitHub：[github.com/luodeCoding/ios26-adaptation-skill](https://github.com/luodeCoding/ios26-adaptation-skill) ⭐

| 日期 | 要求 | 影响 |
|------|------|------|
| **2026-04-28**（已生效） | 强制使用 iOS 26 SDK | 不合规 = 直接拒审 ❌ |
| **~2026-09** | Xcode 27 发布，Liquid Glass 强制启用 | `UIDesignRequiresCompatibility` 失效 |
| **~2027-04（预估）** | 强制使用 iOS 27 SDK（WWDC26 已确认） | 未迁移 UIScene 生命周期 = **App 无法启动** ❌ |

> 📅 每个时间节点该适配什么，项目里有一页式总览：`docs/timeline.zh.md`

---

## 🛡 低冲击适配：只动 iOS 26/27，不碰你的业务代码

很多人不敢让 AI 直接改主项目，怕改飞了。这套方案把**影响边界写进了技能文档**，AI 执行时必须遵守：

| ✅ 只会改 | ❌ 绝不碰 |
|-----------|-----------|
| 扫描命中的废弃 API 调用点 | Deployment Target / 最低支持版本 |
| SceneDelegate 架构 + Info.plist 场景清单 | 业务逻辑、无关文件的重构/格式化 |
| 新增的扩展/适配器文件 | iOS 12 及更早的兼容路径 |
| `#available` 版本分支包裹的差异 | `Pods/` 和第三方 SDK 源码 |

执行流程也可审计：**扫描 → 列出改动文件清单 + 逐项理由 → 确认后才动手 → 改完重扫直到 Error 清零**。

每一项适配要求都能追溯到苹果官方来源（Upcoming Requirements、Release Notes、WWDC、TN3187），不夹带私货。

---

## 🛠 两阶段适配策略

### Phase 1：SDK 构建适配（4 月 28 日前必须完成）

**核心任务**：
1. `keyWindow` / `delegate.window` → 统一窗口访问接口
2. `UNNotificationPresentationOptionAlert` → `Banner \| List`（iOS 14.0+）
3. SceneDelegate 架构迁移
4. 临时禁用 Liquid Glass：`UIDesignRequiresCompatibility = YES`
5. StoreKit 1 → StoreKit 2（Xcode 26 中 StoreKit 1 已**移除**）
6. 添加 Privacy Manifest：`PrivacyInfo.xcprivacy`

### Phase 2：Liquid Glass 完整适配（Xcode 27 发布前）

**核心任务**：
1. 移除兼容标志
2. 处理浮动 TabBar 导致的 safeArea 变化
3. 移除自定义背景色，避免与 glass 效果冲突

---

## 🔍 自动化扫描工具

![图2-工具核心效果](待补充：一张图展示工具如何帮你完成 iOS 26 适配)
> **图2：工具核心效果**。这张图展示扫描工具的运行结果，或 Before/After 改造对比，让读者一眼看懂"这个工具能帮我做什么"。

### 一行命令检测废弃 API

```bash
python3 scripts/ios26-scanner.py /path/to/your/ios/project
```

输出示例：

```
# iOS 26 Adaptation Scan Report
**Files Scanned:** 247
**Total Issues:** 12  (Errors: 3, Warnings: 9)

| Rule ID | Severity | File | Line | Message |
|---------|----------|------|------|---------|
| WINDOW-001 | ERROR | LoginVC.swift | 45 | Deprecated keyWindow usage |
| STOREKIT-001 | ERROR | IAPManager.m | 128 | StoreKit 1 API removed |
| PRIVACY-001 | ERROR | ./ | 0 | Missing PrivacyInfo.xcprivacy |
```

### 三层规则体系（50+ 规则）

| 类别 | 规则数 | 代表规则 |
|------|--------|---------|
| 窗口访问 | 6 | `keyWindow`、`delegate.window`、`UIScreen.main` |
| 通知 | 1 | `UNNotificationPresentationOptionAlert` |
| StoreKit | 1 | `SKPaymentTransaction` 等 StoreKit 1 API |
| SiriKit | 1 | 废弃 intent domain |
| SwiftUI | 3 | `NavigationView`、`.cornerRadius()`、`.foregroundColor()` |
| CoreData | 1 | iCloud 同步 key 移除 |
| 网络 | 1 | TLS 1.0/1.1 |
| 隐私 | 1 | `PrivacyInfo.xcprivacy` 缺失 |
| Web | 1 | `UIWebView` |
| 照片 | 1 | `UIImagePickerController` |

### 核心设计：规则即配置

```python
RULES = [
    {
        "id": "WINDOW-001",
        "name": "Deprecated keyWindow usage (Swift)",
        "pattern": re.compile(r"UIApplication\.shared\.keyWindow"),
        "extensions": {".swift"},
        "severity": "error",
        "suggestion": "Use UIApplication.shared.mainWindow",
    },
]
```

新增规则只需加 5 行代码，无需改扫描引擎。除上表外，还覆盖：iOS 26 运行时实战坑（`tabBar` KVC 闪退、`navigationBar addSubview` 失效、`rightBarButtonItems` 顺序反转）和 iOS 27 前瞻检查（`canOpenURL`、`-ld_classic`、`LSApplicationQueriesSchemes` 25 条上限、ODR、MetricKit）。项目级检查新增：**启动屏强制项**（含生成式 Info.plist）、App 扩展 target、第三方 SDK 清单核对。

### 🧾 为什么 AI 适配不再漏项：50 项覆盖总账

用 AI 做适配最常见的痛点：**一会儿漏这样、一会儿漏那样**。本方案用三层机制堵死遗漏：

1. **覆盖总账**（`scripts/adaptation-ledger.json`）：50 项适配项的完整清单（Phase 1/2/3 + 环境 + 上线门禁），每项绑定检测方式、规则 ID、验收标准、苹果官方来源。AI 必须逐项对照执行，不允许凭记忆取子集。
2. **报告自带人工核对清单 + 上线门禁（SHIP-01~05）**：扫描报告末尾会列出无法静态检测的项（如转场动画 completion 幂等、C++ find 语义），并定义"可上线"的完成标准——门禁全绿才算完成，而不是"代码能编译"。
3. **CI 一致性测试**：总账中每个自动检测项必须对应真实存在的扫描规则，未来漏项会直接测试失败。

目标效果：**用这套技能改完后，再修一轮 bug，基本就能上线。**完整 50 项矩阵见仓库 `docs/coverage.zh.md`。

---

## 📁 模板速览

```
templates/
├── swift/
│   ├── UIApplication+MainWindow.swift
│   ├── SceneDelegate.swift
│   ├── AppDelegate+Setup.swift
│   ├── UNNotificationOptions+Adapter.swift
│   └── Swift6ConcurrencyAdapter.swift     # Swift 6 并发适配
├── objc/
│   ├── UIApplication+MainWindow.h/.m
│   ├── SceneDelegate.h/.m
│   ├── AppDelegate+Setup.h/.m
│   └── UNNotificationOptionsAdapter.h/.m
├── mixed/
│   └── README.md                          # 混合项目桥接指南
└── PrivacyInfo.xcprivacy                  # Privacy Manifest 模板
```

---

## 🧐 两轮 QA 排查：15 个盲点

### 第一轮（基础适配项）

| # | 差距项 | 优先级 | 状态 |
|---|--------|--------|------|
| 1 | `UIScreen.main` 正式废弃 | 🔴 | ✅ |
| 2 | Swift 6 严格并发检查 | 🔴 | ✅ |
| 3 | Liquid Glass TabBar safeArea 变化 | 🔴 | ✅ |
| 4 | TLS 1.0/1.1 最低版本提升 | 🟡 | ✅ |
| 5 | CoreData iCloud Sync Key 移除 | 🟡 | ✅ |

### 第二轮（进阶项）

| # | 差距项 | 优先级 | 状态 |
|---|--------|--------|------|
| 6 | Privacy Manifest 缺失 | 🔴 | ✅ |
| 7 | StoreKit 1 API 移除 | 🔴 | ✅ |
| 8 | SiriKit Intent Domains 废弃 | 🔴 | ✅ |
| 9 | SwiftUI `NavigationView` 废弃 | 🟡 | ✅ |
| 10 | `UIImagePickerController` 废弃 | 🟡 | ✅ |

**合计：15 项差距，全部已修复。**

---

## 📦 第三方 SDK 兼容性

| SDK | 问题 | 最低兼容版本 |
|-----|------|------------|
| Facebook iOS SDK | StoreKit 1 API 编译失败 | 18.1.0+ |
| RevenueCat | StoreKit 1 废弃警告 | 5.0.0+ |
| Firebase Analytics | 缺少 Privacy Manifest | 10.24.0+ |
| 极光推送 | 通知选项替换逻辑 | 最新版 |

完整列表见项目 `docs/sdk-compatibility.md`。

---

## 🚀 快速开始

### 方式一：装成 AI 技能，一句话搞定（推荐）

```bash
# Claude Code：安装到用户技能目录
git clone https://github.com/luodeCoding/ios26-adaptation-skill.git ~/.claude/skills/ios26-adaptation

# 然后在你的 iOS 项目里对 AI 说：
#   “帮我适配 iOS 26”
# AI 会自动：加载 50 项总账 → 扫描 → 列改动清单 → 修改代码 → 重扫验证 → 关闭上线门禁
```

Qoder / 其他 Agent 工具同理：从 GitHub 地址安装为插件，或克隆后让 Agent 指向该目录。

### 方式二：手动扫描 + 复制模板

```bash
# 1. 克隆项目
git clone https://github.com/luodeCoding/ios26-adaptation-skill.git

# 2. 扫描你的项目
cd ios26-adaptation-skill
python3 scripts/ios26-scanner.py /path/to/your/ios/project

# 3. 根据扫描结果，复制模板修改
cp templates/swift/*.swift /your/project/path/
```

---

## 📝 总结

这套方案不是简单代码片段，而是经过**两轮深度 QA 排查**、对照 Apple 官方文档验证后的系统性解决方案。

如果你的团队正在面临 iOS 26 适配 deadline，希望这套开源方案能帮你省下几周的踩坑时间。

> ⭐ 有用的话欢迎点 Star，也欢迎提 Issue 和 PR！

**相关链接**：
- GitHub：[github.com/luodeCoding/ios26-adaptation-skill](https://github.com/luodeCoding/ios26-adaptation-skill)
- Apple 官方要求：[developer.apple.com/news/upcoming-requirements](https://developer.apple.com/news/upcoming-requirements)
- 时间线总览（仓库内）：`docs/timeline.zh.md`
- 覆盖矩阵（仓库内）：`docs/coverage.zh.md`
- 适配影响声明（仓库内）：`INTEGRATION.md`
