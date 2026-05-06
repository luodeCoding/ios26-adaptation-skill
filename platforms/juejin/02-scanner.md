# 🔍 我写了一个 Python 脚本，自动扫描 iOS 26 废弃 API

> 分享一个零依赖的 Python 扫描工具，20+ 条规则覆盖窗口访问、通知、StoreKit、SwiftUI、CoreData 等场景。附带源码解析。

---

## 为什么写这个工具

iOS 26 SDK 有个特点：**很多 API 不是废弃，而是直接移除**。比如 StoreKit 1 的 `SKPaymentTransaction`、`SKProductsRequest`，在 Xcode 26 中直接编译报错。

手动 grep 太慢，Xcode 静态分析也不够全面。于是写了一个零依赖的扫描脚本。

---

## 使用效果

```bash
python3 scripts/ios26-scanner.py /path/to/your/ios/project
```

输出：

```
# iOS 26 Adaptation Scan Report
**Files Scanned:** 247
**Total Issues:** 12  (Errors: 3, Warnings: 9)

| Rule ID | Severity | File | Line | Message |
|---------|----------|------|------|---------|
| WINDOW-001 | ERROR | LoginVC.swift | 45 | Deprecated keyWindow usage |
| STOREKIT-001 | ERROR | IAPManager.m | 128 | StoreKit 1 API removed |
| SCREEN-001 | WARNING | HomeVC.swift | 88 | Deprecated UIScreen.main usage |
```

---

## 核心设计

```python
RULES = [
    {
        "id": "WINDOW-001",
        "name": "Deprecated keyWindow usage (Swift)",
        "pattern": re.compile(r"UIApplication\.shared\.keyWindow"),
        "extensions": {".swift"},
        "severity": "error",
        "suggestion": "Use UIApplication.shared.mainWindow",
    },
    # ... 更多规则
]
```

每条规则包含：
- 唯一 ID
- 正则表达式匹配模式
- 适用文件后缀
- 严重级别（error / warning / info）
- 修复建议

---

## 支持的 20+ 条规则

| 规则 ID | 检测内容 | 级别 |
|---------|---------|------|
| WINDOW-001~006 | keyWindow, delegate.window, window链式调用 | error/warning |
| NOTIF-001 | UNNotificationPresentationOptionAlert | warning |
| SCREEN-001/002 | UIScreen.main / [UIScreen mainScreen] | warning |
| WEB-001 | UIWebView | error |
| TLS-001 | TLS 1.0/1.1 | warning |
| COREDATA-001 | NSPersistentStoreUbiquitousContentNameKey | error |
| STOREKIT-001 | SKPaymentTransaction 等 StoreKit 1 API | error |
| SIRIKIT-001 | 废弃的 SiriKit intent domain | warning |
| SWIFTUI-001/002/003 | NavigationView, cornerRadius, foregroundColor | warning |
| PHOTOS-001 | UIImagePickerController | warning |
| SWIFT6-001 | Swift 6 并发潜在问题 | info |
| STATUS-001~003 | statusBarStyle | warning |
| PRIVACY-001 | 缺失 PrivacyInfo.xcprivacy | error |

---

## 亮点：自动排除误报

```python
def _should_skip_issue(rule_id: str, line: str, filepath: Path) -> bool:
    # UIApplication+Extension 文件中访问 delegate.window 是合法 fallback
    if rule_id == "WINDOW-003" and "UIApplication+Extension" in str(filepath):
        return True
    # iOS 12 fallback 路径中的 UIScreen.main 是合法的
    if rule_id in ("SCREEN-001", "SCREEN-002") and "iOS 12" in line:
        return True
    return False
```

---

## 如何扩展新规则

新增一条规则只需要 5 行代码：

```python
{
    "id": "YOUR-001",
    "name": "Your custom rule",
    "pattern": re.compile(r"DeprecatedPattern"),
    "extensions": {".swift", ".m"},
    "severity": "warning",
    "suggestion": "Use NewAPI instead",
},
```

---

## 项目地址

- GitHub：[github.com/luodeCoding/ios26-adaptation-skill](https://github.com/luodeCoding/ios26-adaptation-skill)
- 扫描脚本路径：`scripts/ios26-scanner.py`
