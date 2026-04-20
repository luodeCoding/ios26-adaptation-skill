# iOS 26 适配框架指南

> **文档定位**: 元适配指南 - 指导项目扫描与方案生成  
> **适用语言**: Objective-C / Swift  
> **版本**: v1.0

---

## 一、适配阶段与时间节点

### 1.1 苹果官方强制时间表

| 截止日期 | 要求内容 | 影响范围 | 阶段 |
|---------|---------|---------|------|
| **2026-04-28** | 必须使用 iOS 26 SDK 构建 | 所有新提交和更新包 | **第一阶段** |
| **Xcode 27 发布前** (~2026-09) | Liquid Glass 完整适配，`UIDesignRequiresCompatibility` 失效 | 所有应用 | **第二阶段** |
| **Xcode 27 发布前** (~2026-09) | UIScene 生命周期迁移强制完成 | UIKit 应用 | **第二阶段** |

### 1.2 两阶段适配策略

#### 第一阶段：SDK 构建适配（2026-04-28 前必须完成）

**目标**: 使用 iOS 26 SDK 构建，保持现有 UI 稳定

**核心工作**:
- 升级 Xcode 至 26.0+
- 修复编译错误（废弃 API 替换）
- 临时禁用 Liquid Glass（`UIDesignRequiresCompatibility = true`）
- 完成 SceneDelegate 基础架构迁移

**关键理解**:
- ❌ 不需要修改 Deployment Target（保持 iOS 12/13 等）
- ❌ 用户不需要升级到 iOS 26（运行要求由 Deployment Target 决定）
- ✅ 仅影响新提交和更新包，现有上架版本不受影响
- ✅ 无宽限期，4月28日强制执行

#### 第二阶段：Liquid Glass 完整适配（Xcode 27 发布前）

**目标**: 完整适配 Liquid Glass 设计语言

**核心工作**:
- 移除 `UIDesignRequiresCompatibility` 配置
- 验证所有 UI 控件在 Liquid Glass 下的表现
- 调整自定义 UI 与系统控件的视觉协调
- 处理导航栏、TabBar、键盘等系统控件的新样式

**关键理解**:
- `UIDesignRequiresCompatibility` 是**临时过渡**选项，Xcode 27 将强制移除
- 使用标准 UIKit/SwiftUI 控件的应用会自动获得 Liquid Glass 效果
- 自定义控件需要手动适配新的视觉风格

### 1.3 构建环境要求

| 工具 | 最低版本 | 说明 |
|-----|---------|------|
| Xcode | 26.0+（推荐 26.3） | 必须使用 Xcode 26 才能构建 iOS 26 SDK |
| macOS | Sequoia 15.3+ | Xcode 26 对 macOS 版本有要求 |
| iOS SDK | 26.0+ | Xcode 26 自带 |
| Swift | 5.x / 6.0 | Swift 5 仍受支持，不强制升级 |

---

## 二、适配时机决策指南

> **重要提示**: 请根据您的 App 上线计划，选择合适的适配策略。

### 2.1 决策流程图

```
                    ┌─────────────────────────────────────┐
                    │   您的下次上线时间是什么时候？        │
                    └──────────────┬──────────────────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          │                        │                        │
          ▼                        ▼                        ▼
┌─────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│ 2026-04-28 前   │    │ 2026-04-28 ~        │    │ Xcode 27 发布后     │
│                 │    │ Xcode 27 发布前     │    │ (~2026-09 后)       │
└────────┬────────┘    └──────────┬──────────┘    └──────────┬──────────┘
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│ 建议策略 A           │  │ 建议策略 B           │  │ 建议策略 C           │
│                     │  │                     │  │                     │
│ • 当前版本暂不改动   │  │ • 必须完成第一阶段   │  │ • 可两阶段一起完成   │
│ • 新分支提前适配     │  │ • 评估第二阶段优先级 │  │ • 一次性完整适配     │
│ • 为后续版本做准备   │  │ • Xcode27 前上线需   │  │ • 减少分支切换成本   │
│                     │  │   完成第二阶段       │  │                     │
└─────────────────────┘  └─────────────────────┘  └─────────────────────┘
```

### 2.2 三种建议策略详解

#### 策略 A：当前版本暂缓，新分支提前适配（适合 4月28日 前需上线的项目）

**适用场景**:
- 您的 App 在 2026-04-28 前有计划内的版本上线
- 不想在当前版本引入适配风险

**操作建议**:
1. **主分支保持现状** - 当前版本的代码不做任何改动
2. **新建适配分支** - 从主分支创建 `feature/ios26-adaptation` 分支
3. **提前完成适配** - 在新分支上完成第一阶段适配，充分测试
4. **4月28日后合并** - 下一个版本开发时，基于已适配的分支继续

**分支管理**:
```bash
# 从当前主分支创建适配分支
git checkout -b feature/ios26-adaptation

# 在该分支完成第一阶段适配
# ... 适配工作 ...

# 4月28日后，将适配分支合并到主分支
git checkout main
git merge feature/ios26-adaptation
```

