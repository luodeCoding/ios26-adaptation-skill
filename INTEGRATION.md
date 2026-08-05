# iOS 26 Adaptation — 使用说明

> 本仓库是**纯 AI 技能工具**，不参与任何项目编译。

---

## 核心定位

```
┌─────────────────────────────────────────────────────────────┐
│                    主项目（你的 iOS App）                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ AppDelegate │  │ SceneDelegate│  │ UIApplication+Ext   │  │
│  │ （手动修改） │  │ （手动添加） │  │ （手动添加）        │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│                                                             │
│  所有代码都是开发者手动复制/编写，和 skill 仓库无引用关系       │
└─────────────────────────────────────────────────────────────┘
                              ↑
                              │ AI 读取 skill 知识，指导开发
                              │
┌─────────────────────────────────────────────────────────────┐
│           ios26-adaptation-skill（本仓库）                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ SKILL.md │  │ templates│  │ scripts  │  │ docs     │    │
│  │ 知识文档  │  │ 代码模板  │  │ 扫描脚本  │  │ 参考文档  │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
│                                                             │
│  仅作为 AI 知识和开发者参考，不加入任何 Xcode 项目编译          │
└─────────────────────────────────────────────────────────────┘
```

---

## 使用方式

### 方式1：AI 助手驱动（推荐）

AI 读取本仓库的知识，直接在主项目中生成和修改代码。

**开发者只需要说：**

```
"帮我适配 iOS 26"
"扫描一下项目有哪些废弃 API"
"生成 SceneDelegate 代码"
```

**AI 的工作流程：**

1. 读取 `SKILL.md` 了解适配策略
2. 读取 `AGENTS.md` 了解检查清单
3. 运行 `scripts/ios26-scanner.py` 扫描主项目
4. 参考 `templates/` 中的代码模板
5. **直接在主项目中**生成/修改代码

### 方式2：开发者手动参考

```bash
# 1. 下载到本地任意位置（和主项目完全独立）
git clone https://github.com/luodeCoding/ios26-adaptation-skill.git

# 2. 查看需要的模板代码
cat ios26-adaptation-skill/templates/swift/SceneDelegate.swift

# 3. 手动复制粘贴到主项目，按需修改
# 直接复制代码，不是引用文件！

# 4. 运行扫描脚本检查遗漏
python3 ios26-adaptation-skill/scripts/ios26-scanner.py /path/to/your/ios/project
```

---

## 适配影响声明（低冲击承诺）

把本技能应用到你的主项目时，**只动 iOS 26/27 相关的部分**，其余代码原样保留：

### ✅ 只会修改的范围

| 范围 | 具体内容 |
|------|---------|
| 废弃 API 调用点 | 仅替换扫描命中的废弃写法（`keyWindow`、`delegate.window`、通知选项等），逐行对应替换 |
| 生命周期架构 | 新增 SceneDelegate 文件、Info.plist 增加 `UIApplicationSceneManifest`、AppDelegate 抽取启动方法 |
| Info.plist | 仅新增适配相关键（场景清单、`UIDesignRequiresCompatibility`、启动屏键） |
| 新增适配文件 | 按扫描结果，从 `templates/` 拷贝实际需要的扩展/分类/适配器文件 |
| 版本分支 | 所有行为差异用 `#available` / `@available` 包裹，**不删除任何旧系统路径** |

### ❌ 绝不触碰的部分

| 禁止项 | 原因 |
|--------|------|
| 修改 **Deployment Target / 最低 iOS 版本** | 苹果无此要求，改了会悄悄改变你的用户覆盖范围 |
| 重构业务逻辑、重命名符号、格式化无关文件 | 超出适配范围，只会制造噪音 diff 和回归风险 |
| 删除 iOS 12 / iOS 13 之前的兼容路径 | 老系统运行时支持必须保留 |
| “顺便”替换未废弃的 API（如 SwiftUI 现代化、能正常编译就不动的 StoreKit 重写） | 只修复阻塞 iOS 26/27 强制要求、或扫描器报 Error 的项 |
| 修改 `Pods/` / 第三方 SDK 源码 | 升级依赖版本，不打补丁 |
| 擅自开启 Swift 6 严格并发迁移 | 属于独立项目决策，只建议、不代执行 |

### 官方标准对齐

