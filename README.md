# iOS 26 Adaptation Skill

<div align="right">
  <b>🌐 Language:</b> English | <a href="./README.zh.md">中文</a>
</div>

---

> **Languages**: Objective-C / Swift  
> **Platform**: iOS  
> **Minimum iOS Version**: 12.0+  
> **Last Updated**: 2026-04-21

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

## Two-Phase Adaptation

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
│   └── testing-guide.md   # Testing guide
│
├── .claude/               # 🎯 Claude-specific guides
│   └── iOS26-适配框架指南.md
│
├── examples/              # ✅ Checklists
│   ├── phase1-checklist.md
│   ├── phase1-checklist.zh.md
│   ├── phase2-checklist.md
│   └── phase2-checklist.zh.md
│
├── scripts/               # 🔍 Scanning scripts
│   └── ios26-scanner.py   # Deprecated API scanner
│
└── templates/             # 📋 Code templates (reference only, not compiled)
    ├── swift/             # Swift templates
    │   ├── UIApplication+MainWindow.swift
    │   ├── SceneDelegate.swift
    │   ├── AppDelegate+Setup.swift
    │   └── UNNotificationOptions+Adapter.swift
    └── objc/              # Objective-C templates
        ├── UIApplication+MainWindow.h/.m
        ├── SceneDelegate.h/.m
        ├── AppDelegate+Setup.h/.m
        └── UNNotificationOptionsAdapter.h/.m
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
# Scan main project for deprecated APIs
python3 scripts/ios26-scanner.py /path/to/your/ios/project

# Output JSON report
python3 scripts/ios26-scanner.py /path/to/your/ios/project --format json --output report.json
```

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

## License

MIT License - see LICENSE file

---

**Author**: roder
