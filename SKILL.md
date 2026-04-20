---
name: ios26-adaptation
description: iOS 26 adaptation expert. Guides through SDK build adaptation and Liquid Glass design language migration. Handles SceneDelegate architecture, deprecated API replacement, and two-phase adaptation strategy.
---

# iOS 26 Adaptation Expert

## Critical Information

### Deadlines

| Date | Requirement | Phase |
|------|-------------|-------|
| **2026-04-28** | Must build with iOS 26 SDK | Phase 1 |
| **~2026-09** | Liquid Glass mandatory, `UIDesignRequiresCompatibility` removed | Phase 2 |

### Common Misconceptions

- ❌ **Deployment Target change required**: No, keep your current minimum version
- ❌ **Users forced to iOS 26**: No, runtime requirement unchanged
- ❌ **Existing apps removed**: No, only affects new submissions
- ❌ **Grace period exists**: No, April 28 is a hard deadline

---

## Decision Framework

### Step 1: Determine Adaptation Strategy

Based on your next release date:

```
┌─────────────────────────────────────────────┐
│  When is your next app release?              │
└─────────────────────┬───────────────────────┘
                      │
    ┌─────────────────┼─────────────────┐
    │                 │                 │
    ▼                 ▼                 ▼
┌──────────┐   ┌──────────────┐   ┌──────────────┐
│ Before   │   │ 2026-04-28 ~ │   │ After Xcode  │
│ 2026-04- │   │ Xcode 27     │   │ 27 (~2026-09)│
│ 28       │   │              │   │              │
└────┬─────┘   └──────┬───────┘   └──────┬───────┘
     │                │                  │
     ▼                ▼                  ▼
┌──────────┐   ┌──────────────┐   ┌──────────────┐
│ Strategy │   │ Strategy B   │   │ Strategy C   │
│    A     │   │              │   │              │
└──────────┘   └──────────────┘   └──────────────┘
```

### Strategy A: Branch-based Adaptation (Before 2026-04-28 release)

**When to use**: You have a release planned before April 28, 2026

**Approach**:
1. Keep main branch unchanged for current release
2. Create `feature/ios26-adaptation` branch
3. Complete Phase 1 adaptation in branch
4. Merge after April 28 deadline

**Branch Commands**:
```bash
git checkout main
git checkout -b feature/ios26-adaptation
# Complete adaptation work
git checkout main
git merge feature/ios26-adaptation
```

### Strategy B: Phase 1 Required, Phase 2 Evaluated (April 28 ~ Xcode 27)

**When to use**: Release between April 28 and Xcode 27 launch

**Approach**:
1. Must complete Phase 1 (SDK build adaptation)
2. Temporarily disable Liquid Glass
3. Evaluate Phase 2 based on pre-Xcode 27 releases

### Strategy C: Combined Phases (After Xcode 27)

**When to use**: No release until after Xcode 27

**Approach**:
1. Complete both phases in single iteration
2. No temporary disabling needed
3. Full Liquid Glass adaptation upfront

---

## Phase 1: SDK Build Adaptation

### Goal
Build with iOS 26 SDK, maintain existing UI appearance

### Key Tasks

#### 1. Environment Setup

| Tool | Minimum Version |
|------|-----------------|
| Xcode | 26.0+ (recommend 26.3) |
| macOS | Sequoia 15.3+ |
| iOS SDK | 26.0+ |

#### 2. Deprecated API Replacement

| Deprecated API | Replacement | Severity |
|---------------|-------------|----------|
| `keyWindow` | Unified window access interface | Error |
| `delegate.window` | Unified window access interface | Error |
| `UNNotificationPresentationOptionAlert` | `Banner \| List` | Warning |
| `UNAuthorizationOptionAlert` | `Banner` | Warning |

#### 3. SceneDelegate Architecture

**Required Changes**:

1. **Create UIApplication Extension** (Unified Access)
   - `mainWindow()` - Get current window
   - `visibleViewController()` - Get top visible VC
   - `currentNavigationController()` - Get current nav controller

2. **Modify AppDelegate**
   - Add `sharedInstance` class method
   - Separate `setupApplication(launchOptions:)` method
   - Separate `setupSceneUI(window:)` method
   - Add Scene Session configuration

3. **Create/Modify SceneDelegate**
   - Window creation in `willConnectTo`
   - Forward to AppDelegate for business setup
   - Lifecycle event forwarding

4. **Global Code Replacement**
   - Replace all `keyWindow` calls
   - Replace all `delegate.window` calls
   - Update window-based navigation

