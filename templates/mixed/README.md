# Mixed (Swift/Objective-C) Project Guide

This guide covers iOS 26 adaptation for projects that contain **both Swift and Objective-C** code.

## Why Mixed Projects Need Special Attention

In a pure Swift or pure Objective-C project, you pick one template set and apply it. In a mixed project, `AppDelegate` might be Objective-C while `SceneDelegate` is Swift (or vice-versa), and window-access code must work from both languages without duplication.

## Common Mixed Architectures

| Architecture | Typical Scenario | Recommended Approach |
|--------------|------------------|----------------------|
| **Objective-C AppDelegate + Swift SceneDelegate** | Legacy project gradually migrating to Swift | Keep setup methods in Objective-C AppDelegate; Swift SceneDelegate calls them via bridging header. |
| **Swift AppDelegate + Objective-C SceneDelegate** | New project with some Objective-C UI code | Expose `sharedInstance()` and `setupSceneUI(_:)` with `@objc`/`@objcMembers`. |
| **Both Objective-C, mostly Swift VCs** | Older mixed project | Use Objective-C `UIApplication+MainWindow` category; Swift VCs access via bridging header. |

## Window Access Strategy

**Rule of thumb**: Implement the unified window accessor once in Objective-C. Swift sees it automatically through the bridging header.

### Objective-C Category (Single Source of Truth)

Use `templates/objc/UIApplication+MainWindow.h` and `.m`. Add the header to your bridging header:

```objc
// YourProject-Bridging-Header.h
#import "UIApplication+MainWindow.h"
```

### Swift Usage

```swift
let window = UIApplication.shared.mainWindow()
let vc = UIApplication.shared.visibleViewController()
```

> Note the parentheses — Swift sees Objective-C methods as methods, not properties.

### If You Prefer Property Syntax In Swift

Add a thin Swift wrapper (no logic duplication):

```swift
// UIApplication+SwiftWrappers.swift
import UIKit

extension UIApplication {
    var mainWindow: UIWindow? {
        return self.mainWindow()
    }

    var visibleViewController: UIViewController? {
        return self.visibleViewController()
    }
}
```

## Cross-Language AppDelegate / SceneDelegate

### Scenario A: Objective-C AppDelegate + Swift SceneDelegate

**Bridging Header**
```objc
#import "AppDelegate.h"
```

**Swift SceneDelegate**
```swift
import UIKit

class SceneDelegate: UIResponder, UIWindowSceneDelegate {
    var window: UIWindow?

    func scene(_ scene: UIScene, willConnectTo session: UISceneSession, options connectionOptions: UIScene.ConnectionOptions) {
        guard let windowScene = scene as? UIWindowScene else { return }
        let window = UIWindow(windowScene: windowScene)
        self.window = window
        AppDelegate.sharedInstance()?.setupSceneUI(window)
    }

    // ... lifecycle forwarding ...
}
```

### Scenario B: Swift AppDelegate + Objective-C SceneDelegate

**Swift AppDelegate** (must expose methods to Objective-C)
```swift
import UIKit

@main
@objcMembers
class AppDelegate: UIResponder, UIApplicationDelegate {
    var window: UIWindow?

    class func sharedInstance() -> AppDelegate? {
        return UIApplication.shared.delegate as? AppDelegate
    }

    func setupSceneUI(window: UIWindow) {
        // Build your UI
        window.rootViewController = UINavigationController(rootViewController: RootViewController())
        window.makeKeyAndVisible()

        if #available(iOS 13.0, *) {
            // SceneDelegate owns the window on iOS 13+
        } else {
            self.window = window
        }
    }

    // ... other delegate methods ...
}
```

**Objective-C SceneDelegate**
```objc
#import "SceneDelegate.h"
#import "YourProject-Swift.h"   // Auto-generated Swift header

@implementation SceneDelegate

- (void)scene:(UIScene *)scene willConnectToSession:(UISceneSession *)session options:(UISceneConnectionOptions *)connectionOptions {
    if (![scene isKindOfClass:[UIWindowScene class]]) return;
    UIWindowScene *windowScene = (UIWindowScene *)scene;
    UIWindow *window = [[UIWindow alloc] initWithWindowScene:windowScene];
    self.window = window;
    [[AppDelegate sharedInstance] setupSceneUI:window];
}

// ... lifecycle forwarding ...

@end
```

## Lifecycle Forwarding in Mixed Projects

Regardless of which language each delegate is written in, **always forward lifecycle events** to the AppDelegate so analytics, state saving, and other SDKs continue to work.

If your AppDelegate is Objective-C and SceneDelegate is Swift, the bridging header lets Swift call the Objective-C lifecycle methods directly.

If your AppDelegate is Swift and SceneDelegate is Objective-C, mark the lifecycle methods with `@objc`:

```swift
@objc func applicationDidBecomeActive(_ application: UIApplication) { ... }
@objc func applicationWillResignActive(_ application: UIApplication) { ... }
@objc func applicationWillEnterForeground(_ application: UIApplication) { ... }
@objc func applicationDidEnterBackground(_ application: UIApplication) { ... }
```

## Notification Options in Mixed Projects

Use the Objective-C `NotificationAdapter` (`templates/objc/UNNotificationOptionsAdapter.h/.m`) from both languages:

**Objective-C**
```objc
#import "UNNotificationOptionsAdapter.h"
completionHandler([NotificationAdapter presentationOptions]);
```

**Swift**
```swift
// Via bridging header
completionHandler(NotificationAdapter.presentationOptions())
```

Alternatively, use the Swift adapter (`templates/swift/UNNotificationOptions+Adapter.swift`) and expose it to Objective-C with `@objc`, but the Objective-C adapter is simpler for mixed projects.

## Checklist for Mixed Projects

- [ ] Identify which language your `AppDelegate` and `SceneDelegate` are written in
- [ ] Ensure bridging header is up to date and included in Build Settings
- [ ] Add Objective-C `UIApplication+MainWindow` to the bridging header
- [ ] Verify Swift code calling `mainWindow()` compiles (note the parentheses)
- [ ] If AppDelegate is Swift, add `@objcMembers` or `@objc` to methods called by Objective-C SceneDelegate
- [ ] Confirm auto-generated Swift header (`YourProject-Swift.h`) is imported in Objective-C files that call Swift
- [ ] Test lifecycle forwarding works in both directions
