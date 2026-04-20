# iOS 26 Adaptation Skill

<div align="right">
  <b>🌐 Language:</b> English | <a href="./README.zh.md">中文</a>
</div>

---

> **Language**: Objective-C / Swift  
> **Platform**: iOS  
> **Minimum iOS Version**: 12.0+  
> **Last Updated**: 2026-04-14

A comprehensive skill for adapting iOS applications to iOS 26 SDK and Liquid Glass design language.

## Overview

Apple requires all apps submitted after **April 28, 2026** to be built with iOS 26 SDK. This skill provides:

- 📋 **Two-phase adaptation strategy** - SDK build adaptation and Liquid Glass full adaptation
- 🔍 **Project scanning rules** - Identify deprecated APIs and required changes
- 📊 **Decision flowcharts** - Choose the right adaptation strategy based on your timeline
- ✅ **Checklists** - Track progress through each phase

## Critical Deadlines

| Date | Requirement | Impact |
|------|-------------|--------|
| **2026-04-28** | Must build with iOS 26 SDK | Cannot submit updates without compliance |
| **~2026-09** | Xcode 27 release, Liquid Glass mandatory | `UIDesignRequiresCompatibility` will be removed |

## Two-Phase Adaptation

### Phase 1: SDK Build Adaptation (Before 2026-04-28)

**Goal**: Build with iOS 26 SDK while maintaining existing UI

**Key Tasks**:
- Upgrade to Xcode 26.0+
- Fix deprecated API calls (keyWindow, etc.)
- Temporarily disable Liquid Glass
- Complete SceneDelegate architecture migration

### Phase 2: Liquid Glass Full Adaptation (Before Xcode 27)

**Goal**: Fully adapt to Liquid Glass design language

**Key Tasks**:
- Remove `UIDesignRequiresCompatibility` flag
- Verify all UI controls under Liquid Glass
- Adjust custom UI for visual harmony

## Quick Start

### 1. Install via CocoaPods

Add this line to your project's `Podfile`:

```ruby
pod 'iOS26Adaptation', '~> 1.0'
```

Then run:

```bash
pod install
```

> **Why CocoaPods?** This package contains only documentation, code templates, and scanner scripts — **zero compiled code** is added to your app. After you finish iOS 26 adaptation and bug verification, you can safely remove the pod without any impact on your project.

After installation, all resources are available at:

```
Pods/iOS26Adaptation/iOS26Adaptation.bundle/
├── templates/       # Swift & Objective-C code templates
├── scripts/         # ios26-scanner.py
├── docs/            # FAQ and testing guide
├── examples/        # Phase-by-phase checklists
└── *.md             # Documentation
```

### 2. Determine Your Strategy

Based on your next app release date:

| Release Date | Recommended Strategy |
|-------------|---------------------|
| Before 2026-04-28 | **Strategy A**: Adapt in new branch, merge after deadline |
| 2026-04-28 ~ Xcode 27 | **Strategy B**: Complete Phase 1, evaluate Phase 2 |
| After Xcode 27 | **Strategy C**: Complete both phases together |

### 3. Scan Your Project

Use the included scanner for an automated report:

```bash
# If installed via CocoaPods, run from the bundle
python3 Pods/iOS26Adaptation/iOS26Adaptation.bundle/scripts/ios26-scanner.py /path/to/your/ios/project

# Or if using this repository directly
python3 scripts/ios26-scanner.py /path/to/your/ios/project

# Generate a JSON report for further processing
python3 Pods/iOS26Adaptation/iOS26Adaptation.bundle/scripts/ios26-scanner.py /path/to/your/ios/project --format json --output report.json
```

The scanner checks for:
- Deprecated APIs (`keyWindow`, `delegate.window`, notification options, etc.)
- Missing `SceneDelegate` or `UIApplicationSceneManifest`
- Missing `sharedInstance` in `AppDelegate`

Or search manually for common deprecated patterns:

```bash
# Common patterns to search for
grep -r "keyWindow" --include="*.swift" --include="*.m" --include="*.mm"
grep -r "delegate\.window" --include="*.swift" --include="*.m" --include="*.mm"
grep -r "UNNotificationPresentationOptionAlert" --include="*.swift" --include="*.m"
grep -r "UNAuthorizationOptionAlert" --include="*.swift" --include="*.m"
```

### 4. Apply Code Templates

Reference the relevant templates from the installed bundle (or from `templates/` if using this repo directly) and copy them into your Xcode project, adjusting class names to match your project:

