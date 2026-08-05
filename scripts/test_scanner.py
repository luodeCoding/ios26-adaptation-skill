#!/usr/bin/env python3
"""
Unit tests for ios26-scanner.py

Run: python3 scripts/test_scanner.py
"""

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

# Load scanner module whose filename contains a hyphen
_spec = importlib.util.spec_from_file_location("ios26_scanner", Path(__file__).parent / "ios26-scanner.py")
_scanner = importlib.util.module_from_spec(_spec)
sys.modules["ios26_scanner"] = _scanner
_spec.loader.exec_module(_scanner)

scan_file = _scanner.scan_file
scan_project = _scanner.scan_project
check_architecture = _scanner.check_architecture
check_launch_screens = _scanner.check_launch_screens
check_extensions = _scanner.check_extensions
check_third_party_sdks = _scanner.check_third_party_sdks
ScanIssue = _scanner.ScanIssue
RULES = _scanner.RULES
PROJECT_RULE_IDS = _scanner.PROJECT_RULE_IDS


class TestScannerRules(unittest.TestCase):
    """Test individual scanner rules against known patterns."""

    def _make_file(self, content: str, suffix: str = ".swift") -> Path:
        """Create a temporary file with given content."""
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=suffix, delete=False)
        tmp.write(content)
        tmp.close()
        return Path(tmp.name)

    # --- Window Rules ---

    def test_window_001_keywindow_swift(self):
        f = self._make_file("let w = UIApplication.shared.keyWindow")
        issues = scan_file(f, [r for r in RULES if r["id"] == "WINDOW-001"])
        f.unlink()
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].rule_id, "WINDOW-001")

    def test_window_003_delegate_window(self):
        f = self._make_file("let w = someobj.delegate.window")
        issues = scan_file(f, [
            r for r in __import__("ios26_scanner").RULES if r["id"] == "WINDOW-003"
        ])
        f.unlink()
        self.assertEqual(len(issues), 1)

    # --- Window Rules (new in v1.8) ---

    def test_window_007_shared_windows_swift(self):
        f = self._make_file("let w = UIApplication.shared.windows.first")
        issues = scan_file(f, [r for r in RULES if r["id"] == "WINDOW-007"])
        f.unlink()
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].severity, "warning")

    def test_window_008_shared_windows_oc(self):
        f = self._make_file("UIWindow *w = [UIApplication sharedApplication].windows.firstObject;", ".m")
        issues = scan_file(f, [r for r in RULES if r["id"] == "WINDOW-008"])
        f.unlink()
        self.assertEqual(len(issues), 1)

    def test_window_003_skips_mainwindow_template_fallback(self):
        """UIApplication+MainWindow template's iOS 12 fallback should not be flagged."""
        with tempfile.TemporaryDirectory() as tmpdir:
            f = Path(tmpdir) / "UIApplication+MainWindow.swift"
            f.write_text("return delegate?.window ?? nil")
            issues = scan_file(f, [r for r in RULES if r["id"] == "WINDOW-003"])
            self.assertEqual(len(issues), 0)

    # --- Screen Rules (new in v1.3) ---

    def test_screen_001_uiscreen_main_swift(self):
        f = self._make_file("let frame = UIScreen.main.bounds")
        issues = scan_file(f, [
            r for r in __import__("ios26_scanner").RULES if r["id"] == "SCREEN-001"
        ])
        f.unlink()
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].rule_id, "SCREEN-001")

    def test_screen_002_uiscreen_mainscreen_oc(self):
        f = self._make_file("CGRect frame = [[UIScreen mainScreen] bounds];", ".m")
        issues = scan_file(f, [
            r for r in __import__("ios26_scanner").RULES if r["id"] == "SCREEN-002"
        ])
        f.unlink()
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].rule_id, "SCREEN-002")

    def test_screen_skips_ios12_fallback_comment(self):
        f = self._make_file("let frame = UIScreen.main.bounds // iOS 12 fallback path")
        issues = scan_file(f, [
            r for r in __import__("ios26_scanner").RULES if r["id"] == "SCREEN-001"
        ])
        f.unlink()
        self.assertEqual(len(issues), 0)

    # --- Notification Rules ---

    def test_notif_001_presentation_option_alert(self):
        f = self._make_file("options = UNNotificationPresentationOptionAlert")
        issues = scan_file(f, [
            r for r in __import__("ios26_scanner").RULES if r["id"] == "NOTIF-001"
        ])
        f.unlink()
        self.assertEqual(len(issues), 1)

    # --- WebView Rule (new in v1.3) ---

    def test_web_001_uiwebview(self):
        f = self._make_file("let webView = UIWebView()")
        issues = scan_file(f, [
            r for r in __import__("ios26_scanner").RULES if r["id"] == "WEB-001"
        ])
        f.unlink()
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].severity, "error")

    # --- TLS Rule (new in v1.3) ---

    def test_tls_001_legacy_tls(self):
        f = self._make_file("config.tlsMinimumSupportedProtocolVersion = .TLSv10")
        issues = scan_file(f, [
            r for r in __import__("ios26_scanner").RULES if r["id"] == "TLS-001"
        ])
        f.unlink()
        self.assertEqual(len(issues), 1)

    # --- CoreData Rule (new in v1.3) ---

    def test_coredata_001_ubiquitous_key(self):
        f = self._make_file('options[NSPersistentStoreUbiquitousContentNameKey] = "MyStore"')
        issues = scan_file(f, [
            r for r in __import__("ios26_scanner").RULES if r["id"] == "COREDATA-001"
        ])
        f.unlink()
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].severity, "error")

    # --- StoreKit Rule (new in v1.4) ---

    def test_storekit_001_skpaymenttransaction(self):
        f = self._make_file("let tx: SKPaymentTransaction")
        issues = scan_file(f, [
            r for r in __import__("ios26_scanner").RULES if r["id"] == "STOREKIT-001"
        ])
        f.unlink()
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].severity, "error")

    # --- SiriKit Rule (new in v1.4) ---

    def test_sirikit_001_deprecated_intent(self):
        f = self._make_file("class Intent: INSearchForPhotosIntent {}")
        issues = scan_file(f, [
            r for r in __import__("ios26_scanner").RULES if r["id"] == "SIRIKIT-001"
        ])
        f.unlink()
        self.assertEqual(len(issues), 1)

    # --- SwiftUI Rules (new in v1.4) ---

    def test_swiftui_001_navigationview(self):
        f = self._make_file("NavigationView { ContentView() }")
        issues = scan_file(f, [
            r for r in __import__("ios26_scanner").RULES if r["id"] == "SWIFTUI-001"
        ])
        f.unlink()
        self.assertEqual(len(issues), 1)

    def test_swiftui_002_corner_radius(self):
        f = self._make_file(".cornerRadius(8)")
        issues = scan_file(f, [
            r for r in __import__("ios26_scanner").RULES if r["id"] == "SWIFTUI-002"
        ])
        f.unlink()
        self.assertEqual(len(issues), 1)

    def test_swiftui_003_foreground_color(self):
        f = self._make_file(".foregroundColor(.red)")
        issues = scan_file(f, [
            r for r in __import__("ios26_scanner").RULES if r["id"] == "SWIFTUI-003"
        ])
        f.unlink()
        self.assertEqual(len(issues), 1)

    # --- Photos Rule (new in v1.4) ---

    def test_photos_001_uiimagepicker(self):
        f = self._make_file("let picker = UIImagePickerController()")
        issues = scan_file(f, [
            r for r in __import__("ios26_scanner").RULES if r["id"] == "PHOTOS-001"
        ])
        f.unlink()
        self.assertEqual(len(issues), 1)

    # --- Keyboard Rules (new in unreleased) ---

    def test_keyboard_001_custom_textfield_swift(self):
        f = self._make_file("class MyTextField: UITextField {}")
        issues = scan_file(f, [
            r for r in __import__("ios26_scanner").RULES if r["id"] == "KEYBOARD-001"
        ])
        f.unlink()
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].severity, "info")

    def test_keyboard_001_custom_textfield_oc(self):
        f = self._make_file("@interface MyTextField : UITextField\n@end", ".h")
        issues = scan_file(f, [
            r for r in __import__("ios26_scanner").RULES if r["id"] == "KEYBOARD-001"
        ])
        f.unlink()
        self.assertEqual(len(issues), 1)

    def test_keyboard_002_custom_textview_swift(self):
        f = self._make_file("class MyTextView: UITextView {}")
        issues = scan_file(f, [
            r for r in __import__("ios26_scanner").RULES if r["id"] == "KEYBOARD-002"
        ])
        f.unlink()
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].severity, "info")

    def test_keyboard_003_input_accessory_view(self):
        f = self._make_file("textField.inputAccessoryView = myToolbar")
        issues = scan_file(f, [
            r for r in __import__("ios26_scanner").RULES if r["id"] == "KEYBOARD-003"
        ])
        f.unlink()
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].severity, "info")

    # --- Status Bar Rule (new in v1.8) ---

    def test_status_004_statusbarframe(self):
        f = self._make_file("let h = UIApplication.shared.statusBarFrame.height")
        issues = scan_file(f, [r for r in RULES if r["id"] == "STATUS-004"])
        f.unlink()
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].severity, "warning")

    def test_status_004_skips_statusbarmanager(self):
        """Modern statusBarManager.statusBarFrame replacement should not be flagged."""
        f = self._make_file("let h = windowScene.statusBarManager?.statusBarFrame.height")
        issues = scan_file(f, [r for r in RULES if r["id"] == "STATUS-004"])
        f.unlink()
        self.assertEqual(len(issues), 0)

    # --- iOS 26 runtime pitfall rules (new in v1.9) ---

    def test_tabbar_001_kvc_override_oc(self):
        f = self._make_file('[self setValue:customTabBar forKey:@"tabBar"];', ".m")
        issues = scan_file(f, [r for r in RULES if r["id"] == "TABBAR-001"])
        f.unlink()
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].severity, "error")

    def test_tabbar_001_kvc_override_swift(self):
        f = self._make_file('setValue(customTabBar, forKey: "tabBar")')
        issues = scan_file(f, [r for r in RULES if r["id"] == "TABBAR-001"])
        f.unlink()
        self.assertEqual(len(issues), 1)

    def test_navbar_001_addsubview_oc(self):
        f = self._make_file("[self.navigationController.navigationBar addSubview:badge];", ".m")
        issues = scan_file(f, [r for r in RULES if r["id"] == "NAVBAR-001"])
        f.unlink()
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].severity, "warning")

    def test_navbar_001_addsubview_swift(self):
        f = self._make_file("navigationController?.navigationBar.addSubview(badge)")
        issues = scan_file(f, [r for r in RULES if r["id"] == "NAVBAR-001"])
        f.unlink()
        self.assertEqual(len(issues), 1)

    def test_barbutton_001_rightbarbuttonitems(self):
        f = self._make_file("navigationItem.rightBarButtonItems = [shareItem, editItem]")
        issues = scan_file(f, [r for r in RULES if r["id"] == "BARBUTTON-001"])
        f.unlink()
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].severity, "info")

    # --- iOS 27 forward-looking rules (new in v1.9) ---

    def test_openurl_001_canopenurl(self):
        f = self._make_file("if UIApplication.shared.canOpenURL(url) { }")
        issues = scan_file(f, [r for r in RULES if r["id"] == "OPENURL-001"])
        f.unlink()
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].severity, "info")

    def test_openurl_001_skips_comment(self):
        f = self._make_file("// canOpenURL is deprecated in iOS 27")
        issues = scan_file(f, [r for r in RULES if r["id"] == "OPENURL-001"])
        f.unlink()
        self.assertEqual(len(issues), 0)

    def test_odr_001_bundle_resource_request(self):
        f = self._make_file("let request = NSBundleResourceRequest(tags: tags)")
        issues = scan_file(f, [r for r in RULES if r["id"] == "ODR-001"])
        f.unlink()
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].severity, "warning")

    def test_metrickit_001_mxmetricmanager(self):
        f = self._make_file("MXMetricManager.shared.add(self)")
        issues = scan_file(f, [r for r in RULES if r["id"] == "METRICKIT-001"])
        f.unlink()
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].severity, "warning")

    # --- False Positive Tests ---

    def test_notif_002_removed_no_longer_flags(self):
        """UNAuthorizationOptionAlert should NOT be flagged (removed in v1.2)."""
        f = self._make_file("options = UNAuthorizationOptionAlert")
        all_issues = scan_file(f, __import__("ios26_scanner").RULES)
        f.unlink()
        notif_issues = [i for i in all_issues if "UNAuthorizationOptionAlert" in i.match]
        self.assertEqual(len(notif_issues), 0)

    # --- AssetsLibrary Rules (new in v1.7) ---

    def test_assetslibrary_001_swift_import(self):
        f = self._make_file("import AssetsLibrary\nclass Foo {}")
        issues = scan_file(f, [
            r for r in __import__("ios26_scanner").RULES if r["id"] == "ASSETSLIBRARY-001"
        ])
        f.unlink()
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].severity, "error")

    def test_assetslibrary_002_oc_import(self):
        f = self._make_file('#import <AssetsLibrary/AssetsLibrary.h>\n@interface Foo @end', ".m")
        issues = scan_file(f, [
            r for r in __import__("ios26_scanner").RULES if r["id"] == "ASSETSLIBRARY-002"
        ])
        f.unlink()
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].severity, "error")

    def test_assetslibrary_003_alassetslibrary_usage(self):
        f = self._make_file("let lib = ALAssetsLibrary()")
        issues = scan_file(f, [
            r for r in __import__("ios26_scanner").RULES if r["id"] == "ASSETSLIBRARY-003"
        ])
        f.unlink()
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].severity, "error")

    # --- SCREEN false positive: Pods/Vender skip (new in v1.7) ---

    def test_screen_skips_pods_directory(self):
        f = self._make_file("let frame = UIScreen.main.bounds")
        # Manually rename to simulate Pods path
        pods_path = f.parent / "Pods" / "SomeLib" / "File.swift"
        pods_path.parent.mkdir(parents=True, exist_ok=True)
        f.rename(pods_path)
        issues = scan_file(pods_path, [
            r for r in __import__("ios26_scanner").RULES if r["id"] == "SCREEN-001"
        ])
        # _should_skip_issue now filters out SCREEN issues in Pods/Vender/ThirdParty directories
        pods_path.unlink()
        self.assertEqual(len(issues), 0)


