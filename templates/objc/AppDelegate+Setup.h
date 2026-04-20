//
//  AppDelegate+Setup.h
//  iOS 26 Adaptation Template
//
//  Example AppDelegate modifications for dual-path support (iOS 12 vs iOS 13+).
//  Add these declarations to your existing AppDelegate header.
//

#import <UIKit/UIKit.h>

NS_ASSUME_NONNULL_BEGIN

@interface AppDelegate (Setup)

/// Class method to access the shared AppDelegate instance.
+ (instancetype)sharedInstance;

/// Setup called once when the application launches.
/// Use this for one-time SDK initializations, not UI setup.
- (void)setupApplication:(nullable NSDictionary<UIApplicationLaunchOptionsKey, id> *)launchOptions;

/// Setup called when a window is ready (iOS 13+ via SceneDelegate, iOS 12 directly).
/// Use this for root view controller setup and any UI-dependent initialization.
- (void)setupSceneUI:(UIWindow *)window;

@end

NS_ASSUME_NONNULL_END
