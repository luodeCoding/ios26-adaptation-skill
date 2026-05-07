# 🚀 iOS 26 适配完全指南：自动化扫描 + 20+ 规则 + 踩坑实录

> **TL;DR**：4 月 28 日 App Store 强制 iOS 26 SDK。本文分享一套 **AI 适配技能（Skill）**：把你的 AI 助手接入这套知识库，它能自动扫描你的项目、定位废弃 API、输出改造方案，并直接提供 Swift/OC 双语言模板。不需要手动跑脚本，AI 替你完成排查和适配。

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

![图2-Xcode报错痛点图](待补充：Xcode编译报错截图，红字高亮keyWindow废弃)
> **图2：Xcode 报错痛点图**。截图你的 Xcode 编译报错界面，红字高亮 `'keyWindow' was deprecated in iOS 26.0`，让读者瞬间共鸣。

---

## ⏰ 关键时间节点

![图3-Phase1-2适配路线图](待补充：两阶段时间线信息图)
> **图3：Phase 1/2 适配路线图**。左橙右蓝时间线，直观展示 4月28日 deadline 和 Xcode 27 的 Liquid Glass 强制启用节点。替代纯文字表格的第一印象。

| 日期 | 要求 | 影响 |
|------|------|------|
| **2026-04-28** | 强制使用 iOS 26 SDK | 不合规 = 直接拒审 ❌ |
| **~2026-09** | Xcode 27 发布，Liquid Glass 强制启用 | `UIDesignRequiresCompatibility` 失效 |

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

![图4-Scanner扫描对比图](待补充：Scanner左右对比演示图)
> **图4：Scanner 扫描演示图**。左屏 = 有红色下划线的脏乱代码，右屏 = 分 ERROR/WARNING/INFO 三色的清晰扫描报告。已有提示词：platforms/images/prompts/03-scanner-demo.md

### AI 自动扫描废弃 API

你把项目路径告诉 AI，AI 会调用内置扫描能力分析你的代码：

```
AI > 扫描项目：/path/to/your/ios/project

# iOS 26 Adaptation Scan Report
**Files Scanned:** 247
**Total Issues:** 12  (Errors: 3, Warnings: 9)

| Rule ID | Severity | File | Line | Message |
|---------|----------|------|------|---------|
| WINDOW-001 | ERROR | LoginVC.swift | 45 | Deprecated keyWindow usage |
| STOREKIT-001 | ERROR | IAPManager.m | 128 | StoreKit 1 API removed |
| PRIVACY-001 | ERROR | ./ | 0 | Missing PrivacyInfo.xcprivacy |
```

**你不需要手动运行任何命令**，AI 会直接读取这套 Skill 中的规则配置，自动完成扫描并给出修复建议。

输出示例（AI 直接展示）：

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

### 20+ 条内置扫描规则

这套 Skill 内置了完整的规则引擎，AI 直接调用：

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

新增规则只需在 Skill 配置中加 5 行字典，AI 立即生效。

---

## 📁 模板速览

![图5-项目4模块架构图](待补充：4个方块信息图)
> **图5：项目 4 模块架构图**。4 个等大方块（扫描/模板/指南/兼容），深色背景。让读者不看代码先理解项目组成。已有提示词：platforms/images/prompts/02-architecture.md

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

![图6-代码Before-After对比](待补充：左右分栏代码对比图)
> **图6：代码 Before/After 对比**。左（红底删除线：`UIApplication.shared.keyWindow`）→ 右（绿底高亮：`UIApplication.shared.mainWindow`）。证明模板"复制粘贴就能用"，降低读者尝试门槛。

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

## 🚀 快速开始

```
1. 把这套 iOS 26 Adaptation Skill 接入你的 AI 助手
   （放到 AI 可读取的项目目录或知识库中）

2. 告诉 AI："帮我做 iOS 26 适配"

3. AI 自动完成：
   - 扫描你的项目，定位所有废弃 API
   - 判断你的发版时间，推荐 Strategy A/B/C
   - 输出改造代码（Swift/OC/Mixed 三选一）
   - 提供检查清单，逐项验证
```

---

## 📝 总结

这套方案不是简单代码片段，而是经过**两轮深度 QA 排查**、对照 Apple 官方文档验证后的系统性 AI 知识库。

如果你的团队正在面临 iOS 26 适配 deadline，把这套 Skill 交给你的 AI，几小时的排查工作可以压缩到几分钟。

**相关参考**：
- Apple 官方要求：[developer.apple.com/news/upcoming-requirements](https://developer.apple.com/news/upcoming-requirements)
