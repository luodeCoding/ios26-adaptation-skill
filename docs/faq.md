# iOS 26 Adaptation FAQ

> **Last Updated:** 2026-08-03

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

> **Note for pure Swift projects:** If your deployment target is iOS 13+ and you don't have SceneDelegate yet, the app will still compile on iOS 26 SDK (backward compatibility is maintained). However, **iOS 27 has been confirmed at WWDC26 to make the scene-based lifecycle mandatory** — apps built with the iOS 27 SDK without it **fail to launch**. Migrate now to avoid last-minute issues (see Q36).

### Q5a: My pure Swift project doesn't have SceneDelegate. Is that a build error?

**No.** For pure Swift projects targeting iOS 13+, the absence of SceneDelegate does not cause a compilation failure on iOS 26 SDK. Apple maintains backward compatibility for legacy AppDelegate.window apps.

However, you will encounter **compile errors** for removed APIs like `UIApplication.shared.keyWindow`. The fix is to replace `keyWindow` with a SceneDelegate-compatible window accessor (e.g., `UIApplication.shared.mainWindow`) **and** add SceneDelegate — iOS 27 makes it mandatory (apps fail to launch without it, see Q36).

Use the simplified pure-Swift templates (`templates/swift/SceneDelegate+SwiftOnly.swift`, `templates/swift/AppDelegate+SwiftOnly.swift`) which avoid `@objc` annotations and use `static let shared` instead of `sharedInstance`.

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

This becomes an **error** in iOS 26 SDK. Replace all occurrences with the unified window access interface. See `templates/swift/UIApplication+MainWindow.swift` or `templates/objc/UIApplication+MainWindow.h/.m`.

### Q14a: Build error: `'ALAssetsLibrary' is unavailable in iOS`

`AssetsLibrary.framework` and `ALAssetsLibrary` are **obsoleted in iOS 26** (not just deprecated). Any `import AssetsLibrary` or `#import <AssetsLibrary/AssetsLibrary.h>` will cause a build error.

**Fix:**
1. Remove all `import AssetsLibrary` / `#import <AssetsLibrary/AssetsLibrary.h>` statements
2. Replace any `ALAssetsLibrary` usage with `PHPhotoLibrary` from the `Photos` framework
3. Most projects only used AssetsLibrary for photo permissions — these should already be using `PHPhotoLibrary.authorizationStatus()`

### Q15: Build error: `Cannot find 'SceneDelegate' in scope`

Your `Info.plist` references `SceneDelegate` under `UIApplicationSceneManifest`, but the file does not exist in your project. Create `SceneDelegate.swift` (or `SceneDelegate.m` / `SceneDelegate.h`).

### Q16: Runtime issue: `window` returns `nil` on iOS 13+

You are likely still accessing `AppDelegate.window` or `UIApplication.shared.keyWindow` somewhere. In the SceneDelegate architecture, the key window belongs to the active `UIWindowScene`, not the app delegate. Use the `UIApplication+MainWindow` template to safely retrieve the current window across all iOS versions.

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

### Q19a: Build warning: `windows` / `statusBarFrame` deprecated

Two more window-related deprecations become noisy under the iOS 26 SDK:

- **`UIApplication.shared.windows`** (deprecated since iOS 15): enumerate `connectedScenes` and use `UIWindowScene.windows` instead — or simply use the `UIApplication+MainWindow` template which already does this.
- **`UIApplication.shared.statusBarFrame`** (deprecated since iOS 13): use the scene's status bar manager:

  ```swift
  let height = UIApplication.shared.mainWindow?
      .windowScene?.statusBarManager?.statusBarFrame.height ?? 0
  ```

The scanner flags these as `WINDOW-007/008` and `STATUS-004`.

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

### Q25: Multiple right navigation bar buttons look wrong on iOS 26

iOS 26 Liquid Glass merges multiple navigation-bar buttons into a shared glass background. To restore independent backgrounds, set `hidesSharedBackground = true` on each `UIBarButtonItem`.

However, this causes two side effects:
1. **Extra spacing** appears between buttons (system injects fixed spacing between private `PlatterView` containers).
2. **Order reversal** — `rightBarButtonItems` may render in reverse order compared to earlier iOS versions.

