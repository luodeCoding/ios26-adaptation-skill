//
//  AppDelegate+Setup.m
//  iOS 26 Adaptation Template
//
//  Example AppDelegate modifications for dual-path support (iOS 12 vs iOS 13+).
//  Add these implementations to your existing AppDelegate implementation file.
//

#import "AppDelegate+Setup.h"
#import "RootViewController.h" // Replace with your actual root view controller

@implementation AppDelegate (Setup)

+ (instancetype)sharedInstance {
    return (AppDelegate *)[UIApplication sharedApplication].delegate;
}

- (void)setupApplication:(NSDictionary<UIApplicationLaunchOptionsKey, id> *)launchOptions {
    // Example: Analytics SDK setup
    // [Analytics setup];
    
    // Example: Push notification registration
    // [self registerForPushNotifications];
}

- (void)setupSceneUI:(UIWindow *)window {
    RootViewController *rootViewController = [[RootViewController alloc] init];
    UINavigationController *navController = [[UINavigationController alloc] initWithRootViewController:rootViewController];
    window.rootViewController = navController;
    [window makeKeyAndVisible];
    
    // Store reference if iOS 12 path still needs it
    if (@available(iOS 13.0, *)) {
        // iOS 13+ uses SceneDelegate.window; no need to store in AppDelegate
    } else {
        self.window = window;
    }
}

@end

#pragma mark - UIApplicationDelegate (iOS 12 path)

/*
 In your AppDelegate, keep the traditional iOS 12 launch path:
 
 - (BOOL)application:(UIApplication *)application
     didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
     
     // One-time setup
     [self setupApplication:launchOptions];
     
     if (@available(iOS 13.0, *)) {
         // iOS 13+ uses SceneDelegate for UI setup
     } else {
         // iOS 12: create window directly
         // Note: [UIScreen mainScreen] is deprecated in iOS 26 SDK but still required for iOS 12 path.
         // For iOS 13+, window is created from UIWindowScene in SceneDelegate.
         UIWindow *window = [[UIWindow alloc] initWithFrame:[[UIScreen mainScreen] bounds]];
         [self setupSceneUI:window];
     }
     
     return YES;
 }
 */

#pragma mark - Scene Session Configuration (required)

/*
 Add this to your AppDelegate to inform the system that you use SceneDelegate:
 
 - (UISceneConfiguration *)application:(UIApplication *)application
     configurationForConnectingSceneSession:(UISceneSession *)connectingSceneSession
                                    options:(UISceneConnectionOptions *)options {
     return [[UISceneConfiguration alloc] initWithName:@"Default Configuration"
                                            sessionRole:connectingSceneSession.role];
 }
 */
