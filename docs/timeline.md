# iOS 26 / 27 Timeline & Adaptation Scope Overview

> **Last updated**: 2026-08-03
> **Audience**: Developers who need to explain "what must be done when" to their team or management
> **Sources**: Apple official announcements, WWDC25/WWDC26, iOS 27 Beta Release Notes, TN3187

This document is the **single authoritative timeline reference** for this skill repository.
Every milestone states: what Apple mandates, which adaptation scope is required,
the consequence of inaction, and which checklist applies.

---

## Timeline at a Glance

```
2025-06          2025-09           2026-04-28        ~2026-09          ~2027-04 (est.)
  │                │                  │                 │                  │
  ▼                ▼                  ▼                 ▼                  ▼
WWDC25           iOS 26 GA         App Store          Xcode 27 ships     App Store
iOS 26 SDK       released           mandates iOS 26    with iOS 27 GA     mandates iOS 27
debuts;          Liquid Glass       SDK builds         Liquid Glass       SDK builds
Liquid Glass     on by default      (now in effect❗)   mandatory;         (Phase 3 done)
introduced       for new SDK        ──────────────     compat flag        ──────────────
                 builds             Phase 1            removed            Phase 3
                 ──────────────     mandatory          ──────────────     mandatory
                 Opt-out:                              Phase 2
                 UIDesignRequires                      window closes
                 Compatibility
```

---

## Milestone Details

### Milestone 1: 2025-06 (WWDC25) — iOS 26 SDK Released

| Item | Detail |
|------|--------|
| Apple action | Ships Xcode 26 / iOS 26 SDK with the Liquid Glass design language |
| Mandate | None (fully voluntary) |
| Recommended | Trial-build in beta to estimate adaptation effort |

### Milestone 2: 2025-09 — iOS 26 General Release

| Item | Detail |
|------|--------|
| Apple action | iOS 26 reaches user devices |
| Mandate | Apps built with the iOS 26 SDK get Liquid Glass by default |
| Escape hatch | `UIDesignRequiresCompatibility = YES` temporarily restores the old look (**time-limited**, see Milestone 4) |
| Recommended | Start Phase 1 adaptation; do not wait for the deadline |

### Milestone 3: **2026-04-28** (now in effect❗) — App Store Mandates iOS 26 SDK Builds

| Item | Detail |
|------|--------|
| Apple mandate | All new apps and updates must be built with the iOS 26 SDK (Xcode 26+) |
| Consequence | **Submission rejected** — no grace period |
| Required scope | **Phase 1** (table below) |

**Phase 1 scope (iOS 26 SDK build compliance)**:

| # | Adaptation item | Nature | Scanner rules |
|---|-----------------|--------|---------------|
| 1 | Deprecated window access: `keyWindow` / `delegate.window` / `windows` / `statusBarFrame` | Build error/warning | WINDOW-001~008, STATUS-004 |
| 2 | SceneDelegate architecture migration (Info.plist `UIApplicationSceneManifest` + SceneDelegate + AppDelegate refactor) | Architecture requirement (also satisfies the iOS 27 mandate) | ARCH-001~003 |
| 3 | Notification options: `UNNotificationPresentationOptionAlert` → `.banner \| .list` | Deprecation warning | NOTIF-001 |
| 4 | StoreKit 1 → StoreKit 2 (StoreKit 1 **removed** in Xcode 26) | Build failure | STOREKIT-001 |
| 5 | AssetsLibrary removal, `UIWebView` cleanup | Build failure/rejection | ASSETSLIBRARY-*, WEB-001 |
| 6 | Privacy Manifest (`PrivacyInfo.xcprivacy`) | Rejection | PRIVACY-001 |
| 7 | CoreData iCloud sync keys removed, TLS 1.2 minimum | Runtime/connection failure | COREDATA-001, TLS-001 |
| 8 | Temporarily disable Liquid Glass: `UIDesignRequiresCompatibility = YES` | Optional transition aid | PHASE2-001 (removal reminder) |

> 📋 Full checklist: [examples/phase1-checklist.md](../examples/phase1-checklist.md)

### Milestone 4: **~2026-09** — Xcode 27 Ships, Liquid Glass Mandatory (Phase 2 Window Closes)

| Item | Detail |
|------|--------|
| Apple action | iOS 27 GA + Xcode 27 ship with iPhone 18 |
| Apple mandate | The `UIDesignRequiresCompatibility` flag is **removed**; Liquid Glass can no longer be disabled |
| Consequence | After upgrading to Xcode 27, app appearance switches to Liquid Glass; un-adapted custom UI suffers visual glitches and layout shifts |
| Required scope | **Phase 2** (table below) |
| Environment | Xcode 27 requires macOS Tahoe 26.4+, Apple Silicon only |

**Phase 2 scope (Liquid Glass visual compliance)**:

