# iOS 26 适配代码模板集：Swift / Objective-C / 混合项目全覆盖

**摘要**：本文介绍一套开源的 iOS 26 SDK 适配代码模板，覆盖 Swift、Objective-C 及混合项目，包含窗口统一访问、SceneDelegate 双路径架构、通知选项适配、Swift 6 并发迁移及 Privacy Manifest 模板。

---

## 一、模板目录结构

```
templates/
├── swift/
│   ├── UIApplication+MainWindow.swift      # 统一窗口访问
│   ├── SceneDelegate.swift                  # 完整生命周期实现
│   ├── AppDelegate+Setup.swift              # 双路径重构示例
│   ├── UNNotificationOptions+Adapter.swift  # 通知选项适配
│   └── Swift6ConcurrencyAdapter.swift       # Swift 6 并发迁移
├── objc/
│   ├── UIApplication+MainWindow.h/.m
│   ├── SceneDelegate.h/.m
│   ├── AppDelegate+Setup.h/.m
│   └── UNNotificationOptionsAdapter.h/.m
├── mixed/
│   └── README.md                            # 混合项目桥接指南
└── PrivacyInfo.xcprivacy                    # Privacy Manifest 模板
```

---

## 二、Swift 模板详解

### 1. UIApplication+MainWindow.swift

统一窗口访问接口，兼容 iOS 12 和 iOS 13+：

```swift
extension UIApplication {
    var mainWindow: UIWindow? {
        if #available(iOS 13.0, *) {
            for scene in connectedScenes {
                if let windowScene = scene as? UIWindowScene,
                   windowScene.activationState == .foregroundActive {
                    return windowScene.windows.first(where: { $0.isKeyWindow })
                }
            }
            return connectedScenes
                .compactMap { ($0 as? UIWindowScene)?.windows.first(where: \.isKeyWindow) }
                .first
        }
        return delegate?.window
    }
    
    var visibleViewController: UIViewController? {
        guard let root = mainWindow?.rootViewController else { return nil }
        return findTopViewController(from: root)
    }
}
```

### 2. SceneDelegate.swift

完整生命周期实现，包含 URL 转发：

```swift
class SceneDelegate: UIResponder, UIWindowSceneDelegate {
    var window: UIWindow?

    func scene(_ scene: UIScene, willConnectTo session: UISceneSession,
               options connectionOptions: UIScene.ConnectionOptions) {
        guard let windowScene = scene as? UIWindowScene else { return }
        let window = UIWindow(windowScene: windowScene)
        self.window = window
        AppDelegate.sharedInstance()?.setupSceneUI(window: window)
    }

    // 生命周期转发到 AppDelegate
    func sceneWillEnterForeground(_ scene: UIScene) {
        AppDelegate.sharedInstance()?.applicationWillEnterForeground(UIApplication.shared)
    }
}
```

### 3. Swift6ConcurrencyAdapter.swift

Swift 6 严格并发迁移模式：

```swift
// @MainActor 标记 UI 相关 ViewModel
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

// @unchecked Sendable 用于手动验证线程安全的引用类型
final class SharedCache: @unchecked Sendable {
    private var storage: [String: Data] = [:]
    private let lock = NSLock()
    
    func set(_ data: Data, forKey key: String) {
        lock.lock()
        storage[key] = data
        lock.unlock()
    }
}
```

---

## 三、Objective-C 模板详解

### UIApplication+MainWindow.m

```objc
@implementation UIApplication (Extension)

- (UIWindow *)mainWindow {
    if (@available(iOS 13.0, *)) {
        for (UIScene *scene in self.connectedScenes) {
            if ([scene isKindOfClass:[UIWindowScene class]] && 
                scene.activationState == UISceneActivationStateForegroundActive) {
                UIWindowScene *windowScene = (UIWindowScene *)scene;
                for (UIWindow *window in windowScene.windows) {
                    if (window.isKeyWindow) return window;
                }
            }
        }
    }
    return self.delegate.window;
}

@end
```

---

## 四、混合项目桥接

当 `AppDelegate` 是 Objective-C 而 `SceneDelegate` 是 Swift 时：

**Bridging Header**（Swift 调用 OC）：
```objc
#import "AppDelegate.h"
#import "UIApplication+MainWindow.h"
```

**Swift SceneDelegate**：
```swift
class SceneDelegate: UIResponder, UIWindowSceneDelegate {
    var window: UIWindow?
    
    func scene(_ scene: UIScene, willConnectTo session: UISceneSession,
               options connectionOptions: UIScene.ConnectionOptions) {
        guard let windowScene = scene as? UIWindowScene else { return }
        let window = UIWindow(windowScene: windowScene)
        self.window = window
        AppDelegate.sharedInstance()?.setupSceneUI(window)
    }
}
```

---

## 五、PrivacyInfo.xcprivacy 模板

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" 
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>NSPrivacyAccessedAPITypes</key>
    <array>
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategoryFileTimestamp</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array><string>C617.1</string></array>
        </dict>
    </array>
    <key>NSPrivacyCollectedDataTypes</key>
    <array>
        <!-- 声明收集的数据类型 -->
    </array>
    <key>NSPrivacyTracking</key>
    <false/>
</dict>
</plist>
```

完整模板包含所有 Required Reason API 的示例声明。

---

## 六、使用方法

1. 根据项目语言选择模板目录（swift / objc / mixed）
2. 将文件复制到主项目中，修改类名和逻辑
3. 运行扫描脚本验证：`python3 scripts/ios26-scanner.py /your/project`

---

## 七、项目地址

- GitHub：[github.com/luodeCoding/ios26-adaptation-skill](https://github.com/luodeCoding/ios26-adaptation-skill)
- 模板路径：`templates/`

---

**关键词**：iOS 26 模板、SceneDelegate、Swift 6、Privacy Manifest、Objective-C、混合项目