#### 4. Info.plist Configuration

```xml
<!-- Temporarily disable Liquid Glass -->
<key>UIDesignRequiresCompatibility</key>
<true/>

<!-- SceneDelegate configuration -->
<key>UIApplicationSceneManifest</key>
<dict>
    <key>UIApplicationSupportsMultipleScenes</key>
    <false/>
    <key>UISceneConfigurations</key>
    <dict>
        <key>UIWindowSceneSessionRoleApplication</key>
        <array>
            <dict>
                <key>UISceneConfigurationName</key>
                <string>Default Configuration</string>
                <key>UISceneDelegateClassName</key>
                <string>SceneDelegate</string>
            </dict>
        </array>
    </dict>
</dict>
```

#### 5. Complete Implementation Example (Swift)

Below is a minimal but complete example for a typical iOS app supporting iOS 12+.
Production-ready versions with Objective-C support are available in `templates/`.

**UIApplication+Extension.swift**
```swift
import UIKit

extension UIApplication {
    var mainWindow: UIWindow? {
        if #available(iOS 13.0, *) {
            return connectedScenes
                .compactMap { $0 as? UIWindowScene }
                .first(where: { $0.activationState == .foregroundActive })?
                .windows.first(where: \.isKeyWindow)
                ?? connectedScenes
                .compactMap { $0 as? UIWindowScene }
                .first?
                .windows.first(where: \.isKeyWindow)
                ?? windows.first(where: \.isKeyWindow)
        } else {
            return delegate?.window ?? nil
        }
    }

    var visibleViewController: UIViewController? {
        guard let root = mainWindow?.rootViewController else { return nil }
        return findTop(from: root)
    }

    var currentNavigationController: UINavigationController? {
        return visibleViewController?.navigationController
    }

    private func findTop(from root: UIViewController) -> UIViewController {
        if let presented = root.presentedViewController {
            return findTop(from: presented)
        }
        if let nav = root as? UINavigationController, let visible = nav.visibleViewController {
            return findTop(from: visible)
        }
        if let tab = root as? UITabBarController, let selected = tab.selectedViewController {
            return findTop(from: selected)
        }
        return root
    }
}
```

**AppDelegate.swift**
```swift
import UIKit

@main
class AppDelegate: UIResponder, UIApplicationDelegate {
    var window: UIWindow?

    class func sharedInstance() -> AppDelegate? {
        return UIApplication.shared.delegate as? AppDelegate
    }

    func application(_ application: UIApplication,
                     didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        setupApplication(launchOptions: launchOptions)

        if #available(iOS 13.0, *) {
            // iOS 13+ uses SceneDelegate for UI setup
        } else {
            let window = UIWindow(frame: UIScreen.main.bounds)
            setupSceneUI(window: window)
        }
        return true
    }

    func setupApplication(launchOptions: [UIApplication.LaunchOptionsKey: Any]?) {
        // One-time SDK initializations (analytics, push setup, etc.)
    }

    func setupSceneUI(window: UIWindow) {
        let root = UINavigationController(rootViewController: RootViewController())
        window.rootViewController = root
        window.makeKeyAndVisible()

        if #available(iOS 13.0, *) {
            // SceneDelegate owns the window on iOS 13+
        } else {
            self.window = window
        }
    }

    func application(_ application: UIApplication,
                     configurationForConnecting connectingSceneSession: UISceneSession,
                     options: UIScene.ConnectionOptions) -> UISceneConfiguration {
        return UISceneConfiguration(name: "Default Configuration", sessionRole: connectingSceneSession.role)
    }
}
```

**SceneDelegate.swift**
```swift
import UIKit

class SceneDelegate: UIResponder, UIWindowSceneDelegate {
    var window: UIWindow?

    func scene(_ scene: UIScene, willConnectTo session: UISceneSession, options connectionOptions: UIScene.ConnectionOptions) {
        guard let windowScene = scene as? UIWindowScene else { return }
        let window = UIWindow(windowScene: windowScene)
        self.window = window
        AppDelegate.sharedInstance()?.setupSceneUI(window: window)
    }

    func sceneDidBecomeActive(_ scene: UIScene) {
        AppDelegate.sharedInstance()?.applicationDidBecomeActive(UIApplication.shared)
    }

    func sceneWillResignActive(_ scene: UIScene) {
        AppDelegate.sharedInstance()?.applicationWillResignActive(UIApplication.shared)
    }

    func sceneWillEnterForeground(_ scene: UIScene) {
        AppDelegate.sharedInstance()?.applicationWillEnterForeground(UIApplication.shared)
    }

    func sceneDidEnterBackground(_ scene: UIScene) {
        AppDelegate.sharedInstance()?.applicationDidEnterBackground(UIApplication.shared)
    }
}
```

