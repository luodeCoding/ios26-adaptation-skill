//
//  AppDelegate.swift
//  iOS 26 Adaptation Template — Pure Swift Project
//
//  Simplified AppDelegate for Swift-only projects migrating to SceneDelegate.
//  No @objc annotations. Uses static let shared instead of sharedInstance.
//

import UIKit

@main
class AppDelegate: UIResponder, UIApplicationDelegate {
    
    /// Singleton access for SceneDelegate forwarding and app-wide access.
    /// For Swift-only projects, use static let shared (no @objc needed).
    static let shared: AppDelegate = UIApplication.shared.delegate as! AppDelegate
    
    var window: UIWindow?
    
    private var launchOptions: [UIApplication.LaunchOptionsKey: Any]?

    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        self.launchOptions = launchOptions
        
        // iOS 13+ window creation is handled by SceneDelegate
        // iOS 12 fallback: create window here
        if #available(iOS 13.0, *) {
            // SceneDelegate will create the window
        } else {
            let window = UIWindow(frame: UIScreen.main.bounds)
            self.window = window
            setupSceneUI(window: window)
        }
        
        return true
    }
    
    func application(_ application: UIApplication, configurationForConnecting connectingSceneSession: UISceneSession, options: UIScene.ConnectionOptions) -> UISceneConfiguration {
        let configuration = UISceneConfiguration(name: nil, sessionRole: connectingSceneSession.role)
        if #available(iOS 13.0, *) {
            configuration.delegateClass = SceneDelegate.self
        }
        return configuration
    }
    
    /// UI setup entry point called by both AppDelegate (iOS 12) and SceneDelegate (iOS 13+)
    func setupSceneUI(window: UIWindow?) {
        self.window = window
        window?.backgroundColor = .white
        window?.makeKeyAndVisible()
        
        setupApplication()
        
        // Configure your root view controller here
        // window?.rootViewController = YourRootViewController()
    }
    
    /// One-time application initialization (networking, third-party SDKs, etc.)
    func setupApplication() {
        // Configure networking, analytics, push notifications, etc.
    }
    
    // MARK: - URL Handling
    
    func application(_ app: UIApplication, open url: URL, options: [UIApplication.OpenURLOptionsKey : Any] = [:]) -> Bool {
        // Handle deep links / URL schemes
        return true
    }
    
    // MARK: - Lifecycle
    
    func applicationWillEnterForeground(_ application: UIApplication) {}
    
    func applicationDidEnterBackground(_ application: UIApplication) {}
}
