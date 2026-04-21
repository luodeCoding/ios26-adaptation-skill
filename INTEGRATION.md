# iOS 26 Adaptation — 快速集成指南

> 本文档说明如何将本仓库作为本地文件夹引用到主项目中。

---

## 核心思路

本仓库**不作为 CocoaPods / SPM 包使用**，而是作为**本地文件夹**直接引用到主项目 Xcode 中。

**好处：**
- 所有文件都在本地磁盘，改完立刻编译验证
- 在 Xcode 里修改 skill 项目文件 = 直接修改本地 git 仓库
- 随时可进入 skill 项目目录提交到 GitHub
- 无需复制文件、无需等待同步

---

## 步骤

### 1. 下载本仓库到本地

```bash
# 推荐：git clone（方便后续更新和提交）
git clone https://github.com/luodeCoding/ios26-adaptation-skill.git

# 或者下载 ZIP 解压
```

记住这个路径，比如 `~/Projects/ios26-adaptation-skill/`。

### 2. 在 Xcode 中引用为 Folder Reference

1. 打开你的**主项目** Xcode
2. 右键点击项目导航栏中的项目根目录 → **Add Files to "YourProject"...**
3. 找到你下载的 `ios26-adaptation-skill` 文件夹
4. ⚠️ **关键**：选择 **"Create folder references"**（蓝色文件夹图标）
   
   <img src="https://i.imgur.com/placeholder.png" width="400">
   
5. 勾选你的 app target
6. 点击 **Add**

完成后，你会在 Xcode 中看到一个**蓝色文件夹** `ios26-adaptation-skill/`，里面包含所有模板、脚本和文档。

### 3. 将需要的模板加入编译目标

Folder Reference 中的文件**不会自动编译**。把需要的模板文件加入你的 target：

**Swift 项目：**

从 `ios26-adaptation-skill/templates/swift/` 中选择：
- `UIApplication+MainWindow.swift` — 统一窗口访问
- `SceneDelegate.swift` — SceneDelegate 实现
- `AppDelegate+Setup.swift` — AppDelegate 改造参考
- `UNNotificationOptions+Adapter.swift` — 通知选项适配

右键 → **Add Files to "YourProject"...** → 选择 **"Create groups"** + 勾选 target。

这些文件会以**黄色文件夹**（group）形式加入，会被编译进你的 app。

> 💡 **小技巧**：你也可以不加入 target，只是参考模板代码，然后在自己的项目文件里手写。这样更灵活。

### 4. 修改模板适配你的项目

| 需要修改的地方 | 说明 |
|---------------|------|
| `RootViewController` | 替换为你项目的根视图控制器 |
| `AppDelegate.sharedInstance()` | 如果已有类似方法，合并即可 |
| `setupSceneUI(window:)` | 根据你的 UI 结构调整 |

### 5. 修改 Info.plist

添加 SceneDelegate 配置和 Liquid Glass 临时禁用：

```xml
<!-- 临时禁用 Liquid Glass -->
<key>UIDesignRequiresCompatibility</key>
<true/>

<!-- SceneDelegate 配置 -->
<key>UIApplicationSceneManifest</key>
<dict>
    <key>UIApplicationSupportsMultipleScenes</key>
    <false/>
    <key>UISceneConfigurations</key>
    <dict>
        <key>UIWindowSceneSessionRoleApplication</key>
        <array>
            <dict>
                <key>UISceneConfigurationName</key>
                <string>Default Configuration</string>
                <key>UISceneDelegateClassName</key>
                <string>SceneDelegate</string>
            </dict>
        </array>
    </dict>
</dict>
```

### 6. 运行扫描脚本

```bash
python3 ~/Projects/ios26-adaptation-skill/scripts/ios26-scanner.py /path/to/your/ios/project
```

---

## 工作流：遇到问题时的快速调整

```
主项目编译报错
    ↓
查看 ios26-adaptation-skill/ 中的模板或文档
    ↓
直接在 Xcode 里修改 skill 项目中的文件（蓝色文件夹）
    ↓
⌘+B 编译验证，修改即时生效
    ↓
验证通过后，提交 skill 项目到 GitHub
    ↓
cd ~/Projects/ios26-adaptation-skill
git add .
git commit -m "fix: xxx"
git push
```

---

## 常见问题

**Q: Folder Reference 和 Group 有什么区别？**

| | Folder Reference（蓝色） | Group（黄色） |
|--|------------------------|--------------|
| 与磁盘关系 | 实时同步文件夹内容 | 独立管理，可重命名/移动 |
| 文件编译 | ❌ 不编译 | ✅ 编译 |
| 用途 | 引用外部资源、文档 | 项目源代码 |

**Q: 为什么模板文件要再用 Group 加入一次？**

因为 Folder Reference 只是引用，不编译。需要编译的代码文件必须用 Group 方式加入 target。

**Q: 我在 Xcode 里改了蓝色文件夹里的文件，会同步到 GitHub 吗？**

会。因为蓝色文件夹直接指向本地 git 仓库的文件夹。改完后进入该目录提交即可：

```bash
cd ~/Projects/ios26-adaptation-skill
git status  # 能看到你的修改
git add .
git commit -m "fix: xxx"
git push
```

**Q: 团队协作时别人也需要这样设置吗？**

是的。每个开发者都需要：
1. `git clone` 本仓库到本地
2. 在 Xcode 中用同样方式引用（路径可以不同，Xcode 会记录相对路径）

**Q: 适配完成后怎么移除？**

直接删除 Xcode 中的蓝色文件夹引用即可。不会留下任何残留。