### Phase 1 Checklist

#### Preparation
- [ ] Determine next release date
- [ ] Choose adaptation strategy (A/B/C)
- [ ] Create adaptation branch
- [ ] Upgrade Xcode to 26.0+
- [ ] Upgrade macOS to Sequoia 15.3+ if needed

#### Scanning
- [ ] Scan for `keyWindow` usage
- [ ] Scan for `delegate.window` usage
- [ ] Scan for notification option alerts
- [ ] Check SceneDelegate configuration status
- [ ] Evaluate third-party SDK compatibility

#### Implementation
- [ ] Create UIApplication extension for unified access
- [ ] Create SceneDelegate (if not exists)
- [ ] Modify AppDelegate for dual-path support
- [ ] Replace all deprecated window access
- [ ] Replace notification option enums
- [ ] Add Info.plist configurations

#### Verification
- [ ] Build succeeds with iOS 26 SDK
- [ ] No deprecated API warnings
- [ ] iOS 12 device: launch normal
- [ ] iOS 13+ device: launch normal
- [ ] Lifecycle events work correctly
- [ ] Global popups display correctly
- [ ] Navigation works correctly
- [ ] Liquid Glass disabled (no new effects)

---

## Phase 2: Liquid Glass Full Adaptation

### Goal
Full adaptation to Liquid Glass design language

### Understanding Liquid Glass

**Auto-adapting System Controls**:
- UITabBar / UITabBarController
- UINavigationBar / UINavigationController
- Keyboard (new glassmorphism style)
- UIToolbar
- UIAlertController / UIActionSheet
- UIButton, UISlider, UISwitch, UISegmentedControl
- UIScrollView (`allowsLiquidTransform` enabled by default)
- SwiftUI standard components

**Visual Changes**:
- Glass optical effects (refraction, reflection)
- Rounded corners and shadows on keyboard
- Enhanced translucency in TabBar
- Navigation bar button styling changes

### Key Tasks

#### 1. Remove Temporary Configuration

Remove from Info.plist:
```xml
<!-- Delete this entire entry -->
<key>UIDesignRequiresCompatibility</key>
<true/>
```

Then clean-build and verify on an iOS 26 device that system controls now show the new glassmorphism style.

#### 2. Audit Custom UI Components

Identify every custom component that touches system chrome or may clash with the new style:

| Category | Examples | What to Check |
|----------|----------|---------------|
| Navigation | Custom nav bars, nav-bar background images, title views | Hardcoded colors, frame math, blur overrides |
| TabBar | Custom tab bars, tab item badges, background images | Translucency conflicts, unreadable selected states |
| Keyboard | Input accessory views, custom input views, keyboard observers | Layout gaps, safe-area mismatches |
| Backgrounds | Full-screen gradients, solid color backgrounds | Clash with glass refraction behind system bars |
| Controls | Custom buttons/switches/sliders placed next to system ones | Visual harmony, size mismatch, color drift |

#### 3. Fix Navigation Bar Issues

Common problems after removing `UIDesignRequiresCompatibility`:

- **Hardcoded background colors** that fight the new translucency  
  → Use `UINavigationBarAppearance` or let the system manage the background.
- **Manual frame calculations on nav-bar subviews**  
  → Avoid adding subviews directly to `UINavigationBar`. Use `navigationItem.titleView` or custom container VCs.
- **Back-button image replacements looking cropped**  
  → Re-test all custom back-button assets in Light, Dark, and tinted modes.

#### 4. Fix Keyboard & Input Issues

- Verify every text field still sits in the correct position when the keyboard appears.
- Check input accessory views: their background may now sit on top of a glass keyboard. Consider using `UIInputView` with a system background or adding subtle padding.
- Re-test secure text entry fields; their visual treatment may have changed.

#### 5. Fix Scroll View & Animation Issues

- `UIScrollView.allowsLiquidTransform` is **enabled by default** on iOS 26. If any scroll view looks distorted during edge scrolling, explicitly set `allowsLiquidTransform = false`.
- Custom transition animations may be interrupted mid-flight on iOS 26. Add guards so your completion blocks do not run twice.
- Navigation-bar frame math may return negative Y coordinates. Replace manual frame reads with `safeAreaInsets` or `layoutMarginsGuide` where possible.

#### 6. Visual Regression Testing

