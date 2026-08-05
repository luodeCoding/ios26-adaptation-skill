# iOS 26/27 Adaptation Coverage Matrix (Coverage Ledger)

> **Single source of truth**: [`scripts/adaptation-ledger.json`](../scripts/adaptation-ledger.json) (v1.12.0, 50 items).
> This document mirrors the ledger. If the two disagree, the JSON ledger wins.
> A CI consistency test guarantees: every `auto` item's rule IDs must exist in the scanner — **future omissions fail the build**.

## How Zero-Omission Adaptation Is Guaranteed

The most common AI adaptation failure is "missing something different every time". This skill blocks omissions with three layers:

| Layer | Mechanism | Covers |
|---|---|---|
| 1. Auto-detection | `scripts/ios26-scanner.py`: 37 line-level rules + 14 project-level rules | All `detection: auto` items |
| 2. Manual audit | **Manual Audit Checklist** at the end of the scan report | All `detection: manual` items (not statically detectable) |
| 3. Ship gate | **Completion Gate** at the end of the scan report (SHIP-01~05) | Definition of "ship-ready" |

**Usage**: run the scanner in the project root — the report includes the checklist and the gate. AI agents follow the "Zero-Omission Loop" in `SKILL.md` until the gate is fully green.

```bash
python3 scripts/ios26-scanner.py /path/to/YourProject --format markdown
```

Detection legend:

- **auto** — detected by the scanner, with rule IDs
- **manual** — not statically detectable; listed item by item in the report's manual checklist
- **test** — verified via build/runtime/test matrix (see [testing-guide.md](testing-guide.md))

---

## Phase 1: iOS 26 SDK Build Adaptation (deadline **2026-04-28**)

| ID | Item | Detection | Rule IDs | Verification |
|---|---|---|---|---|
| P1-01 | Replace deprecated window access (keyWindow / delegate.window / windows) | auto | WINDOW-001~008 | Unified `UIApplication.mainWindow`, zero compile warnings |
| P1-02 | Replace status bar APIs (statusBarStyle / statusBarFrame) | auto | STATUS-001~004 | Use safeAreaLayoutGuide / statusBarManager |
| P1-03 | Replace UIScreen.main | auto | SCREEN-001~002 | Use UIWindowScene.screen (keep iOS 12 path, commented) |
| P1-04 | Notification foreground options (Alert → Banner\|List) | auto | NOTIF-001 | Wrapped in `#available(iOS 14)` |
| P1-05 | SceneDelegate file exists | auto | ARCH-001 | iOS 13+ path creates window via SceneDelegate |
| P1-06 | Info.plist UIApplicationSceneManifest | auto | ARCH-002 / ARCH-004 | Static routing or dynamic scene-configuration |
| P1-07 | AppDelegate sharedInstance / lifecycle forwarding | auto | ARCH-003 | setupApplication / setupSceneUI extracted |
| P1-08 | Lifecycle forwarding completeness (foreground/background/active) | test | — | Testing guide scenario 3: analytics + state saving intact |
| P1-09 | StoreKit 1 → StoreKit 2 (StoreKit 1 removed in Xcode 26) | auto | STOREKIT-001 | StoreKit 2 on iOS 15+, dual path below |
| P1-10 | AssetsLibrary framework removed | auto | ASSETSLIBRARY-001~003 | Migrate to Photos |
| P1-11 | Remove UIWebView | auto | WEB-001 | Migrate to WKWebView (rejection risk) |
| P1-12 | Privacy Manifest (PrivacyInfo.xcprivacy) | auto | PRIVACY-001 | Required Reason APIs + data collection declared |
| P1-13 | CoreData iCloud Ubiquitous sync keys removed | auto | COREDATA-001 | Migrate to NSPersistentCloudKitContainer / SwiftData |
| P1-14 | TLS minimum 1.2 | auto | TLS-001 | Remove TLS exceptions, verify internal services |
| P1-15 | SiriKit intent domains → App Intents | auto | SIRIKIT-001 | Xcode auto-conversion + regression |
| P1-16 | SwiftUI deprecated APIs (NavigationView, etc.) | auto | SWIFTUI-001~003 | Modern replacements per deployment target |
| P1-17 | UIImagePickerController → PHPickerViewController | auto | PHOTOS-001 | PhotosUI picker regression |
| P1-18 | Swift 6 strict concurrency new-warning triage | auto | SWIFT6-001 | Only fix warnings introduced by the new SDK (low-impact boundary) |
| P1-19 | Temporary Liquid Glass opt-out (UIDesignRequiresCompatibility) | auto | PHASE2-001 | May add in Phase 1; must remove in Phase 2 |
| P1-20 | iOS 26 SDK build succeeds with no deprecation warnings | test | — | Xcode 26 clean build, warnings zeroed |

