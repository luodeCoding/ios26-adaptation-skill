# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [1.12.0] - 2026-08-03

### Added — Zero-Omission Adaptation Engine
- **Coverage Ledger** `scripts/adaptation-ledger.json` — 50 adaptation items (Phase 1 ×20, Phase 2 ×10, Phase 3 ×12, environment ×3, ship gates ×5) as the single complete task list; each item binds a detection method (`auto`/`manual`/`test`), rule IDs, verification criteria, and an Apple-official source
- **New scanner project-level rules**:
  - `LAUNCH-001/002/003` — iOS 27 launch screen mandate (four Info.plist keys; `UILaunchImages` flagged as insufficient; generated-Info.plist projects verified via `INFOPLIST_KEY_UILaunch*` build settings)
  - `ARCH-004` — generated Info.plist detection (`GENERATE_INFOPLIST_FILE = YES`)
  - `EXT-001` — app extension target detection (each extension must build with the new SDK)
  - `SDK-001/002` — third-party dependency manifest audit against `docs/sdk-compatibility.md`
- **Scan report additions**: Manual Audit Checklist (items that cannot be statically detected) and Completion Gate (SHIP-01~05, the ship-ready Definition of Done); JSON output gains a `completion_gate` field
- **Coverage matrix docs** `docs/coverage.md` / `docs/coverage.zh.md` — human-readable mirror of the ledger with per-phase tables
- **CI consistency tests**: every `auto` ledger item's rule IDs must exist in the scanner; phase coverage validated (58 tests total)

### Changed
- `SKILL.md`: new mandatory "Zero-Omission Adaptation Loop" workflow (ledger → scan → fix in ledger order → rescan → close gate) + Definition of Done; Resources index adds coverage matrix
- `AGENTS.md`: standard workflow now requires loading the ledger and closing the SHIP gate before declaring ship-ready
- `README.md` / `README.zh.md`: version v1.12.0, "Zero-Omission Guarantee" section, updated structure tree and doc tables
- `LINKER-001` now also scans `Podfile` for `-ld_classic`

## [1.11.0] - 2026-08-03

### Added
- **Distribution-ready release** — the repo can now be installed directly as an AI skill and safely applied to production projects
- **Adaptation Impact Statement (low-impact promise)**: explicit boundaries of what the skill may and may not change in a user's main project
  - `SKILL.md`: new "Adaptation Impact Boundaries (MANDATORY for AI agents)" section — allowed changes, forbidden changes, Apple-official compliance principle, auditable deliverable format
  - `AGENTS.md`: new "Minimal-Impact Adaptation Rules (MANDATORY)" section + Phase 3 entry in the skill overview
  - `INTEGRATION.md`: new user-facing "适配影响声明（低冲击承诺）" section
  - `README.md` / `README.zh.md`: "Adaptation Impact Guarantee" highlights
- **New timeline docs `docs/timeline.md` / `docs/timeline.zh.md`** — single authoritative reference for every iOS 26/27 milestone (2025-06 → ~2027-04) with the required adaptation scope, consequences of inaction, matching scanner rules, and checklist links per phase
- **Skill installation guide**: one-command Claude Code install (`~/.claude/skills/`) and Qoder/other-agent guidance in README (EN/ZH) and the Juejin article
- **`platforms/article.md`**: refreshed for promotion — iOS 27 deadline row, low-impact section, 40+ rule coverage, skill-install quick start

### Changed
- README (EN/ZH): version bumped to v1.11.0; structure tree and AI-skill-document tables include the new timeline docs

## [1.10.0] - 2026-08-03

