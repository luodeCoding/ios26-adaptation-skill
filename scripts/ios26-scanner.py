#!/usr/bin/env python3
"""
iOS 26 Adaptation Scanner

Scans an iOS project for deprecated APIs and required architectural changes
related to iOS 26 SDK adaptation.

Usage:
    python3 ios26-scanner.py /path/to/your/ios/project
    python3 ios26-scanner.py /path/to/your/ios/project --format json --output report.json
"""

import argparse
import json

import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import List


@dataclass
class ScanIssue:
    rule_id: str
    severity: str  # error, warning, info
    message: str
    file: str
    line: int
    column: int
    match: str
    suggestion: str


@dataclass
class ScanResult:
    total_files_scanned: int = 0
    total_issues: int = 0
    errors: int = 0
    warnings: int = 0
    infos: int = 0
    issues: List[ScanIssue] = field(default_factory=list)
    architecture: dict = field(default_factory=dict)


RULES = [
    {
        "id": "WINDOW-001",
        "name": "Deprecated keyWindow usage (Swift)",
        "pattern": re.compile(r"UIApplication\.shared\.keyWindow"),
        "extensions": {".swift"},
        "severity": "error",
        "suggestion": "Use UIApplication.shared.mainWindow (via extension)",
    },
    {
        "id": "WINDOW-002",
        "name": "Deprecated keyWindow usage (Objective-C)",
        "pattern": re.compile(r"\[UIApplication\s+sharedApplication\]\s*\.keyWindow"),
        "extensions": {".m", ".mm"},
        "severity": "error",
        "suggestion": "Use [[UIApplication sharedApplication] mainWindow] (via extension)",
    },
    {
        "id": "WINDOW-003",
        "name": "Delegate window access",
        "pattern": re.compile(r"delegate\s*\.\s*window"),
        "extensions": {".swift", ".m", ".mm"},
        "severity": "warning",
        "suggestion": "Use unified window access interface (UIApplication+Extension)",
    },
    {
        "id": "WINDOW-004",
        "name": "AppDelegate window property access",
        "pattern": re.compile(r"AppDelegate\S*\.window"),
        "extensions": {".swift", ".m", ".mm"},
        "severity": "warning",
        "suggestion": "Use unified window access interface",
    },
    {
        "id": "WINDOW-005",
        "name": "Window rootViewController chain",
        "pattern": re.compile(r"\.window\.rootViewController"),
        "extensions": {".swift", ".m", ".mm"},
        "severity": "warning",
        "suggestion": "Use UIApplication.shared.visibleViewController",
    },
    {
        "id": "WINDOW-006",
        "name": "Window visibleViewController chain",
        "pattern": re.compile(r"\.window\.visibleViewController"),
        "extensions": {".swift", ".m", ".mm"},
        "severity": "warning",
        "suggestion": "Use UIApplication.shared.visibleViewController",
    },
    {
        "id": "WINDOW-007",
        "name": "Deprecated UIApplication.shared.windows usage (Swift)",
        "pattern": re.compile(r"UIApplication\.shared\.windows"),
        "extensions": {".swift"},
        "severity": "warning",
        "suggestion": "Deprecated since iOS 15. Enumerate connectedScenes and use UIWindowScene.windows instead",
    },
    {
        "id": "WINDOW-008",
        "name": "Deprecated UIApplication windows usage (Objective-C)",
        "pattern": re.compile(r"\[UIApplication\s+sharedApplication\]\s*\.windows"),
        "extensions": {".m", ".mm"},
        "severity": "warning",
        "suggestion": "Deprecated since iOS 15. Enumerate connectedScenes and use UIWindowScene.windows instead",
    },
    {
        "id": "NOTIF-001",
        "name": "Deprecated UNNotificationPresentationOptionAlert",
        "pattern": re.compile(r"UNNotificationPresentationOptionAlert"),
        "extensions": {".swift", ".m", ".mm"},
        "severity": "warning",
        "suggestion": "Use NotificationAdapter.presentationOptions or version-check to Banner|List",
    },
    # NOTIF-002 removed: UNAuthorizationOptionAlert is NOT deprecated in iOS 26 SDK.
    # Do NOT flag it — it remains valid and should not be replaced.
    {
        "id": "SCREEN-001",
        "name": "Deprecated UIScreen.main usage (Swift)",
        "pattern": re.compile(r"UIScreen\.main"),
        "extensions": {".swift"},
        "severity": "warning",
        "suggestion": "Use UIWindowScene screen bounds for iOS 13+; annotate iOS 12 fallback with comment",
    },
    {
        "id": "SCREEN-002",
        "name": "Deprecated UIScreen mainScreen usage (Objective-C)",
        "pattern": re.compile(r"\[UIScreen\s+mainScreen\]"),
        "extensions": {".m", ".mm"},
        "severity": "warning",
        "suggestion": "Use UIWindowScene screen bounds for iOS 13+; annotate iOS 12 fallback with comment",
    },
    {
        "id": "WEB-001",
        "name": "Removed UIWebView usage",
        "pattern": re.compile(r"UIWebView"),
        "extensions": {".swift", ".m", ".mm"},
        "severity": "error",
        "suggestion": "Replace with WKWebView (available since iOS 8)",
    },
    {
        "id": "TLS-001",
        "name": "Legacy TLS version (1.0/1.1)",
        "pattern": re.compile(r"TLSv10|TLSv11|tlsMinimumSupportedProtocolVersion\s*=\s*\.TLSv1[01]|kCFStreamSSLLevel"),
        "extensions": {".swift", ".m", ".mm"},
        "severity": "warning",
        "suggestion": "Upgrade server to TLS 1.2+; remove legacy TLS workaround code",
    },
    {
        "id": "COREDATA-001",
        "name": "Removed CoreData iCloud ubiquitous sync keys",
        "pattern": re.compile(r"NSPersistentStoreUbiquitousContentNameKey|NSPersistentStoreUbiquitousContentURLKey|NSPersistentStoreUbiquitousPeerTokenOption|NSPersistentStoreRemoveUbiquitousMetadataOption|NSPersistentStoreUbiquitousContainerIdentifierKey|NSPersistentStoreRebuildFromUbiquitousContentOption"),
        "extensions": {".swift", ".m", ".mm"},
        "severity": "error",
        "suggestion": "Migrate to NSPersistentCloudKitContainer (iOS 13+) or SwiftData (iOS 17+)",
    },
    {
        "id": "SWIFT6-001",
        "name": "Swift 6 strict concurrency — potential Sendable issue",
        "pattern": re.compile(r"@StateObject|@ObservedObject|completionHandler.*@escaping"),
        "extensions": {".swift"},
        "severity": "info",
        "suggestion": "Review for Swift 6 strict concurrency: add @MainActor, conform to Sendable, or use async/await",
    },
    {
        "id": "STATUS-001",
        "name": "Global statusBarStyle assignment",
        "pattern": re.compile(r"statusBarStyle\s*=\s*UIStatusBarStyle"),
        "extensions": {".swift", ".m", ".mm"},
        "severity": "warning",
        "suggestion": "Implement preferredStatusBarStyle in ViewController instead",
    },
    {
        "id": "STATUS-002",
        "name": "UIApplication shared statusBarStyle access",
        "pattern": re.compile(r"UIApplication\.shared\.\w*statusBarStyle"),
        "extensions": {".swift"},
        "severity": "warning",
        "suggestion": "Implement preferredStatusBarStyle in ViewController instead",
    },
    {
        "id": "STATUS-003",
        "name": "UIApplication shared statusBarStyle access (OC)",
        "pattern": re.compile(r"\[UIApplication\s+sharedApplication\]\.\w*statusBarStyle"),
        "extensions": {".m", ".mm"},
        "severity": "warning",
        "suggestion": "Implement preferredStatusBarStyle in ViewController instead",
    },
    {
        "id": "STATUS-004",
        "name": "Deprecated statusBarFrame access",
        "pattern": re.compile(r"statusBarFrame"),
        "extensions": {".swift", ".m", ".mm"},
        "severity": "warning",
        "suggestion": "Use UIWindowScene.statusBarManager.statusBarFrame (iOS 13+) instead of UIApplication statusBarFrame",
    },
    {
        "id": "STOREKIT-001",
        "name": "StoreKit 1 API usage (removed in Xcode 26)",
        "pattern": re.compile(r"SKPaymentTransaction|SKProductsRequest|SKProductsRequestDelegate|SKPaymentQueue|SKPaymentTransactionObserver"),
        "extensions": {".swift", ".m", ".mm"},
        "severity": "error",
        "suggestion": "Migrate to StoreKit 2 (Product.purchase(), Transaction, App Store Server API). iOS 15+ required.",
    },
    {
        "id": "SIRIKIT-001",
        "name": "Deprecated SiriKit intent domain",
        "pattern": re.compile(r"INSetAudioSourceInCarIntent|INSetClimateSettingsInCarIntent|INSetDefrosterSettingsInCarIntent|INSetSeatSettingsInCarIntent|INSaveProfileInCarIntent|INSetProfileInCarIntent|INSetRadioStationIntent|INAppendToNoteIntent|INCreateTaskListIntent|INDeleteTasksIntent|INPayBillIntent|INSearchForBillsIntent|INTransferMoneyIntent|INSearchForPhotosIntent|INStartPhotoPlaybackIntent|INGetVisualCodeIntent|INSearchCallHistoryIntent"),
        "extensions": {".swift", ".m", ".mm"},
        "severity": "warning",
        "suggestion": "Migrate to App Intents framework. SiriKit intent domains are deprecated.",
    },
    {
        "id": "SWIFTUI-001",
        "name": "Deprecated NavigationView (SwiftUI)",
        "pattern": re.compile(r"NavigationView\b"),
        "extensions": {".swift"},
        "severity": "warning",
        "suggestion": "Use NavigationStack (iOS 16+) with navigationDestination(for:)",
    },
    {
        "id": "SWIFTUI-002",
        "name": "Deprecated cornerRadius modifier (SwiftUI)",
        "pattern": re.compile(r"\.cornerRadius\("),
        "extensions": {".swift"},
        "severity": "warning",
        "suggestion": "Use clipShape(.rect(cornerRadius:)) or RoundedRectangle instead",
    },
    {
        "id": "SWIFTUI-003",
        "name": "Deprecated foregroundColor modifier (SwiftUI)",
        "pattern": re.compile(r"\.foregroundColor\("),
        "extensions": {".swift"},
        "severity": "warning",
        "suggestion": "Use foregroundStyle() instead",
    },
    {
        "id": "PHOTOS-001",
        "name": "Deprecated UIImagePickerController",
        "pattern": re.compile(r"UIImagePickerController"),
        "extensions": {".swift", ".m", ".mm"},
        "severity": "warning",
        "suggestion": "Use PHPickerViewController (PhotosUI, iOS 14+) for photo selection",
    },
    {
        "id": "ASSETSLIBRARY-001",
        "name": "Removed AssetsLibrary import (Swift)",
        "pattern": re.compile(r"import AssetsLibrary"),
        "extensions": {".swift"},
        "severity": "error",
        "suggestion": "Remove AssetsLibrary import. ALAssetsLibrary is obsoleted in iOS 26. Use PHPhotoLibrary from Photos framework.",
    },
    {
        "id": "ASSETSLIBRARY-002",
        "name": "Removed AssetsLibrary import (Objective-C)",
        "pattern": re.compile(r"#import\s+<AssetsLibrary/AssetsLibrary\.h>|@import AssetsLibrary"),
        "extensions": {".m", ".mm", ".h"},
        "severity": "error",
        "suggestion": "Remove AssetsLibrary import. ALAssetsLibrary is obsoleted in iOS 26. Use PHPhotoLibrary from Photos framework.",
    },
    {
        "id": "ASSETSLIBRARY-003",
        "name": "Removed ALAssetsLibrary usage",
        "pattern": re.compile(r"ALAssetsLibrary"),
        "extensions": {".swift", ".m", ".mm", ".h"},
        "severity": "error",
        "suggestion": "ALAssetsLibrary is obsoleted in iOS 26. Use PHPhotoLibrary from Photos framework.",
    },
    {
        "id": "KEYBOARD-001",
        "name": "Custom UITextField subclass detected",
        "pattern": re.compile(r"class\s+\w+\s*:\s*UITextField|@interface\s+\w+\s*:\s*UITextField"),
        "extensions": {".swift", ".m", ".mm", ".h"},
        "severity": "info",
        "suggestion": "Review for Liquid Glass keyboard toolbar effect. If the glass inputAccessoryView looks disruptive, set inputAccessoryView = UIView() on iOS 26+ (see templates/swift/UITextInput+LiquidGlassAdapter)",
    },
    {
        "id": "KEYBOARD-002",
        "name": "Custom UITextView subclass detected",
        "pattern": re.compile(r"class\s+\w+\s*:\s*UITextView|@interface\s+\w+\s*:\s*UITextView"),
        "extensions": {".swift", ".m", ".mm", ".h"},
        "severity": "info",
        "suggestion": "Review for Liquid Glass keyboard toolbar effect. If the glass inputAccessoryView looks disruptive, set inputAccessoryView = UIView() on iOS 26+ (see templates/swift/UITextInput+LiquidGlassAdapter)",
    },
    {
        "id": "KEYBOARD-003",
        "name": "inputAccessoryView assignment found",
        "pattern": re.compile(r"inputAccessoryView\s*="),
        "extensions": {".swift", ".m", ".mm"},
        "severity": "info",
        "suggestion": "Verify Liquid Glass compatibility: if this is a custom toolbar, ensure it renders correctly over the glass keyboard. If it's clearing the default accessory view, confirm iOS 26+ guard is present.",
    },
    {
        "id": "TABBAR-001",
        "name": "Private KVC override of tabBar (crashes on iOS 26)",
        "pattern": re.compile(r"forKey:\s*@?\s*\"tabBar\""),
        "extensions": {".swift", ".m", ".mm"},
        "severity": "error",
        "suggestion": "iOS 26 adds runtime protection for the tabBar property: setValue:forKey:@\"tabBar\" crashes or produces an extra tab. Use UITabBarAppearance for styling, or a custom container controller for a fully custom tab bar.",
    },
    {
        "id": "NAVBAR-001",
        "name": "Direct addSubview on UINavigationBar",
        "pattern": re.compile(r"navigationBar\s+addSubview|navigationBar\.addSubview"),
        "extensions": {".swift", ".m", ".mm"},
        "severity": "warning",
        "suggestion": "iOS 26's new navigation bar compositing layer swallows subviews added directly to navigationBar (they disappear after push/pop). Add the view to navigationController.view or use navigationItem.titleView instead.",
    },
    {
        "id": "BARBUTTON-001",
        "name": "rightBarButtonItems array assignment",
        "pattern": re.compile(r"rightBarButtonItems\s*="),
        "extensions": {".swift", ".m", ".mm"},
        "severity": "info",
        "suggestion": "iOS 26 reverses the display order of rightBarButtonItems compared to earlier versions. Verify the order visually and branch with #available(iOS 26, *) if needed.",
    },
    {
        "id": "OPENURL-001",
        "name": "canOpenURL usage (deprecated in iOS 27)",
        "pattern": re.compile(r"canOpenURL"),
        "extensions": {".swift", ".m", ".mm"},
        "severity": "info",
        "suggestion": "Deprecated at iOS 27. Migrate to attempt-and-handle: open(_:options:completionHandler:) is not constrained by LSApplicationQueriesSchemes. For presence checks use the universalLinksOnly open option.",
    },
    {
        "id": "ODR-001",
        "name": "On Demand Resources usage (deprecated in iOS 27)",
        "pattern": re.compile(r"NSBundleResourceRequest"),
        "extensions": {".swift", ".m", ".mm"},
        "severity": "warning",
        "suggestion": "NSBundleResourceRequest / On Demand Resources are deprecated in iOS 27. Plan migration to the Background Assets framework.",
    },
    {
        "id": "METRICKIT-001",
        "name": "MXMetricManager usage (replaced in iOS 27)",
        "pattern": re.compile(r"MXMetricManager"),
        "extensions": {".swift", ".m", ".mm"},
        "severity": "warning",
        "suggestion": "MetricKit is restructured in iOS 27: MXMetricManager is replaced by MetricManager (async sequences, Codable + Sendable reports). Plan migration when adopting the iOS 27 SDK.",
    },
]

