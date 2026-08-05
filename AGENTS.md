# Agent Guide: iOS 26 Adaptation Skill

## What This Skill Is

This is a **Claude Code skill** for guiding iOS developers through the mandatory iOS 26 SDK adaptation. It covers:

- **Phase 1**: SDK build adaptation (deadline: 2026-04-28)
  - Fix deprecated APIs (`keyWindow`, `delegate.window`, notification options)
  - Migrate to `SceneDelegate` architecture
  - Temporarily disable Liquid Glass via `UIDesignRequiresCompatibility`
- **Phase 2**: Liquid Glass full adaptation (deadline: before Xcode 27 ~2026-09)
  - Remove compatibility flag
  - Verify UI harmony with the new glassmorphism design language
- **Phase 3** (preview): iOS 27 mandates confirmed at WWDC26 (deadline: ~2027-04 est.)
  - UIScene lifecycle mandatory (app fails to launch without it), launch screen mandatory,
    `canOpenURL` deprecation, `-ld_classic` removal — see `docs/ios27-preview.md`

For the complete milestone-by-milestone timeline and per-phase scope, point users to
`docs/timeline.md` / `docs/timeline.zh.md`.

## When to Use This Skill

Trigger this skill when the user mentions any of the following:

- iOS 26 adaptation / migration / upgrade
- Xcode 26 / iOS 26 SDK build requirement
- `keyWindow` deprecation errors or `delegate.window` issues
- `SceneDelegate` migration
- Liquid Glass design language
- `UIDesignRequiresCompatibility`
- April 28, 2026 deadline
- `UNNotificationPresentationOptionAlert` warnings

**iOS 27 forward-looking triggers** (confirmed at WWDC26, see `docs/ios27-preview.md`):

- iOS 27 / Xcode 27 adaptation or SDK build mandate
- UIScene lifecycle mandatory / app fails to launch without SceneDelegate
- Launch screen requirement / App Store rejection for missing launch screen
- `canOpenURL` deprecation / `LSApplicationQueriesSchemes` 25-entry limit
- `-ld_classic` linker removal / Clang module de-duplication build failures
- On Demand Resources / `NSBundleResourceRequest` / `MXMetricManager` deprecations
- iOS 26 runtime crashes: `setValue:forKey:@"tabBar"`, `navigationBar addSubview` disappearing
- TN3187 / scene-based lifecycle migration technote
- iOS 27 code-level breaking changes: NSURL double-encoding fix, C++ `multimap/multiset::find()` semantics, `FilePath.stat()` name collision
- Xcode 27 environment requirements (macOS Tahoe 26.4+, Apple Silicon only)

## Standard Workflow

When assisting with iOS 26 adaptation, **always follow this flow**:

```
1. Assess Context
   └── Ask: release timeline, current iOS minimum version, language (Swift/OC/Mixed)

2. Scan Project
   ├── Use scripts/ios26-scanner.py (if available in user's project)
   ├── ALWAYS load scripts/adaptation-ledger.json as the complete task list (never rely on memory)
   └── Or grep for: keyWindow, delegate.window, UNNotificationPresentationOptionAlert,
       UIApplicationSceneManifest, statusBarStyle, inputAccessoryView,
       subclass UITextField, subclass UITextView

3. Determine Strategy (A / B / C)
   ├── Strategy A: Release before 2026-04-28 → branch-based adaptation
   ├── Strategy B: Release between 2026-04-28 and Xcode 27 → Phase 1 required, Phase 2 evaluated
   └── Strategy C: Release after Xcode 27 → combined phases

4. Generate Adaptation Plan
   ├── File change list (add / modify / delete)
   ├── Code replacement map
   ├── Third-party SDK notes
   └── Test verification checklist

5. Execute Changes (if user requests)
   ├── Add UIApplication+Extension (unified window access)
   ├── Add/Modify SceneDelegate
   ├── Refactor AppDelegate (sharedInstance, setupApplication, setupSceneUI)
   ├── Replace deprecated API calls globally
   └── Add Info.plist configurations

6. Verify (Zero-Omission Loop — see SKILL.md)
   ├── Build with iOS 26 SDK succeeds
   ├── Test on minimum supported iOS version
   ├── Test on iOS 13+ (SceneDelegate path)
   ├── Test on iOS 26 (Liquid Glass disabled/enabled depending on phase)
   ├── Re-run scanner: every ledger item = fixed / verified-clean / not-applicable (with reason)
   ├── Manual Audit Checklist in scan report fully ticked
   └── Completion Gate SHIP-01~05 all green → only then declare ship-ready
```

