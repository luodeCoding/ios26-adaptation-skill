# iOS 26 Adaptation FAQ

> **Last Updated:** 2026-04-14

---

## General

### Q1: Why is iOS 26 adaptation mandatory?

Apple requires all apps submitted after **April 28, 2026** to be built with the iOS 26 SDK. This is a hard deadline — there is no grace period. Apps that are not built with iOS 26 SDK will be rejected from App Store submission.

### Q2: Do I need to change my Deployment Target to iOS 26?

**No.** Keep your current minimum iOS version (e.g., iOS 12, 13, 15). The runtime requirement for users is still determined by your Deployment Target. Only the **SDK used to build** the app must be iOS 26.

### Q3: Will my existing app be removed from the App Store?

**No.** Only **new submissions and updates** are affected. Existing app versions already on the App Store will remain available.

### Q4: Do users have to upgrade to iOS 26?

**No.** As long as your Deployment Target remains lower (e.g., iOS 13), users on older iOS versions can still download and run your app.

---

## Phase 1: SDK Build Adaptation

### Q5: Does every project need SceneDelegate migration?

If your app targets **iOS 13+** and does not yet use `SceneDelegate`, then **yes**, you should migrate. iOS 26 SDK enforces stricter window access patterns, and `keyWindow` / `delegate.window` will cause build errors or runtime issues.

If your app only targets **iOS 12** (extremely rare today), SceneDelegate is not required, but you must still build with iOS 26 SDK.

### Q6: My project uses CocoaPods. What if Pods contain deprecated APIs?

**Do not modify Pods directly.** Instead:
1. Run `pod update` or check each pod's changelog for iOS 26 / Xcode 26 compatibility.
2. If a pod is unmaintained, consider:
   - Forking and updating it yourself
   - Replacing it with a maintained alternative
   - Using `post_install` hooks only as a last resort

### Q7: Can I use the iOS 26 simulator for Phase 1 testing?

**Yes**, but with caveats:
- You can verify builds and basic functionality.
- Some features (push notifications, camera, precise lifecycle events) behave differently on simulators.
- **Strongly recommended**: test on a physical device before release.

### Q8: Does `UIDesignRequiresCompatibility` work on the simulator?

Yes. It works on both simulator and physical devices running iOS 26. Its purpose is to force the legacy UI appearance instead of Liquid Glass.

### Q9: Do I have to complete Phase 1 and Phase 2 in the same release?

**No.** That's exactly why there are two phases:
- **Phase 1** (before 2026-04-28) is mandatory for any release after the deadline.
- **Phase 2** (before Xcode 27 ~2026-09) is only mandatory if you plan to release after Xcode 27, or if Apple begins enforcing Liquid Glass earlier.

### Q10: My app is written in SwiftUI. Do I still need SceneDelegate?

SwiftUI apps using `App` lifecycle (`@main`) do not need manual `SceneDelegate` creation. However:
- If your SwiftUI app mixes UIKit (e.g., uses `UIApplication.shared.keyWindow`), those calls must still be updated.
- `UIDesignRequiresCompatibility` still applies in `Info.plist` if you want to temporarily disable Liquid Glass.

---

## Phase 2: Liquid Glass

### Q11: What happens if I forget Phase 2 and Xcode 27 releases?

When Xcode 27 is released, `UIDesignRequiresCompatibility` will be **ignored or rejected**. Your app will automatically show Liquid Glass effects. If you have not tested them, you risk visual regressions, layout bugs, or App Store rejection for poor UI quality.

### Q12: Which UI components are automatically adapted to Liquid Glass?

Standard UIKit controls get the new look automatically:
- `UINavigationBar` / `UINavigationController`
- `UITabBar` / `UITabBarController`
- `UIToolbar`
- `UIAlertController` / `UIActionSheet`
- `UIButton`, `UISlider`, `UISwitch`, `UISegmentedControl`
- Keyboard (new glassmorphism style)
- `UIScrollView` (`allowsLiquidTransform` is on by default)
- SwiftUI standard components