### Added
- **`docs/ios27-preview.md` major refresh (based on Aug-2026 research)**
  - Xcode 27 environment requirements (macOS Tahoe 26.4+, Swift 6.4, Apple Silicon only, iOS 17+ device debugging, x86_64 removed from ARCHS_STANDARD)
  - Three new code-level P1 risks: NSURL double-encoding fix, C++ `multimap/multiset::find()` semantics change, System framework `FilePath.stat()` name collision
  - New section 6 "iOS 27 Beta known issues" table (Address Sanitizer, Core AI + Metal, Memory Tagging, MusicKit @State, legacy-app launch crash)
  - TN3187 technote reference + real iOS 27.0 beta crash case for legacy AppDelegate-only apps (Tencent Cloud community)
  - Beta progress update (iOS 27.0 beta 3 / public beta shipped; official release expected Sep 2026 with iPhone 18)
- **FAQ**: added Q40 (Xcode 27 environment requirements & beta timeline), Q41 (code-level breaking-change audit checklist)
- **SKILL.md**: iOS 27 section enriched with TN3187, code-level P1 changes, beta status; AGENTS.md gained matching triggers

### Fixed
- **SKILL.md**: Resources internal-doc links unified from `../docs/` to repo-root-relative `docs/` (broken links removed)
- **README (EN/ZH)**: key-deadline table now marks 2026-04-28 as in effect and notes the closing Phase 2 window

## [1.9.2] - 2026-08-03

### Fixed
- **README.md / README.zh.md**: added missing `INTEGRATION.md` references — new entry in the project structure tree, a pointer link in the "How to Use" section, and a row in the AI skill documents table
- **README.zh.md**: the "this file" label in the project structure tree corrected from `README.md` to `README.zh.md`
- **INTEGRATION.md**: file-purpose table now includes the missing root-level docs (README (EN/ZH), INTEGRATION, CHANGELOG)

## [1.9.1] - 2026-07-30

### Added
- **New checklists `examples/phase3-checklist.md` / `.zh.md`** — iOS 27 readiness checklist (Phase 3 preview): UIScene mandate, launch screen keys, `canOpenURL` migration, linker/build-chain checks, layout modernization, with matching scanner rule IDs
- **Phase 2 checklists (EN/ZH)**: added iOS 26 runtime pitfall items — no `tabBar` private KVC, no direct `navigationBar addSubview`, `AlwaysOriginal` tinting, no `statusBarFrame`-based layout
- **Testing guide (`docs/testing-guide.md`)**: added iOS 26 pitfall test cases (custom TabBar crash, nav bar overlay views, right bar button order, image button tinting) and a Phase 3 forward-looking test section

### Fixed
- **README.md / README.zh.md**: synced from stale v1.6.0 state — version badge, v1.7-v1.9 changelog rows, iOS 27 deadline row, Phase 3 preview section, current project structure (mixed templates, docs, phase 3 checklists, test suite), scanner coverage summary, resource links
- **INTEGRATION.md**: file-purpose table and scanner coverage list updated to the actual v1.9 rule set (was still listing only the 6 original checks)

## [1.9.0] - 2026-07-30

### Added
- **New doc `docs/ios27-preview.md`** — iOS 27 / Xcode 27 adaptation preview (Phase 3), based on WWDC26 Session 278 + Apple docs and community field reports. Covers mandatory UIScene lifecycle (apps fail to launch without it), mandatory launch screen, `canOpenURL` deprecation + `LSApplicationQueriesSchemes` 50→25 limit, build-chain removals (`-ld_classic`, Clang module de-dup, ODR, MetricKit), layout `resize` changes, and a three-phase timeline.
- **New scanner rules (`scripts/ios26-scanner.py`)**
  - iOS 26 runtime pitfalls (field reports): `TABBAR-001` (private KVC `setValue:forKey:@"tabBar"` crash, Error), `NAVBAR-001` (direct `navigationBar addSubview`, Warning), `BARBUTTON-001` (`rightBarButtonItems` order/spacing, Info)
  - iOS 27 forward-looking: `OPENURL-001` (`canOpenURL` deprecation, Info), `ODR-001` (`NSBundleResourceRequest`, Warning), `METRICKIT-001` (`MXMetricManager`, Warning)
  - Project-level: `LINKER-001` (`-ld_classic` in `.xcconfig`/`.pbxproj`, Warning), `OPENURL-002` (`LSApplicationQueriesSchemes` over the 25-entry limit, Warning)
  - Comment-only line filtering extended to the new behavior rules to avoid false positives
