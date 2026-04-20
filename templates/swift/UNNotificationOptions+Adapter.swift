//
//  UNNotificationOptions+Adapter.swift
//  iOS 26 Adaptation Template
//
//  Helper for adapting notification options to iOS 26 deprecated API changes.
//

import UserNotifications

public enum UNNotificationOptionsAdapter {
    
    /// Presentation options for notification foreground display.
    /// Replaces deprecated `.alert` with `.banner` and `.list` on iOS 26+.
    static var presentationOptions: UNNotificationPresentationOptions {
        if #available(iOS 26.0, *) {
            return [.banner, .list, .sound, .badge]
        } else {
            return [.alert, .sound, .badge]
        }
    }
    
    /// Authorization options for requesting push notification permission.
    /// Replaces deprecated `.alert` with `.banner` on iOS 26+.
    static var authorizationOptions: UNAuthorizationOptions {
        if #available(iOS 26.0, *) {
            return [.banner, .sound, .badge]
        } else {
            return [.alert, .sound, .badge]
        }
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
