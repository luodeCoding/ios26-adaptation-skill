# 基于 Python 的 iOS 26 废弃 API 自动化扫描工具实现

**摘要**：本文介绍一个零第三方依赖的 Python 扫描工具实现，支持 20+ 条 iOS 26 SDK 适配检测规则，涵盖窗口访问、StoreKit、SwiftUI、CoreData 等场景。附带源码解析和扩展方法。

---

## 一、工具背景

iOS 26 SDK 与此前版本最大的不同在于：**部分 API 不是 deprecated，而是直接 removed**。例如：

- StoreKit 1：`SKPaymentTransaction`、`SKProductsRequest`、`SKPaymentQueue`
- CoreData：`NSPersistentStoreUbiquitousContentNameKey` 系列 key
- WebView：`UIWebView`

这些 API 在 Xcode 26 中直接产生编译错误，而非警告。传统的手动 grep 方式效率低且容易遗漏，因此开发了这套自动化扫描方案。

---

## 二、架构设计

### 核心数据结构

```python
@dataclass
class ScanIssue:
    rule_id: str
    severity: str      # error / warning / info
    message: str
    file: str
    line: int
    column: int
    match: str
    suggestion: str
```

### 规则定义

每条规则由字典定义，包含正则表达式、适用文件后缀、严重级别和修复建议：

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
]
```

### 扫描流程

```
输入项目路径
  ↓
递归遍历所有 .swift / .m / .mm 文件
  ↓
逐行匹配规则正则
  ↓
过滤误报（注释行、合法 fallback 路径）
  ↓
架构检查（SceneDelegate、Privacy Manifest、sharedInstance）
  ↓
输出 Markdown / JSON 报告
```

---

## 三、误报过滤机制

扫描工具的关键难点在于减少误报。实现方案：

```python
def _should_skip_issue(rule_id: str, line: str, filepath: Path) -> bool:
    # 跳过纯注释行中的 window 相关规则
    if rule_id in ("WINDOW-003", "WINDOW-004") and _is_comment_line(line):
        return True
    
    # UIApplication+Extension 文件中访问 delegate.window 是合法 iOS 12 fallback
    if rule_id == "WINDOW-003" and "UIApplication+Extension" in str(filepath):
        if "self.delegate.window" in line or ("delegate.window" in line and "return" in line):
            return True
    
    # UIScreen.main 在 iOS 12 fallback 注释旁是合法的
    if rule_id in ("SCREEN-001", "SCREEN-002"):
        if "iOS 12" in line or "fallback" in line.lower() or "deprecated" in line.lower():
            return True
    
    return False
```

---

## 四、规则扩展方法

新增一条检测规则仅需补充一个字典：

```python
{
    "id": "CUSTOM-001",
    "name": "Custom deprecated pattern",
    "pattern": re.compile(r"DeprecatedAPI\s*\("),
    "extensions": {".swift", ".m", ".mm"},
    "severity": "warning",
    "suggestion": "Replace with NewAPI()",
},
```

无需修改扫描引擎逻辑。

---

## 五、完整规则列表

| 规则 ID | 检测内容 | 级别 | 适用文件 |
|---------|---------|------|---------|
| WINDOW-001 | `UIApplication.shared.keyWindow` | error | .swift |
| WINDOW-002 | `[UIApplication sharedApplication].keyWindow` | error | .m, .mm |
| WINDOW-003 | `delegate.window` | warning | 全部 |
| WINDOW-004 | `AppDelegate.*window` | warning | 全部 |
| WINDOW-005/006 | `.window.rootViewController` / `.window.visibleViewController` | warning | 全部 |
| NOTIF-001 | `UNNotificationPresentationOptionAlert` | warning | 全部 |
| SCREEN-001/002 | `UIScreen.main` / `[UIScreen mainScreen]` | warning | .swift / .m |
| WEB-001 | `UIWebView` | error | 全部 |
| TLS-001 | `TLSv10`, `TLSv11` | warning | 全部 |
| COREDATA-001 | `NSPersistentStoreUbiquitousContentNameKey` | error | 全部 |
| STOREKIT-001 | `SKPaymentTransaction` 等 StoreKit 1 API | error | 全部 |
| SIRIKIT-001 | 废弃 SiriKit intent domain | warning | 全部 |
| SWIFTUI-001/002/003 | `NavigationView`, `.cornerRadius()`, `.foregroundColor()` | warning | .swift |
| PHOTOS-001 | `UIImagePickerController` | warning | 全部 |
| SWIFT6-001 | `@StateObject`, `@ObservedObject` | info | .swift |
| STATUS-001~003 | `statusBarStyle` | warning | 全部 |
| PRIVACY-001 | 缺失 `PrivacyInfo.xcprivacy` | error | 项目级 |
| ARCH-001~003 | SceneDelegate / Manifest / sharedInstance | error/warning | 项目级 |

---

## 六、单元测试

项目包含完整的单元测试套件，覆盖所有规则：

```bash
cd scripts
python3 test_scanner.py
```

测试结果：

```
Ran 19 tests in 0.017s
OK
```

测试覆盖：
- 单条规则命中验证
- 误报过滤验证
- 架构检查验证
- 完整项目扫描验证

---

## 七、项目地址

- GitHub：[github.com/luodeCoding/ios26-adaptation-skill](https://github.com/luodeCoding/ios26-adaptation-skill)
- 扫描脚本：`scripts/ios26-scanner.py`
- 测试文件：`scripts/test_scanner.py`
- CI 配置：`.github/workflows/ci.yml`

---

**关键词**：iOS 26 扫描工具、Python 正则表达式、废弃 API 检测、StoreKit 2、Privacy Manifest、CI/CD
