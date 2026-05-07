# iOS 26 SDK 适配完整方案：自动化扫描脚本 + 20+ 检测规则 + 代码模板全覆盖

**摘要**：2026 年 4 月 28 日起，Apple 强制要求所有 App Store 提交使用 iOS 26 SDK 构建。本文介绍一套完整的 **AI 适配技能（Skill）**：将你的 AI 助手接入这套知识库后，它能自动扫描你的 iOS 项目、定位废弃 API、输出改造方案，并直接提供 Swift/Objective-C 双语言模板。不需要手动运行任何脚本，AI 替你完成排查和适配。

<!--
【图1：封面头图 / 文章头图】
使用方式：上传到 CSDN 博客封面图设置
内容：iOS 26 主题视觉，深色科技风，中央大号发光"26"
尺寸：1000×560（CSDN 建议）
已有提示词：platforms/images/prompts/01-cover.md
-->

---

## 一、背景与 deadline

Apple 官方公告：自 **2026 年 4 月 28 日**起，上传到 App Store Connect 的应用必须使用 iOS 26 SDK 构建。不满足要求的提交将被直接拒绝。

![图2-Xcode报错痛点图](待补充：Xcode编译报错截图，红字高亮keyWindow废弃)
> **图2：Xcode 报错痛点图**。截图 Xcode 编译报错界面，红字高亮 `'keyWindow' was deprecated in iOS 26.0`，让读者瞬间明白问题所在。

| 时间节点 | 要求 | 影响 |
|---------|------|------|
| 2026-04-28 | 强制使用 iOS 26 SDK | 不合规提交被拒 |
| ~2026-09 | Xcode 27 发布 | Liquid Glass 兼容标志失效 |

---

## 二、两阶段适配策略

![图3-Phase1-2适配路线图](待补充：两阶段时间线信息图)
> **图3：Phase 1/2 适配路线图**。左橙（Phase 1 紧急修复）右蓝（Phase 2 Liquid Glass），展示两个 deadline 节点。已有提示词：platforms/images/prompts/04-roadmap.md

### Phase 1：SDK 构建适配（4 月 28 日前）

目标：使用 iOS 26 SDK 成功构建，保持现有 UI 不变。

核心任务：
1. 修复废弃 API：`keyWindow`、`delegate.window`、`UIScreen.main`
2. 通知选项适配：`UNNotificationPresentationOptionAlert` → `Banner \| List`
3. SceneDelegate 架构迁移
4. 临时禁用 Liquid Glass：`UIDesignRequiresCompatibility = YES`
5. StoreKit 1 → StoreKit 2（Xcode 26 中 StoreKit 1 已移除）
6. 添加 Privacy Manifest：`PrivacyInfo.xcprivacy`

### Phase 2：Liquid Glass 完整适配（Xcode 27 前）

目标：完全适配 Liquid Glass 设计语言。

核心任务：
1. 移除 `UIDesignRequiresCompatibility`
2. 处理浮动 TabBar 导致的 safeAreaInsets 变化
3. 移除自定义导航栏/工具栏背景色，避免与 glass 效果冲突
4. 验证 UIDropShadowView 自动插入对布局的影响

---

## 三、自动化扫描工具

![图4-Scanner扫描对比图](待补充：Scanner左右对比演示图)
> **图4：Scanner 扫描演示图**。左屏 = 有红色下划线的脏乱代码，右屏 = 分 ERROR/WARNING/INFO 三色的清晰扫描报告。已有提示词：platforms/images/prompts/03-scanner-demo.md

### 使用方法

```bash
python3 scripts/ios26-scanner.py /path/to/your/ios/project
```

### 输出示例

```markdown
# iOS 26 Adaptation Scan Report
**Files Scanned:** 247
**Total Issues:** 12  (Errors: 3, Warnings: 9)

| Rule ID | Severity | File | Line | Message |
|---------|----------|------|------|---------|
| WINDOW-001 | ERROR | LoginVC.swift | 45 | Deprecated keyWindow usage |
| STOREKIT-001 | ERROR | IAPManager.m | 128 | StoreKit 1 API usage |
| PRIVACY-001 | ERROR | ./ | 0 | Missing PrivacyInfo.xcprivacy |
```

### 扫描规则列表（20+ 条）