- **SKILL.md**: added iOS 27 deadline row + "iOS 27 Confirmed at WWDC26" section, a Phase 2 "iOS 26 Runtime Pitfalls (Field Reports)" table, three new Scanner Rules Reference tables, and internal/external resource links (conorluddy/LiquidGlassReference, fatbobman, cnblogs weicy)
- **FAQ**: added Q25b-Q25e (iOS 26 runtime pitfalls: tabBar KVC crash, navigationBar addSubview, AlwaysOriginal tint, statusBarFrame 0) and a new "iOS 27 Preview" section Q36-Q39 (UIScene mandate, launch screen, `canOpenURL` migration, build-chain changes)
- **AGENTS.md**: added iOS 27 forward-looking trigger keywords
- **Tests**: 12 new unit tests covering the new code-level and project-level rules (47 total, all passing)

## [1.8.0] - 2026-07-30

### Added
- **New scanner rules (`scripts/ios26-scanner.py`)**
  - `WINDOW-007/008` — detects deprecated `UIApplication.shared.windows` / `[UIApplication sharedApplication].windows` (deprecated since iOS 15)
  - `STATUS-004` — detects deprecated `statusBarFrame` access (skips the modern `statusBarManager.statusBarFrame` replacement)
  - `PHASE2-001` — project-level reminder when `UIDesignRequiresCompatibility` is present in Info.plist (Phase 2 pending before Xcode 27)
  - Deployment target detection now falls back to parsing `IPHONEOS_DEPLOYMENT_TARGET` from `.pbxproj` when no Podfile declares it (uses the lowest value found)
- **SKILL.md**: Scanner Rules Reference synced with the actual rule set — added `WINDOW-007/008`, `STATUS-003/004`, `ASSETSLIBRARY-001/002/003`, and a new "Project-Level Checks" table (`PRIVACY-001`, `ARCH-001/002/003`, `PHASE2-001`)
- **FAQ**: added Q19a (`UIApplication.shared.windows` / `statusBarFrame` deprecations)
- **Tests**: 8 new unit tests covering the new rules, `.pbxproj` deployment target parsing, and false-positive filters (35 total)

### Fixed
- **Scanner crash**: `TypeError` when scanning a pure Swift project with no Podfile/pbxproj deployment target (`None >= 13.0` comparison in architecture severity logic)
- **Scanner false positive**: `WINDOW-003` skip filter only matched the legacy `UIApplication+Extension` filename — now also matches the actual `UIApplication+MainWindow` template name
- **FAQ duplicate question numbers**: two Q25 entries and reused Q19-Q23 in Testing/Strategy sections — renumbered to Q25a and Q31-Q35
- **FAQ broken template references**: `templates/*/UIApplication+Extension.*` corrected to the actual `UIApplication+MainWindow.*` filenames
- **SKILL.md**: Swift example heading renamed from `UIApplication+Extension.swift` to `UIApplication+MainWindow.swift` to match the shipped template
- **CHANGELOG.zh.md**: backfilled the missing 1.7.0 entry

## [1.7.0] - 2026-06-02

### Added
- **Pure Swift project adaptation support**
  - `templates/swift/SceneDelegate+SwiftOnly.swift` — simplified SceneDelegate without @objc annotations, with @MainActor for Swift 6
  - `templates/swift/AppDelegate+SwiftOnly.swift` — pure Swift AppDelegate using `static let shared` instead of `@objc static let shared` / `sharedInstance`
  - Updated `templates/swift/UIApplication+MainWindow.swift` with `@MainActor` and cross-language usage comments
