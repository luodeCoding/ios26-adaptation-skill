//
//  UNNotificationOptionsAdapter.m
//  iOS 26 Adaptation Template
//

#import "UNNotificationOptionsAdapter.h"

@implementation NotificationAdapter

+ (UNNotificationPresentationOptions)presentationOptions {
    if (@available(iOS 14.0, *)) {
        return UNNotificationPresentationOptionBanner |
               UNNotificationPresentationOptionList |
               UNNotificationPresentationOptionSound |
               UNNotificationPresentationOptionBadge;
    } else {
        return UNNotificationPresentationOptionAlert |
               UNNotificationPresentationOptionSound |
               UNNotificationPresentationOptionBadge;
    }
}

+ (UNAuthorizationOptions)authorizationOptions {
    // UNAuthorizationOptionAlert is NOT deprecated and remains valid in iOS 26 SDK.
    // UNAuthorizationOptionBanner does NOT exist in the SDK.
    return UNAuthorizationOptionAlert |
           UNAuthorizationOptionSound |
           UNAuthorizationOptionBadge;
}

@end

#pragma mark - Usage Example in UNUserNotificationCenterDelegate

/*
 #import "NotificationAdapter.h"
 
 - (void)userNotificationCenter:(UNUserNotificationCenter *)center
          willPresentNotification:(UNNotification *)notification
            withCompletionHandler:(void (^)(UNNotificationPresentationOptions))completionHandler {
     completionHandler([NotificationAdapter presentationOptions]);
 }
 */

#pragma mark - Usage Example for Authorization Request

/*
 [[UNUserNotificationCenter currentNotificationCenter]
     requestAuthorizationWithOptions:[NotificationAdapter authorizationOptions]
                   completionHandler:^(BOOL granted, NSError * _Nullable error) {
     // Handle result
 }];
 */