**Fix**:
- Use the `UINavigationBar+LiquidGlassAdapter` template (Swift or Objective-C). It swizzles `layoutSubviews`, finds all `PlatterView` containers at runtime, and repositions them with zero spacing while restoring the correct visual order.
- **Recommended**: apply the fix to **right-side items only** (`applyRightBarButtonItemsFix`). The system back button on the left usually looks fine; only apply left-side fixes if your design team explicitly requires it.
- Call `navController.applyLiquidGlassRightButtonFix()` (Swift) or `[navController lg_applyLiquidGlassRightButtonFix]` (Objective-C) after creating your navigation controller.

### Q25a: Custom background colors look wrong with Liquid Glass

Liquid Glass uses **refraction layers** that expect translucency. Custom solid `backgroundColor` on `UINavigationBar`, `UITabBar`, or `UIToolbar` creates visual seams.

**Fix**:
- Remove custom `backgroundColor` on these bars
- Use `UIBlurEffect` / `UIVisualEffectView` if you need a custom background
- Or let the system apply the default glass material

### Q25b: App crashes on iOS 26 with custom TabBar (`setValue:forKey:@"tabBar"`)

iOS 26 adds **runtime protection** to the `tabBar` property of `UITabBarController`. The classic private-KVC trick:

```objc
[self setValue:customTabBar forKey:@"tabBar"];   // 💥 iOS 26
```

now causes a **crash**, an extra tab appearing, or the custom tab bar silently failing.

**Fix**:
- For styling only: use `UITabBarAppearance` (`standardAppearance` / `scrollEdgeAppearance`)
- For a fully custom tab bar: build a custom container view controller and hide the system tab bar, instead of overriding the private property
- The scanner flags this as `TABBAR-001` (Error)

### Q25c: View added to navigationBar disappears on iOS 26

iOS 26's new navigation bar uses a **compositing layer structure** that swallows subviews added directly via `[navigationBar addSubview:]` — typically the view vanishes after a push/pop.

**Fix**:
- Add overlay views to `navigationController.view` instead
- For title-area content, use `navigationItem.titleView`
- The scanner flags this as `NAVBAR-001` (Warning)

### Q25d: Bar button image shows blue tint despite `AlwaysOriginal` on iOS 26

On iOS 26, a `UIBarButtonItem` created from an image with `UIImageRenderingModeAlwaysOriginal` may still render with the blue `tintColor`.

**Fix** (either works):
- Set `item.tintColor = UIColor.clear` on the affected item, or
- Use a `customView` `UIButton` with the image instead of an image-based bar button item

### Q25e: `statusBarFrame` returns 0 on iOS 26

`windowScene.statusBarManager.statusBarFrame` can return a zero frame at certain lifecycle moments on iOS 26 (early in scene connection, during transitions).

**Fix**: don't base layout on status-bar frame math — use `view.safeAreaLayoutGuide` / `safeAreaInsets`, which the system keeps correct at all times.

---

## App Store Submission

### Q26: App Store Connect rejected my build for missing Privacy Manifest

Since May 2024, Apple requires every app to include a `PrivacyInfo.xcprivacy` file. iOS 26 submissions will be **automatically rejected** without it.

**What to do**:
1. In Xcode: File → New → App Privacy → name it `PrivacyInfo.xcprivacy`
2. Add it to your app target
3. Declare:
   - **Required Reason APIs** you use (file timestamps, disk space, User Defaults, etc.)
   - **Data types** you collect (with usage purposes)
   - **Third-party SDKs** that don't bundle their own manifest
4. Generate a Privacy Report in Xcode Organizer to validate

> ⚠️ Common blocker: Firebase, Facebook SDK, or older analytics SDKs may not include a privacy manifest. Update to the latest version, or manually declare their data usage in your app's manifest.

### Q27: Build error: `SKPaymentTransaction` is deprecated / not found

StoreKit 1 APIs (`SKPaymentTransaction`, `SKProductsRequest`, `SKPaymentQueue`) are **removed** in Xcode 26. You must migrate to **StoreKit 2** (iOS 15+).