| Component | Check Point |
|-----------|-------------|
| Navigation Bar | Coordination with custom styling |
| Keyboard | Input field positioning, accessory views |
| TabBar | Text/icon readability |
| Scroll Views | Scroll performance, visual effects |
| Custom Controls | Harmony with system controls |

#### 7. Technical Adaptations Summary

- **Transition Animations**: iOS 26 allows interruption — add idempotency guards.
- **Frame Adjustments**: Navigation bar may have negative Y coordinates — prefer Auto Layout / safe area.
- **Custom Navigation**: Verify compatibility with new system behavior after removing the compatibility flag.

### Phase 2 Checklist

#### Preparation
- [ ] Confirm Xcode 27 release timeline
- [ ] Schedule dedicated UI testing time
- [ ] Prepare iOS 26+ test devices

#### Implementation
- [ ] Remove `UIDesignRequiresCompatibility` flag
- [ ] Review all custom UI components
- [ ] Check navigation bar customizations
- [ ] Verify keyboard accessory views
- [ ] Test TabBar readability

#### Verification
- [ ] Liquid Glass effects display correctly
- [ ] Navigation bar visual harmony
- [ ] Keyboard interactions work correctly
- [ ] TabBar text/icon readability
- [ ] Long list scrolling smooth
- [ ] Modal presentation normal
- [ ] Custom controls coordinate with system

---

## Testing Framework

### Version Compatibility Matrix

| iOS Version | Phase 1 | Phase 2 | Priority |
|-------------|---------|---------|----------|
| Minimum supported | ✅ | ✅ | P0 |
| iOS 13-15 | ✅ | - | P0 |
| iOS 16-25 | ✅ | - | P1 |
| iOS 26+ | ✅ | ✅ | P0 |

### Critical Test Scenarios

1. **Cold Launch**: App launch from terminated state
2. **Hot Launch**: Resume from background
3. **Lifecycle**: Background/foreground transitions
4. **Window Access**: Global alerts, toasts, loading
5. **Navigation**: Push/pop/present/dismiss
6. **Notifications**: Receive and tap handling
7. **Deep Link**: URL scheme handling
8. **Rotation**: Device orientation changes

### Third-Party SDK Testing

| SDK Type | Test Points |
|----------|-------------|
| Push Notifications | Receive, tap, token refresh |
| Share SDK | Share sheet, callback handling |
| Analytics | Lifecycle event accuracy |
| Maps | Location, map display |
| Login | OAuth, callback |

---

## Risk Assessment

| Risk | Level | Mitigation | Phase |
|------|-------|------------|-------|
| April 28 deadline missed | Critical | Start early, track progress | 1 |
| Global replacement missed | High | Multiple scan rounds | 1 |
| iOS 12 compatibility broken | Medium | Strict version branching | 1 |
| Third-party SDK issues | Medium | Test all SDK functionality | 1/2 |
| Lifecycle events lost | High | Ensure SceneDelegate forwarding | 1 |
| Xcode 27 unprepared | Critical | Reserve Phase 2 time | 2 |
| Liquid Glass visual issues | Medium | UI regression testing | 2 |
| Keyboard layout broken | Medium | Check all input fields | 2 |

---

## Scanner Rules Reference

### Window Access Patterns

| Rule ID | Pattern | Severity |
|---------|---------|----------|
| WINDOW-001 | `UIApplication.shared.keyWindow` | Error |
| WINDOW-002 | `[UIApplication sharedApplication].keyWindow` | Error |
| WINDOW-003 | `delegate.window` | Warning |
| WINDOW-004 | `AppDelegate.*window` | Warning |
| WINDOW-005 | `.window.rootViewController` | Warning |
| WINDOW-006 | `.window.visibleViewController` | Warning |

### Notification Patterns

| Rule ID | Pattern | Severity |
|---------|---------|----------|
| NOTIF-001 | `UNNotificationPresentationOptionAlert` | Warning |
| NOTIF-002 | `UNAuthorizationOptionAlert` | Warning |

### Status Bar Patterns

| Rule ID | Pattern | Severity |
|---------|---------|----------|
| STATUS-001 | `statusBarStyle = UIStatusBarStyle` | Warning |
| STATUS-002 | `UIApplication.shared.*statusBarStyle` | Warning |

---

## Code Replacement Templates

### Window Access

**Before**:
```swift
// Swift
let window = UIApplication.shared.keyWindow
let appDelegate = UIApplication.shared.delegate as! AppDelegate
let vc = appDelegate.window?.rootViewController
```