- **Scanner improvements (`scripts/ios26-scanner.py`)**
  - `ASSETSLIBRARY-001/002/003` — detects `import AssetsLibrary`, `#import <AssetsLibrary/AssetsLibrary.h>`, and `ALAssetsLibrary` usage (Error severity)
  - `detect_project_type()` — auto-detects pure Swift / mixed / Objective-C projects and deployment target
  - ARCH-001/002 severity now adapts to project type: pure Swift iOS 13+ projects without SceneDelegate are downgraded from Error to Warning (backward compatibility still works, but iOS 27 will require migration)
  - SCREEN-001/002 false-positive filtering: skips `Pods/`, `Vender/`, `vendor/`, `ThirdParty/` directories
  - ARCH-003 suggestion updated to mention `static let shared` for Swift projects
- **Documentation updates**
  - SKILL.md: added "Pure Swift Project Notes (iOS 26+)" section under Swift Projects
  - FAQ: added Q5a (pure Swift SceneDelegate migration), Q14a (ALAssetsLibrary build error)

## [1.6.0] - 2026-05-12

### Added
- **Keyboard Liquid Glass toolbar adapter**: `templates/swift/UITextInput+LiquidGlassAdapter.swift` and `templates/objc/UITextInput+LiquidGlassAdapter.h/.m`
  - Optional `lg_clearLiquidGlassAccessoryIfNeeded()` extension for `UITextField` / `UITextView`
  - Clears default `inputAccessoryView` on iOS 26+ when the glassmorphism keyboard toolbar is visually disruptive
  - Documented in SKILL.md Phase 2 with per-control / subclass / global sweep strategy table
- **Scanner rules** for keyboard adaptation:
  - `KEYBOARD-001` — detects custom `UITextField` subclasses
  - `KEYBOARD-002` — detects custom `UITextView` subclasses
  - `KEYBOARD-003` — detects `inputAccessoryView` assignments
- **AGENTS.md updates**: added `inputAccessoryView`, custom text input scanning to Standard Workflow; added custom text input check to Must-Check Items
- **Phase 2 checklists** (EN/ZH): added Liquid Glass toolbar decision and custom text input scan items

## [1.5.0] - 2026-05-06

### Added
- **`templates/PrivacyInfo.xcprivacy`** — Privacy Manifest template with required reason APIs and data collection examples
- **`templates/swift/Swift6ConcurrencyAdapter.swift`** — Swift 6 strict concurrency migration patterns (@MainActor, @Sendable, async/await, global actors)
- **`docs/sdk-compatibility.md`** — Third-party SDK iOS 26 compatibility cheat sheet (Firebase, Facebook, RevenueCat, Branch, etc.)
- **`scripts/test_scanner.py`** — Unit test suite covering all 19 scanner rules + architecture checks + full project scan
- **`.github/workflows/ci.yml`** — GitHub Actions CI pipeline (scanner tests, Python lint, markdown link validation)

## [1.4.0] - 2026-05-06

### Added (Round 2 QA Gap Analysis)
- **Privacy Manifest coverage**: `PRIVACY-001` scanner rule detects missing `PrivacyInfo.xcprivacy`; docs explain required reason APIs and third-party SDK declarations
- **StoreKit 1 → StoreKit 2**: `STOREKIT-001` scanner rule detects removed StoreKit 1 APIs; SKILL.md and FAQ include migration table and dual-path guidance
- **SiriKit → App Intents**: `SIRIKIT-001` scanner rule detects deprecated SiriKit intent domains; FAQ covers automatic Xcode conversion
- **SwiftUI modern APIs**: `SWIFTUI-001/002/003` scanner rules for `NavigationView`, `.cornerRadius()`, `.foregroundColor()`; SKILL.md includes full replacement table
- **Photos migration**: `PHOTOS-001` scanner rule detects `UIImagePickerController`; FAQ provides `PHPickerViewController` sample code
- New FAQ entries (Q26-Q30): Privacy Manifest, StoreKit 2, SiriKit, SwiftUI deprecations, PHPicker

## [1.3.0] - 2026-05-06

