# Phase 1 Checklist: SDK Build Adaptation

> **Deadline**: April 28, 2026  
> **Goal**: Build with iOS 26 SDK, maintain existing UI

---

## Pre-Adaptation

### Environment Check
- [ ] Xcode version is 26.0 or higher
- [ ] macOS version is Sequoia 15.3 or higher
- [ ] iOS 26 SDK is available

### Strategy Decision
- [ ] Determined next release date
- [ ] Chosen adaptation strategy (A/B/C)
- [ ] Created adaptation branch: `feature/ios26-adaptation`
- [ ] Team members notified

---

## Project Scanning

### Automated Scan
- [ ] Ran `scripts/ios26-scanner.py` on the project
- [ ] Reviewed scanner report (errors & warnings)
- [ ] Excluded `Pods/` and other non-project directories if needed

### Deprecated API Scan (Manual or Verified)
- [ ] Scanned for `keyWindow` usage
- [ ] Scanned for `delegate.window` usage
- [ ] Scanned for `AppDelegate.window` usage
- [ ] Scanned for notification option alerts
- [ ] Scanned for status bar style settings

### Architecture Scan
- [ ] Checked SceneDelegate existence
- [ ] Checked AppDelegate `sharedInstance` method
- [ ] Checked Info.plist `UIApplicationSceneManifest`
- [ ] Listed all files requiring changes

### Third-Party SDK Scan
- [ ] Listed all SDKs and versions
- [ ] Checked SDK iOS 26 compatibility
- [ ] Identified SDKs requiring updates

---

## Implementation

### New Files Creation
- [ ] Created `UIApplication+Extension` (unified window access)
- [ ] Created `SceneDelegate` (if not exists)

### AppDelegate Modifications
- [ ] Added `sharedInstance` class method
- [ ] Created `setupApplication(launchOptions:)` method
- [ ] Created `setupSceneUI(window:)` method
- [ ] Added Scene Session configuration
- [ ] Separated iOS 12 and iOS 13+ launch paths

### SceneDelegate Implementation
- [ ] Implemented `willConnectTo` with window creation
- [ ] Forwarded to AppDelegate for business setup
- [ ] Implemented lifecycle forwarding (all 6 methods)
- [ ] Implemented URL handling forwarding

### Global Code Replacement
- [ ] Replaced all `keyWindow` calls
- [ ] Replaced all `delegate.window` calls
- [ ] Replaced all `AppDelegate.window` calls
- [ ] Updated window-based navigation
- [ ] Updated global popup display logic

### Notification API Updates
- [ ] Updated `willPresentNotification` completion handlers
- [ ] Updated `requestAuthorization` options
- [ ] Added `@available(iOS 26.0, *)` version checks

### Info.plist Configuration
- [ ] Added `UIDesignRequiresCompatibility` = true
- [ ] Added `UIApplicationSceneManifest` configuration
- [ ] Verified `UISceneDelegateClassName` points to SceneDelegate

---

## Compilation Verification

### Build Checks
- [ ] Project builds with iOS 26 SDK
- [ ] No compilation errors
- [ ] No deprecated API warnings
- [ ] Archive creation succeeds

### Static Analysis
- [ ] No analyzer warnings
- [ ] No static analysis errors

---

## Testing

### Device Testing
- [ ] Tested on minimum supported iOS version device
- [ ] Tested on iOS 13/14 device
- [ ] Tested on iOS 15/16 device
- [ ] Tested on iOS 17 device
- [ ] Tested on iOS 26 device

### Launch Testing
- [ ] Cold launch works on all versions
- [ ] Hot launch works on all versions
- [ ] Launch from push notification works
- [ ] Launch from deep link works

### Lifecycle Testing
- [ ] Background/foreground transitions work
- [ ] Application lifecycle events fire correctly
- [ ] Scene lifecycle events fire correctly

### Window Access Testing
- [ ] Global toasts display correctly
- [ ] Global alerts display correctly
- [ ] Loading indicators display correctly
- [ ] Action sheets display correctly

### Navigation Testing
- [ ] Push navigation works
- [ ] Pop navigation works
- [ ] Present modal works
- [ ] Dismiss modal works
- [ ] TabBar switching works

### Feature Testing
- [ ] Push notifications work
- [ ] Deep linking works
- [ ] Sharing works
- [ ] Camera/photo access works
- [ ] Location services work

### Liquid Glass Verification
- [ ] App does NOT show Liquid Glass effects
- [ ] UI looks same as before adaptation
- [ ] No visual changes in system controls

---

## Documentation

- [ ] Updated CHANGELOG
- [ ] Updated README if needed
- [ ] Documented any workaround implementations
- [ ] Added code comments for version-specific logic

---

## Pre-Release

- [ ] All checklist items completed
- [ ] Code review passed
- [ ] QA sign-off obtained
- [ ] Product manager approval
- [ ] Branch merged to main/release branch

---

## Post-Release Monitoring

- [ ] Monitor crash reports
- [ ] Monitor user feedback
- [ ] Check app store review feedback
- [ ] Verify analytics events are firing

---

**Author**: roder
