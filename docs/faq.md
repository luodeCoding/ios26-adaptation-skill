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

`UNNotificationPresentationOptionAlert` was deprecated in **iOS 14.0**, not iOS 26.0. Replace it with a version-checked call using `.banner` and `.list` on iOS 14.0+:

```swift
if #available(iOS 14.0, *) {
    completionHandler([.banner, .list, .sound, .badge])
} else {
    completionHandler([.alert, .sound, .badge])
}
```

> ⚠️ **Do NOT confuse with `UNAuthorizationOptions`**: `UNAuthorizationOptionAlert` is **NOT deprecated** and remains valid in iOS 26 SDK. There is no `UNAuthorizationOptionBanner` — it does not exist in the SDK.

See `templates/swift/UNNotificationOptions+Adapter.swift` or `templates/objc/UNNotificationOptionsAdapter.h/.m`.

---

## Build & SDK

### Q19: Build warning: `UIScreen.main` is deprecated

`UIScreen.main` has been promoted from `API_TO_BE_DEPRECATED` to **deprecated** in the iOS 26 SDK.

- **For iOS 13+**: Get screen bounds from `UIWindowScene`:
  ```swift
  if let scene = UIApplication.shared.connectedScenes
      .first(where: { $0.activationState == .foregroundActive }) as? UIWindowScene {
      let bounds = scene.screen.bounds
  }
  ```
- **For iOS 12 fallback path**: You may still use `UIScreen.main.bounds` inside the `else` branch of `#available(iOS 13.0, *)`. The compiler warning is acceptable here because there is no alternative on iOS 12.

> ⚠️ If your deployment target is iOS 13+, remove all `UIScreen.main` usage entirely.

### Q20: Hundreds of new concurrency warnings after building with Xcode 26

Xcode 26 ships with **Swift 6** and enables strict concurrency checking by default.

Common fixes:
1. **Add `@MainActor`** to ViewModels and any class that updates UI:
   ```swift
   @MainActor
   class MyViewModel: ObservableObject { }
   ```
2. **Mark mutable reference types** that cross isolation boundaries:
   ```swift
   final class MyManager: @unchecked Sendable { }
   ```
   > Use `@unchecked Sendable` only when you have verified thread safety manually.
3. **Replace `DispatchQueue.main.async`** with `@MainActor` methods or `MainActor.run`:
   ```swift
   await MainActor.run {
       self.updateUI()
   }
   ```
4. **Migrate completion handlers to `async/await`** for new or heavily used APIs.

Plan time for this — projects with many `@escaping` closures may see hundreds of warnings.

### Q21: Network requests fail after building with iOS 26 SDK

iOS 26 SDK raises the **minimum TLS version** for `URLSession` and Network framework from 1.0 to **1.2**.

- Check `Info.plist` for `NSExceptionMinimumTLSVersion` or `NSAllowsArbitraryLoads` and remove them if possible
- Verify all backend APIs and third-party services support TLS 1.2+
- Corporate VPN / intranet connections using legacy TLS may break — coordinate with IT to upgrade

### Q22: CoreData build error: `NSPersistentStoreUbiquitousContentNameKey` not found

These deprecated CoreData iCloud sync keys have been **removed** in iOS 26:

- `NSPersistentStoreUbiquitousContentNameKey`
- `NSPersistentStoreUbiquitousContentURLKey`
- `NSPersistentStoreUbiquitousPeerTokenOption`
- `NSPersistentStoreRemoveUbiquitousMetadataOption`
- `NSPersistentStoreUbiquitousContainerIdentifierKey`
- `NSPersistentStoreRebuildFromUbiquitousContentOption`

**Migration path**:
- iOS 13+: Use `NSPersistentCloudKitContainer`
- iOS 17+: Use `SwiftData`

After removing these keys, the local persistent store remains usable (without iCloud sync). Plan a separate migration for cloud sync.

---

## Liquid Glass

### Q23: Floating TabBar breaks my bottom-aligned UI (FAB, bottom sheet, etc.)

iOS 26 TabBar is now **floating** instead of full-width docked. This changes `safeAreaInsets.bottom`.

**Symptoms**:
- Floating action button (FAB) sits too low or overlaps the TabBar
- Custom bottom sheets have incorrect bottom padding
- Manually calculated `bottom: 80` constants no longer align

**Fix**:
- Use `UIViewController.additionalSafeAreaInsets` instead of hardcoded padding
- Respond to `viewSafeAreaInsetsDidChange()` to recalculate layouts dynamically
- For SwiftUI, use `safeAreaInset(edge: .bottom)` with dynamic content

### Q24: My custom navigation bar hit-testing is broken after Liquid Glass

Liquid Glass causes the system to **auto-insert `UIDropShadowView`** behind navigation bars and toolbars. This can interfere with:
- Custom hit-testing logic that traverses `subviews`
- Code that assumes `navigationBar.subviews.first` is your custom view
- View-index-based logic

**Fix**:
- Do not rely on exact subview indexes for system bars
- Use `UINavigationBar.standardAppearance` / `scrollEdgeAppearance` for customization instead of manual subview manipulation
- If you must traverse subviews, filter by class type rather than index

### Q25: Custom background colors look wrong with Liquid Glass

Liquid Glass uses **refraction layers** that expect translucency. Custom solid `backgroundColor` on `UINavigationBar`, `UITabBar`, or `UIToolbar` creates visual seams.

**Fix**:
- Remove custom `backgroundColor` on these bars
- Use `UIBlurEffect` / `UIVisualEffectView` if you need a custom background
- Or let the system apply the default glass material

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
