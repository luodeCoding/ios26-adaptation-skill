# iOS 26 Adaptation Guide

<div align="right">
  <b>🌐 Language:</b> English | <a href="./README.zh.md">中文</a>
</div>

---

> **Languages**: Objective-C / Swift  
> **Platform**: iOS  
> **Minimum iOS Version**: 12.0+  
> **Last Updated**: 2026-04-21

A comprehensive skill guide for adapting to the iOS 26 SDK and Liquid Glass design language.

## Overview

Apple requires all apps submitted after **April 28, 2026** to be built with the iOS 26 SDK. This guide provides:

- 📋 **Two-phase adaptation strategy** — SDK build adaptation and Liquid Glass full adaptation
- 🔍 **Project scanning rules** — Identify deprecated APIs and required changes
- 📊 **Decision flowchart** — Choose the right strategy based on your timeline
- ✅ **Checklists** — Track progress for each phase

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

## Quick Start

### 1. Download This Repository Locally

```bash
# Option 1: git clone (recommended, easy to update later)
git clone https://github.com/luodeCoding/ios26-adaptation-skill.git

# Option 2: Download ZIP
# Visit https://github.com/luodeCoding/ios26-adaptation-skill/archive/refs/heads/main.zip
```

### 2. Reference the Local Folder in Your Main Project

**Xcode Steps:**