## Phase 2: Liquid Glass Full Adaptation (before Xcode 27, ~**2026-09**)

| ID | Item | Detection | Rule IDs | Verification |
|---|---|---|---|---|
| P2-01 | Remove UIDesignRequiresCompatibility | auto | PHASE2-001 | Glass effect renders on iOS 26 device after clean build |
| P2-02 | Custom TabBar private KVC (tabBar setValue) crash audit | auto | TABBAR-001 | Use UITabBarAppearance / custom container |
| P2-03 | navigationBar addSubview overlay breakage audit | auto | NAVBAR-001 | Use titleView / navigationController.view |
| P2-04 | rightBarButtonItems order reversal + shared background spacing | auto | BARBUTTON-001 | Apply LiquidGlassAdapter + visual regression |
| P2-05 | Keyboard glass toolbar (inputAccessoryView) as needed | auto | KEYBOARD-001~003 | Only fix visually conflicting inputs |
| P2-06 | Floating TabBar safeArea change (bottom layout) | manual | — | Audit hardcoded bottom constants; use additionalSafeAreaInsets |
| P2-07 | UIScrollView.allowsLiquidTransform edge distortion | manual | — | Visual check of long-list edge scrolling |
| P2-08 | UIDropShadowView auto-insertion vs view-traversal assumptions | manual | — | Audit code indexing system-bar subviews |
| P2-09 | Interruptible transitions (completion idempotency) | manual | — | Audit double-fired completion in custom transitions |
| P2-10 | Full UI regression (Light / Dark / tinted) | test | — | Visual regression matrix in testing guide passes |

## Phase 3: iOS 27 SDK Build Adaptation (mandated ~**2027-04**)

| ID | Item | Detection | Rule IDs | Verification |
|---|---|---|---|---|
| P3-01 | UIScene lifecycle mandatory (app won't launch without it) | auto | ARCH-001~002 | Launch check on iOS 27 device/simulator |
| P3-02 | Launch screen: one of four Info.plist keys mandatory | auto | LAUNCH-001~003 | One key present; generated plists checked via build settings |
| P3-03 | Remove leftover -ld_classic linker flag | auto | LINKER-001 | Clean from xcconfig / pbxproj / Podfile |
| P3-04 | Clang module name de-duplication | manual | — | `find . -name module.modulemap` for duplicate names |
| P3-05 | canOpenURL deprecation + LSApplicationQueriesSchemes 25-entry cap | auto | OPENURL-001~002 | Migrate to attempt-and-handle; trim list to ≤25 |
| P3-06 | On Demand Resources deprecation | auto | ODR-001 | Evaluate alternatives |
| P3-07 | MXMetricManager → MetricManager | auto | METRICKIT-001 | MetricKit reporting regression |
| P3-08 | NSURL URLWithString double-encoding fix impact review | manual | — | Search URL-encoding workarounds and re-verify each |
| P3-09 | C++ multimap/multiset::find() semantics change | manual | — | Use lower_bound/equal_range in C++ layers |
| P3-10 | FilePath.stat() name collision | manual | — | Qualify custom stat() extensions as Darwin.stat() |
| P3-11 | idiom/orientation layout checks → size classes | manual | — | Audit resizable iPad scenarios |
| P3-12 | App Extensions / multi-target sync adaptation | auto | EXT-001 | Build each extension separately with iOS 26/27 SDK |

## Environment Items

| ID | Item | Detection | Rule IDs | Verification |
|---|---|---|---|---|
| ENV-01 | Xcode 26.0+ (26.3+ recommended) with macOS Sequoia 15.3+ | manual | — | `xcodebuild -version` |
| ENV-02 | Xcode 27 environment: macOS Tahoe 26.4+, Apple Silicon, iOS 17+ device | manual | — | Check devices and CI machines before upgrading |
| ENV-03 | Third-party SDK compatibility audit | auto | SDK-001~002 | Upgrade per [sdk-compatibility.md](sdk-compatibility.md) |

## Ship Gate (Definition of Done — all green before submission)

| ID | Gate | Verification |
|---|---|---|
| SHIP-01 | Scanner errors zeroed | Re-run scan, errors == 0 |
| SHIP-02 | Every warning triaged | Fixed or documented exemption; no unhandled warnings |
| SHIP-03 | Manual audit checklist fully checked | All items in the report's Manual Audit Checklist ticked |
| SHIP-04 | Test matrix passed | Min version / iOS 13+ / iOS 26 device P0 all green |
| SHIP-05 | Low-impact boundary confirmed | git diff contains only iOS 26/27 adaptation files; Deployment Target unchanged |

---

**Related docs**: [timeline.md](timeline.md) (deadlines) · [testing-guide.md](testing-guide.md) (test matrix) · [sdk-compatibility.md](sdk-compatibility.md) (SDK reference) · [faq.md](faq.md)