| 类别 | 规则 ID | 检测内容 | 级别 |
|------|---------|---------|------|
| 窗口访问 | WINDOW-001~006 | keyWindow, delegate.window, UIScreen.main | error/warning |
| 通知 | NOTIF-001 | UNNotificationPresentationOptionAlert | warning |
| StoreKit | STOREKIT-001 | SKPaymentTransaction, SKProductsRequest | error |
| SiriKit | SIRIKIT-001 | 废弃 intent domain | warning |
| SwiftUI | SWIFTUI-001~003 | NavigationView, cornerRadius, foregroundColor | warning |
| CoreData | COREDATA-001 | NSPersistentStoreUbiquitousContentNameKey | error |
| 网络 | TLS-001 | TLS 1.0/1.1 | warning |
| 隐私 | PRIVACY-001 | 缺失 PrivacyInfo.xcprivacy | error |
| Web | WEB-001 | UIWebView | error |
| 照片 | PHOTOS-001 | UIImagePickerController | warning |

### 核心设计

每条规则由字典定义，包含正则表达式、适用文件后缀、严重级别和修复建议：

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

新增规则只需在 Skill 配置中补充一个字典，AI 立即生效。

---

## 四、代码模板

![图5-项目4模块架构图](待补充：4个方块信息图)
> **图5：项目 4 模块架构图**。4 个等大方块分别对应：扫描工具、代码模板、适配指南、兼容方案。已有提示词：platforms/images/prompts/02-architecture.md

项目提供三套完整模板：

```
templates/
├── swift/
│   ├── UIApplication+MainWindow.swift
│   ├── SceneDelegate.swift
│   ├── AppDelegate+Setup.swift
│   ├── UNNotificationOptions+Adapter.swift
│   └── Swift6ConcurrencyAdapter.swift
├── objc/
│   ├── UIApplication+MainWindow.h/.m
│   ├── SceneDelegate.h/.m
│   ├── AppDelegate+Setup.h/.m
│   └── UNNotificationOptionsAdapter.h/.m
├── mixed/
│   └── README.md
└── PrivacyInfo.xcprivacy
```

**Swift 6 并发适配示例**：

```swift
@MainActor
final class MainActorViewModel: ObservableObject {
    @Published var items: [String] = []
    
    func loadData() async {
        let result = await Task.detached {
            return ["Item 1", "Item 2"]
        }.value
        self.items = result  // 安全：已在 MainActor 上
    }
}
```

---

## 五、两轮 QA 排查成果

### 第一轮排查（8 项差距）

| 差距项 | 优先级 | 状态 |
|--------|--------|------|
| UIScreen.main 正式废弃 | 🔴 | ✅ 已修复 |
| Swift 6 严格并发检查 | 🔴 | ✅ 已修复 |
| Liquid Glass TabBar safeArea 变化 | 🔴 | ✅ 已修复 |
| TLS 1.2 最低版本提升 | 🟡 | ✅ 已修复 |
| CoreData iCloud Sync Key 移除 | 🟡 | ✅ 已修复 |

### 第二轮排查（7 项差距）

| 差距项 | 优先级 | 状态 |
|--------|--------|------|
| Privacy Manifest 缺失 | 🔴 | ✅ 已修复 |
| StoreKit 1 → StoreKit 2 | 🔴 | ✅ 已修复 |
| SiriKit → App Intents | 🔴 | ✅ 已修复 |
| SwiftUI 现代 API | 🟡 | ✅ 已修复 |
| Photos PHPicker 迁移 | 🟡 | ✅ 已修复 |

**合计 15 项差距，全部已修复。**

---

## 六、第三方 SDK 兼容性

| SDK | 问题 | 最低兼容版本 |
|-----|------|------------|
| Facebook iOS SDK | StoreKit 1 API 编译失败 | 18.1.0+ |
| RevenueCat | StoreKit 1 废弃警告 | 5.0.0+ |
| Firebase Analytics | 缺少 Privacy Manifest | 10.24.0+ |
| 极光推送 | 通知选项替换逻辑 | 最新版 |

完整列表见项目 `docs/sdk-compatibility.md`。

---

## 七、项目信息

- **类型**：AI 适配技能（Skill）/ 知识库
- **语言**：Objective-C / Swift
- **最低 iOS 版本**：12.0+
- **许可证**：MIT

---

## 八、快速开始

```
1. 将 iOS 26 Adaptation Skill 接入你的 AI 助手
   （放入 AI 可读取的工作目录或知识库）

2. 向 AI 提出适配需求：
   "帮我做 iOS 26 适配"

3. AI 自动完成：
   - 扫描项目代码，定位废弃 API 和架构问题
   - 根据发版时间推荐 Strategy A/B/C
   - 生成改造代码（Swift/OC/Mixed）
   - 提供 Phase 1/2 检查清单
```

---

**关键词**：iOS 26 适配、Xcode 26、Liquid Glass、SceneDelegate、StoreKit 2、Privacy Manifest、Swift 6、自动化扫描
