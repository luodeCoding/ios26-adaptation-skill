//
//  UIApplication+Extension.swift
//  iOS 26 Adaptation Template
//
//  Unified window and navigation access interface for SceneDelegate architecture.
//  Compatible with iOS 12+ (iOS 12 uses AppDelegate.window, iOS 13+ uses connectedScenes).
//

import UIKit

public extension UIApplication {
    
    /// Returns the current key window, compatible with both iOS 12 and iOS 13+.
    var mainWindow: UIWindow? {
        if #available(iOS 13.0, *) {
            return connectedScenes
                .compactMap { $0 as? UIWindowScene }
                .first(where: { $0.activationState == .foregroundActive })?
                .windows
                .first(where: \.isKeyWindow)
                ?? connectedScenes
                .compactMap { $0 as? UIWindowScene }
                .first?
                .windows
                .first(where: \.isKeyWindow)
                ?? windows.first(where: \.isKeyWindow)
        } else {
            return delegate?.window ?? nil
        }
    }
    
    /// Returns the topmost visible view controller from the current window.
    var visibleViewController: UIViewController? {
        guard let rootViewController = mainWindow?.rootViewController else {
            return nil
        }
        return findTopViewController(from: rootViewController)
    }
    
    /// Returns the current active navigation controller, if any.
    var currentNavigationController: UINavigationController? {
        return visibleViewController?.navigationController
    }
    
    // MARK: - Private Helpers
    
    private func findTopViewController(from root: UIViewController) -> UIViewController {
        if let presented = root.presentedViewController {
            return findTopViewController(from: presented)
        }
        if let nav = root as? UINavigationController,
           let visible = nav.visibleViewController {
            return findTopViewController(from: visible)
        }
        if let tab = root as? UITabBarController,
           let selected = tab.selectedViewController {
            return findTopViewController(from: selected)
        }
        return root
    }
}