### Added (Round 1 QA Gap Analysis)
- **QA gap analysis**: Scanned against latest iOS 26 SDK docs and community migration guides
- New scanner rules in `scripts/ios26-scanner.py`:
  - `SCREEN-001/002` — `UIScreen.main` deprecation detection
  - `WEB-001` — removed `UIWebView` detection
  - `TLS-001` — legacy TLS 1.0/1.1 detection
  - `COREDATA-001` — removed CoreData iCloud ubiquitous sync keys detection
  - `SWIFT6-001` — Swift 6 strict concurrency info flag
- New FAQ entries in `docs/faq.md` (Q19-Q25): Swift 6 concurrency, TLS 1.2, CoreData keys, TabBar safeArea, UIDropShadowView, background color conflicts
- New section in `SKILL.md`: "Additional iOS 26 SDK Changes" covering Swift 6, TLS, CoreData, Liquid Glass structural impacts
- Updated `docs/testing-guide.md` with TabBar safeArea, UIDropShadowView, and background conflict test cases

### Fixed
- **Self-referencing deprecated API**: `SKILL.md` and `templates/swift/AppDelegate+Setup.swift` examples now annotate `UIScreen.main` usage in iOS 12 fallback path
- **Critical correction**: `UNNotificationPresentationOptionAlert` was deprecated in **iOS 14.0**, not iOS 26.0 — updated all templates and docs
- **Critical correction**: `UNAuthorizationOptionAlert` is **NOT deprecated** in iOS 26 SDK — removed replacement logic from all templates
- Removed `NOTIF-002` scanner rule that incorrectly flagged `UNAuthorizationOptionAlert` as deprecated
- Updated `AGENTS.md` language-specific notes with clearer mixed-project guidance
- Fixed template filename references in `AGENTS.md` (`UIApplication+MainWindow`, `UNNotificationOptions+Adapter`)

## [1.1.0] - 2026-04-14

### Added
- `templates/` directory with production-ready Swift and Objective-C code templates:
  - `UIApplication+Extension` (unified window/navigation access)
  - `SceneDelegate` (full lifecycle and URL forwarding implementation)
  - `AppDelegate+Setup` (dual-path refactoring examples)
  - `NotificationAdapter` (centralized notification option adapter for deprecated API changes)
- `scripts/ios26-scanner.py` — automated project scanner that detects deprecated APIs and architectural gaps
- `docs/faq.md` — comprehensive FAQ covering strategy, build errors, and Liquid Glass
- `AGENTS.md` — agent usage guide for Claude Code integration
- Complete Swift implementation example in `SKILL.md` (AppDelegate + SceneDelegate + UIApplication Extension)
- `UNAuthorizationOptionAlert` code replacement examples in `SKILL.md`

### Fixed
- Tree structure formatting in `README.zh.md`
- Objective-C code examples in `SKILL.md` to use instance method syntax (`[[UIApplication sharedApplication] mainWindow]`)

## [1.0.0] - 2026-04-10

### Added
- Initial release of iOS 26 Adaptation Skill
- Comprehensive two-phase adaptation strategy (SDK Build & Liquid Glass)
- Project scanning rules for deprecated APIs
- Decision flowcharts and checklists
- Bilingual documentation (English & Chinese)
- Phase 1 & Phase 2 checklists
- SKILL.md for Claude Code integration

### Features
- 📋 Two-phase adaptation strategy guide
- 🔍 Deprecated API scanning rules (keyWindow, notification options, etc.)
- 📊 Decision flowcharts based on release timeline
- ✅ Detailed checklists for both adaptation phases
- 🌐 Full bilingual support (EN/ZH)

### Documentation
- README.md - Quick start guide (English)
- README.zh.md - Quick start guide (Chinese)
- SKILL.md - Detailed skill documentation
- .claude/iOS26-适配框架指南.md - Full adaptation framework (Chinese)
- docs/testing-guide.md - Testing guide for QA team
- examples/phase1-checklist.md - Phase 1 execution checklist (English)
- examples/phase1-checklist.zh.md - Phase 1 execution checklist (Chinese)
- examples/phase2-checklist.md - Phase 2 execution checklist (English)
- examples/phase2-checklist.zh.md - Phase 2 execution checklist (Chinese)

---

**Author**: roder