**⚠️ 咨询点**: 是否需要为您创建 `feature/ios26-adaptation` 分支？

---

#### 策略 B：必须完成第一阶段，评估第二阶段（适合 4月28日 ~ Xcode27 之间需上线的项目）

**适用场景**:
- 您的 App 在 2026-04-28 到 Xcode 27 发布之间有上线计划
- 需要在 4月28日 后能够正常提交更新

**操作建议**:
1. **立即开始第一阶段** - 必须完成 SDK 构建适配
2. **临时禁用 Liquid Glass** - 使用 `UIDesignRequiresCompatibility = true`
3. **评估第二阶段**:
   - 如果 Xcode 27 发布前**还有**上线计划 → 必须完成第二阶段
   - 如果 Xcode 27 发布前**没有**上线计划 → 可延后到下次迭代

**时间节点检查清单**:
- [ ] 2026-04-28 前完成第一阶段
- [ ] 确认 Xcode 27 发布前的上线计划
- [ ] 如有上线计划，预留第二阶段适配时间

---

#### 策略 C：两阶段一起完成（适合 Xcode 27 发布后才需上线的项目）

**适用场景**:
- 您的 App 在 Xcode 27 发布前没有上线计划
- 或希望一次性完成所有适配工作

**操作建议**:
1. **同时完成两个阶段** - 在一个迭代周期内完成
2. **不添加临时禁用配置** - 直接适配 Liquid Glass
3. **充分测试** - 确保所有 UI 在新风格下表现正常

---

### 2.3 关键决策点检查表

在制定适配计划前，请先回答以下问题：

| 问题 | 您的答案 | 影响 |
|-----|---------|------|
| Q1: 2026-04-28 前是否有上线计划？ | 是 / 否 | 决定是否需要策略 A |
| Q2: 2026-04-28 ~ Xcode27 间是否有上线计划？ | 是 / 否 | 决定是否需要策略 B |
| Q3: 当前是否已配置 SceneDelegate？ | 是 / 否 | 影响第一阶段工作量 |
| Q4: 是否使用大量废弃 API（keyWindow 等）？ | 是 / 否 | 影响第一阶段工作量 |
| Q5: 团队当前是否有足够开发资源？ | 是 / 否 | 决定是否可以两阶段一起完成 |
| Q6: 是否有复杂的自定义 UI/导航栏？ | 是 / 否 | 影响第二阶段工作量 |

**根据答案选择策略**:
- Q1=是 → 选择策略 A
- Q1=否, Q2=是 → 选择策略 B
- Q1=否, Q2=否 → 选择策略 C

---

### 2.4 分支管理最佳实践

#### 推荐分支结构

```
main (主分支，保持稳定，随时可发布)
  │
  ├── feature/ios26-adaptation (iOS 26 适配分支)
  │     │
  │     ├── feature/ios26-phase1 (可选：第一阶段子分支)
  │     │
  │     └── feature/ios26-phase2 (可选：第二阶段子分支)
  │
  └── release/x.x.x (发布分支)
```

#### 分支操作指南

**创建适配分支**:
```bash
# 从主分支创建
git checkout main
git pull origin main
git checkout -b feature/ios26-adaptation

# 推送到远程
git push -u origin feature/ios26-adaptation
```

**两阶段分离（可选）**:
```bash
# 第一阶段分支
git checkout -b feature/ios26-phase1
# ... 完成第一阶段 ...
git checkout feature/ios26-adaptation
git merge feature/ios26-phase1

# 第二阶段分支
git checkout -b feature/ios26-phase2
# ... 完成第二阶段 ...
git checkout feature/ios26-adaptation
git merge feature/ios26-phase2
```

**合并时机**:
- 策略 A: 4月28日后合并到主分支
- 策略 B/C: 适配完成后合并到主分支

---

## 三、适配方向总览

### 3.1 架构层适配

| 方向 | 说明 | 影响范围 | 阶段 |
|-----|------|---------|------|
| **SceneDelegate 架构** | iOS 13+ 多窗口支持 | AppDelegate、窗口获取、生命周期 | 第一/二阶段 |
| **废弃 API 替换** | iOS 26 标记废弃的接口 | 通知、窗口、状态栏 | 第一阶段 |
| **液态玻璃兼容** | iOS 26 新设计语言 | UI 控件、导航栏、主题 | 第二阶段 |

### 3.2 代码层适配

| 方向 | 说明 | 扫描目标 | 阶段 |
|-----|------|---------|------|
| **全局窗口访问** | keyWindow / delegate.window 调用 | 所有源文件 | 第一阶段 |
| **生命周期方法** | AppDelegate 生命周期分流 | AppDelegate、SceneDelegate | 第一/二阶段 |
| **通知选项枚举** | Alert → Banner/List 替换 | 推送相关代码 | 第一阶段 |
| **状态栏样式** | 全局设置 → ViewController 设置 | 状态栏相关代码 | 第一阶段 |

### 3.3 Liquid Glass 影响范围

