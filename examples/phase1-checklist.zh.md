# 第一阶段检查清单：SDK 构建适配

> **截止日期**: 2026年4月28日  
> **目标**: 使用 iOS 26 SDK 构建，保持现有 UI 不变

---

## 适配前准备

### 环境检查
- [ ] Xcode 版本为 26.0 或更高
- [ ] macOS 版本为 Sequoia 15.3 或更高
- [ ] iOS 26 SDK 可用

### 策略决策
- [ ] 确定下次发布日期
- [ ] 选择适配策略 (A/B/C)
- [ ] 创建适配分支: `feature/ios26-adaptation`
- [ ] 通知团队成员

---

## 项目扫描

### 自动化扫描
- [ ] 在项目根目录运行 `scripts/ios26-scanner.py`
- [ ] 审阅扫描报告（错误和警告）
- [ ] 如有需要，排除 `Pods/` 等非项目目录

### 废弃 API 扫描（手动或复核）
- [ ] 扫描 `keyWindow` 使用情况
- [ ] 扫描 `delegate.window` 使用情况
- [ ] 扫描 `AppDelegate.window` 使用情况
- [ ] 扫描通知选项 Alert
- [ ] 扫描状态栏样式设置

### 架构扫描
- [ ] 检查 SceneDelegate 是否存在
- [ ] 检查 AppDelegate `sharedInstance` 方法
- [ ] 检查 Info.plist `UIApplicationSceneManifest`
- [ ] 列出所有需要修改的文件

### 第三方 SDK 扫描
- [ ] 列出所有 SDK 及其版本
- [ ] 检查 SDK iOS 26 兼容性
- [ ] 识别需要更新的 SDK

---

## 实施阶段

### 新增文件
- [ ] 创建 `UIApplication+Extension`（统一窗口访问）
- [ ] 创建 `SceneDelegate`（如果不存在）

### AppDelegate 修改
- [ ] 添加 `sharedInstance` 类方法
- [ ] 创建 `setupApplication(launchOptions:)` 方法
- [ ] 创建 `setupSceneUI(window:)` 方法
- [ ] 添加 Scene Session 配置
- [ ] 分离 iOS 12 和 iOS 13+ 的启动路径

### SceneDelegate 实现
- [ ] 实现 `willConnectTo` 并创建窗口
- [ ] 转发到 AppDelegate 进行业务设置
- [ ] 实现生命周期转发（所有 6 个方法）
- [ ] 实现 URL 处理转发

### 全局代码替换
- [ ] 替换所有 `keyWindow` 调用
- [ ] 替换所有 `delegate.window` 调用
- [ ] 替换所有 `AppDelegate.window` 调用
- [ ] 更新基于窗口的导航
- [ ] 更新全局弹窗显示逻辑

### 通知 API 更新
- [ ] 更新 `willPresentNotification` 完成处理程序
- [ ] 更新 `requestAuthorization` 选项
- [ ] 添加 `@available(iOS 26.0, *)` 版本检查

### Info.plist 配置
- [ ] 添加 `UIDesignRequiresCompatibility` = true
- [ ] 添加 `UIApplicationSceneManifest` 配置
- [ ] 验证 `UISceneDelegateClassName` 指向 SceneDelegate

---

## 编译验证

### 构建检查
- [ ] 项目使用 iOS 26 SDK 构建
- [ ] 无编译错误
- [ ] 无废弃 API 警告
- [ ] Archive 打包成功

### 静态分析
- [ ] 无分析器警告
- [ ] 无静态分析错误

---

## 测试

### 设备测试
- [ ] 在最低支持 iOS 版本设备上测试
- [ ] 在 iOS 13/14 设备上测试
- [ ] 在 iOS 15/16 设备上测试
- [ ] 在 iOS 17 设备上测试
- [ ] 在 iOS 26 设备上测试

### 启动测试
- [ ] 冷启动在所有版本上正常工作
- [ ] 热启动在所有版本上正常工作
- [ ] 从推送通知启动正常
- [ ] 从深度链接启动正常

### 生命周期测试
- [ ] 前后台切换正常
- [ ] 应用生命周期事件正确触发
- [ ] Scene 生命周期事件正确触发

### 窗口访问测试
- [ ] 全局 Toast 显示正常
- [ ] 全局 Alert 显示正常
- [ ] 加载指示器显示正常
- [ ] 操作表显示正常

### 导航测试
- [ ] Push 导航正常
- [ ] Pop 导航正常
- [ ] 模态展示正常
- [ ] 模态关闭正常
- [ ] TabBar 切换正常

### 功能测试
- [ ] 推送通知正常
- [ ] 深度链接正常
- [ ] 分享功能正常
- [ ] 相机/照片访问正常
- [ ] 定位服务正常

### Liquid Glass 验证
- [ ] 应用不显示 Liquid Glass 效果
- [ ] UI 与适配前保持一致
- [ ] 系统控件无视觉变化

---

## 文档

- [ ] 更新 CHANGELOG
- [ ] 根据需要更新 README
- [ ] 记录任何变通实现方案
- [ ] 为版本特定逻辑添加代码注释

---

## 发布前

- [ ] 完成所有检查清单项
- [ ] 通过代码审查
- [ ] 获得 QA 签字
- [ ] 获得产品经理批准
- [ ] 分支合并到 main/release 分支

---

## 发布后监控

- [ ] 监控崩溃报告
- [ ] 监控用户反馈
- [ ] 检查应用商店评论反馈
- [ ] 验证分析事件是否正常触发

---

**作者**: roder