DEFAULT_EXCLUDES = {
    ".git",
    ".svn",
    "Pods",
    "Carthage",
    "node_modules",
    "build",
    "Build",
    "DerivedData",
    ".build",
    "fastlane",
    "vendor",
    "ThirdParty",
}

# Project-level rules are emitted by scan_project() rather than the per-line RULES
# table. Kept here so the coverage-ledger consistency test can validate them.
PROJECT_RULE_IDS = {
    "PRIVACY-001", "PHASE2-001", "LINKER-001", "OPENURL-002",
    "ARCH-001", "ARCH-002", "ARCH-003", "ARCH-004",
    "LAUNCH-001", "LAUNCH-002", "LAUNCH-003",
    "EXT-001", "SDK-001", "SDK-002",
}

# iOS 27 launch screen mandate: Info.plist must contain one of these four keys
LAUNCH_KEYS = ("UILaunchStoryboardName", "UILaunchStoryboards", "UILaunchScreen", "UILaunchScreens")

# Third-party SDKs with known iOS 26 compatibility constraints
# (see docs/sdk-compatibility.md for the full maintained table)
KNOWN_SDKS = [
    (re.compile(r"FBSDK\w+|FacebookCore|FacebookLogin|FacebookShare|FBSDKCoreKit", re.I), "Facebook iOS SDK"),
    (re.compile(r"\bFirebase\w*", re.I), "Firebase"),
    (re.compile(r"RevenueCat", re.I), "RevenueCat"),
    (re.compile(r"JPush|JCore", re.I), "极光推送 JPush"),
    (re.compile(r"\bAFNetworking\b", re.I), "AFNetworking"),
    (re.compile(r"\bSDWebImage\b", re.I), "SDWebImage"),
]


