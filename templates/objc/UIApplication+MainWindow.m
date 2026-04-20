//
//  UIApplication+MainWindow.m
//  iOS 26 Adaptation Template
//

#import "UIApplication+MainWindow.h"

@implementation UIApplication (Extension)

- (nullable UIWindow *)mainWindow {
    if (@available(iOS 13.0, *)) {
        for (UIScene *scene in self.connectedScenes) {
            if ([scene isKindOfClass:[UIWindowScene class]] && scene.activationState == UISceneActivationStateForegroundActive) {
                UIWindowScene *windowScene = (UIWindowScene *)scene;
                for (UIWindow *window in windowScene.windows) {
                    if (window.isKeyWindow) {
                        return window;
                    }
                }
            }
        }
        
        for (UIScene *scene in self.connectedScenes) {
            if ([scene isKindOfClass:[UIWindowScene class]]) {
                UIWindowScene *windowScene = (UIWindowScene *)scene;
                for (UIWindow *window in windowScene.windows) {
                    if (window.isKeyWindow) {
                        return window;
                    }
                }
            }
        }
        
        for (UIWindow *window in self.windows) {
            if (window.isKeyWindow) {
                return window;
            }
        }
        return nil;
    } else {
        return self.delegate.window;
    }
}

- (nullable UIViewController *)visibleViewController {
    UIViewController *rootViewController = self.mainWindow.rootViewController;
    if (!rootViewController) {
        return nil;
    }
    return [self findTopViewControllerFrom:rootViewController];
}

- (nullable UINavigationController *)currentNavigationController {
    return self.visibleViewController.navigationController;
}

#pragma mark - Private Helpers

- (UIViewController *)findTopViewControllerFrom:(UIViewController *)root {
    if (root.presentedViewController) {
        return [self findTopViewControllerFrom:root.presentedViewController];
    }
    if ([root isKindOfClass:[UINavigationController class]]) {
        UINavigationController *nav = (UINavigationController *)root;
        if (nav.visibleViewController) {
            return [self findTopViewControllerFrom:nav.visibleViewController];
        }
    }
    if ([root isKindOfClass:[UITabBarController class]]) {
        UITabBarController *tab = (UITabBarController *)root;
        if (tab.selectedViewController) {
            return [self findTopViewControllerFrom:tab.selectedViewController];
        }
    }
    return root;
}

@end