**自动适配的系统控件**（使用 iOS 26 SDK 编译后自动获得新外观）:
- UITabBar / UITabBarController
- UINavigationBar / UINavigationController
- Keyboard（键盘样式变化，带毛玻璃折射效果）
- UIToolbar
- UIAlertController / UIActionSheet
- UIButton、UISlider、UISwitch、UISegmentedControl
- UIScrollView（`allowsLiquidTransform` 默认开启）
- SwiftUI 所有标准组件

**需重点检查的自定义内容**:
- 自定义导航栏样式（可能与系统新效果不协调）
- 自定义 TabBar 样式
- 自定义键盘附件视图
- 与系统控件相邻的自定义 UI 元素（视觉协调性）

---

### 阶段一：项目扫描（第一阶段前完成）

**目标**: 识别需要适配的代码位置和模式

**扫描项清单**:

```
1. 架构检测
   - 是否存在 SceneDelegate
   - AppDelegate 是否包含 sharedInstance 类方法
   - Info.plist 是否配置 UIApplicationSceneManifest

2. 代码模式扫描
   - UIApplication.shared.keyWindow (Swift)
   - [UIApplication sharedApplication].keyWindow (OC)
   - UIApplication.shared.delegate?.window (Swift)
   - [UIApplication sharedApplication].delegate.window (OC)
   - AppDelegate 实例的 window 属性访问
   - window.rootViewController 链式调用
   - window.visibleViewController 链式调用
   - UNNotificationPresentationOptionAlert
   - UNAuthorizationOptionAlert
   - UIApplication.shared.statusBarStyle 设置

3. 第三方 SDK 检测
   - 初始化位置（是否在 didFinishLaunching）
   - 是否依赖 window 对象
   - 生命周期回调需求

4. UI 框架检测
   - 是否使用 QMUIKit / RxSwift / 其他 UI 框架
   - 自定义导航栏实现
   - 自定义转场动画
```

### 阶段二：方案生成（第一阶段前完成）

**目标**: 根据扫描结果生成项目特定的适配方案

**方案应包含**:
1. 文件修改清单（增/删/改）
2. 代码替换映射表（具体到文件和行号）
3. 第三方 SDK 适配建议
4. 测试验证清单
5. 风险评估

### 阶段三：代码改造（第一阶段执行）

**目标**: 执行适配方案

**执行顺序**:
1. 新增兼容工具类（统一窗口/导航访问接口）
2. 修改 AppDelegate（分离初始化方法）
3. 新增/修改 SceneDelegate
4. 批量替换全局窗口访问代码
5. 修复废弃 API 调用

### 阶段四：验证测试（贯穿两阶段）

**目标**: 确保功能完整性和向后兼容

---

## 五、各方向详细实现指南

### 方向 1: SceneDelegate 架构适配（第一/二阶段）

#### 5.1.1 判断是否需适配

**触发条件**:
- 项目需要支持 iOS 13+
- 当前未配置 SceneDelegate 或配置不完整

**检测方法**:
- 检查文件系统是否存在 SceneDelegate.swift/SceneDelegate.m
- 检查 Info.plist 中 UIApplicationSceneManifest 配置
- 检查 AppDelegate 是否包含 `application:configurationForConnectingSceneSession:`

#### 5.1.2 架构设计原则

```
┌─────────────────────────────────────────┐
│           iOS 12 及以下                  │
│  AppDelegate.window ← 直接创建           │
│       ↓                                 │
│  业务逻辑直接执行                        │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│           iOS 13+                        │
│  SceneDelegate.window ← 系统创建         │
│       ↓                                 │
│  转发到 AppDelegate.setupSceneUI()       │
│       ↓                                 │
│  执行业务逻辑                            │
└─────────────────────────────────────────┘
```

**核心要求**:
- iOS 12 路径完全保持不变
- iOS 13+ 路径通过转发复用业务逻辑
- 所有版本最终调用相同的业务方法

#### 5.1.3 需要新增的文件

| 文件 | 作用 | 必要性 |
|-----|------|-------|
| `SceneDelegate` | iOS 13+ 窗口管理、生命周期转发 | 必须 |
| `UIApplication+Extension` | 统一窗口/导航访问接口 | 推荐 |

#### 5.1.4 AppDelegate 改造要点

**改造点 1: 添加单例访问方法**
- 目的: 方便 SceneDelegate 和其他代码获取实例
- 实现: 类方法返回 shared application 的 delegate

**改造点 2: 分离 SDK 初始化方法**
- 目的: 供 iOS 12 直接调用，iOS 13+ 通过 SceneDelegate 转发调用
- 方法签名: `(application, launchOptions) -> Void`

**改造点 3: 分离 UI 设置方法**
- 目的: SceneDelegate 创建 window 后调用
- 方法签名: `(window) -> Void`
- 职责: 设置 rootViewController，初始化 SDK

**改造点 4: 添加 Scene Session 配置**
- 目的: 告知系统使用 SceneDelegate
- 方法: `application:configurationForConnectingSceneSession:options:` (OC)
- 方法: `application(_:configurationForConnecting:options:)` (Swift)

