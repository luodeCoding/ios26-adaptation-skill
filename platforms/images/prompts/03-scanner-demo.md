# Scanner 扫描器演示图提示词

## 用途
展示扫描器核心功能和输出效果，放在文章"自动化扫描工具"章节。

## 文章核心信息
- 一行命令：`python3 scripts/ios26-scanner.py /path/to/project`
- 输出包含：Rule ID、Severity、File、Line、Message
- 20+ 条规则，覆盖 WINDOW、NOTIF、STOREKIT、SWIFTUI 等类别
- 文章输出示例：
  - WINDOW-001 | ERROR | LoginVC.swift | 45 | Deprecated keyWindow usage
  - STOREKIT-001 | ERROR | IAPManager.m | 128 | StoreKit 1 API removed
  - PRIVACY-001 | ERROR | ./ | 0 | Missing PrivacyInfo.xcprivacy

## 推荐尺寸
1600 x 900（16:9 横版）

---

## Gemini / ChatGPT / Claude 提示词

**视觉目标**：左边是"有问题的代码"，右边是"扫描报告"，中间是"扫描动作"。报告要和文章中的表格格式一致。

```
生成一张分屏对比图，横版 16:9，深色背景接近纯黑。

【左半屏 / 占画面 42% 宽度，位于左侧】
显示一段 iOS 代码，像 Xcode 深色主题编辑器（背景 #1E1E1E）。
- 代码约 12-15 行，等宽字体
- 第 3 行：包含 "UIApplication.shared.keyWindow"，这行有红色下划线和黄色高亮背景
- 第 7 行：包含 "UIWebView"，有红色下划线
- 第 10 行：包含 "NavigationView"，有橙色高亮背景
- 第 12 行：包含 "UIImagePickerController"，有橙色高亮背景
- 整体代码看起来有问题、急需修复
- 左侧边缘有行号（1、2、3...），像真实编辑器
- 屏幕有微微暗角，暗示"老旧/待修复"

【右半屏 / 占画面 42% 宽度，位于右侧】
显示扫描结果报告面板，整洁现代。
- 顶部有一条细长的绿色进度条，显示扫描完成
- 下方是一个表格，有 4 列：Rule ID、Severity、File、Message
- 表格第一行（红色）：WINDOW-001 | ERROR | LoginVC.swift | Deprecated keyWindow
- 表格第二行（红色）：WEB-001 | ERROR | WebVC.m | UIWebView usage
- 表格第三行（橙色）：SWIFTUI-001 | WARNING | SettingsView.swift | NavigationView
- 表格第四行（橙色）：PHOTOS-001 | WARNING | PhotoPicker.swift | UIImagePickerController
- 表格用颜色区分严重级别：红色表示 ERROR，橙色表示 WARNING
- 表格下方有一行统计："Scanned: 247 files | Issues: 4"
- 整体看起来清晰、专业、已分类

【中间分隔 / 占画面 16% 宽度，位于正中央】
中间有一条垂直分界线。
- 分界线左侧是暗红色，右侧是亮绿色，形成渐变过渡
- 分界线中央有一个发光的扫描光标图标（像雷达圆周扫描动画的静态帧），发出扇形光束向左照射
- 光束照亮左侧代码，暗示"正在扫描"
- 分界线下方有一个小型的 Python 蛇形图标，暗示这是 Python 脚本

【绝对不要】
不要真实可读的长文字（用模拟占位符），不要中文，不要多余的 UI 元素（菜单栏、窗口按钮）。左右对比要强烈、直观。表格中的文字用短缩写即可，不需要完整句子。

风格：开发者工具截图风格，高对比度，信息设计清晰，像真实工具界面。
```

---

## 如果扫描报告不够像真实表格

```
右侧面板要更像一个真实的表格 UI：有表头（Rule / Severity / File / Message），每行有分割线，ERROR 行左侧有红色圆点，WARNING 行左侧有橙色圆点。表格上方有一个小标题栏写着"Scan Results"。
```