**Quick migration**:
| Old (StoreKit 1) | New (StoreKit 2) |
|-----------------|-----------------|
| `SKProductsRequest` | `Product.products(for: ids)` |
| `SKPaymentQueue.add()` | `product.purchase()` |
| `SKPaymentTransactionObserver` | `Transaction.updates` async sequence |
| Receipt `verifyReceipt` | App Store Server API |

If you support iOS 12-14, wrap StoreKit 2 code in `#available(iOS 15.0, *)` and keep StoreKit 1 for older versions.

### Q28: Siri no longer responds to my app's voice commands

Apple has deprecated multiple SiriKit intent domains. If your app uses any of these, Siri will reply "I can't support that request":

- CarPlay intents (climate, audio, seat settings)
- Lists & Notes intents
- Payment intents (transfer money, pay bill)
- Photo search / playback intents
- Visual Code intents
- VoIP call history intents

**Migration**: Convert your SiriKit Intents to **App Intents**. Xcode provides automatic conversion: select your `.intentdefinition` file → Editor → Convert to App Intents.

### Q29: SwiftUI build warnings: `NavigationView` is deprecated

SwiftUI modern API replacements for iOS 26 compatibility:

| Deprecated | Use Instead |
|-----------|-------------|
| `NavigationView` | `NavigationStack` (iOS 16+) |
| `.cornerRadius()` | `.clipShape(.rect(cornerRadius:))` |
| `.foregroundColor()` | `.foregroundStyle()` |
| `ObservableObject` / `@StateObject` | `@Observable` macro + `@State` (iOS 17+) |
| `onChange(of:) { value in }` | `onChange(of:) { old, new in }` |
| `presentationMode` | `@Environment(\.dismiss)` |

These are warnings, not errors, but cleaning them up reduces technical debt.

### Q30: Build warning: `UIImagePickerController` is deprecated

Use `PHPickerViewController` (PhotosUI, iOS 14+) instead:

```swift
import PhotosUI

var config = PHPickerConfiguration(photoLibrary: .shared())
config.selectionLimit = 1
config.filter = .images
let picker = PHPickerViewController(configuration: config)
picker.delegate = self
present(picker, animated: true)
```

Benefits: no photo library permission required, supports multi-selection and filtering.

---

## Testing

### Q31: What is the minimum device matrix I should test?

| iOS Version | Priority | What to verify |
|-------------|----------|----------------|
| Minimum supported (e.g., 12.x) | P0 | Launch path unchanged, backward compatibility |
| iOS 13-15 | P0 | SceneDelegate path works, lifecycle events fire |
| iOS 16-17 | P1 | General stability |
| iOS 26.x | P0 | Build success, new APIs work, Liquid Glass disabled (Phase 1) or enabled (Phase 2) |

### Q32: Can I automate the scanning process?

Yes. This skill includes `scripts/ios26-scanner.py`, which scans your project for deprecated APIs and architectural gaps. Run it like this:

```bash
python3 scripts/ios26-scanner.py /path/to/your/ios/project
python3 scripts/ios26-scanner.py /path/to/your/ios/project --format json --output scan-report.json
```

---

## Strategy & Planning

### Q33: We have a release planned for April 20, 2026. What should we do?

Use **Strategy A**: keep `main` unchanged for the April 20 release, and create `feature/ios26-adaptation` to prepare Phase 1. Merge the branch after April 28.

### Q34: We have no release planned until October 2026. What should we do?

Use **Strategy C**: combine Phase 1 and Phase 2 into a single iteration. You do not need `UIDesignRequiresCompatibility`; instead, fully adapt to Liquid Glass upfront.

### Q35: Should I create separate branches for Phase 1 and Phase 2?

You can, but it is optional. A single `feature/ios26-adaptation` branch is usually sufficient. If Phase 2 work is large or involves a design team, consider sub-branches (`feature/ios26-phase1`, `feature/ios26-phase2`).

---

## iOS 27 Preview (Confirmed at WWDC26)

> Full details: [docs/ios27-preview.md](./ios27-preview.md)

