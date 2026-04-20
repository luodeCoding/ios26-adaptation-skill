//
//  UIApplication+MainWindow.h
//  iOS 26 Adaptation Template
//
//  Unified window and navigation access interface for SceneDelegate architecture.
//  Compatible with iOS 12+ (iOS 12 uses AppDelegate.window, iOS 13+ uses connectedScenes).
//

#import <UIKit/UIKit.h>

NS_ASSUME_NONNULL_BEGIN

@interface UIApplication (Extension)

/// Returns the current key window, compatible with both iOS 12 and iOS 13+.
- (nullable UIWindow *)mainWindow;

/// Returns the topmost visible view controller from the current window.
- (nullable UIViewController *)visibleViewController;

/// Returns the current active navigation controller, if any.
- (nullable UINavigationController *)currentNavigationController;

@end

NS_ASSUME_NONNULL_END