def should_exclude(path: Path, explicit_excludes: List[str]) -> bool:
    parts = set(path.parts)
    if parts & DEFAULT_EXCLUDES:
        return True
    if parts & set(explicit_excludes):
        return True
    return False


def _is_comment_line(line: str) -> bool:
    """Rough heuristic: skip lines that are purely comments."""
    stripped = line.strip()
    return stripped.startswith("//") or stripped.startswith("*") or stripped.startswith("/*")


def _should_skip_issue(rule_id: str, line: str, filepath: Path) -> bool:
    """Filter out false positives."""
    # Skip comment-only lines for window-related rules
    if rule_id in ("WINDOW-003", "WINDOW-004") and _is_comment_line(line):
        return True
    # Skip comment-only lines for iOS 26/27 behavior rules (often referenced in notes)
    if rule_id in ("TABBAR-001", "NAVBAR-001", "BARBUTTON-001", "OPENURL-001") and _is_comment_line(line):
        return True
    # UIApplication+Extension / UIApplication+MainWindow files legitimately access
    # delegate.window as iOS 12 fallback
    if rule_id == "WINDOW-003" and ("UIApplication+Extension" in str(filepath) or "UIApplication+MainWindow" in str(filepath)):
        if "self.delegate.window" in line or ("delegate.window" in line and "return" in line):
            return True
    # statusBarManager.statusBarFrame is the modern replacement — do not flag it
    if rule_id == "STATUS-004" and "statusBarManager" in line:
        return True
    # UIScreen.main in iOS 12 fallback path is legitimate but should be annotated
    if rule_id in ("SCREEN-001", "SCREEN-002") and ("iOS 12" in line or "fallback" in line.lower() or "deprecated" in line.lower()):
        return True
    # AppDelegate templates legitimately use UIScreen.main for iOS 12 path
    if rule_id in ("SCREEN-001", "SCREEN-002") and "AppDelegate" in str(filepath):
        if "iOS 12" in line or "fallback" in line.lower():
            return True
    # UIScreen.main used inside a SceneDelegate-unaffected local pod or vendor library
    # is a known limitation; these should be updated in their upstream repos
    if rule_id in ("SCREEN-001", "SCREEN-002") and any(x in str(filepath) for x in ["Pods/", "Vender/", "vendor/", "ThirdParty/"]):
        return True
    return False