### Q36: Is it true that apps will fail to launch on iOS 27 without SceneDelegate?

**Yes — confirmed by Apple.** Per the official migration guide: "Beginning in iOS 27, iPadOS 27, Mac Catalyst 27, tvOS 27, and visionOS 27, apps built with the latest SDK must adopt the scene-based life cycle **or they fail to launch**."

Key nuances:
- The trigger is **the SDK you build with**, not the user's OS version. Shipped binaries built with the iOS 26 SDK keep working on iOS 27.
- You need to migrate if **either**: your Info.plist has no `UIApplicationSceneManifest` configuration, **or** your AppDelegate doesn't implement `application(_:configurationForConnecting:options:)`.
- **Multi-window support stays optional** — only the lifecycle itself is mandated.
- UIKit has logged a migration warning for affected apps since iOS 18.4.

Completing this skill's Phase 1 SceneDelegate migration satisfies the requirement.

### Q37: Will my app be rejected for a missing launch screen on iOS 27?

**Yes**, for apps built with the 27.0 SDK. The Info.plist must contain one of: `UILaunchStoryboardName`, `UILaunchStoryboards`, `UILaunchScreen`, or `UILaunchScreens`. Missing all four → App Store **rejects** the submission (iOS/iPadOS only).

⚠️ **Don't audit by grepping the repo**: Xcode 13+ projects with generated Info.plist (`GENERATE_INFOPLIST_FILE = YES`) write the key at build time via `INFOPLIST_KEY_UILaunchScreen_Generation = YES` — no file in the repository contains it. Ask the build system instead:

```bash
xcodebuild -showBuildSettings -project YourApp.xcodeproj -target YourApp \
  -configuration Release -sdk iphoneos 2>/dev/null \
  | grep -E "^ +(GENERATE_INFOPLIST_FILE|INFOPLIST_FILE|INFOPLIST_KEY_UILaunch)"
```

Highest-risk group: old projects still using the long-deprecated `UILaunchImages` key — it does **not** count.

### Q38: `canOpenURL` is deprecated in iOS 27 — what do I use instead?

Apple's guidance is **attempt-and-handle**: call `open(_:options:completionHandler:)` directly and handle the failure, instead of validating first. The `open` method is **not constrained** by `LSApplicationQueriesSchemes`.

```swift
let opened = await UIApplication.shared.open(url)
if !opened { presentWebFallback() }
```

Two things to plan for:
1. **`LSApplicationQueriesSchemes` limit drops from 50 to 25** for apps linked against the iOS 27 SDK — excess entries silently return `false`. The scanner flags >25 entries as `OPENURL-002`.
2. "Is app X installed?" checks without side effects lose their direct equivalent. The surviving option is `universalLinksOnly: true` (Universal Links only, not custom schemes).

### Q39: What build-chain changes should I prepare for Xcode 27?

Confirmed P0/P1 items:

| Change | Impact | Quick check |
|--------|--------|-------------|
| `-ld_classic` / ld64 removed | Build failure | `grep -r "ld_classic" --include="*.xcconfig" --include="*.pbxproj" .` |
| Clang module name dedup enforced | Build failure | `find . -name "module.modulemap" \| sort` |
| On Demand Resources deprecated | Migrate to Background Assets | `grep -r "NSBundleResourceRequest" --include="*.swift" --include="*.m" .` |
| `MXMetricManager` → `MetricManager` | MetricKit rework | scanner rule `METRICKIT-001` |

The scanner covers `-ld_classic` (`LINKER-001`), ODR (`ODR-001`), and MetricKit (`METRICKIT-001`) automatically.

### Q40: What are the environment requirements for Xcode 27?

Confirmed at WWDC26 (as of iOS 27.0 beta 3 / Xcode 27 beta 3, 2026-07):

- Xcode 27 beta requires **macOS Tahoe 26.4+**, ships **Swift 6.4** and the iOS 27 SDK.
- Xcode 27 runs on **Apple Silicon Macs only** — Intel Macs cannot install it.
- Physical-device debugging requires **iOS 17+** devices; simulators still support older versions.
- `ARCHS_STANDARD` for macOS 27.0+ targets no longer includes x86_64.
- iOS 27 official release is expected in **September 2026** alongside iPhone 18; the public beta was already rolled out in mid-July 2026.

