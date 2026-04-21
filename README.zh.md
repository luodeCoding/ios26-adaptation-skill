# iOS 26 适配指南

<div align="right">
  <b>🌐 语言:</b> <a href="./README.md">English</a> | 中文
</div>

---

> **语言**: Objective-C / Swift  
> **平台**: iOS  
> **最低 iOS 版本**: 12.0+  
> **最后更新**: 2026-04-21

全面适配 iOS 26 SDK 和 Liquid Glass 设计语言的技能指南。

## 概览

Apple 要求所有在 **2026年4月28日** 之后提交的应用必须使用 iOS 26 SDK 构建。本指南提供：

- 📋 **两阶段适配策略** - SDK 构建适配 和 Liquid Glass 完整适配
- 🔍 **项目扫描规则** - 识别废弃 API 和需要的改动
- 📊 **决策流程图** - 根据你的时间安排选择合适的适配策略
- ✅ **检查清单** - 跟踪每个阶段的进度

## 关键时间节点

| 日期 | 要求 | 影响 |
|------|------|------|
| **2026-04-28** | 必须使用 iOS 26 SDK 构建 | 不合规将无法提交应用更新 |
| **~2026-09** | Xcode 27 发布，Liquid Glass 强制启用 | `UIDesignRequiresCompatibility` 将被移除 |

## 两阶段适配

### 第一阶段：SDK 构建适配（2026-04-28 前）

**目标**: 使用 iOS 26 SDK 构建，同时保持现有 UI 不变

**关键任务**:
- 升级到 Xcode 26.0+
- 修复废弃 API 调用（keyWindow 等）
- 暂时禁用 Liquid Glass
- 完成 SceneDelegate 架构迁移

### 第二阶段：Liquid Glass 完整适配（Xcode 27 前）

**目标**: 完整适配 Liquid Glass 设计语言

**关键任务**:
- 移除 `UIDesignRequiresCompatibility` 标记
- 验证所有 UI 控件在 Liquid Glass 下的表现
- 调整自定义 UI 以达到视觉协调

## 快速开始

### 1. 下载本仓库到本地

```bash
# 方式1：git clone（推荐，方便后续更新）
git clone https://github.com/luodeCoding/ios26-adaptation-skill.git

# 方式2：直接下载 ZIP
# 访问 https://github.com/luodeCoding/ios26-adaptation-skill/archive/refs/heads/main.zip
```

### 2. 在主项目中引用本地文件夹

**Xcode 操作步骤：**

