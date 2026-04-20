//
//  AppDelegate+Setup.swift
//  iOS 26 Adaptation Template
//
//  Example AppDelegate modifications for dual-path support (iOS 12 vs iOS 13+).
//  Add these methods to your existing AppDelegate.
//

import UIKit

// MARK: - Example additions to your AppDelegate class

extension AppDelegate {
    
    /// Class method to access the shared AppDelegate instance.
    /// Used by SceneDelegate and other classes that need the app delegate.
    @objc class func sharedInstance() -> AppDelegate? {
        return UIApplication.shared.delegate as? AppDelegate
    }
    
    /// Setup called once when the application launches.
    /// Use this for one-time SDK initializations, not UI setup.
    @objc func setupApplication(launchOptions: [UIApplication.LaunchOptionsKey: Any]?) {
        // Example: Analytics SDK setup
        // Analytics.setup()
        
        // Example: Push notification registration
        // registerForPushNotifications()
    }
    
    /// Setup called when a window is ready (iOS 13+ via SceneDelegate, iOS 12 directly).
    /// Use this for root view controller setup and any UI-dependent initialization.
    @objc func setupSceneUI(window: UIWindow) {
        let rootViewController = RootViewController() // Replace with your root VC
        let navController = UINavigationController(rootViewController: rootViewController)
        window.rootViewController = navController
        window.makeKeyAndVisible()
        
        // Store reference if iOS 12 path still needs it
        if #available(iOS 13.0, *) {
            // iOS 13+ uses SceneDelegate.window; no need to store in AppDelegate
        } else {
            self.window = window
        }
    }
}

// MARK: - UIApplicationDelegate (iOS 12 path)

/*
 In your AppDelegate, keep the traditional iOS 12 launch path:
 
 func application(_ application: UIApplication,
                  didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
     
     // One-time setup
     setupApplication(launchOptions: launchOptions)
     
     if #available(iOS 13.0, *) {
         // iOS 13+ uses SceneDelegate for UI setup
     } else {
         // iOS 12: create window directly
         let window = UIWindow(frame: UIScreen.main.bounds)
         setupSceneUI(window: window)
     }
     
     return true
 }
 */

// MARK: - Scene Session Configuration (required)

/*
 Add this to your AppDelegate to inform the system that you use SceneDelegate:
 
 func application(_ application: UIApplication,
                  configurationForConnecting connectingSceneSession: UISceneSession,
                  options: UIScene.ConnectionOptions) -> UISceneConfiguration {
     return UISceneConfiguration(name: "Default Configuration", sessionRole: connectingSceneSession.role)
 }
 */