### Q41: Besides the build chain, which code-level breaking changes should I audit before linking against the iOS 27 SDK?

Three P1 behavior changes that won't be caught by the scanner:

1. **NSURL double-encoding fix** — `+[NSURL URLWithString:]` no longer double-encodes `%` inside valid percent-escape sequences. Any workaround you wrote for the old behavior may now break URL parsing. Search and review your URL-encoding workarounds.
2. **C++ standard library semantics** — `multimap/multiset::find()` no longer guarantees returning the *first* equivalent element; use `lower_bound`/`equal_range` instead. Also `bitset::operator[]` now returns `bool`. Matters mostly for projects with C++ layers (media, maps, game engines).
3. **`stat()` name collision** — new `FilePath.stat()` / `FileDescriptor.stat()` instance methods in the System framework can clash with unqualified `stat()` calls in custom extensions, breaking compilation. Qualify with `Darwin.stat()` or migrate to the new Swift API.

Also see the beta known-issues table (Address Sanitizer needs Xcode 26.5+, etc.) in [ios27-preview.md §6](./ios27-preview.md#6-ios-27-beta-已知问题截至-2026-07).

---

## Using This Skill (Impact & Installation)

### Q42: If an AI applies this skill to my main project, will it touch my business code?

**No — the skill is bound by an explicit low-impact promise** (see SKILL.md § Adaptation Impact Boundaries and INTEGRATION.md § 适配影响声明):

- ✅ Only iOS 26/27-related code is changed: scanner-flagged deprecated call sites, SceneDelegate lifecycle architecture, Info.plist adaptation keys, and new adapter files from `templates/`
- ✅ All version differences are wrapped in `#available` / `@available`; pre-iOS 13 fallback paths are preserved
- ❌ Never touched: Deployment Target, business logic, unrelated files, third-party SDK sources (`Pods/`), and any “drive-by modernization”
- ✅ Auditable flow: scan → file change list with reasons → apply only after confirmation → re-scan until Error-level findings are zero

Every requirement traces back to Apple official sources (Upcoming Requirements, release notes, WWDC, TN3187) — nothing invented.

### Q43: Where can I see every iOS 26/27 deadline and what each one requires?

**[docs/timeline.md](./timeline.md)** ([中文](./timeline.zh.md)) is the single authoritative reference: six milestones from 2025-06 to ~2027-04, each with Apple's mandate, the required adaptation scope (itemized with scanner rule IDs), the consequence of inaction, and the matching checklist. Key nodes: **2026-04-28** (iOS 26 SDK builds, now in effect), **~2026-09** (Xcode 27, Liquid Glass mandatory), **~2027-04 est.** (iOS 27 SDK builds; apps without UIScene lifecycle fail to launch).

### Q44: How do I install this repo as an AI skill?

**Claude Code** (native SKILL.md format):

```bash
git clone https://github.com/luodeCoding/ios26-adaptation-skill.git ~/.claude/skills/ios26-adaptation
```

Then, inside your iOS project, just say "帮我适配 iOS 26" / "Help me adapt to iOS 26".

**Qoder / other agent tools**: install the repo as a plugin/skill from its GitHub URL, or clone it anywhere and point the agent at the folder — `SKILL.md` + `AGENTS.md` contain everything the agent needs. No file from this repo ever enters your Xcode project or build.

---

## Related Documents

- [SKILL.md](../SKILL.md) — Detailed adaptation strategy and implementation guides
- [Timeline & Adaptation Scope (docs/timeline.md)](./timeline.md) — Every iOS 26/27 milestone and its required scope ([中文](./timeline.zh.md))
- [Testing Guide (docs/testing-guide.md)](./testing-guide.md) — Complete testing framework for QA teams
- [iOS 27 Preview (docs/ios27-preview.md)](./ios27-preview.md) — Confirmed iOS 27 / Xcode 27 mandates and migration paths
- [templates/](../templates/) — Production-ready Swift and Objective-C code templates

---

**Author**: roder
