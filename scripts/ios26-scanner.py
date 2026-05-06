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
import os
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import List, Optional


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
    # UIApplication+Extension files legitimately access delegate.window as iOS 12 fallback
    if rule_id == "WINDOW-003" and "UIApplication+Extension" in str(filepath):
        if "self.delegate.window" in line or ("delegate.window" in line and "return" in line):
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


def check_architecture(project_path: Path) -> dict:
    """Check for SceneDelegate, sharedInstance, and Info.plist configuration."""
    has_scenedelegate = False
    has_shared_instance = False
    has_scene_manifest = False

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

    # Look for Info.plist with UIApplicationSceneManifest
    for plist in project_path.rglob("Info.plist"):
        # Exclude Pods/ and build directories explicitly again
        if any(part in DEFAULT_EXCLUDES for part in plist.parts):
            continue
        try:
            content = plist.read_text(encoding="utf-8", errors="ignore")
            if "UIApplicationSceneManifest" in content:
                has_scene_manifest = True
                break
        except Exception:
            pass

    return {
        "has_scenedelegate": has_scenedelegate,
        "has_shared_instance": has_shared_instance,
        "has_scene_manifest": has_scene_manifest,
    }


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

    # Add architecture infos
    if not result.architecture["has_scenedelegate"]:
        result.issues.append(
            ScanIssue(
                rule_id="ARCH-001",
                severity="error",
                message="Missing SceneDelegate file",
                file=str(project_path),
                line=0,
                column=0,
                match="SceneDelegate.swift/m not found",
                suggestion="Create SceneDelegate and configure UIApplicationSceneManifest in Info.plist",
            )
        )
    if not result.architecture["has_scene_manifest"]:
        result.issues.append(
            ScanIssue(
                rule_id="ARCH-002",
                severity="error",
                message="Missing UIApplicationSceneManifest in Info.plist",
                file=str(project_path),
                line=0,
                column=0,
                match="UIApplicationSceneManifest not found in any Info.plist",
                suggestion="Add UIApplicationSceneManifest configuration to Info.plist",
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
                suggestion="Add a sharedInstance class method to AppDelegate for SceneDelegate forwarding",
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
