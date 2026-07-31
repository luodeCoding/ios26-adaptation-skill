# Phase 3 Checklist: iOS 27 Readiness (Preview)

> **Deadline**: Before the iOS 27 SDK build mandate (**~2027-04 est.**)  
> **Goal**: Satisfy the iOS 27 mandates confirmed at WWDC26 ahead of time  
> **Reference**: [docs/ios27-preview.md](../docs/ios27-preview.md)

All items below are **confirmed requirements** (WWDC26 / Apple documentation), not speculation. Most of them can be verified today with the iOS 26 toolchain.

---

## P0 — App Fails to Launch / Build Fails

### UIScene Lifecycle (Mandatory)
- [ ] `Info.plist` contains `UIApplicationSceneManifest`
- [ ] AppDelegate implements `application(_:configurationForConnecting:options:)`
- [ ] SceneDelegate exists and forwards all lifecycle events to AppDelegate
- [ ] App launches and runs correctly through the scene-based path on iOS 13+
- [ ] Run the scanner: no `ARCH-001` / `ARCH-002` findings

> Apps built with the iOS 27 SDK **fail to launch** without the scene-based lifecycle. Completing Phase 1 of this skill already satisfies this.

### Linker Flags
- [ ] No `-ld_classic` / `-ld64` in any `.xcconfig`, `.pbxproj`, or Podfile `post_install` hook (scanner rule `LINKER-001`)
- [ ] Project links successfully with the modern linker (build once without the flag today)

---

## P0 — App Store Rejection

### Launch Screen (Mandatory)
- [ ] `Info.plist` contains one of: `UILaunchStoryboardName` / `UILaunchStoryboards` / `UILaunchScreen` / `UILaunchScreens`
- [ ] If using generated Info.plist: `xcodebuild -showBuildSettings | grep -i launch` confirms `INFOPLIST_KEY_UILaunchScreen_Generation = YES`
- [ ] No legacy `UILaunchImages` usage (removed; migrate to storyboard/`UILaunchScreen`)

---

## P1 — Deprecations to Migrate

### canOpenURL → Attempt-and-Handle
- [ ] Inventoried all `canOpenURL` call sites (scanner rule `OPENURL-001`)
- [ ] Migrated to `open(_:options:completionHandler:)` with failure handling where possible
- [ ] `LSApplicationQueriesSchemes` trimmed to ≤ 25 entries (scanner rule `OPENURL-002`)
- [ ] Considered `universalLinksOnly` option where only universal-link checks are needed

### On Demand Resources
- [ ] Inventoried `NSBundleResourceRequest` usage (scanner rule `ODR-001`)
- [ ] Planned migration to Background Assets framework

### MetricKit
- [ ] Inventoried `MXMetricManager` usage (scanner rule `METRICKIT-001`)
- [ ] Planned migration to `MetricManager`

---

## P1 — Build Chain

### Clang Modules
- [ ] No duplicate module names across dependencies (Xcode 27 enforces de-duplication)
- [ ] All third-party SDKs updated to versions that build with Xcode 26+ (see [docs/sdk-compatibility.md](../docs/sdk-compatibility.md))

---

## P2 — Layout Modernization

- [ ] Layout logic driven by size classes, not device idiom / orientation checks
- [ ] `UIScreen.main.scale` replaced with `traitCollection.displayScale`
- [ ] Evaluated impact of `UIRequiresFullscreen` becoming discrete-resize behavior
- [ ] App tested with window resizing on iPadOS

---

## Verification

- [ ] `python3 scripts/ios26-scanner.py <project>` shows no iOS 27 forward-looking findings (`OPENURL-001/002`, `ODR-001`, `METRICKIT-001`, `LINKER-001`)
- [ ] Full regression pass on the current release build
- [ ] Re-check [Apple Upcoming Requirements](https://developer.apple.com/news/upcoming-requirements/) for updated dates

---

**Author**: roder