1. Open your main project in Xcode
2. Right-click the project root in the navigator → **Add Files to "YourProject"...**
3. In the file picker, locate your downloaded `ios26-adaptation-skill` folder
4. **Important**: Check **"Create folder references"** (NOT Create groups!)
   
   ![create-folder-reference](https://i.imgur.com/placeholder.png)
   
5. Make sure your app target is checked
6. Click **Add**

> 💡 **Why "Create folder references"?**
> - The folder appears with a blue icon in Xcode
> - Folder contents stay in sync with the local disk
> - Editing files in Xcode = editing the local repo directly
> - Editing files in Finder = changes appear in Xcode immediately

**Resulting project structure:**

```
YourMainProject/
├── ios26-adaptation-skill/     ← Blue folder (folder reference)
│   ├── templates/
│   │   ├── swift/
│   │   └── objc/
│   ├── scripts/
│   ├── docs/
│   └── ...
├── YourApp/
└── YourApp.xcodeproj
```

### 3. Add Template Code to Your Build Target

Files in a folder reference are **not compiled automatically**. You need to add the template files you need to your target:

1. From `ios26-adaptation-skill/templates/swift/`, select the files you need:
   - `UIApplication+MainWindow.swift`
   - `SceneDelegate.swift`
   - `AppDelegate+Setup.swift`
   - `UNNotificationOptions+Adapter.swift`
   
2. Right-click → **Add Files to "YourProject"...**
3. This time choose **"Create groups"** + check your target
4. These files will be added as yellow folders (groups) and will be compiled

> ⚠️ **Note**: Files added this way are **copied** into your main project. If you want to reference the skill repo files directly (without copying), you can:
> - Option A: Copy to main project for easier editing (recommended)
> - Option B: Don't add to target, just reference, and write manually in your project

### 4. Scan Your Project

```bash
# Run the local script directly
python3 /path/to/ios26-adaptation-skill/scripts/ios26-scanner.py /path/to/your/ios/project

# Generate JSON report
python3 /path/to/ios26-adaptation-skill/scripts/ios26-scanner.py /path/to/your/ios/project --format json --output report.json
```

### 5. Apply Code Templates

Copy the files you need from `templates/` into your Xcode project and adjust class names as needed:

| Template | Swift | Objective-C | Purpose |
|----------|-------|-------------|---------|
| `UIApplication+MainWindow` | [Swift](./templates/swift/UIApplication+MainWindow.swift) | [OC](./templates/objc/UIApplication+MainWindow.h) | Unified window/navigation access |
| `SceneDelegate` | [Swift](./templates/swift/SceneDelegate.swift) | [OC](./templates/objc/SceneDelegate.h) | Window creation & lifecycle forwarding |
| `AppDelegate+Setup` | [Swift](./templates/swift/AppDelegate+Setup.swift) | [OC](./templates/objc/AppDelegate+Setup.h) | Dual-path launch refactoring |
| `UNNotificationOptions+Adapter` | [Swift](./templates/swift/UNNotificationOptions+Adapter.swift) | [OC](./templates/objc/UNNotificationOptionsAdapter.h) | iOS 26 notification options adapter |

See [`templates/README.md`](./templates/README.md) for detailed integration instructions.

### 6. Follow the Checklists

See [SKILL.md](./SKILL.md) for:
- Decision flowcharts
- Implementation guides
- Phase-by-phase checklists
- Testing framework

### 7. Check the FAQ

Have common questions? See [docs/faq.md](./docs/faq.md).

---

## Workflow: Quick Adjustment When Issues Arise

```
Main project Xcode build error
        ↓
Check templates/docs in ios26-adaptation-skill/
        ↓
Edit skill project files directly in Xcode (blue folder)
        ↓
Changes take effect immediately, no copy/sync needed
        ↓
After verification, commit to GitHub from skill project directory
        ↓
cd /path/to/ios26-adaptation-skill
git add .
git commit -m "fix: xxx"
git push
```

> ✅ **Core advantage**: All files are local. Edit and compile immediately. Editing skill project files edits the local repo directly. Commit to GitHub anytime.

---

## Project Structure

```
ios26-adaptation-skill/
├── README.md              # This file - quick start guide
├── README.zh.md           # Chinese version
├── SKILL.md               # Detailed skill documentation
├── CHANGELOG.md           # Version history
├── LICENSE                # MIT License
├── AGENTS.md              # Claude Code Agent guide
├── docs/
│   ├── testing-guide.md   # Testing guide for QA teams
│   └── faq.md             # Frequently asked questions
├── .claude/
│   └── iOS26-适配框架指南.md  # Full adaptation framework (Chinese)
├── examples/
│   ├── phase1-checklist.md    # Phase 1 execution checklist (English)
│   ├── phase1-checklist.zh.md # Phase 1 execution checklist (Chinese)
│   ├── phase2-checklist.md    # Phase 2 execution checklist (English)
│   └── phase2-checklist.zh.md # Phase 2 execution checklist (Chinese)
├── scripts/
│   └── ios26-scanner.py   # Automated project scanning script
└── templates/
    ├── swift/                 # Swift code templates
    └── objc/                  # Objective-C code templates
```

## Common Misconceptions

| Misconception | Fact |
|--------------|------|
| Must change Deployment Target to iOS 26 | ❌ No. Keep your current minimum version (iOS 12/13, etc.) |
| Users must upgrade to iOS 26 | ❌ No. Runtime requirements are determined by Deployment Target |
| Existing app versions will be removed | ❌ No. Only affects new submissions and updates |
| There is a grace period | ❌ No. April 28, 2026 is a hard deadline |

## Core Concepts

### SceneDelegate Architecture (iOS 13+)

- **Problem**: `UIApplication.keyWindow` and `AppDelegate.window` are unreliable on iOS 13+
- **Solution**: Use a unified access interface via `UIApplication` extension
- **Impact**: All window access must go through the new interface

### Deprecated APIs (iOS 26)

| Deprecated API | Replacement |
|---------------|-------------|
| `keyWindow` | SceneDelegate-based window access |
| `UNNotificationPresentationOptionAlert` | `UNNotificationPresentationOptionBanner \| List` |
| `UNAuthorizationOptionAlert` | `UNAuthorizationOptionBanner` |

### Liquid Glass Design

- **What**: iOS 26's new visual language
- **Auto-adapt**: Standard UIKit controls automatically get the new look
- **Custom**: Custom UI requires manual adjustment
- **Timeline**: Optional in Phase 1, mandatory in Phase 2

## Decision Checklist

Before starting adaptation, answer these questions:

- [ ] When is your next app release planned?
- [ ] Are development resources available now?
- [ ] Is SceneDelegate already configured?
- [ ] How many deprecated API calls exist in the project?
- [ ] Are there many custom UI components?

## Resources

- [Apple Developer News](https://developer.apple.com/news/)
- [iOS 26 Release Notes](https://developer.apple.com/documentation/ios-release-notes)
- [Liquid Glass Design Guide](https://developer.apple.com/design/)

## License

MIT License - see LICENSE file

---

**Author**: roder