def scan_file(filepath: Path, rules: List[dict]) -> List[ScanIssue]:
    issues = []
    ext = filepath.suffix
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return issues

    lines = content.splitlines()
    for rule in rules:
        if ext not in rule["extensions"]:
            continue
        pattern = rule["pattern"]
        for line_no, line in enumerate(lines, start=1):
            for match in pattern.finditer(line):
                if _should_skip_issue(rule["id"], line, filepath):
                    continue
                issues.append(
                    ScanIssue(
                        rule_id=rule["id"],
                        severity=rule["severity"],
                        message=rule["name"],
                        file=str(filepath),
                        line=line_no,
                        column=match.start() + 1,
                        match=match.group(0),
                        suggestion=rule["suggestion"],
                    )
                )
    return issues


def detect_project_type(project_path: Path) -> dict:
    """Detect if project is Swift-only, mixed, or Objective-C only. Also detect deployment target."""
    swift_count = 0
    objc_count = 0
    deployment_target = None

    for filepath in project_path.rglob("*"):
        if should_exclude(filepath, []):
            continue
        if not filepath.is_file():
            continue
        if filepath.suffix == ".swift":
            swift_count += 1
        elif filepath.suffix in {".m", ".mm"}:
            objc_count += 1

    # Try to detect deployment target from Podfile or project files
    for podfile in project_path.rglob("Podfile"):
        if should_exclude(podfile, []):
            continue
        try:
            content = podfile.read_text(encoding="utf-8", errors="ignore")
            match = re.search(r"platform\s+:ios,\s*['\"](\d+(?:\.\d+)?)['\"]", content)
            if match:
                deployment_target = float(match.group(1))
                break
        except Exception:
            pass

    # Fallback: parse IPHONEOS_DEPLOYMENT_TARGET from .pbxproj (use the lowest value found)
    if deployment_target is None:
        for pbxproj in project_path.rglob("*.pbxproj"):
            if should_exclude(pbxproj, []):
                continue
            try:
                content = pbxproj.read_text(encoding="utf-8", errors="ignore")
                targets = [float(m) for m in re.findall(r"IPHONEOS_DEPLOYMENT_TARGET\s*=\s*(\d+(?:\.\d+)?)", content)]
                if targets:
                    deployment_target = min(targets)
                    break
            except Exception:
                pass

    return {
        "is_swift_only": swift_count > 0 and objc_count == 0,
        "is_mixed": swift_count > 0 and objc_count > 0,
        "is_objc_only": swift_count == 0 and objc_count > 0,
        "swift_files": swift_count,
        "objc_files": objc_count,
        "deployment_target": deployment_target,
    }


