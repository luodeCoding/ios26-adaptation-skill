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
ScanIssue = _scanner.ScanIssue
RULES = _scanner.RULES


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

    # --- False Positive Tests ---

    def test_notif_002_removed_no_longer_flags(self):
        """UNAuthorizationOptionAlert should NOT be flagged (removed in v1.2)."""
        f = self._make_file("options = UNAuthorizationOptionAlert")
        all_issues = scan_file(f, __import__("ios26_scanner").RULES)
        f.unlink()
        notif_issues = [i for i in all_issues if "UNAuthorizationOptionAlert" in i.match]
        self.assertEqual(len(notif_issues), 0)


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


if __name__ == "__main__":
    unittest.main(verbosity=2)
