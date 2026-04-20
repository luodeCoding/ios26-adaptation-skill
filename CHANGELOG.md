# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.1.0] - 2026-04-14

### Added
- `templates/` directory with production-ready Swift and Objective-C code templates:
  - `UIApplication+Extension` (unified window/navigation access)
  - `SceneDelegate` (full lifecycle and URL forwarding implementation)
  - `AppDelegate+Setup` (dual-path refactoring examples)
  - `NotificationAdapter` (centralized iOS 26 notification option adapter)
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