def check_architecture(project_path: Path) -> dict:
    """Check for SceneDelegate, sharedInstance, and Info.plist configuration."""
    has_scenedelegate = False
    has_shared_instance = False
    has_scene_manifest = False
    has_compatibility_flag = False

    # Look for SceneDelegate files
    for candidate in project_path.rglob("SceneDelegate.*"):
        if candidate.suffix in {".swift", ".m", ".mm", ".h"}:
            has_scenedelegate = True
            break

    # Look for sharedInstance in AppDelegate
    for appdelegate in project_path.rglob("AppDelegate.*"):
        if appdelegate.suffix in {".swift", ".m", ".mm", ".h"}:
            try:
                content = appdelegate.read_text(encoding="utf-8", errors="ignore")
                if "sharedInstance" in content:
                    has_shared_instance = True
            except Exception:
                pass
            break

    # Look for Info.plist with UIApplicationSceneManifest / UIDesignRequiresCompatibility
    for plist in project_path.rglob("Info.plist"):
        # Exclude Pods/ and build directories explicitly again
        if any(part in DEFAULT_EXCLUDES for part in plist.parts):
            continue
        try:
            content = plist.read_text(encoding="utf-8", errors="ignore")
            if "UIApplicationSceneManifest" in content:
                has_scene_manifest = True
            if "UIDesignRequiresCompatibility" in content:
                has_compatibility_flag = True
            if has_scene_manifest and has_compatibility_flag:
                break
        except Exception:
            pass

    return {
        "has_scenedelegate": has_scenedelegate,
        "has_shared_instance": has_shared_instance,
        "has_scene_manifest": has_scene_manifest,
        "has_compatibility_flag": has_compatibility_flag,
    }


def check_launch_screens(project_path: Path) -> List[ScanIssue]:
    """iOS 27 launch screen mandate: app Info.plist must contain one of the four
    launch-screen keys, or the build must inject one via a generated Info.plist."""
    issues: List[ScanIssue] = []
    for plist in project_path.rglob("Info.plist"):
        if any(part in DEFAULT_EXCLUDES for part in plist.parts):
            continue
        try:
            content = plist.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        # Only audit application plists; extensions/frameworks have no launch screen
        if "CFBundlePackageType" in content and "APPL" not in content:
            continue
        has_launch_key = any(key in content for key in LAUNCH_KEYS)
        if has_launch_key:
            continue
        if "UILaunchImages" in content:
            issues.append(
                ScanIssue(
                    rule_id="LAUNCH-002",
                    severity="warning",
                    message="UILaunchImages is deprecated and does NOT satisfy the iOS 27 launch screen mandate",
                    file=str(plist),
                    line=0,
                    column=0,
                    match="UILaunchImages",
                    suggestion="Replace UILaunchImages with one of the four mandated keys: UILaunchStoryboardName / UILaunchStoryboards / UILaunchScreen / UILaunchScreens",
                )
            )
        # No valid mandate key present — always surface the gap (even alongside LAUNCH-002)
        issues.append(
            ScanIssue(
                rule_id="LAUNCH-001",
                severity="warning",
                message="No launch screen key found in app Info.plist (iOS 27 rejects submissions without one)",
                file=str(plist),
                line=0,
                column=0,
                match="none of " + " / ".join(LAUNCH_KEYS),
                suggestion="Add UILaunchStoryboardName (storyboard) or UILaunchScreen (empty dict is valid). "
                "If Info.plist is generated at build time, see any LAUNCH-003/ARCH-004 notes and verify "
                "with xcodebuild -showBuildSettings",
            )
        )

    # Generated Info.plist projects (Xcode 13+): keys may only exist as build settings
    pbxproj_contents = []
    for pbxproj in project_path.rglob("*.pbxproj"):
        if should_exclude(pbxproj, []):
            continue
        try:
            pbxproj_contents.append(pbxproj.read_text(encoding="utf-8", errors="ignore"))
        except Exception:
            continue
    generated = any("GENERATE_INFOPLIST_FILE = YES" in c for c in pbxproj_contents)
    if generated and any(i.rule_id == "LAUNCH-001" for i in issues):
        launch_build_keys = ("INFOPLIST_KEY_UILaunchScreen_Generation", "INFOPLIST_KEY_UILaunchStoryboardName", "INFOPLIST_KEY_UILaunchScreen")
        if any(k in c for c in pbxproj_contents for k in launch_build_keys):
            # Launch screen is injected at build time — downgrade to an informational note
            issues = [i for i in issues if i.rule_id != "LAUNCH-001"]
            issues.append(
                ScanIssue(
                    rule_id="LAUNCH-003",
                    severity="info",
                    message="Generated Info.plist: launch screen appears to come from build settings",
                    file=str(project_path),
                    line=0,
                    column=0,
                    match="GENERATE_INFOPLIST_FILE = YES",
                    suggestion="Verify with: xcodebuild -showBuildSettings | grep INFOPLIST_KEY_UILaunch",
                )
            )
        else:
            issues.append(
                ScanIssue(
                    rule_id="ARCH-004",
                    severity="info",
                    message="Generated Info.plist detected (GENERATE_INFOPLIST_FILE = YES)",
                    file=str(project_path),
                    line=0,
                    column=0,
                    match="GENERATE_INFOPLIST_FILE = YES",
                    suggestion="Scene manifest and launch screen may live in build settings (INFOPLIST_KEY_*). Verify with xcodebuild -showBuildSettings -configuration Release -sdk iphoneos | grep -E 'INFOPLIST_KEY_UILaunch|SceneManifest'",
                )
            )
    return issues


