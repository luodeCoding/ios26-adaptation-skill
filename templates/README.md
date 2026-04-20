# iOS 26 Adaptation Code Templates

This directory contains production-ready code templates for the most common iOS 26 adaptation tasks.

## Structure

```
templates/
├── swift/                    # Swift templates
│   ├── UIApplication+Extension.swift   # Unified window/navigation access
│   ├── SceneDelegate.swift             # Full SceneDelegate implementation
│   ├── AppDelegate+Setup.swift         # AppDelegate refactoring example
│   └── NotificationAdapter.swift       # Notification options adapter
└── objc/                     # Objective-C templates
    ├── UIApplication+Extension.h/.m
    ├── SceneDelegate.h/.m
    ├── AppDelegate+Setup.h/.m
    └── NotificationAdapter.h/.m
```

## How to Use

1. **Copy** the relevant files into your Xcode project.
2. **Rename** classes (e.g., `RootViewController`) to match your project.
3. **Adapt** method signatures if your existing `AppDelegate` already has similar methods.
4. **Verify** all lifecycle events are forwarded correctly in `SceneDelegate`.

## Important Notes

- These templates assume **iOS 12+** support.
- `UIApplication+Extension` gracefully falls back to `delegate.window` on iOS 12.
- `NotificationAdapter` centralizes version checks so you don't scatter `@available` checks everywhere.
- The `AppDelegate+Setup` templates are designed as **extensions/commented examples** — integrate them into your existing AppDelegate rather than replacing it entirely.
