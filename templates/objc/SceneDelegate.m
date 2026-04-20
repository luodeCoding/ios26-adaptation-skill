//
//  SceneDelegate.m
//  iOS 26 Adaptation Template
//
//  Full SceneDelegate implementation with lifecycle and URL forwarding.
//  Assumes AppDelegate has sharedInstance, setupApplication: and setupSceneUI: methods.
//

#import "SceneDelegate.h"
#import "AppDelegate.h"

@implementation SceneDelegate

#pragma mark - Scene Connection

- (void)scene:(UIScene *)scene willConnectToSession:(UISceneSession *)session options:(UISceneConnectionOptions *)connectionOptions {
    if (![scene isKindOfClass:[UIWindowScene class]]) return;
    
    UIWindowScene *windowScene = (UIWindowScene *)scene;
    UIWindow *window = [[UIWindow alloc] initWithWindowScene:windowScene];
    self.window = window;
    
    // Forward to AppDelegate for business setup
    [[AppDelegate sharedInstance] setupSceneUI:window];
    
    // Handle any URL contexts that were passed at launch
    if (connectionOptions.URLContexts.count > 0) {
        [self handleURLContexts:connectionOptions.URLContexts];
    }
}

#pragma mark - Lifecycle Forwarding

- (void)sceneDidBecomeActive:(UIScene *)scene {
    [[AppDelegate sharedInstance] applicationDidBecomeActive:[UIApplication sharedApplication]];
}

- (void)sceneWillResignActive:(UIScene *)scene {
    [[AppDelegate sharedInstance] applicationWillResignActive:[UIApplication sharedApplication]];
}

- (void)sceneWillEnterForeground:(UIScene *)scene {
    [[AppDelegate sharedInstance] applicationWillEnterForeground:[UIApplication sharedApplication]];
}

- (void)sceneDidEnterBackground:(UIScene *)scene {
    [[AppDelegate sharedInstance] applicationDidEnterBackground:[UIApplication sharedApplication]];
}

- (void)sceneDidDisconnect:(UIScene *)scene {
    // Optional: perform cleanup when scene is discarded by the system
}

#pragma mark - URL Handling Forwarding

- (void)scene:(UIScene *)scene openURLContexts:(NSSet<UIOpenURLContext *> *)URLContexts {
    [self handleURLContexts:URLContexts];
}

#pragma mark - Private Helpers

- (void)handleURLContexts:(NSSet<UIOpenURLContext *> *)URLContexts {
    UIOpenURLContext *urlContext = URLContexts.anyObject;
    if (!urlContext) return;
    
    AppDelegate *appDelegate = [AppDelegate sharedInstance];
    if (!appDelegate) return;
    
    NSDictionary *options = @{
        UIApplicationOpenURLOptionsSourceApplicationKey: urlContext.options.sourceApplication ?: @"",
        UIApplicationOpenURLOptionsAnnotationKey: urlContext.options.annotation ?: [NSNull null]
    };
    
    [appDelegate application:[UIApplication sharedApplication]
                     openURL:urlContext.URL
                     options:options];
}

@end