1. 打开你的主项目 Xcode
2. 右键点击项目导航栏中的项目根目录 → **Add Files to "YourProject"...**
3. 在弹出的文件选择器中，找到你下载的 `ios26-adaptation-skill` 文件夹
4. **关键**：勾选 **"Create folder references"**（不是 Create groups！）
   
   ![create-folder-reference](https://i.imgur.com/placeholder.png)
   
5. 确保勾选你的 app target
6. 点击 **Add**

> 💡 **为什么选择 "Create folder references"？**
> - 文件夹以蓝色图标显示在 Xcode 中
> - 文件夹内容与本地磁盘实时同步
> - 在 Xcode 里修改文件 = 直接修改本地仓库文件
> - 在 Finder 里修改文件 = Xcode 立刻看到变化

**引用后的项目结构：**

```
YourMainProject/
├── ios26-adaptation-skill/     ← 蓝色文件夹（folder reference）
│   ├── templates/
│   │   ├── swift/
│   │   └── objc/
│   ├── scripts/
│   ├── docs/
│   └── ...
├── YourApp/
└── YourApp.xcodeproj
```

### 3. 将模板代码加入编译

folder reference 中的文件**不会自动编译**，需要把需要的模板文件单独加入 target：

1. 从 `ios26-adaptation-skill/templates/swift/` 中，选择你需要的文件：
   - `UIApplication+MainWindow.swift`
   - `SceneDelegate.swift`
   - `AppDelegate+Setup.swift`
   - `UNNotificationOptions+Adapter.swift`
   
2. 右键 → **Add Files to "YourProject"...**
3. 这次选择 **"Create groups"** + 勾选你的 target
4. 这些文件会以黄色文件夹（group）形式加入，会被编译

> ⚠️ **注意**：这样加入的模板文件是**复制**到主项目中的。如果你想直接引用 skill 仓库里的文件（不复制），可以：
> - 方式 A：复制到主项目，改起来更方便（推荐）
> - 方式 B：不加入 target，只是参考，手动在自己的项目里写

### 4. 扫描你的项目

```bash
# 直接运行本地脚本
python3 /path/to/ios26-adaptation-skill/scripts/ios26-scanner.py /path/to/your/ios/project

# 生成 JSON 报告
python3 /path/to/ios26-adaptation-skill/scripts/ios26-scanner.py /path/to/your/ios/project --format json --output report.json
```

### 5. 应用代码模板

从 `templates/` 目录复制需要的文件到你的 Xcode 项目，并根据需要调整类名：

| 模板 | Swift | Objective-C | 用途 |
|------|-------|-------------|------|
| `UIApplication+MainWindow` | [Swift](./templates/swift/UIApplication+MainWindow.swift) | [OC](./templates/objc/UIApplication+MainWindow.h) | 统一窗口/导航访问 |
| `SceneDelegate` | [Swift](./templates/swift/SceneDelegate.swift) | [OC](./templates/objc/SceneDelegate.h) | 窗口创建与生命周期转发 |
| `AppDelegate+Setup` | [Swift](./templates/swift/AppDelegate+Setup.swift) | [OC](./templates/objc/AppDelegate+Setup.h) | 双路径启动改造 |
| `UNNotificationOptions+Adapter` | [Swift](./templates/swift/UNNotificationOptions+Adapter.swift) | [OC](./templates/objc/UNNotificationOptionsAdapter.h) | iOS 26 通知选项适配 |

详细的集成说明请见 [`templates/README.md`](./templates/README.md)。

### 6. 遵循检查清单

详见 [SKILL.md](./SKILL.md) 获取：
- 决策流程图
- 实施指南
- 分阶段检查清单
- 测试框架

### 7. 查看常见问题

遇到常见疑问？请参阅 [docs/faq.md](./docs/faq.md)。

---

## 工作流：遇到问题时的快速调整

```
主项目 Xcode 编译报错
        ↓
查看 ios26-adaptation-skill/ 中的模板/文档
        ↓
直接在 Xcode 里修改 skill 项目中的文件（蓝色文件夹）
        ↓
修改即时生效，无需复制/同步
        ↓
验证通过后，进入 skill 项目目录提交到 GitHub
        ↓
cd /path/to/ios26-adaptation-skill
git add .
git commit -m "fix: xxx"
git push
```

> ✅ **核心优势**：所有文件都在本地，改完立刻编译验证，改 skill 项目的文件就是改本地仓库，随时可提交到 GitHub。

---

## 项目结构

```
ios26-adaptation-skill/
├── README.md              # 本文件 - 快速入门指南
├── README.zh.md           # 中文版 README
├── SKILL.md               # 详细技能文档
├── CHANGELOG.md           # 版本历史
├── LICENSE                # MIT 许可证
├── AGENTS.md              # Claude Code Agent 使用指南
├── docs/
│   ├── testing-guide.md   # 测试团队测试指南
│   └── faq.md             # 常见问题解答
├── .claude/
│   └── iOS26-适配框架指南.md  # 完整适配框架指南（中文）
├── examples/
│   ├── phase1-checklist.md    # 第一阶段执行检查清单（英文）
│   ├── phase1-checklist.zh.md # 第一阶段执行检查清单（中文）
│   ├── phase2-checklist.md    # 第二阶段执行检查清单（英文）
│   └── phase2-checklist.zh.md # 第二阶段执行检查清单（中文）
├── scripts/
│   └── ios26-scanner.py   # 自动化项目扫描脚本
└── templates/
    ├── swift/                 # Swift 代码模板
    └── objc/                  # Objective-C 代码模板
```

## 常见误区

| 误区 | 事实 |
|-----|------|
| 必须将 Deployment Target 改为 iOS 26 | ❌ 不需要。保持你当前的最低版本（iOS 12/13 等） |
| 用户必须升级到 iOS 26 | ❌ 不需要。运行时要求由 Deployment Target 决定 |
| 现有应用版本将被下架 | ❌ 不会。仅影响新提交和更新包 |
| 有宽限期 | ❌ 没有。2026年4月28日是硬性截止日期 |

## 核心概念

### SceneDelegate 架构（iOS 13+）

- **问题**: `UIApplication.keyWindow` 和 `AppDelegate.window` 在 iOS 13+ 中不可靠
- **解决方案**: 通过 `UIApplication` 扩展使用统一访问接口
- **影响**: 所有窗口访问必须通过新接口进行

### 废弃 API（iOS 26）

| 废弃 API | 替代方案 |
|---------|---------|
| `keyWindow` | 基于 SceneDelegate 的窗口访问 |
| `UNNotificationPresentationOptionAlert` | `UNNotificationPresentationOptionBanner \| List` |
| `UNAuthorizationOptionAlert` | `UNAuthorizationOptionBanner` |

### Liquid Glass 设计

- **是什么**: iOS 26 的新视觉语言
- **自动适配**: 标准 UIKit 控件自动获得新外观
- **自定义**: 自定义 UI 需要手动调整
- **时间线**: 第一阶段可选，第二阶段强制

## 决策检查清单

开始适配前，请回答以下问题：

- [ ] 下次应用发布计划是什么时候？
- [ ] 现在是否有可用的开发资源？
- [ ] SceneDelegate 是否已经配置？
- [ ] 项目中有多少废弃 API 调用？
- [ ] 是否使用了大量自定义 UI 组件？

## 资源

- [Apple Developer 新闻](https://developer.apple.com/news/)
- [iOS 26 发布说明](https://developer.apple.com/documentation/ios-release-notes)
- [Liquid Glass 设计指南](https://developer.apple.com/design/)

## 许可证

MIT 许可证 - 详见 LICENSE 文件

---

**作者**: roder
