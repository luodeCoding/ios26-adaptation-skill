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

## Standard Workflow

When assisting with iOS 26 adaptation, **always follow this flow**:

```
1. Assess Context
   └── Ask: release timeline, current iOS minimum version, language (Swift/OC/Mixed)

2. Scan Project
   ├── Use scripts/ios26-scanner.py (if available in user's project)
   └── Or grep for: keyWindow, delegate.window, UNNotificationPresentationOptionAlert,
       UIApplicationSceneManifest, statusBarStyle

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

6. Verify
   ├── Build with iOS 26 SDK succeeds
   ├── Test on minimum supported iOS version
   ├── Test on iOS 13+ (SceneDelegate path)
   └── Test on iOS 26 (Liquid Glass disabled/enabled depending on phase)
```

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
- [ ] What is the app's **minimum iOS version**? (This determines iOS 12 fallback path necessity.)
- [ ] What is the **next release date**? (This determines strategy A/B/C.)

## Code Template References

When user needs copy-pasteable code, point them to the `templates/` directory:

- `templates/swift/UIApplication+MainWindow.swift`
- `templates/swift/SceneDelegate.swift`
- `templates/swift/AppDelegate+Setup.swift`
- `templates/swift/UNNotificationOptions+Adapter.swift`
- `templates/swift/Swift6ConcurrencyAdapter.swift` — Swift 6 strict concurrency patterns
- `templates/objc/UIApplication+MainWindow.h/.m`
- `templates/objc/SceneDelegate.h/.m`
- `templates/objc/AppDelegate+Setup.h/.m`
- `templates/objc/UNNotificationOptionsAdapter.h/.m`
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