#### 5.1.5 SceneDelegate 实现要点

**职责 1: 窗口创建**
- 在 `scene(_:willConnectTo:options:)` / `scene:willConnectToSession:options:` 中创建
- 必须基于 UIWindowScene 创建

**职责 2: 业务转发**
- 调用 AppDelegate 的 UI 设置方法
- 传递创建好的 window

**职责 3: 生命周期转发**
- 所有 Scene 生命周期方法转发到 AppDelegate 对应方法
- 确保业务逻辑（如数据统计、状态保存）正常执行
- 转发事件: willEnterForeground, didEnterBackground, didBecomeActive, willResignActive

**职责 4: URL 处理转发**
- `scene(_:openURLContexts:)` 转发到 AppDelegate 的 `application(_:open:options:)`

#### 5.1.6 统一访问接口设计

**目的**: 屏蔽 iOS 版本差异，业务代码无需判断版本

**应提供的方法**:
- `mainWindow()` - 获取当前主窗口
- `visibleViewController()` - 获取当前可见页面（处理模态、导航、TabBar）
- `currentNavigationController()` - 获取当前导航控制器

**实现逻辑**:
```
if (iOS 13+) {
    从 connectedScenes 中获取活跃 Scene 的 window
} else {
    返回 AppDelegate.window
}
```

---

### 方向 2: 废弃 API 替换（第一阶段）

#### 5.2.1 窗口访问 API

| 废弃写法 | 问题 | 新写法 |
|---------|------|-------|
| `UIApplication.shared.keyWindow` | iOS 13+ 废弃，可能返回 nil | 统一访问接口 mainWindow() |
| `UIApplication.shared.delegate.window` | SceneDelegate 架构下不可靠 | 统一访问接口 mainWindow() |
| `AppDelegate.window` | iOS 13+ 不被系统维护 | 统一访问接口 mainWindow() |

**扫描规则**:

| 规则 ID | 模式 | 文件类型 | 严重程度 |
|--------|------|---------|---------|
| WINDOW-001 | `UIApplication.shared.keyWindow` | .swift, .m, .mm | Error |
| WINDOW-002 | `\[UIApplication sharedApplication\]\.keyWindow` | .m, .mm | Error |
| WINDOW-003 | `delegate\.window` | .swift, .m, .mm | Warning |
| WINDOW-004 | `AppDelegate.*\.window` | .swift, .m, .mm | Warning |
| WINDOW-005 | `\.window\.rootViewController` | .swift, .m, .mm | Warning |
| WINDOW-006 | `\.window\.visibleViewController` | .swift, .m, .mm | Warning |

#### 5.2.2 通知选项 API (iOS 26)

| 废弃枚举 | 替代枚举 | 适用版本 |
|---------|---------|---------|
| `UNNotificationPresentationOptionAlert` | `UNNotificationPresentationOptionBanner` + `UNNotificationPresentationOptionList` | iOS 26+ |
| `UNAuthorizationOptionAlert` | `UNAuthorizationOptionBanner` | iOS 26+ |

**适配逻辑**:
```
if (iOS 26+) {
    使用新枚举 (Banner | List)
} else {
    使用旧枚举 (Alert)
}
```

**扫描规则**:

| 规则 ID | 模式 | 文件类型 | 严重程度 |
|--------|------|---------|---------|
| NOTIF-001 | `UNNotificationPresentationOptionAlert` | .swift, .m, .mm | Warning |
| NOTIF-002 | `UNAuthorizationOptionAlert` | .swift, .m, .mm | Warning |

#### 5.2.3 状态栏样式 API

| 废弃写法 | 问题 | 新写法 |
|---------|------|-------|
| `UIApplication.shared.statusBarStyle = ...` | iOS 13+ 无效 | 在 ViewController 中实现 `preferredStatusBarStyle` |

**扫描规则**:

| 规则 ID | 模式 | 文件类型 | 严重程度 |
|--------|------|---------|---------|
| STATUS-001 | `statusBarStyle\s*=\s*UIStatusBarStyle` | .swift, .m, .mm | Warning |
| STATUS-002 | `UIApplication.shared.*statusBarStyle` | .swift, .m, .mm | Warning |
| STATUS-003 | `\[UIApplication sharedApplication\].*statusBarStyle` | .m, .mm | Warning |

---

### 方向 3: 液态玻璃兼容（第二阶段）

#### 5.3.1 配置策略（第一阶段）

**第一阶段策略**: 临时禁用液态玻璃，确保现有 UI 稳定

**配置项** (Info.plist):
```
UIDesignRequiresCompatibility: Boolean = true
```

**重要提醒**:
- 此配置是**临时过渡方案**，Xcode 27 发布后将失效
- 第二阶段必须完整适配 Liquid Glass，移除此配置

**扫描规则**:

| 规则 ID | 检查项 | 严重程度 | 阶段 |
|--------|-------|---------|------|
| LIQUID-001 | Info.plist 是否包含 UIDesignRequiresCompatibility | Info | 第一阶段 |
| LIQUID-002 | 第二阶段是否已移除此配置 | Warning | 第二阶段 |