```objc
// Objective-C
UIWindow *window = [UIApplication sharedApplication].keyWindow;
AppDelegate *appDelegate = [AppDelegate sharedInstance];
UIViewController *vc = [appDelegate.window rootViewController];
```

**After**:
```swift
// Swift
let window = UIApplication.shared.mainWindow
let vc = UIApplication.shared.visibleViewController
```

```objc
// Objective-C
UIWindow *window = [[UIApplication sharedApplication] mainWindow];
UIViewController *vc = [[UIApplication sharedApplication] visibleViewController];
```

### Notification Options

**Before**:
```swift
// Swift
completionHandler([.alert, .sound, .badge])
```

```objc
// Objective-C
completionHandler(UNNotificationPresentationOptionAlert |
                 UNNotificationPresentationOptionSound |
                 UNNotificationPresentationOptionBadge);
```

**After**:
```swift
// Swift
if #available(iOS 26.0, *) {
    completionHandler([.banner, .list, .sound, .badge])
} else {
    completionHandler([.alert, .sound, .badge])
}
```

```objc
// Objective-C
if (@available(iOS 26.0, *)) {
    completionHandler(UNNotificationPresentationOptionBanner |
                     UNNotificationPresentationOptionList |
                     UNNotificationPresentationOptionSound |
                     UNNotificationPresentationOptionBadge);
} else {
    completionHandler(UNNotificationPresentationOptionAlert |
                     UNNotificationPresentationOptionSound |
                     UNNotificationPresentationOptionBadge);
}
```

### Authorization Options

**Before**:
```swift
// Swift
let options: UNAuthorizationOptions = [.alert, .sound, .badge]
```

```objc
// Objective-C
UNAuthorizationOptions options = UNAuthorizationOptionAlert |
                                 UNAuthorizationOptionSound |
                                 UNAuthorizationOptionBadge;
```

**After**:
```swift
// Swift
let options: UNAuthorizationOptions
if #available(iOS 26.0, *) {
    options = [.banner, .sound, .badge]
} else {
    options = [.alert, .sound, .badge]
}
```

```objc
// Objective-C
UNAuthorizationOptions options;
if (@available(iOS 26.0, *)) {
    options = UNAuthorizationOptionBanner |
              UNAuthorizationOptionSound |
              UNAuthorizationOptionBadge;
} else {
    options = UNAuthorizationOptionAlert |
              UNAuthorizationOptionSound |
              UNAuthorizationOptionBadge;
}
```

---

## Troubleshooting

### Build Errors

**Error**: `'keyWindow' was deprecated in iOS 13.0`
- **Solution**: Replace with unified window access interface

**Error**: `Cannot find 'SceneDelegate' in scope`
- **Solution**: Create SceneDelegate.swift/m file

**Error**: `UIApplicationSceneManifest` missing
- **Solution**: Add to Info.plist

### Runtime Issues

**Issue**: Window returns nil on iOS 13+
- **Cause**: Still using AppDelegate.window in SceneDelegate architecture
- **Solution**: Use unified access interface that checks connectedScenes

**Issue**: Lifecycle events not firing
- **Cause**: SceneDelegate not forwarding to AppDelegate
- **Solution**: Implement forwarding in all SceneDelegate lifecycle methods

**Issue**: Notifications not displaying correctly on iOS 26
- **Cause**: Using deprecated Alert option
- **Solution**: Update to Banner/List options with version check

---

## Consultation Triggers

### Must Consult

- Uncertain about release timeline
- More than 100 deprecated API occurrences
- Extensive custom UI components
- Old third-party SDK versions
- No iOS 26 testing devices available

### Recommended to Confirm

- Branch creation: `feature/ios26-adaptation`
- Phase separation strategy
- Testing device allocation
- Rollback plan if issues arise

---

## Resources

### Internal Documents
- [Code Templates](../templates/) — Production-ready Swift and Objective-C templates
- [FAQ](../docs/faq.md) — Common questions about deadlines, build errors, and Liquid Glass
- [Testing Guide](../docs/testing-guide.md) — Complete testing framework for QA teams
- [Chinese Framework Guide](../.claude/iOS26-适配框架指南.md) — Full adaptation framework in Chinese

### External Links
- [Apple Developer News](https://developer.apple.com/news/)
- [iOS 26 Release Notes](https://developer.apple.com/documentation/ios-release-notes)
- [SceneDelegate Documentation](https://developer.apple.com/documentation/uikit/app_and_environment/scenes)
- [Liquid Glass Design](https://developer.apple.com/design/)

---

**Author**: roder