| Template | Swift | Objective-C | Purpose |
|----------|-------|-------------|---------|
| Template | Swift | Objective-C | Purpose |
|----------|-------|-------------|---------|
| `UIApplication+Extension` | [Swift](./templates/swift/UIApplication+Extension.swift) | [OC](./templates/objc/UIApplication+Extension.h) | Unified window/navigation access |
| `SceneDelegate` | [Swift](./templates/swift/SceneDelegate.swift) | [OC](./templates/objc/SceneDelegate.h) | Window creation & lifecycle forwarding |
| `AppDelegate+Setup` | [Swift](./templates/swift/AppDelegate+Setup.swift) | [OC](./templates/objc/AppDelegate+Setup.h) | Dual-path startup refactoring |
| `NotificationAdapter` | [Swift](./templates/swift/NotificationAdapter.swift) | [OC](./templates/objc/NotificationAdapter.h) | iOS 26 notification options adapter |

> After CocoaPods installation, these templates are also available at `Pods/iOS26Adaptation/iOS26Adaptation.bundle/templates/`.

See `Pods/iOS26Adaptation/iOS26Adaptation.bundle/templates/README.md` (or [`templates/README.md`](./templates/README.md) in this repo) for detailed integration instructions.

### 5. Follow the Checklist

See [SKILL.md](./SKILL.md) for detailed:
- Decision flowcharts
- Implementation guides
- Phase-by-phase checklists
- Testing frameworks

### 6. Check the FAQ

Stuck on a common issue? See [docs/faq.md](./docs/faq.md) for answers to questions like:
- Do I need to change my Deployment Target?
- What if my CocoaPods contain deprecated APIs?
- Can I test on the simulator only?

## Project Structure

```
ios26-adaptation-skill/
├── README.md              # This file - quick start guide
├── README.zh.md           # Chinese version of README
├── SKILL.md               # Detailed skill documentation
├── CHANGELOG.md           # Version history
├── LICENSE                # MIT License
├── AGENTS.md              # Agent usage guide for Claude Code
├── docs/
│   ├── testing-guide.md   # Testing guide for QA team
│   └── faq.md             # Frequently asked questions
├── .claude/
│   └── iOS26-适配框架指南.md  # Full adaptation framework guide (Chinese)
├── examples/
│   ├── phase1-checklist.md    # Phase 1 execution checklist (EN)
│   ├── phase1-checklist.zh.md # Phase 1 execution checklist (ZH)
│   ├── phase2-checklist.md    # Phase 2 execution checklist (EN)
│   └── phase2-checklist.zh.md # Phase 2 execution checklist (ZH)
├── scripts/
│   └── ios26-scanner.py   # Automated project scanner
└── templates/
    ├── swift/                 # Swift code templates
    └── objc/                  # Objective-C code templates
```

## Common Misconceptions

| Misconception | Reality |
|--------------|---------|
| Must change Deployment Target to iOS 26 | ❌ No. Keep your current minimum version (iOS 12/13/etc.) |
| Users must upgrade to iOS 26 | ❌ No. Runtime requirement is determined by Deployment Target |
| Existing app versions will be removed | ❌ No. Only affects new submissions and updates |
| There is a grace period | ❌ No. April 28, 2026 is a hard deadline |

## Key Concepts

### SceneDelegate Architecture (iOS 13+)

- **Problem**: `UIApplication.keyWindow` and `AppDelegate.window` are unreliable in iOS 13+
- **Solution**: Use unified access interface through `UIApplication` extension
- **Impact**: All window access must go through the new interface

### Deprecated APIs (iOS 26)

| Deprecated | Replacement |
|-----------|-------------|
| `keyWindow` | SceneDelegate-based window access |
| `UNNotificationPresentationOptionAlert` | `UNNotificationPresentationOptionBanner \| List` |
| `UNAuthorizationOptionAlert` | `UNAuthorizationOptionBanner` |

### Liquid Glass Design

- **What**: New visual language in iOS 26
- **Auto-adapting**: Standard UIKit controls get new look automatically
- **Customization**: Custom UI needs manual adjustment
- **Timeline**: Optional in Phase 1, mandatory in Phase 2

## Decision Checklist

Before starting adaptation, answer these questions:

- [ ] When is your next app release planned?
- [ ] Do you have development resources available now?
- [ ] Is SceneDelegate already configured?
- [ ] How many deprecated API calls exist in the project?
- [ ] Do you use extensive custom UI components?

## Resources

- [Apple Developer News](https://developer.apple.com/news/)
- [iOS 26 Release Notes](https://developer.apple.com/documentation/ios-release-notes)
- [Liquid Glass Design Guidelines](https://developer.apple.com/design/)

## License

MIT License - See LICENSE file for details

---

**Author**: roder