#### 5.3.2 Liquid Glass 视觉适配要点

**导航系统变化**:
- 导航栏按钮自动应用液态玻璃效果
- 可能与现有自定义布局不协调
- **建议**: 检查导航栏按钮位置、大小、样式兼容性

**键盘系统变化**:
- 自带毛玻璃折射效果
- 自带圆角和阴影
- **建议**: 检查键盘附件视图、输入框位置

**TabBar 系统变化**:
- 半透明毛玻璃效果增强
- 选中态视觉风格变化
- **建议**: 检查 TabBar 图标、文字可读性

**滚动视图变化**:
- `allowsLiquidTransform` 默认开启
- 滚动时可能有新的视觉变换效果
- **建议**: 检查关键滚动页面的用户体验

#### 5.3.3 技术适配检查

**转场动画**:
- iOS 26 转场动画可被打断
- 检查自定义转场动画的鲁棒性

**Frame 设置**:
- 导航栏 Frame 可能出现异常坐标（y 可能出现负值如 -113）
- 检查手动设置 Frame 的代码

**适配建议**:
- 使用已适配 iOS 26 的 UI 框架（如 QMUIKit）
- 对自定义控件进行 Liquid Glass 下的视觉回归测试
- 重点检查与系统控件相邻的自定义 UI 元素

---

> **完整代码模板参考**：本文档中的架构和替换模式均有可直接复制到项目中的生产级代码模板，详见项目根目录 `templates/swift/` 和 `templates/objc/`。

## 六、代码替换通用模式

### 6.1 窗口访问替换

**替换模式**:
```
替换前:
    UIApplication.shared.keyWindow
    
替换后:
    UIApplication.shared.mainWindow  // 通过统一接口扩展
```

```
替换前:
    let appDelegate = UIApplication.shared.delegate as! AppDelegate
    let window = appDelegate.window
    
替换后:
    let window = UIApplication.shared.mainWindow
```

### 6.2 可见页面获取替换

**替换模式**:
```
替换前:
    let appDelegate = UIApplication.shared.delegate as! AppDelegate
    let vc = appDelegate.window?.visibleViewController
    
替换后:
    let vc = UIApplication.shared.visibleViewController
```

### 6.3 导航 Push 替换

**替换模式**:
```
替换前:
    appDelegate.navigationController?.pushViewController(vc, animated: true)
    
替换后:
    let nav = UIApplication.shared.currentNavigationController
    nav?.pushViewController(vc, animated: true)
```

### 6.4 通知选项替换

**替换模式**:
```
替换前:
    completionHandler([.alert, .sound, .badge])
    
替换后:
    if #available(iOS 26.0, *) {
        completionHandler([.banner, .list, .sound, .badge])
    } else {
        completionHandler([.alert, .sound, .badge])
    }
```

---

## 七、测试验证框架

### 7.1 第一阶段测试重点

| 测试项 | 验证点 | 测试方法 |
|-------|-------|---------|
| SDK 构建 | 使用 Xcode 26 无编译错误 | Archive 打包验证 |
| 废弃 API | 无运行时警告 | 控制台日志检查 |
| SceneDelegate | iOS 13+ 启动正常 | iOS 13/15/17 设备测试 |
| 向后兼容 | iOS 12 启动流程不变 | iOS 12 设备测试 |
| Liquid Glass 禁用 | `UIDesignRequiresCompatibility` 生效 | iOS 26 设备检查无新效果 |

### 7.2 第二阶段测试重点

| 测试项 | 验证点 | 测试方法 |
|-------|-------|---------|
| Liquid Glass 启用 | 移除配置后系统控件有新效果 | iOS 26 设备视觉检查 |
| 导航栏协调 | 自定义导航与系统效果协调 | 各页面导航栏检查 |
| 键盘适配 | 键盘样式变化后输入正常 | 各输入框测试 |
| TabBar 可读 | TabBar 文字/图标清晰可读 | 各 Tab 页面检查 |
| 滚动视图 | 滚动时无异常视觉问题 | 长列表页面测试 |

### 7.3 基础功能验证（贯穿两阶段）

| 测试项 | 验证点 | 测试方法 |
|-------|-------|---------|
| 冷启动 | App 从关闭状态启动正常 | 终止 App 后重新打开 |
| 热启动 | App 从后台恢复正常 | Home 键切出后返回 |
| 生命周期 | 前后台切换回调正确 | 日志验证回调执行 |
| 窗口获取 | 全局弹窗显示正常 | 触发 Toast/Alert |
| 页面导航 | Push/Pop 正常 | 页面间跳转测试 |

### 7.4 版本兼容验证

| 版本 | 验证点 | 优先级 | 阶段 |
|-----|-------|-------|------|
| 最低支持版本 | 原有启动流程不变 | P0 | 第一/二阶段 |
| iOS 13-15 | SceneDelegate 路径正常 | P0 | 第一/二阶段 |
| iOS 16-25 | SceneDelegate 路径正常 | P1 | 第一/二阶段 |
| iOS 26+ | 新 API 工作正常，Liquid Glass 效果正常 | P0 | 第一/二阶段 |

