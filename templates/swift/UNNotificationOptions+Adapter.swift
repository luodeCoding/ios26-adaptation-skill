//
//  UNNotificationOptions+Adapter.swift
//  iOS 26 Adaptation Template
//
//  Helper for adapting notification options to iOS 26 deprecated API changes.
//

import UserNotifications

public enum UNNotificationOptionsAdapter {
    
    /// Presentation options for notification foreground display.
    /// `.alert` was deprecated in iOS 14.0; use `.banner` and `.list` on iOS 14+.
    static var presentationOptions: UNNotificationPresentationOptions {
        if #available(iOS 14.0, *) {
            return [.banner, .list, .sound, .badge]
        } else {
            return [.alert, .sound, .badge]
        }
    }
    
    /// Authorization options for requesting push notification permission.
    /// `.alert` is NOT deprecated and remains valid in iOS 26 SDK.
    /// `.banner` does NOT exist for UNAuthorizationOptions.
    static var authorizationOptions: UNAuthorizationOptions {
        return [.alert, .sound, .badge]
    }
}

// MARK: - Usage Example in UNUserNotificationCenterDelegate

/*
 extension AppDelegate: UNUserNotificationCenterDelegate {
     
     func userNotificationCenter(
         _ center: UNUserNotificationCenter,
         willPresent notification: UNNotification,
         withCompletionHandler completionHandler: @escaping (UNNotificationPresentationOptions) -> Void
     ) {
         completionHandler(UNNotificationOptionsAdapter.presentationOptions)
     }
 }
 */

// MARK: - Usage Example for Authorization Request

/*
 UNUserNotificationCenter.current().requestAuthorization(
     options: UNNotificationOptionsAdapter.authorizationOptions
 ) { granted, error in
     // Handle result
 }
 */
