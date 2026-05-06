# 🧐 两轮 QA 排查后，我发现了 15 个 iOS 26 适配盲点

> 网上搜索 + 对照 Apple 官方文档 + 实际项目验证，两轮排查共发现 15 项差距。有些是编译错误，有些是隐形坑。

---

## 排查方法

1. **网上调研**：Apple Developer Release Notes、WWDC25 Labs、社区迁移指南
2. **项目对照**：逐条检查 SKILL.md / templates / scanner / docs 的覆盖范围
3. **差距定级**：按影响面和紧急程度分为高/中/低三级

---

## 第一轮排查：基础适配项

### 🔴 高优先级

**1. UIScreen.main 正式废弃**

iOS 26 SDK 中 `UIScreen.main` 从 `API_TO_BE_DEPRECATED` 正式变为 `deprecated`。我们的模板代码里居然还在用！

修复：iOS 13+ 从 `UIWindowScene` 获取，iOS 12 fallback 路径保留但加注释。

**2. Swift 6 严格并发检查**

Xcode 26 默认 Swift 6，启用完整 strict concurrency。几百个 `@escaping` 闭包可能同时报警告。

修复：`@MainActor`、`@Sendable`、async/await 迁移。

**3. Liquid Glass TabBar 导致 safeArea 变化**

浮动 TabBar 改变了底部 `safeAreaInsets`。我们以为只是视觉变化，结果手动计算的底部间距全错位了。

修复：用 `additionalSafeAreaInsets` + `viewSafeAreaInsetsDidChange()`。

### 🟡 中优先级

**4. TLS 最低版本 1.0 → 1.2**

企业内部 API 还在用 TLS 1.0 的直接断连。

**5. CoreData iCloud Sync Key 移除**

`NSPersistentStoreUbiquitousContentNameKey` 等 key 在 iOS 26 中被移除，编译直接报错。

---

## 第二轮排查：进阶项

### 🔴 高优先级

**6. Privacy Manifest 完全缺失**

自 2024-05-01 起强制要求 `PrivacyInfo.xcprivacy`。我们项目里完全没提！

**7. StoreKit 1 API 在 Xcode 26 中被移除**

不是废弃，是移除。`SKPaymentTransaction`、`SKProductsRequest` 直接编译失败。

**8. SiriKit Intent Domains 废弃**

CarPlay、Lists、Payments、Photos 等多个 domain 被废弃，需迁移到 App Intents。

### 🟡 中优先级

**9. SwiftUI NavigationView 废弃**

`NavigationView` → `NavigationStack`，`.cornerRadius()` → `.clipShape()`。

**10. Photos UIImagePickerController 废弃**

`PHPickerViewController` 是替代方案，iOS 14+ 可用。

---

## 排查成果

| 轮次 | 发现问题数 | 高优先级 | 已修复 |
|------|-----------|---------|--------|
| 第一轮 | 8 | 3 | 8 |
| 第二轮 | 7 | 3 | 7 |
| **合计** | **15** | **6** | **15** |

---

## 给开发者的建议

1. **不要只关注编译错误**，warning 在 Swift 6 中可能变成 error
2. **第三方 SDK 是最大变数**，Facebook SDK 18.0.0 曾因 StoreKit 1 问题无法编译
3. **Privacy Manifest 是硬性门槛**，没有就直接拒审
4. **Liquid Glass 不只是视觉**，布局结构也会变

---

## 项目地址

- GitHub：[github.com/luodeCoding/ios26-adaptation-skill](https://github.com/luodeCoding/ios26-adaptation-skill)
- 包含：20+ 条扫描规则、三套模板、30 个 FAQ、SDK 兼容性速查表