### 7.5 第三方 SDK 验证

| SDK 类型 | 验证点 |
|---------|-------|
| 推送 SDK | 通知接收、点击跳转、Token 获取 |
| 分享 SDK | 分享面板、回调处理 |
| 统计 SDK | 生命周期事件上报准确性 |
| 地图 SDK | 定位、地图显示 |
| 登录 SDK | 授权、回调 |

---

## 八、风险与应对

| 风险 | 等级 | 应对措施 | 阶段 |
|-----|------|---------|------|
| **2026-04-28 截止压力** | **高** | 提前规划，分阶段执行 | 第一阶段 |
| 全局替换遗漏 | 高 | 多轮扫描，关键字组合搜索，正则匹配 | 第一阶段 |
| iOS 12 兼容性破坏 | 中 | 严格版本分支，保持原路径不变 | 第一阶段 |
| 第三方 SDK 异常 | 中 | SDK 初始化位置调整，完整回归测试 | 第一阶段 |
| 生命周期事件丢失 | 高 | 确保 SceneDelegate 转发所有事件到 AppDelegate | 第一阶段 |
| 多窗口问题 | 低 | 设置 UIApplicationSupportsMultipleScenes = false | 第一阶段 |
| 通知行为改变 | 中 | iOS 26 设备专项测试通知展示 | 第一阶段 |
| **Xcode 27 强制 Liquid Glass** | **高** | 预留第二阶段排期，提前适配 | 第二阶段 |
| Liquid Glass 视觉不协调 | 中 | UI 回归测试，调整自定义控件 | 第二阶段 |
| 键盘样式变化影响布局 | 中 | 检查键盘附件视图、输入框位置 | 第二阶段 |
| 导航栏转场异常 | 中 | 充分测试各种转场场景 | 第二阶段 |

---

## 九、扫描工具设计参考

### 9.1 扫描器输入

```yaml
project_path: "项目根目录"
language: "Objective-C" | "Swift" | "Mixed"
min_ios_version: "12.0"
known_frameworks:
  - QMUIKit
  - RxSwift
  - ...
exclude_paths:
  - Pods/
  - ThirdParty/
```

### 9.2 扫描器输出

```json
{
  "scan_metadata": {
    "timestamp": "2026-04-09T14:35:00Z",
    "project_language": "Objective-C",
    "min_ios_version": "12.0",
    "total_files_scanned": 350
  },
  "architecture_analysis": {
    "has_scenedelegate": false,
    "has_shared_instance": false,
    "has_scene_manifest": false
  },
  "issues": [
    {
      "rule_id": "WINDOW-001",
      "severity": "error",
      "message": "使用废弃的 keyWindow API",
      "file": "Utils/HUD.swift",
      "line": 45,
      "column": 25,
      "match": "UIApplication.shared.keyWindow",
      "suggestion": "使用 UIApplication.shared.mainWindow"
    }
  ],
  "statistics": {
    "total_issues": 120,
    "errors": 45,
    "warnings": 75
  }
}
```

### 9.3 扫描规则定义

每个扫描规则应包含:

| 字段 | 说明 |
|-----|------|
| rule_id | 唯一标识符 |
| name | 可读描述 |
| description | 详细说明 |
| pattern | 正则表达式或 AST 查询 |
| file_extensions | 适用的文件扩展名 |
| severity | error / warning / info |
| suggestion | 修复建议描述 |
| auto_fixable | 是否支持自动替换 |
| replacement | 自动替换模板（如支持）|

### 9.4 扫描规则示例

```yaml
rules:
  - rule_id: "WINDOW-001"
    name: "使用废弃的 keyWindow"
    description: "UIApplication.keyWindow 在 iOS 13+ 已废弃"
    pattern: "UIApplication\.shared\.keyWindow"
    file_extensions: [".swift"]
    severity: "error"
    suggestion: "使用 UIApplication.shared.mainWindow"
    auto_fixable: true
    replacement: "UIApplication.shared.mainWindow"
```

---

## 十、方案生成模板

基于扫描结果，自动生成项目特定的适配方案文档:

