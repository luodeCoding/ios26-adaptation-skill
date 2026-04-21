# iOS 26 Adaptation Code Templates

This directory contains production-ready code templates for the most common iOS 26 adaptation tasks.

## Structure

```
templates/
├── swift/                    # Swift templates
│   ├── UIApplication+MainWindow.swift       # Unified window/navigation access
│   ├── SceneDelegate.swift                  # Full SceneDelegate implementation
│   ├── AppDelegate+Setup.swift              # AppDelegate refactoring example
│   └── UNNotificationOptions+Adapter.swift  # Notification options adapter
└── objc/                     # Objective-C templates
    ├── UIApplication+MainWindow.h/.m
    ├── SceneDelegate.h/.m
    ├── AppDelegate+Setup.h/.m
    └── UNNotificationOptionsAdapter.h/.m
```

## How to Use

### Step 1: Copy files to your project

Drag the files you need from `templates/swift/` (or `templates/objc/`) into your Xcode project:

1. In Xcode, right-click your project folder → **Add Files to "YourProject"...**
2. Select the template files you need
3. Check **"Create groups"** and check your target
4. Click **Add**

### Step 2: Rename and adapt

- Replace `RootViewController` with your actual root view controller class name
- If your `AppDelegate` already has similar methods, merge rather than replace
- Adjust method signatures if your existing code uses different naming conventions

### Step 3: Verify lifecycle forwarding

Make sure all lifecycle events in `SceneDelegate` are correctly forwarded to your `AppDelegate`:

```swift
// SceneDelegate.swift
func sceneDidBecomeActive(_ scene: UIScene) {
    AppDelegate.sharedInstance()?.applicationDidBecomeActive(UIApplication.shared)
}

func sceneWillEnterForeground(_ scene: UIScene) {
    AppDelegate.sharedInstance()?.applicationWillEnterForeground(UIApplication.shared)
}
// ... etc
```

Missing any of these can break analytics, state saving, and push notification handling.

## Important Notes

- These templates assume **iOS 12+** support.
- `UIApplication+Extension` gracefully falls back to `delegate.window` on iOS 12.
- `NotificationAdapter` centralizes version checks so you don't scatter `@available` checks everywhere.
- The `AppDelegate+Setup` templates are designed as **extensions/commented examples** — integrate them into your existing AppDelegate rather than replacing it entirely.
- After copying, these files become part of your project. Modify them freely to fit your needs.
