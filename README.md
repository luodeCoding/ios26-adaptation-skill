# iOS 26 Adaptation Skill

<div align="right">
  <b>🌐 Language:</b> English | <a href="./README.zh.md">中文</a>
</div>

---

> **Languages**: Objective-C / Swift  
> **Platform**: iOS  
> **Minimum iOS Version**: 12.0+  
> **Last Updated**: 2026-07-30  
> **Version**: [v1.9.1](https://github.com/luodeCoding/ios26-adaptation-skill/blob/main/CHANGELOG.md)

**This repository is an AI adaptation skill tool. It does not participate in any project compilation.**

Provides iOS 26 SDK adaptation solutions, templates, scanning scripts, and checklists for AI assistants and developers to reference.

## What Is This?

This repository is a **standalone skill knowledge base** for:

- 🤖 **AI Assistants** — Read SKILL.md, template code, and checklists to guide developers through adaptation
- 👨‍💻 **Developer Reference** — View code templates and copy needed code into the main project
- 🔍 **Project Scanning** — Run scripts to check for deprecated APIs in the main project

**Files in this repository are NOT referenced or compiled by the main project.** All template code requires developers to **manually copy** into their main project.

## Key Deadlines

| Date | Requirement | Impact |
|------|-------------|--------|
| **2026-04-28** | Must build with iOS 26 SDK | Non-compliant submissions will be rejected |
| **~2026-09** | Xcode 27 release, Liquid Glass mandatory | `UIDesignRequiresCompatibility` will be removed |
| **~2027-04 (est.)** | iOS 27 SDK build mandate (confirmed at WWDC26) | Apps without UIScene lifecycle **fail to launch**; launch screen mandatory |

> iOS 27 requirements are already confirmed — see [docs/ios27-preview.md](docs/ios27-preview.md) for the Phase 3 preview.

## Changelog

| Version | Date | Highlights |
|---------|------|------------|
| **[v1.9.1](CHANGELOG.md)** | 2026-07-30 | Phase 3 checklists (EN/ZH), iOS 26 pitfall test cases, README/INTEGRATION doc sync |
| **[v1.9.0](CHANGELOG.md)** | 2026-07-30 | iOS 27 preview doc (Phase 3), iOS 26 runtime pitfall + iOS 27 forward-looking scanner rules, FAQ iOS 27 section |
| **[v1.8.0](CHANGELOG.md)** | 2026-07-30 | `windows`/`statusBarFrame` scanner rules, Phase 2 pending reminder, scanner crash/false-positive fixes |
| **[v1.7.0](CHANGELOG.md)** | 2026-06-02 | Pure Swift project support, AssetsLibrary rules, project type auto-detection |
| **[v1.6.0](CHANGELOG.md)** | 2026-05-12 | Liquid Glass keyboard toolbar adapter, keyboard scanner rules, Phase 2 checklist updates |
| **[v1.5.0](CHANGELOG.md)** | 2026-05-06 | Privacy Manifest template, Swift 6 adapter, SDK compatibility sheet, unit tests, CI |
| **[v1.4.0](CHANGELOG.md)** | 2026-05-06 | StoreKit 2, SiriKit→App Intents, SwiftUI modern APIs, Photos, Privacy Manifest scanner rules |
| **[v1.3.0](CHANGELOG.md)** | 2026-05-06 | Swift 6 concurrency, TLS 1.2, CoreData keys, Liquid Glass structural impacts, scanner rules |
| **[v1.1.0](CHANGELOG.md)** | 2026-04-14 | Production templates, scanner script, FAQ, AGENTS.md |
| **[v1.0.0](CHANGELOG.md)** | 2026-04-10 | Initial release — two-phase strategy, bilingual docs, checklists |

> [View full changelog →](CHANGELOG.md)

## Two-Phase Adaptation (+ Phase 3 Preview)

### Phase 1: SDK Build Adaptation (Before 2026-04-28)

**Goal**: Build with iOS 26 SDK while maintaining existing UI appearance

**Key Tasks**:
- Upgrade to Xcode 26.0+
- Fix deprecated API calls (keyWindow, etc.)
- Temporarily disable Liquid Glass
- Complete SceneDelegate architecture migration

### Phase 2: Liquid Glass Full Adaptation (Before Xcode 27)

**Goal**: Full adaptation to Liquid Glass design language

**Key Tasks**:
- Remove `UIDesignRequiresCompatibility` flag
- Verify all UI components under Liquid Glass
- Adjust custom UI for visual harmony

### Phase 3 Preview: iOS 27 Mandates (Confirmed at WWDC26)

**Goal**: Be ready before the iOS 27 SDK build mandate (~2027-04 est.)

**Key Requirements** (details in [docs/ios27-preview.md](docs/ios27-preview.md)):
- UIScene lifecycle mandatory — apps built with iOS 27 SDK without it **fail to launch**
- Launch screen mandatory — missing keys cause App Store rejection
- `canOpenURL` deprecated; `LSApplicationQueriesSchemes` limit halved to 25
- `-ld_classic` linker removed in Xcode 27

> Completing Phase 1 SceneDelegate migration already satisfies the biggest iOS 27 requirement.

## How to Use

### Option 1: AI Assistant (Recommended)

Load this repository as an AI skill. The AI reads the documentation and templates, then generates/modifies code directly in the main project.

```
Developer: "Help me adapt to iOS 26"
AI: Read SKILL.md → Scan main project → Generate adaptation code → Modify main project files directly
```

### Option 2: Manual Developer Reference

```bash
# 1. Download locally (any location, unrelated to main project)
git clone https://github.com/luodeCoding/ios26-adaptation-skill.git

# 2. View needed templates
cat ios26-adaptation-skill/templates/swift/SceneDelegate.swift

# 3. Manually copy needed code to main project
# Copy and paste, modify as needed

# 4. Run scanner to check for missed items
python3 ios26-adaptation-skill/scripts/ios26-scanner.py /path/to/your/ios/project
```

## Project Structure

```
ios26-adaptation-skill/
├── README.md              # This file
├── README.zh.md           # Chinese version
├── SKILL.md               # 📘 AI core skill document (detailed adaptation guide)
├── AGENTS.md              # 🤖 Claude Code Agent usage guide
├── CHANGELOG.md           # Version history
├── LICENSE                # MIT License
│
├── docs/                  # 📚 Documentation
│   ├── faq.md             # Frequently asked questions
│   ├── testing-guide.md   # Testing guide
│   ├── sdk-compatibility.md # Third-party SDK compatibility sheet
│   └── ios27-preview.md   # iOS 27 / Xcode 27 adaptation preview (Phase 3)
│
├── .claude/               # 🎯 Claude-specific guides
│   └── iOS26-适配框架指南.md
│
├── examples/              # ✅ Checklists
│   ├── phase1-checklist.md / .zh.md
│   ├── phase2-checklist.md / .zh.md
│   └── phase3-checklist.md / .zh.md
│
├── scripts/               # 🔍 Scanning scripts
│   ├── ios26-scanner.py   # Deprecated API scanner (40+ rules)
│   └── test_scanner.py    # Scanner unit tests
│
└── templates/             # 📋 Code templates (reference only, not compiled)
    ├── PrivacyInfo.xcprivacy  # Privacy Manifest template
    ├── swift/             # Swift templates (window access, SceneDelegate,
    │                      #   Swift 6 concurrency, Liquid Glass adapters, ...)
    ├── objc/              # Objective-C templates (same coverage)
    └── mixed/             # Bridging patterns for mixed projects
```

## Core Content Overview

### Deprecated API Replacements

| Deprecated API | Replacement | Template Location |
|---------------|-------------|-------------------|
| `keyWindow` | `UIApplication.mainWindow` | `templates/swift/UIApplication+MainWindow.swift` |
| `delegate.window` | `UIApplication.mainWindow` | Same as above |
| `UNNotificationPresentationOptionAlert` | `.banner \| .list` | `templates/swift/UNNotificationOptions+Adapter.swift` |
| `UNAuthorizationOptionAlert` | Still valid — do NOT replace | Same as above |

### Scanning Script

```bash
# Scan main project for deprecated APIs (40+ rules: iOS 26 + iOS 27 forward-looking)
python3 scripts/ios26-scanner.py /path/to/your/ios/project

# Output JSON report
python3 scripts/ios26-scanner.py /path/to/your/ios/project --format json --output report.json
```

Coverage includes: window access (`keyWindow` / `windows` / `statusBarFrame`), SceneDelegate architecture, notification options, iOS 26 runtime pitfalls (`tabBar` KVC crash, `navigationBar addSubview`), and iOS 27 forward-looking checks (`canOpenURL`, `-ld_classic`, `LSApplicationQueriesSchemes` limit, ODR, MetricKit). Full rule reference in [SKILL.md](SKILL.md).

### AI Skill Documents

| Document | Purpose |
|----------|---------|
| `SKILL.md` | Complete adaptation guide, decision flows, code examples |
| `AGENTS.md` | Claude Code workflow, triggers, checklists |
| `.claude/iOS26-适配框架指南.md` | Chinese complete framework guide |

## Common Misconceptions

| Misconception | Fact |
|--------------|------|
| Must change Deployment Target to iOS 26 | ❌ No. Keep your current minimum version |
| Users must upgrade to iOS 26 | ❌ No. Runtime requirements are determined by Deployment Target |
| Existing app versions will be removed | ❌ No. Only affects new submissions and updates |
| There is a grace period | ❌ No. April 28, 2026 is a hard deadline |

## Resources

- [Apple Developer News](https://developer.apple.com/news/)
- [iOS 26 Release Notes](https://developer.apple.com/documentation/ios-release-notes)
- [Liquid Glass Design Guide](https://developer.apple.com/design/)
- [Upcoming App Store Requirements](https://developer.apple.com/news/upcoming-requirements/)
- [Transitioning to the UIKit scene-based life cycle](https://developer.apple.com/documentation/uikit/transitioning-to-the-uikit-scene-based-life-cycle)

## License

MIT License - see LICENSE file

---

**Author**: roder
