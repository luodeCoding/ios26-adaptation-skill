# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

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
