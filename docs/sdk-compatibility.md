# Third-Party SDK iOS 26 Compatibility Cheat Sheet

> **最后更新**: 2026-05-06  
> **适用范围**: iOS 26 SDK / Xcode 26

---

## 🔴 必须更新（不更新会导致编译失败）

| SDK | 当前问题 | 最低兼容版本 | 操作建议 |
|-----|---------|------------|---------|
| **Facebook iOS SDK** | 使用 StoreKit 1 API (`SKPaymentQueue` 等)，Xcode 26 编译失败 | 18.1.0+ | 升级到最新版，或等待官方修复 |
| **RevenueCat** | StoreKit 1 API 废弃警告 | 5.0.0+ (默认 StoreKit 2) | 升级到 5.x，设置 `.with(storeKitVersion: .storeKit2)` |
| **Branch** | StoreKit 1 废弃警告 | 3.7.0+ | 升级 SDK |
| **Firebase Analytics** | 缺少 Privacy Manifest | 10.24.0+ | 升级以解决 `NSPrivacyAccessedAPICategoryDiskSpace` 错误 |
| **AppsFlyer** | 缺少 Privacy Manifest | 6.14.0+ | 升级 SDK |
| **Adjust** | 缺少 Privacy Manifest | 4.38.0+ | 升级 SDK |
| **UMeng/友盟** | 旧版未适配 Privacy Manifest | 最新版 | 更新到官网最新版本 |
| **Bugly** | 旧版未适配 iOS 26 SDK | 最新版 | 更新 SDK |

---

## 🟡 建议更新（会产生警告或功能异常）

| SDK | 当前问题 | 最低兼容版本 | 操作建议 |
|-----|---------|------------|---------|
| **Alamofire** | TLS 1.0/1.1 配置可能异常 | 5.9.0+ | 检查自定义 `ServerTrustManager` 配置 |
| **SDWebImage** | `UIScreen.main` 使用产生警告 | 5.19.0+ | 升级到使用 `UITraitCollection` 的版本 |
| **Kingfisher** | `UIScreen.main` 使用产生警告 | 7.11.0+ | 升级 |
| **SnapKit** | 无严重问题 | 5.6.0+ | 保持最新即可 |
| **Moya** | 依赖 Alamofire，需同步升级 | 15.0.0+ | 随 Alamofire 一起升级 |
| **Realm** | CoreData iCloud key 无关，但需验证 | 10.50.0+ | 测试 Cloud Sync 功能 |
| **CocoaLumberjack** | 无严重问题 | 3.8.0+ | 保持最新 |
| **SwiftyBeaver** | 无严重问题 | 2.0.0+ | 保持最新 |
| **IQKeyboardManager** | 可能受 Liquid Glass 影响 | 7.0.0+ | 测试键盘弹起时的布局 |
| **SVProgressHUD / MBProgressHUD** | 可能受 `UIScreen.main` 影响 | 最新版 | 检查窗口获取逻辑 |
| **AFNetworking** | `NSURLConnection` 已移除 | 4.0.0+ (使用 NSURLSession) | 升级到 4.x 或迁移到 Alamofire |
| **Masonry / SnapKit-ObjC** | 无严重问题 | 最新版 | 保持最新 |

---

## 🟢 确认兼容（无需特殊处理）

| SDK | 说明 |
|-----|------|
| **Lottie** | 纯渲染库，不受 SDK 变更影响 |
| **RxSwift** | 响应式框架，兼容 Swift 6 (需添加 `@MainActor`) |
| **PromiseKit** | 兼容，但建议逐步迁移到原生 async/await |
| **SwiftLint** | 开发工具，不影响运行时 |
| **SwiftFormat** | 开发工具，不影响运行时 |
| **SwifterSwift** | 兼容，部分 API 可能有废弃警告 |

---

## ⚠️ 需要特别注意的 SDK

### 推送相关

| SDK | 注意点 |
|-----|--------|
| **极光推送 (JPush)** | 验证 `UNNotificationPresentationOptionAlert` 替换逻辑 |
| **个推 (Getui)** | 同上 |
| **Firebase Cloud Messaging** | 最新版已适配 iOS 26 |
| **OneSignal** | 5.x 已适配，旧版需升级 |

### 地图/定位

| SDK | 注意点 |
|-----|--------|
| **高德地图** | 验证 Privacy Manifest 是否包含定位 API 声明 |
| **百度地图** | 同上 |
| **Google Maps** | 8.x+ 已包含 Privacy Manifest |

### 社交分享

| SDK | 注意点 |
|-----|--------|
| **微信 SDK** | 验证是否包含 Privacy Manifest |
| **QQ SDK** | 同上 |
| **微博 SDK** | 同上 |
| **ShareSDK** | 需更新到包含各平台 Privacy Manifest 的版本 |

---

## 🔧 快速检查命令

```bash
# 1. 检查所有依赖是否有更新
pod outdated                    # CocoaPods
swift package update --dry-run  # SPM

# 2. 检查 Privacy Manifest 是否缺失
grep -r "PrivacyInfo.xcprivacy" Pods/ 2>/dev/null | wc -l

# 3. 检查 StoreKit 1 使用
grep -r "SKPaymentTransaction\|SKProductsRequest\|SKPaymentQueue" Pods/ 2>/dev/null

# 4. 检查 UIScreen.main 使用
grep -r "UIScreen.main" Pods/ 2>/dev/null | head -20
```

---

## 📋 SDK 更新检查清单

- [ ] 运行 `pod outdated` 或检查 SPM 依赖更新
- [ ] 确认每个 SDK 的 Privacy Manifest 存在（或在自己的 manifest 中声明）
- [ ] 确认没有 SDK 使用已移除的 StoreKit 1 API
- [ ] 在 iOS 26 模拟器上完整测试所有 SDK 功能
- [ ] 检查 SDK 的 GitHub issues 中是否有 iOS 26 / Xcode 26 相关讨论

---

**免责声明**: 本表基于公开信息和社区反馈整理，SDK 版本兼容性可能随时变化。请以各 SDK 官方文档为准。