def check_extensions(project_path: Path) -> List[ScanIssue]:
    """App extensions ship their own binaries and must also build with the new SDK."""
    ext_count = 0
    for plist in project_path.rglob("Info.plist"):
        if any(part in DEFAULT_EXCLUDES for part in plist.parts):
            continue
        try:
            content = plist.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if "NSExtension" in content and "CFBundlePackageType" in content and "APPL" not in content:
            ext_count += 1
    if ext_count == 0:
        return []
    return [
        ScanIssue(
            rule_id="EXT-001",
            severity="info",
            message=f"Detected {ext_count} app extension target(s) (widgets / share / notification, etc.)",
            file=str(project_path),
            line=0,
            column=0,
            match=f"{ext_count} extension Info.plist file(s)",
            suggestion="Lifecycle/window changes apply to the main app only, but every extension is a separate binary: build and test each one with the iOS 26/27 SDK before release",
        )
    ]


def check_third_party_sdks(project_path: Path) -> List[ScanIssue]:
    """Detect dependency manifests and flag SDKs with known iOS 26 constraints."""
    issues: List[ScanIssue] = []
    manifests = []
    for name in ("Podfile.lock", "Package.resolved", "Cartfile.resolved", "Cartfile", "Podfile"):
        for found in project_path.rglob(name):
            if should_exclude(found, []):
                continue
            manifests.append(found)
    if not manifests:
        return issues

    matched = set()
    total_deps = 0
    for manifest in manifests:
        try:
            content = manifest.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for pattern, sdk_name in KNOWN_SDKS:
            if pattern.search(content):
                matched.add(sdk_name)
        if manifest.name == "Podfile.lock":
            pods_block = re.search(r"^PODS:(.*?)(?:^\n[A-Z]|\Z)", content, re.M | re.S)
            if pods_block:
                total_deps += len(re.findall(r"^  - [\"']?\w", pods_block.group(1), re.M))
        elif manifest.name == "Package.resolved":
            total_deps += len(re.findall(r'"identity"\s*:', content))
        elif manifest.name in ("Cartfile.resolved", "Cartfile"):
            total_deps += len(re.findall(r'^\s*(github|git|binary)', content, re.M))

    for sdk_name in sorted(matched):
        issues.append(
            ScanIssue(
                rule_id="SDK-001",
                severity="info",
                message=f"Third-party SDK detected: {sdk_name}",
                file=str(manifests[0]),
                line=0,
                column=0,
                match=sdk_name,
                suggestion=f"Verify {sdk_name} against the minimum compatible version in docs/sdk-compatibility.md and upgrade before the iOS 26 release",
            )
        )
    issues.append(
        ScanIssue(
            rule_id="SDK-002",
            severity="info",
            message=f"Dependency manifest found ({len(manifests)} file(s), ~{total_deps} dependencies detected)",
            file=str(manifests[0]),
            line=0,
            column=0,
            match=", ".join(sorted({m.name for m in manifests})),
            suggestion="Cross-check every third-party dependency against docs/sdk-compatibility.md; outdated SDKs are a top cause of iOS 26 build failures",
        )
    )
    return issues


