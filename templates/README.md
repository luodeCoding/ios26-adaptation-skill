# iOS 26 Adaptation Code Templates

This directory contains code templates for the most common iOS 26 adaptation tasks.

> ⚠️ **These are reference templates only.** They are not compiled into any project.  
> Copy the code you need into your main project and modify as needed.

## Structure

```
templates/
├── swift/                    # Swift templates
│   ├── UIApplication+MainWindow.swift       # Unified window/navigation access
│   ├── SceneDelegate.swift                  # SceneDelegate implementation
│   ├── AppDelegate+Setup.swift              # AppDelegate refactoring example
│   └── UNNotificationOptions+Adapter.swift  # Notification options adapter
├── objc/                     # Objective-C templates
│   ├── UIApplication+MainWindow.h/.m
│   ├── SceneDelegate.h/.m
│   ├── AppDelegate+Setup.h/.m
│   └── UNNotificationOptionsAdapter.h/.m
└── mixed/                    # Mixed Swift/Objective-C projects
    └── README.md                            # Bridging strategies & cross-language guide
```

## How to Use

### For AI Assistants

Read these templates as reference when generating code for the main project. Use the patterns and structure, but generate code that fits the specific main project.

### For Developers

1. **Open** the template file you need
2. **Copy** the code
3. **Paste** into your main project's appropriate location
4. **Modify** class names (e.g., `RootViewController` → your actual root VC)
5. **Adapt** method signatures if your existing code uses different conventions

### Important Notes

- These templates assume **iOS 12+** support
- `UIApplication+Extension` gracefully falls back to `delegate.window` on iOS 12
- `NotificationAdapter` centralizes version checks so you don't scatter `@available` checks everywhere
- The `AppDelegate+Setup` templates are designed as **extensions/commented examples** — integrate them into your existing AppDelegate rather than replacing it entirely
- **Do not** add these files to your Xcode project directly — copy the code content only