所有适配项均可追溯到 **Apple 官方来源**：[Upcoming Requirements](https://developer.apple.com/news/upcoming-requirements/)、
iOS Release Notes、WWDC Session、Technical Note（如 TN3187）。不编造任何要求；
每个时间节点该做什么，见 [docs/timeline.zh.md](docs/timeline.zh.md)（[English](docs/timeline.md)）。

### AI 执行流程（可预期、可审计）

```
扫描 → 输出问题清单 → 列出“新增/修改文件清单 + 逐项理由”
    → 确认不越界后才动手 → 改完重扫验证 Error 清零
```

---

## 重要说明

### ❌ 不要做的事情

| 不要做 | 原因 |
|--------|------|
| 不要把 skill 仓库文件加入 Xcode 项目 | 这些文件只是参考模板，不需要编译 |
| 不要用 `#import` 或 `import` 引用 skill 文件 | skill 文件不在主项目中 |
| 不要把 skill 仓库作为 git submodule | 完全没必要，AI 直接读取本地文件即可 |
| 不要把 skill 仓库复制到主项目里 | 保持独立，方便更新和 AI 读取 |

### ✅ 正确的工作流

```
主项目遇到 iOS 26 适配问题
        ↓
AI 读取 skill 仓库知识（SKILL.md、模板、检查清单）
        ↓
AI 分析主项目代码，找出问题
        ↓
AI 参考模板，直接在主项目中生成修复代码
        ↓
开发者审阅、调整、编译验证
        ↓
发现问题 → 继续让 AI 调整（循环）
```

---

## 文件用途说明

| 文件/目录 | 用途 | 谁使用 |
|----------|------|--------|
| `README.md` / `README.zh.md` | 仓库入口：关键时间节点、阶段策略、快速上手 | 所有人 |
| `SKILL.md` | 完整适配指南、决策流程、代码示例 | AI + 开发者 |
| `AGENTS.md` | Claude Code 工作流、触发条件 | AI |
| `INTEGRATION.md` | 使用说明、本仓库与主项目的关系 | 开发者 |
| `CHANGELOG.md` / `.zh.md` | 版本历史 | 所有人 |
| `templates/swift/` | Swift 代码模板 | AI 参考后生成代码 |
| `templates/objc/` | Objective-C 代码模板 | AI 参考后生成代码 |
| `templates/mixed/` | 混编项目桥接方案 | AI 参考后生成代码 |
| `templates/PrivacyInfo.xcprivacy` | Privacy Manifest 模板 | 开发者复制后修改 |
| `scripts/ios26-scanner.py` | 废弃 API 扫描脚本（50+ 条规则，三层检测，报告含人工核对清单与上线门禁） | AI / 开发者手动运行 |
| `scripts/adaptation-ledger.json` | 50 项覆盖总账（零遗漏任务清单唯一事实源） | AI 逐项对照执行 |
| `docs/faq.md` | 常见问题解答 | 开发者参考 |
| `docs/timeline.md` / `.zh.md` | iOS 26/27 时间线与适配范围总览（唯一时间线权威参考） | 所有人 |
| `docs/coverage.md` / `.zh.md` | 50 项覆盖矩阵（总账人类可读镜像） | 所有人 |
| `docs/sdk-compatibility.md` | 第三方 SDK 兼容性速查表 | 开发者参考 |
| `docs/ios27-preview.md` | iOS 27 / Xcode 27 适配前瞻（第三阶段） | AI + 开发者 |
| `examples/` | 分阶段检查清单（第一/二/三阶段，双语） | AI + 开发者 |

---

## 扫描脚本使用

```bash
# 基本用法
python3 /path/to/ios26-adaptation-skill/scripts/ios26-scanner.py /path/to/your/ios/project

# 生成 JSON 报告
python3 /path/to/ios26-adaptation-skill/scripts/ios26-scanner.py \
    /path/to/your/ios/project \
    --format json \
    --output report.json
```

扫描内容（共 50+ 项检查，完整规则参考见 `SKILL.md`，全量适配项见 `docs/coverage.zh.md`）：

**iOS 26 核心适配**
- `keyWindow` / `delegate.window` / `windows` / `statusBarFrame` 等窗口访问废弃 API
- `UNNotificationPresentationOptionAlert`（`UNAuthorizationOptionAlert` 未废弃，不会误报）
- SceneDelegate 配置状态、AppDelegate `sharedInstance` 方法
- AssetsLibrary、StoreKit 1、SiriKit、SwiftUI 废弃 API、Privacy Manifest 缺失

**iOS 26 运行时实战坑**
- 私有 KVC `setValue:forKey:@"tabBar"`（iOS 26 闪退）
- `navigationBar addSubview`（被合成层吞掉）
- `rightBarButtonItems` 顺序/间距变化

**iOS 27 前瞻**
- `canOpenURL` 弃用、`LSApplicationQueriesSchemes` 超 25 条上限
- `-ld_classic` 残留链接器标志（Xcode 27 移除）
- `NSBundleResourceRequest`（ODR 弃用）、`MXMetricManager`（替换为 MetricManager）