| # | Adaptation item | Nature | Scanner rules |
|---|-----------------|--------|---------------|
| 1 | Remove `UIDesignRequiresCompatibility` | Required | PHASE2-001 |
| 2 | Audit nav-bar customization: hardcoded backgrounds, `navigationBar addSubview` swallowed by compositing layers | Visual/functional breakage | NAVBAR-001 |
| 3 | `rightBarButtonItems` order reversal + shared glass background spacing fix | Visual breakage | BARBUTTON-001 |
| 4 | Custom TabBar: `setValue:forKey:@"tabBar"` private KVC crashes | **Crash** | TABBAR-001 |
| 5 | Floating TabBar safe-area changes (bottom layout via `additionalSafeAreaInsets`) | Layout misalignment | — |
| 6 | Keyboard glass toolbar (optional; clear `inputAccessoryView` as needed) | Visual harmony | KEYBOARD-001~003 |
| 7 | `UIScrollView.allowsLiquidTransform` edge-scroll distortion handling | Visual breakage | — |
| 8 | Full UI regression testing (Light/Dark/tinted modes) | Quality gate | — |

> 📋 Full checklist: [examples/phase2-checklist.md](../examples/phase2-checklist.md)

### Milestone 5: From 2026-09 — Building with the iOS 27 SDK Triggers Phase 3 Mandates

> ⚠️ The trigger is **the SDK you build with**, not the user's OS version.
> Binaries already shipped with the iOS 26 SDK keep running on iOS 27; the mandates
> activate the moment you rebuild with Xcode 27.

**Phase 3 scope (iOS 27 compliance, confirmed at WWDC26)**:

| # | Adaptation item | Level | Consequence | Scanner rules |
|---|-----------------|-------|-------------|---------------|
| 1 | UIScene lifecycle mandatory (official docs + TN3187) | 🔴 P0 | **App fails to launch** (users see a crash) | ARCH-001~002 |
| 2 | Launch screen: one of `UILaunchStoryboardName` / `UILaunchStoryboards` / `UILaunchScreen` / `UILaunchScreens` in Info.plist | 🔴 P0 | **App Store rejection** | Manual audit (generated Info.plist, see ios27-preview) |
| 3 | Remove leftover `-ld_classic` linker flags | 🔴 P0 | **Build failure**, CI breakage | LINKER-001 |
| 4 | Clang module name de-duplication (duplicate `module.modulemap`) | 🔴 P0 | Build failure | Manual check |
| 5 | `canOpenURL` deprecated + `LSApplicationQueriesSchemes` limit 50→25 | 🟡 P1 | Schemes beyond entry 25 silently return false | OPENURL-001~002 |
| 6 | On Demand Resources (`NSBundleResourceRequest`) deprecated | 🟡 P1 | May be removed later | ODR-001 |
| 7 | `MXMetricManager` → `MetricManager` | 🟡 P1 | MetricKit framework-level rework | METRICKIT-001 |
| 8 | Code-level silent changes: NSURL double-encoding fix, C++ `multimap/multiset::find()` semantics, `FilePath.stat()` name collision | 🟡 P1 | Subtle logic/build errors | Manual review |

> 📋 Full checklist: [examples/phase3-checklist.md](../examples/phase3-checklist.md)
> 📖 Deep dive: [docs/ios27-preview.md](ios27-preview.md)

### Milestone 6: **~2027-04 (est.)** — App Store Mandates iOS 27 SDK Builds

| Item | Detail |
|------|--------|
| Apple mandate (estimated, following the yearly pattern) | All new apps and updates must be built with the iOS 27 SDK (Xcode 27+) |
| Consequence | Submission rejected |
| Required | Phase 1 + Phase 2 + Phase 3, all complete |

---

## What Should I Do When? (Pick a Strategy by Release Date)

| Your next release date | Strategy | Required scope | Details |
|------------------------|----------|----------------|---------|
| Before 2026-04-28 | Strategy A: branch-based | Leave the current release untouched; complete Phase 1 on `feature/ios26-adaptation` | SKILL.md §Decision Framework |
| 2026-04-28 ~ 2026-09 | Strategy B | Phase 1 mandatory; evaluate Phase 2 based on pre-Xcode 27 releases | Same as above |
| After 2026-09 | Strategy C | Phase 1 + 2 + 3 in one iteration (recommended — no rework) | Same as above |

**Key advice**: Under any strategy, **get the Phase 1 SceneDelegate migration right the first time** —
it simultaneously satisfies the 2026-04-28 build mandate and iOS 27's deadliest "fails to launch"
mandate. It has the highest return of any single item on this timeline.

---

## Related Documents

| Document | Content |
|----------|---------|
| [SKILL.md](../SKILL.md) | Full adaptation guide, decision flows, code examples |
| [docs/ios27-preview.md](ios27-preview.md) | iOS 27 / Xcode 27 detailed preview (Phase 3) |
| [examples/](../examples/) | Phase checklists (EN/ZH) |
| [INTEGRATION.md](../INTEGRATION.md) | Usage guide and adaptation impact statement |