```markdown
# [项目名] iOS 26 适配方案

## 项目概况
- 语言: [OC/Swift/Mixed]
- 最低版本: [iOS 版本]
- 扫描文件数: [数字]
- 发现问题数: [数字]
- **第一阶段截止日期**: 2026-04-28
- **第二阶段截止日期**: Xcode 27 发布前 (~2026-09)

## 第一阶段适配（SDK 构建适配）

### 截止时间
**2026年4月28日** - 苹果强制要求使用 iOS 26 SDK 构建

### 目标
- 使用 iOS 26 SDK 构建无编译错误
- 临时禁用 Liquid Glass
- 完成 SceneDelegate 基础架构迁移
- 修复所有废弃 API 调用

### 架构适配检查
- [ ] 已配置 SceneDelegate
- [ ] 已添加 sharedInstance 方法
- [ ] 已配置 UIApplicationSceneManifest

### 需要新增的文件
1. SceneDelegate - 窗口管理和生命周期转发
2. UIApplication+Extension - 统一窗口/导航访问接口

### 需要修改的文件
1. AppDelegate
   - 添加 sharedInstance 类方法
   - 分离 SDK 初始化方法
   - 分离 UI 设置方法
   - 添加 Scene Session 配置

### 代码替换清单（第一阶段）

#### 窗口访问替换
| 原代码模式 | 新代码模式 | 影响文件数 | 影响位置 |
|-----------|-----------|-----------|---------|
| ... | ... | ... | ... |

#### 通知 API 替换
| 原代码模式 | 新代码模式 | 影响文件数 | 影响位置 |
|-----------|-----------|-----------|---------|
| ... | ... | ... | ... |

### Info.plist 配置（第一阶段）
```xml
<!-- 临时禁用 Liquid Glass -->
<key>UIDesignRequiresCompatibility</key>
<true/>

<!-- SceneDelegate 配置 -->
<key>UIApplicationSceneManifest</key>
<dict>
    ...
</dict>
```

### 第一阶段测试计划
- [ ] iOS [最低版本] 冷启动正常
- [ ] iOS 13+ SceneDelegate 路径正常
- [ ] iOS 26 通知选项工作正常
- [ ] 全局弹窗显示正常
- [ ] `UIDesignRequiresCompatibility` 生效（无 Liquid Glass 效果）

---

## 第二阶段适配（Liquid Glass 完整适配）

### 截止时间
**Xcode 27 发布前** (~2026年9月) - `UIDesignRequiresCompatibility` 将失效

### 目标
- 完整适配 Liquid Glass 设计语言
- 验证所有 UI 控件在新风格下的表现
- 移除临时禁用配置

### Liquid Glass 影响检查
- [ ] 导航栏样式与系统效果协调
- [ ] 键盘样式变化后输入正常
- [ ] TabBar 文字/图标清晰可读
- [ ] 滚动视图无异常视觉问题

### 代码调整清单（第二阶段）
| 检查项 | 状态 | 备注 |
|-------|------|------|
| 自定义导航栏样式 | ... | ... |
| 键盘附件视图 | ... | ... |
| TabBar 自定义样式 | ... | ... |

### Info.plist 配置（第二阶段）
```xml
<!-- 移除临时禁用配置 -->
<!-- 删除: UIDesignRequiresCompatibility -->
```

### 第二阶段测试计划
- [ ] Liquid Glass 效果正常显示
- [ ] 导航栏视觉协调性测试
- [ ] 键盘样式变化测试
- [ ] TabBar 可读性测试
- [ ] 各页面滚动视图测试

---

## 第三方 SDK 测试（两阶段）
- [ ] [SDK 名称] - [测试点]

## 风险评估
| 风险 | 等级 | 应对措施 | 阶段 |
|-----|------|---------|------|
| ... | ... | ... | ... |

## 执行时间线
```
[当前日期] ──► [第一阶段完成] ──► 2026-04-28 ──► [第二阶段完成] ──► Xcode 27 发布
     │              │                  │               │
     ▼              ▼                  ▼               ▼
  项目扫描      SDK构建适配        强制截止        Liquid Glass适配
```

## 执行步骤
### 第一阶段
1. [步骤一]
2. [步骤二]
3. ...

### 第二阶段
1. [步骤一]
2. [步骤二]
3. ...
```

---

## 十一、执行检查清单

### 11.1 准备阶段检查清单

在开始适配前，请确认以下准备工作已完成：

| 检查项 | 状态 | 备注 |
|-------|------|------|
| 确定下次上线时间节点 | ☐ | 决定适配策略 |
| 评估团队当前开发资源 | ☐ | 决定是否可以两阶段一起完成 |
| 确认 iOS 最低支持版本 | ☐ | 影响适配方案设计 |
| 检查当前 Xcode 版本 | ☐ | 需升级至 26.0+ |
| 检查 macOS 版本 | ☐ | 需 Sequoia 15.3+ |
| 创建适配分支 | ☐ | `feature/ios26-adaptation` |
| 备份当前主分支 | ☐ | 防止意外情况 |
| 通知相关团队成员 | ☐ | 开发、测试、产品 |

---

### 11.2 第一阶段执行检查清单（2026-04-28 前必须完成）

#### 11.2.1 项目扫描
- [ ] 扫描废弃 API 调用（keyWindow 等）
- [ ] 检查 SceneDelegate 配置状态
- [ ] 统计需要修改的文件数量
- [ ] 评估第三方 SDK 影响

#### 11.2.2 架构改造
- [ ] 新增 UIApplication+Extension（统一窗口访问）
- [ ] 新增/修改 SceneDelegate
- [ ] AppDelegate 添加 sharedInstance 方法
- [ ] AppDelegate 分离 SDK 初始化方法
- [ ] AppDelegate 分离 UI 设置方法
- [ ] Info.plist 添加 UIApplicationSceneManifest
- [ ] Info.plist 添加 UIDesignRequiresCompatibility = true

