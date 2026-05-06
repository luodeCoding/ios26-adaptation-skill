# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.3.0] - 2026-05-06

### Added
- **QA gap analysis**: Scanned against latest iOS 26 SDK docs and community migration guides
- New scanner rules in `scripts/ios26-scanner.py`:
  - `SCREEN-001/002` — `UIScreen.main` deprecation detection
  - `WEB-001` — removed `UIWebView` detection
  - `TLS-001` — legacy TLS 1.0/1.1 detection
  - `COREDATA-001` — removed CoreData iCloud ubiquitous sync keys detection
  - `SWIFT6-001` — Swift 6 strict concurrency info flag
- New FAQ entries in `docs/faq.md`: Swift 6 concurrency, TLS 1.2, CoreData keys, TabBar safeArea, UIDropShadowView, background color conflicts
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