def scan_project(project_path: Path, extra_excludes: List[str]) -> ScanResult:
    result = ScanResult()
    source_extensions = {".swift", ".m", ".mm"}

    files_to_scan = []
    for filepath in project_path.rglob("*"):
        if not filepath.is_file():
            continue
        if should_exclude(filepath, extra_excludes):
            continue
        if filepath.suffix not in source_extensions:
            continue
        files_to_scan.append(filepath)

    result.total_files_scanned = len(files_to_scan)

    for filepath in files_to_scan:
        file_issues = scan_file(filepath, RULES)
        result.issues.extend(file_issues)

    result.architecture = check_architecture(project_path)
    project_type = detect_project_type(project_path)
    result.architecture.update(project_type)

    # Check for Privacy Manifest
    has_privacy_manifest = False
    for privacy_file in project_path.rglob("PrivacyInfo.xcprivacy"):
        if any(part in DEFAULT_EXCLUDES for part in privacy_file.parts):
            continue
        has_privacy_manifest = True
        break

    if not has_privacy_manifest:
        result.issues.append(
            ScanIssue(
                rule_id="PRIVACY-001",
                severity="error",
                message="Missing Privacy Manifest (PrivacyInfo.xcprivacy)",
                file=str(project_path),
                line=0,
                column=0,
                match="PrivacyInfo.xcprivacy not found",
                suggestion="Create PrivacyInfo.xcprivacy and declare Required Reason APIs and data collection practices",
            )
        )

    # Phase 2 reminder: UIDesignRequiresCompatibility is temporary and will be
    # ignored/rejected starting with Xcode 27 (~2026-09)
    if result.architecture.get("has_compatibility_flag"):
        result.issues.append(
            ScanIssue(
                rule_id="PHASE2-001",
                severity="info",
                message="UIDesignRequiresCompatibility flag present — Phase 2 (Liquid Glass) pending",
                file=str(project_path),
                line=0,
                column=0,
                match="UIDesignRequiresCompatibility found in Info.plist",
                suggestion="Plan Phase 2: remove the flag and complete Liquid Glass adaptation before Xcode 27 (~2026-09)",
            )
        )

    # iOS 27 build-chain check: -ld_classic is removed in Xcode 27 (build fails)
    config_files = list(project_path.rglob("*.xcconfig")) + list(project_path.rglob("*.pbxproj")) + list(project_path.rglob("Podfile"))
    for config_file in config_files:
        if should_exclude(config_file, extra_excludes):
            continue
        try:
            content = config_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for line_no, line in enumerate(content.splitlines(), start=1):
            if "ld_classic" in line:
                result.issues.append(
                    ScanIssue(
                        rule_id="LINKER-001",
                        severity="warning",
                        message="-ld_classic linker flag (removed in Xcode 27)",
                        file=str(config_file),
                        line=line_no,
                        column=line.find("ld_classic") + 1,
                        match="ld_classic",
                        suggestion="ld64 is fully removed in Xcode 27 and -ld_classic causes a build failure. Remove the flag and upgrade third-party libraries that depend on the classic linker.",
                    )
                )

    # iOS 27 check: LSApplicationQueriesSchemes limit drops from 50 to 25 entries
    # for apps linked against the iOS 27 SDK
    for plist in project_path.rglob("Info.plist"):
        if any(part in DEFAULT_EXCLUDES for part in plist.parts):
            continue
        try:
            content = plist.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        schemes_block = re.search(
            r"<key>LSApplicationQueriesSchemes</key>\s*<array>(.*?)</array>", content, re.DOTALL
        )
        if schemes_block:
            scheme_count = len(re.findall(r"<string>", schemes_block.group(1)))
            if scheme_count > 25:
                result.issues.append(
                    ScanIssue(
                        rule_id="OPENURL-002",
                        severity="warning",
                        message=f"LSApplicationQueriesSchemes has {scheme_count} entries (iOS 27 limit: 25)",
                        file=str(plist),
                        line=0,
                        column=0,
                        match=f"{scheme_count} scheme entries",
                        suggestion="Apps linked on or after the iOS 27 SDK are limited to 25 LSApplicationQueriesSchemes entries (down from 50); excess schemes silently return false. Trim the list or migrate to attempt-and-handle with open(_:options:completionHandler:).",
                    )
                )

    # Determine severity for architecture issues based on project type
    # For pure Swift iOS 13+ projects without SceneDelegate: downgrade to warning
    # because backward compatibility is still supported (though iOS 27 will require it)
    # NOTE: deployment_target may be None when no Podfile/pbxproj declares it — guard with `or 0`
    arch_severity = "error"
    if result.architecture.get("is_swift_only") and (result.architecture.get("deployment_target") or 0) >= 13.0:
        arch_severity = "warning"

    # Zero-omission project-level checks: launch screen mandate, extensions, third-party SDKs
    result.issues.extend(check_launch_screens(project_path))
    result.issues.extend(check_extensions(project_path))
    result.issues.extend(check_third_party_sdks(project_path))

    # Add architecture infos
    if not result.architecture["has_scenedelegate"]:
        result.issues.append(
            ScanIssue(
                rule_id="ARCH-001",
                severity=arch_severity,
                message="Missing SceneDelegate file",
                file=str(project_path),
                line=0,
                column=0,
                match="SceneDelegate.swift/m not found",
                suggestion="Create SceneDelegate and configure UIApplicationSceneManifest in Info.plist (mandatory for iOS 27)",
            )
        )
    if not result.architecture["has_scene_manifest"]:
        result.issues.append(
            ScanIssue(
                rule_id="ARCH-002",
                severity=arch_severity,
                message="Missing UIApplicationSceneManifest in Info.plist",
                file=str(project_path),
                line=0,
                column=0,
                match="UIApplicationSceneManifest not found in any Info.plist",
                suggestion="Add UIApplicationSceneManifest configuration to Info.plist (mandatory for iOS 27)",
            )
        )
    if not result.architecture["has_shared_instance"]:
        result.issues.append(
            ScanIssue(
                rule_id="ARCH-003",
                severity="warning",
                message="AppDelegate may be missing sharedInstance method",
                file=str(project_path),
                line=0,
                column=0,
                match="sharedInstance not found in AppDelegate",
                suggestion="Add a sharedInstance class method to AppDelegate for SceneDelegate forwarding (Swift projects can use static let shared)",
            )
        )

    result.total_issues = len(result.issues)
    result.errors = sum(1 for i in result.issues if i.severity == "error")
    result.warnings = sum(1 for i in result.issues if i.severity == "warning")
    result.infos = sum(1 for i in result.issues if i.severity == "info")
    return result


