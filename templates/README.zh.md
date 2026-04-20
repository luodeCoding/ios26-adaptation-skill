# iOS 26 适配代码模板

本目录包含可直接用于生产环境的最常见 iOS 26 适配任务代码模板。

## 目录结构

```
templates/
├── swift/                    # Swift 模板
│   ├── UIApplication+MainWindow.swift       # 统一窗口/导航访问
│   ├── SceneDelegate.swift                  # 完整 SceneDelegate 实现
│   ├── AppDelegate+Setup.swift              # AppDelegate 改造示例
│   └── UNNotificationOptions+Adapter.swift  # 通知选项适配器
└── objc/                     # Objective-C 模板
    ├── UIApplication+MainWindow.h/.m
    ├── SceneDelegate.h/.m
    ├── AppDelegate+Setup.h/.m
    └── UNNotificationOptionsAdapter.h/.m
```

## 使用方法

1. **复制** 相关文件到你的 Xcode 项目中。
2. **重命名** 类名（例如将 `RootViewController` 改为你项目中的根视图控制器）。
3. **适配** 方法签名（如果你的 `AppDelegate` 已经有类似方法，需要合并而非替换）。
4. **验证** `SceneDelegate` 中的所有生命周期事件是否正确转发到 `AppDelegate`。

## 重要提示

- 这些模板假设应用支持 **iOS 12+**。
- `UIApplication+Extension` 在 iOS 12 上会优雅回退到 `delegate.window`。
- `NotificationAdapter` 集中处理了版本判断，避免在项目中到处写 `@available`。
- `AppDelegate+Setup` 模板设计为**扩展示例**——建议将其内容整合到你现有的 AppDelegate 中，而不是完全替换。
