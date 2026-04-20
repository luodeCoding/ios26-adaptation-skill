//
//  SceneDelegate.swift
//  iOS 26 Adaptation Template
//
//  Full SceneDelegate implementation with lifecycle and URL forwarding.
//  Assumes AppDelegate has sharedInstance(), setupApplication(launchOptions:),
//  and setupSceneUI(window:) methods.
//

import UIKit

class SceneDelegate: UIResponder, UIWindowSceneDelegate {
    
    var window: UIWindow?
    
    // MARK: - Scene Connection
    
    func scene(_ scene: UIScene, willConnectTo session: UISceneSession, options connectionOptions: UIScene.ConnectionOptions) {
        guard let windowScene = scene as? UIWindowScene else { return }
        
        // 1. Create window
        let window = UIWindow(windowScene: windowScene)
        self.window = window
        
        // 2. Forward to AppDelegate for business setup
        AppDelegate.sharedInstance()?.setupSceneUI(window: window)
        
        // 3. Handle any URL contexts that were passed at launch
        if !connectionOptions.urlContexts.isEmpty {
            handleURLContexts(connectionOptions.urlContexts)
        }
    }
    
    // MARK: - Lifecycle Forwarding
    
    func sceneDidBecomeActive(_ scene: UIScene) {
        AppDelegate.sharedInstance()?.applicationDidBecomeActive(UIApplication.shared)
    }
    
    func sceneWillResignActive(_ scene: UIScene) {
        AppDelegate.sharedInstance()?.applicationWillResignActive(UIApplication.shared)
    }
    
    func sceneWillEnterForeground(_ scene: UIScene) {
        AppDelegate.sharedInstance()?.applicationWillEnterForeground(UIApplication.shared)
    }
    
    func sceneDidEnterBackground(_ scene: UIScene) {
        AppDelegate.sharedInstance()?.applicationDidEnterBackground(UIApplication.shared)
    }
    
    func sceneDidDisconnect(_ scene: UIScene) {
        // Optional: perform cleanup when scene is discarded by the system
    }
    
    // MARK: - URL Handling Forwarding
    
    func scene(_ scene: UIScene, openURLContexts URLContexts: Set<UIOpenURLContext>) {
        handleURLContexts(URLContexts)
    }
    
    // MARK: - Private Helpers
    
    private func handleURLContexts(_ urlContexts: Set<UIOpenURLContext>) {
        guard let urlContext = urlContexts.first,
              let appDelegate = AppDelegate.sharedInstance() else { return }
        
        appDelegate.application(
            UIApplication.shared,
            open: urlContext.url,
            options: [
                UIApplication.OpenURLOptionsKey.sourceApplication: urlContext.options.sourceApplication ?? "",
                UIApplication.OpenURLOptionsKey.annotation: urlContext.options.annotation
            ]
        )
    }
}