def format_markdown(result: ScanResult, project_path: Path) -> str:
    lines = []
    lines.append("# iOS 26 Adaptation Scan Report")
    lines.append("")
    lines.append(f"**Project Path:** `{project_path}`")
    lines.append(f"**Files Scanned:** {result.total_files_scanned}")
    lines.append(f"**Total Issues:** {result.total_issues}  (Errors: {result.errors}, Warnings: {result.warnings}, Info: {result.infos})")
    lines.append("")

    lines.append("## Architecture Check")
    for key, value in result.architecture.items():
        icon = "✅" if value else "❌"
        lines.append(f"- {icon} `{key}`: {'Yes' if value else 'No'}")
    lines.append("")

    if result.issues:
        lines.append("## Issues")
        lines.append("")
        lines.append("| Rule ID | Severity | File | Line | Message | Suggestion |")
        lines.append("|---------|----------|------|------|---------|------------|")
        for issue in sorted(result.issues, key=lambda i: (i.severity != "error", i.severity != "warning", i.file, i.line)):
            file_display = issue.file.replace(str(project_path), ".")
            lines.append(
                f"| {issue.rule_id} | {issue.severity.upper()} | `{file_display}` | {issue.line} | {issue.message} | {issue.suggestion} |"
            )
        lines.append("")
    else:
        lines.append("✅ No issues found. Project appears ready for iOS 26 SDK build.")
        lines.append("")

    lines.append("## Quick Actions")
    lines.append("- [ ] Review all ERROR items immediately")
    lines.append("- [ ] Plan global replacement for WARNING items")
    lines.append("- [ ] Verify third-party SDK compatibility")
    lines.append("- [ ] Run build with Xcode 26 after fixes")
    lines.append("")

    lines.append("## Manual Audit Checklist (cannot be auto-detected)")
    lines.append("Items below are part of the coverage ledger (`scripts/adaptation-ledger.json`) but require human review. Check each one before release:")
    lines.append("- [ ] P2-06 Hardcoded bottom padding vs floating TabBar safe area (`additionalSafeAreaInsets`)")
    lines.append("- [ ] P2-07 `UIScrollView.allowsLiquidTransform` edge-scroll distortion")
    lines.append("- [ ] P2-08 View-traversal assumptions broken by auto-inserted `UIDropShadowView`")
    lines.append("- [ ] P2-09 Custom transition completion blocks are idempotent (iOS 26 allows interruption)")
    lines.append("- [ ] P3-04 Duplicate Clang `module.modulemap` names (Xcode 27 de-duplication)")
    lines.append("- [ ] P3-08 URL-encoding workarounds vs NSURL double-encoding fix")
    lines.append("- [ ] P3-09 C++ `multimap/multiset::find()` reliance on first-equal element")
    lines.append("- [ ] P3-10 Custom `stat()` extensions vs System framework `FilePath.stat()`")
    lines.append("- [ ] P3-11 `idiom`/`orientation` layout checks → size classes")
    lines.append("- [ ] ENV-01/ENV-02 Xcode & macOS versions meet the target phase requirements")
    lines.append("")

    lines.append("## Completion Gate (Ship-Ready Definition of Done)")
    lines.append("The adaptation is complete only when ALL of the following hold:")
    lines.append("- [ ] SHIP-01 This scan reports **0 errors**")
    lines.append("- [ ] SHIP-02 Every warning is fixed or has a recorded exemption reason")
    lines.append("- [ ] SHIP-03 Manual Audit Checklist above fully checked")
    lines.append("- [ ] SHIP-04 Test matrix passed: minimum iOS version + iOS 13+ + iOS 26 device (see docs/testing-guide.md)")
    lines.append("- [ ] SHIP-05 Low-impact boundary confirmed: Deployment Target unchanged, `git diff` contains only iOS 26/27 adaptation files")
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Scan an iOS project for iOS 26 SDK adaptation issues."
    )
    parser.add_argument("project_path", help="Path to the iOS project directory")
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Write output to file instead of stdout",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Additional directory names to exclude (can be used multiple times)",
    )
    args = parser.parse_args()

    project_path = Path(args.project_path).expanduser().resolve()
    if not project_path.exists():
        print(f"Error: Path does not exist: {project_path}", file=sys.stderr)
        sys.exit(1)
    if not project_path.is_dir():
        print(f"Error: Path is not a directory: {project_path}", file=sys.stderr)
        sys.exit(1)

    result = scan_project(project_path, args.exclude)

    if args.format == "json":
        output = json.dumps(
            {
                "scan_metadata": {
                    "project_path": str(project_path),
                    "total_files_scanned": result.total_files_scanned,
                },
                "architecture_analysis": result.architecture,
                "issues": [asdict(i) for i in result.issues],
                "statistics": {
                    "total_issues": result.total_issues,
                    "errors": result.errors,
                    "warnings": result.warnings,
                    "infos": result.infos,
                },
                "completion_gate": [
                    "SHIP-01: scan reports 0 errors",
                    "SHIP-02: every warning fixed or exempted with reason",
                    "SHIP-03: manual audit checklist fully checked",
                    "SHIP-04: test matrix passed (minimum iOS + iOS 13+ + iOS 26 device)",
                    "SHIP-05: low-impact boundary confirmed (Deployment Target unchanged, no out-of-scope diff)",
                ],
            },
            indent=2,
            ensure_ascii=False,
        )
    else:
        output = format_markdown(result, project_path)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Report written to: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
