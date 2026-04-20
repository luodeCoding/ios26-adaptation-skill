//
//  NotificationAdapter.h
//  iOS 26 Adaptation Template
//
//  Helper for adapting notification options to iOS 26 deprecated API changes.
//

#import <UserNotifications/UserNotifications.h>

NS_ASSUME_NONNULL_BEGIN

@interface NotificationAdapter : NSObject

/// Presentation options for notification foreground display.
/// Replaces deprecated UNNotificationPresentationOptionAlert with Banner and List on iOS 26+.
+ (UNNotificationPresentationOptions)presentationOptions;

/// Authorization options for requesting push notification permission.
/// Replaces deprecated UNAuthorizationOptionAlert with Banner on iOS 26+.
+ (UNAuthorizationOptions)authorizationOptions;

@end

NS_ASSUME_NONNULL_END