class TestArchitectureCheck(unittest.TestCase):
    """Test project-level architecture checks."""

    def test_missing_scenedelegate(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project = Path(tmpdir)
            # Create Info.plist without scene manifest
            (project / "Info.plist").write_text("<plist></plist>")
            arch = check_architecture(project)
            self.assertFalse(arch["has_scenedelegate"])
            self.assertFalse(arch["has_scene_manifest"])

    def test_has_scenedelegate(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project = Path(tmpdir)
            (project / "SceneDelegate.swift").write_text("class SceneDelegate {}")
            (project / "Info.plist").write_text("<plist>UIApplicationSceneManifest</plist>")
            arch = check_architecture(project)
            self.assertTrue(arch["has_scenedelegate"])
            self.assertTrue(arch["has_scene_manifest"])

    def test_compatibility_flag_detected(self):
        """UIDesignRequiresCompatibility in Info.plist should be reported (new in v1.8)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project = Path(tmpdir)
            (project / "Info.plist").write_text(
                "<plist>UIApplicationSceneManifest UIDesignRequiresCompatibility</plist>"
            )
            arch = check_architecture(project)
            self.assertTrue(arch["has_compatibility_flag"])
            result = scan_project(project, [])
            rule_ids = {i.rule_id for i in result.issues}
            self.assertIn("PHASE2-001", rule_ids)

    def test_deployment_target_from_pbxproj(self):
        """Deployment target should fall back to .pbxproj parsing (new in v1.8)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project = Path(tmpdir)
            pbx_dir = project / "MyApp.xcodeproj"
            pbx_dir.mkdir()
            (pbx_dir / "project.pbxproj").write_text(
                "IPHONEOS_DEPLOYMENT_TARGET = 13.0;\nIPHONEOS_DEPLOYMENT_TARGET = 15.0;"
            )
            info = _scanner.detect_project_type(project)
            self.assertEqual(info["deployment_target"], 13.0)

    def test_swift_only_without_deployment_target_no_crash(self):
        """Regression: swift-only project with no Podfile/pbxproj must not raise TypeError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project = Path(tmpdir)
            (project / "Main.swift").write_text("let x = 1")
            result = scan_project(project, [])  # must not raise
            self.assertTrue(result.architecture["is_swift_only"])
            self.assertIsNone(result.architecture["deployment_target"])

    def test_linker_001_ld_classic_in_xcconfig(self):
        """-ld_classic in build configs should be flagged (removed in Xcode 27, new in v1.9)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project = Path(tmpdir)
            (project / "Release.xcconfig").write_text(
                'OTHER_LDFLAGS = $(inherited) -Wl,-ld_classic\n'
            )
            result = scan_project(project, [])
            linker_issues = [i for i in result.issues if i.rule_id == "LINKER-001"]
            self.assertEqual(len(linker_issues), 1)
            self.assertEqual(linker_issues[0].line, 1)

    def test_openurl_002_scheme_limit_exceeded(self):
        """LSApplicationQueriesSchemes > 25 entries should warn (iOS 27 limit, new in v1.9)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project = Path(tmpdir)
            schemes = "".join(f"<string>scheme{i}</string>" for i in range(30))
            (project / "Info.plist").write_text(
                f"<plist><key>LSApplicationQueriesSchemes</key><array>{schemes}</array></plist>"
            )
            result = scan_project(project, [])
            openurl_issues = [i for i in result.issues if i.rule_id == "OPENURL-002"]
            self.assertEqual(len(openurl_issues), 1)
            self.assertIn("30", openurl_issues[0].message)

    def test_openurl_002_within_limit_not_flagged(self):
        """25 or fewer scheme entries should not be flagged."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project = Path(tmpdir)
            schemes = "".join(f"<string>scheme{i}</string>" for i in range(25))
            (project / "Info.plist").write_text(
                f"<plist><key>LSApplicationQueriesSchemes</key><array>{schemes}</array></plist>"
            )
            result = scan_project(project, [])
            openurl_issues = [i for i in result.issues if i.rule_id == "OPENURL-002"]
            self.assertEqual(len(openurl_issues), 0)


class TestFullProjectScan(unittest.TestCase):
    """Test scanning a mock project directory."""

    def test_scan_mock_project(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project = Path(tmpdir)
            # Create source files with various issues
            (project / "ViewController.swift").write_text(
                'let w = UIApplication.shared.keyWindow\n'
                'let s = UIScreen.main.bounds\n'
            )
            (project / "OldWebView.m").write_text(
                "UIWebView *webView = [[UIWebView alloc] init];\n"
            )
            (project / "Info.plist").write_text("<plist>UIApplicationSceneManifest</plist>")
            (project / "SceneDelegate.swift").write_text("class SceneDelegate {}")
            (project / "AppDelegate.swift").write_text(
                "class AppDelegate { static func sharedInstance() -> AppDelegate? { nil } }"
            )

            result = scan_project(project, [])

            self.assertGreaterEqual(result.total_files_scanned, 3)
            self.assertGreaterEqual(result.errors, 1)  # UIWebView
            self.assertGreaterEqual(result.warnings, 1)  # UIScreen.main

            rule_ids = {i.rule_id for i in result.issues}
            self.assertIn("WINDOW-001", rule_ids)
            self.assertIn("SCREEN-001", rule_ids)
            self.assertIn("WEB-001", rule_ids)


class TestLaunchScreenChecks(unittest.TestCase):
    """iOS 27 launch screen mandate checks (LAUNCH-001/002/003, ARCH-004)."""

    APP_PLIST_NO_LAUNCH = (
        "<plist><dict><key>CFBundlePackageType</key><string>APPL</string></dict></plist>"
    )

    def test_launch_001_missing_key(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "Info.plist").write_text(self.APP_PLIST_NO_LAUNCH)
            issues = check_launch_screens(Path(tmpdir))
            self.assertIn("LAUNCH-001", [i.rule_id for i in issues])

    def test_launch_ok_with_key(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "Info.plist").write_text(
                "<plist><dict><key>CFBundlePackageType</key><string>APPL</string>"
                "<key>UILaunchScreen</key><dict/></dict></plist>"
            )
            issues = check_launch_screens(Path(tmpdir))
            self.assertNotIn("LAUNCH-001", [i.rule_id for i in issues])

    def test_launch_002_deprecated_uilaunchimages(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "Info.plist").write_text(
                "<plist><dict><key>CFBundlePackageType</key><string>APPL</string>"
                "<key>UILaunchImages</key><array/></dict></plist>"
            )
            issues = check_launch_screens(Path(tmpdir))
            rule_ids = [i.rule_id for i in issues]
            self.assertIn("LAUNCH-002", rule_ids)
            self.assertIn("LAUNCH-001", rule_ids)  # UILaunchImages does not satisfy the mandate

    def test_launch_003_generated_plist_with_build_key(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "Info.plist").write_text(self.APP_PLIST_NO_LAUNCH)
            (Path(tmpdir) / "App.xcodeproj").mkdir()
            (Path(tmpdir) / "App.xcodeproj" / "project.pbxproj").write_text(
                "GENERATE_INFOPLIST_FILE = YES;\nINFOPLIST_KEY_UILaunchScreen_Generation = YES;"
            )
            issues = check_launch_screens(Path(tmpdir))
            rule_ids = [i.rule_id for i in issues]
            self.assertIn("LAUNCH-003", rule_ids)
            self.assertNotIn("LAUNCH-001", rule_ids)

    def test_arch_004_generated_plist_without_launch_key(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "Info.plist").write_text(self.APP_PLIST_NO_LAUNCH)
            (Path(tmpdir) / "App.xcodeproj").mkdir()
            (Path(tmpdir) / "App.xcodeproj" / "project.pbxproj").write_text(
                "GENERATE_INFOPLIST_FILE = YES;"
            )
            issues = check_launch_screens(Path(tmpdir))
            rule_ids = [i.rule_id for i in issues]
            self.assertIn("LAUNCH-001", rule_ids)
            self.assertIn("ARCH-004", rule_ids)

    def test_extension_plist_not_audited_for_launch(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "Info.plist").write_text(
                "<plist><dict><key>CFBundlePackageType</key><string>XPC!</string>"
                "<key>NSExtension</key><dict/></dict></plist>"
            )
            issues = check_launch_screens(Path(tmpdir))
            self.assertEqual(issues, [])


class TestExtensionAndSDKChecks(unittest.TestCase):
    """Multi-target (EXT-001) and third-party SDK (SDK-001/002) checks."""

    def test_ext_001_extension_target_detected(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            widget = Path(tmpdir) / "Widget"
            widget.mkdir()
            (widget / "Info.plist").write_text(
                "<plist><dict><key>CFBundlePackageType</key><string>XPC!</string>"
                "<key>NSExtension</key><dict><key>NSExtensionPointIdentifier</key>"
                "<string>com.apple.widgetkit-extension</string></dict></dict></plist>"
            )
            issues = check_extensions(Path(tmpdir))
            self.assertEqual([i.rule_id for i in issues], ["EXT-001"])

    def test_sdk_001_known_sdks_and_manifest(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "Podfile.lock").write_text(
                "PODS:\n  - FBSDKCoreKit (18.2.0)\n  - Firebase/Analytics (11.0.0)\n  - Alamofire (5.9.0)\n"
            )
            issues = check_third_party_sdks(Path(tmpdir))
            rule_ids = [i.rule_id for i in issues]
            self.assertEqual(rule_ids.count("SDK-001"), 2)  # Facebook + Firebase
            self.assertIn("SDK-002", rule_ids)

    def test_sdk_no_manifest_no_issue(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            issues = check_third_party_sdks(Path(tmpdir))
            self.assertEqual(issues, [])


class TestCoverageLedgerConsistency(unittest.TestCase):
    """The coverage ledger is the zero-omission source of truth: every auto-detected
    item must reference scanner rule IDs that actually exist."""

    def test_ledger_auto_rule_ids_exist_in_scanner(self):
        import json

        ledger_path = Path(__file__).parent / "adaptation-ledger.json"
        self.assertTrue(ledger_path.exists(), "adaptation-ledger.json must exist")
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))

        scanner_rule_ids = {r["id"] for r in RULES} | PROJECT_RULE_IDS
        items = ledger["items"]
        self.assertGreaterEqual(len(items), 40, "ledger must cover all adaptation items")

        auto_items = [i for i in items if i["detection"] == "auto"]
        self.assertGreaterEqual(len(auto_items), 25, "most items must be auto-detected")

        missing = []
        for item in auto_items:
            for rule_id in item["rule_ids"]:
                if rule_id not in scanner_rule_ids:
                    missing.append((item["id"], rule_id))
        self.assertEqual(missing, [], f"Ledger references non-existent scanner rules: {missing}")

    def test_ledger_covers_all_three_phases_and_ship_gate(self):
        import json

        ledger = json.loads((Path(__file__).parent / "adaptation-ledger.json").read_text(encoding="utf-8"))
        phases = {i["phase"] for i in ledger["items"]}
        self.assertIn(1, phases)
        self.assertIn(2, phases)
        self.assertIn(3, phases)
        self.assertIn(0, phases)  # SHIP-* completion gate items


if __name__ == "__main__":
    unittest.main(verbosity=2)