## Minimal-Impact Adaptation Rules (MANDATORY)

This skill is applied directly inside users' production projects. Keep changes surgical:

1. **Only modify iOS 26/27-related code** — scanner-flagged deprecated call sites, lifecycle
   architecture (SceneDelegate / Info.plist scene manifest), and new adapter files from `templates/`.
2. **Never change Deployment Target**, never remove pre-iOS 13 fallback paths, never refactor
   or reformat unrelated business code.
3. **Only fix what is mandated or Error-level** — do not "modernize while we're at it"
   (no unprompted SwiftUI rewrites, Swift 6 strict-concurrency migrations, or StoreKit 2
   rewrites when the project still builds).
4. **Never patch `Pods/` or third-party SDK sources** — advise upgrading the dependency.
5. **Every requirement must trace to an Apple official source** (Upcoming Requirements,
   release notes, WWDC, TN3187). Never invent requirements.
6. **Before editing**: present the scan summary plus the exact file add/modify list with
   one-line reasons. **After editing**: re-run the scanner and report remaining findings.

## Output Format Preferences

- **Decision output**: Use tables and flowcharts (ASCII or markdown tables).
- **Scan output**: Use markdown tables with rule IDs, file paths, line numbers, severity.
- **Plan output**: Use numbered sections and checklists (`- [ ]`).
- **Code output**: Provide both Swift and Objective-C when possible. Prefer the language matching the user's project.
- **Critical deadlines**: Bold the 2026-04-28 and ~2026-09 dates every time they appear.

## Must-Check Items Every Time

- [ ] Does the project already have `SceneDelegate.swift` / `SceneDelegate.m`?
- [ ] Is `UIApplicationSceneManifest` present in `Info.plist`?
- [ ] How many occurrences of `keyWindow` / `delegate.window` exist?
- [ ] Are there notification-related deprecated enums?
- [ ] Any custom `UITextField` / `UITextView` subclasses? (Liquid Glass keyboard toolbar may need `inputAccessoryView` clearing)
- [ ] What is the app's **minimum iOS version**? (This determines iOS 12 fallback path necessity.)
- [ ] What is the **next release date**? (This determines strategy A/B/C.)

## Code Template References

When user needs copy-pasteable code, point them to the `templates/` directory:

- `templates/swift/UIApplication+MainWindow.swift`
- `templates/swift/SceneDelegate.swift`
- `templates/swift/AppDelegate+Setup.swift`
- `templates/swift/UNNotificationOptions+Adapter.swift`
- `templates/swift/Swift6ConcurrencyAdapter.swift` — Swift 6 strict concurrency patterns
- `templates/swift/UITextInput+LiquidGlassAdapter.swift` — Optional keyboard toolbar glass effect remover (iOS 26+)
- `templates/objc/UIApplication+MainWindow.h/.m`
- `templates/objc/SceneDelegate.h/.m`
- `templates/objc/AppDelegate+Setup.h/.m`
- `templates/objc/UNNotificationOptionsAdapter.h/.m`
- `templates/objc/UITextInput+LiquidGlassAdapter.h/.m` — Optional keyboard toolbar glass effect remover (iOS 26+)
- `templates/mixed/README.md` — bridging patterns for mixed Swift/Objective-C projects
- `templates/PrivacyInfo.xcprivacy` — Privacy Manifest template for App Store submission

## Common Pitfalls to Warn About

1. **Do NOT change Deployment Target to iOS 26** unless explicitly requested.
2. **iOS 12 path must remain unchanged** — only iOS 13+ should go through SceneDelegate.
3. **Lifecycle forwarding is critical** — missing `sceneWillEnterForeground` forwarding can break analytics and state saving.
4. **`UIDesignRequiresCompatibility` is temporary** — remind users that Phase 2 is mandatory before Xcode 27.
5. **Pods/ThirdParty files** — advise users to update third-party SDKs rather than patching them locally.

## Language-Specific Notes

- If user's project is **Swift**, default to Swift examples. Mention Objective-C equivalents only if the user asks or if mixed files are found.
- If user's project is **Objective-C**, default to Objective-C examples.
- If **mixed**, reference `templates/mixed/README.md` for bridging strategy, then generate the specific files the user needs:
  - Window access → Objective-C category (single source of truth, visible to Swift via bridging header)
  - AppDelegate/SceneDelegate cross-language calls → `@objc` / bridging header guidance
  - Always label which language each file is in

## Author

roder