#### 11.2.3 代码替换
- [ ] 替换所有 keyWindow 调用
- [ ] 替换所有 delegate.window 调用
- [ ] 替换所有 AppDelegate.window 调用
- [ ] 替换通知选项枚举（Alert → Banner/List）
- [ ] 修复状态栏样式设置（如需要）

#### 11.2.4 编译验证
- [ ] Xcode 26 编译无错误
- [ ] 无废弃 API 警告
- [ ] Archive 打包成功

#### 11.2.5 功能测试
- [ ] iOS 12 设备启动正常
- [ ] iOS 13+ 设备启动正常
- [ ] 生命周期事件正常
- [ ] 全局弹窗显示正常
- [ ] 页面导航正常
- [ ] 推送通知正常
- [ ] Liquid Glass 被禁用（iOS 26 设备无新效果）

---

### 11.3 第二阶段执行检查清单（Xcode 27 发布前必须完成）

#### 11.3.1 视觉适配
- [ ] 移除 UIDesignRequiresCompatibility 配置
- [ ] 检查导航栏与系统效果协调性
- [ ] 检查键盘样式变化影响
- [ ] 检查 TabBar 可读性
- [ ] 检查滚动视图表现

#### 11.3.2 UI 回归测试
- [ ] 所有页面导航栏显示正常
- [ ] 所有输入框键盘交互正常
- [ ] TabBar 各页面切换正常
- [ ] 长列表滚动流畅
- [ ] 模态弹窗显示正常
- [ ] 自定义控件与系统控件协调

#### 11.3.3 兼容性测试
- [ ] iOS 26+ 设备 Liquid Glass 效果正常
- [ ] 向后兼容（最低支持版本）正常

---

### 11.4 上线前最终检查清单

#### 11.4.1 代码检查
- [ ] 所有调试代码已移除
- [ ] 无敏感信息泄露
- [ ] 分支已合并到主分支/release 分支

#### 11.4.2 测试检查
- [ ] 全量功能测试通过
- [ ] 核心流程回归测试通过
- [ ] 第三方 SDK 功能验证通过

#### 11.4.3 文档检查
- [ ] 更新日志已添加
- [ ] 相关文档已更新

---

## 十二、使用流程

```
┌─────────────┐
│  项目扫描    │ ← 使用本指南定义的规则
└──────┬──────┘
       ↓
┌─────────────┐
│  生成方案    │ ← 使用方案生成模板
└──────┬──────┘
       ↓
┌─────────────┐
│  人工审核    │ ← 确认方案准确性
└──────┬──────┘
       ↓
┌─────────────┐
│  执行适配    │ ← 按方案逐步执行
└──────┬──────┘
       ↓
┌─────────────┐
│  验证测试    │ ← 使用测试验证框架
└─────────────┘
```

---

## 关键咨询点与人工介入时机

在使用本指南进行适配时，以下情况建议人工咨询和确认：

### 必须咨询的情况

| 情况 | 建议操作 |
|-----|---------|
| 不确定下次上线时间 | 与产品经理确认版本计划 |
| 废弃 API 调用超过 100 处 | 评估是否需要分批替换 |
| 使用大量自定义 UI 控件 | 评估第二阶段工作量 |
| 第三方 SDK 版本过旧 | 确认 SDK 是否支持 iOS 26 |
| 团队没有 iOS 26 设备 | 协调测试设备或模拟器方案 |

### 推荐主动确认的事项

- **分支创建**: 是否需要创建 `feature/ios26-adaptation` 分支？
- **两阶段分离**: 是否将两个阶段分开在不同分支进行？
- **测试资源**: 是否有足够的 iOS 12/13/15/17/26 测试设备？
- **回滚方案**: 如适配出现问题，回滚方案是什么？

---

**关键时间节点提醒**:

| 日期 | 事件 | 影响 |
|-----|------|------|
| **2026-04-28** | 苹果强制使用 iOS 26 SDK 构建 | 无法提交新包或更新 |
| **~2026-09** | Xcode 27 发布，Liquid Glass 强制 | `UIDesignRequiresCompatibility` 失效 |

**重要理解**:
- ❌ **Deployment Target 不需要修改**（可以保持 iOS 12/13 等）
- ❌ **用户不需要强制升级 iOS 26**（运行要求由 Deployment Target 决定）
- ✅ **仅影响新提交和更新包**（现有上架版本不受影响）
- ✅ **无宽限期**（4月28日强制执行）

**注意事项**:
1. 本指南为框架性文档，不包含具体实现代码
2. 实际项目适配需基于扫描结果生成具体方案
3. 建议先在小范围验证，确认无误后再全面推广
4. **务必为第二阶段预留足够时间**（Liquid Glass 完整适配）
5. 建议在第一阶段就考虑第二阶段的视觉影响，提前规划

---

**作者**: roder