**Custom UI** must be manually reviewed.

### Q13: My custom navigation bar looks weird under Liquid Glass. What do I do?

Common fixes:
- Remove hardcoded background colors that clash with translucency.
- Avoid manual frame calculations on navigation bar subviews.
- Test in both Light and Dark Mode.
- Consider letting the system handle more styling and reduce custom overrides.

---

## Build Errors & Troubleshooting

### Q14: Build error: `'keyWindow' was deprecated in iOS 13.0`

This becomes an **error** in iOS 26 SDK. Replace all occurrences with the unified window access interface. See `templates/swift/UIApplication+Extension.swift` or `templates/objc/UIApplication+Extension.h/.m`.

### Q15: Build error: `Cannot find 'SceneDelegate' in scope`

Your `Info.plist` references `SceneDelegate` under `UIApplicationSceneManifest`, but the file does not exist in your project. Create `SceneDelegate.swift` (or `SceneDelegate.m` / `SceneDelegate.h`).

### Q16: Runtime issue: `window` returns `nil` on iOS 13+

You are likely still accessing `AppDelegate.window` or `UIApplication.shared.keyWindow` somewhere. In the SceneDelegate architecture, the key window belongs to the active `UIWindowScene`, not the app delegate. Use the `UIApplication+Extension` template to safely retrieve the current window across all iOS versions.

### Q17: Runtime issue: Lifecycle events (background/foreground) are not firing

Ensure your `SceneDelegate` forwards all lifecycle events to `AppDelegate`:
- `sceneDidBecomeActive`
- `sceneWillResignActive`
- `sceneWillEnterForeground`
- `sceneDidEnterBackground`

See `templates/swift/SceneDelegate.swift` or `templates/objc/SceneDelegate.m` for a full forwarding implementation.

### Q18: Build warning: `UNNotificationPresentationOptionAlert` is deprecated

Replace it with a version-checked call using `.banner` and `.list` on iOS 26+. See `templates/swift/NotificationAdapter.swift` or `templates/objc/NotificationAdapter.h/.m`.

---

## Testing

### Q19: What is the minimum device matrix I should test?

| iOS Version | Priority | What to verify |
|-------------|----------|----------------|
| Minimum supported (e.g., 12.x) | P0 | Launch path unchanged, backward compatibility |
| iOS 13-15 | P0 | SceneDelegate path works, lifecycle events fire |
| iOS 16-17 | P1 | General stability |
| iOS 26.x | P0 | Build success, new APIs work, Liquid Glass disabled (Phase 1) or enabled (Phase 2) |

### Q20: Can I automate the scanning process?

Yes. This skill includes `scripts/ios26-scanner.py`, which scans your project for deprecated APIs and architectural gaps. Run it like this:

```bash
python3 scripts/ios26-scanner.py /path/to/your/ios/project
python3 scripts/ios26-scanner.py /path/to/your/ios/project --format json --output scan-report.json
```

---

## Strategy & Planning

### Q21: We have a release planned for April 20, 2026. What should we do?

Use **Strategy A**: keep `main` unchanged for the April 20 release, and create `feature/ios26-adaptation` to prepare Phase 1. Merge the branch after April 28.

### Q22: We have no release planned until October 2026. What should we do?

Use **Strategy C**: combine Phase 1 and Phase 2 into a single iteration. You do not need `UIDesignRequiresCompatibility`; instead, fully adapt to Liquid Glass upfront.

### Q23: Should I create separate branches for Phase 1 and Phase 2?

You can, but it is optional. A single `feature/ios26-adaptation` branch is usually sufficient. If Phase 2 work is large or involves a design team, consider sub-branches (`feature/ios26-phase1`, `feature/ios26-phase2`).

---

## Related Documents

- [SKILL.md](../SKILL.md) — Detailed adaptation strategy and implementation guides
- [Testing Guide (docs/testing-guide.md)](./testing-guide.md) — Complete testing framework for QA teams
- [templates/](../templates/) — Production-ready Swift and Objective-C code templates

---

**Author**: roder
