import UIKit

// MARK: - UINavigationBar Liquid Glass Button Adapter (iOS 26+)
//
//  Usage:
//  1. Call `applyLiquidGlassCompatibility()` in your navigation controller setup
//     or in `application(_:didFinishLaunchingWithOptions:)` after window creation.
//  2. For right-side buttons only (recommended), use `applyRightBarButtonItemsFix()`.
//  3. For both left and right, use `applyAllBarButtonItemsFix()`.
//
//  ⚠️ Back button (leftBarButtonItems):
//     In most apps the system back button is acceptable under Liquid Glass.
//     Only apply left-side fixes if your design team explicitly requires it,
//     because the back button's chevron has special layout logic that may
//     conflict with manual PlatterView adjustments.
//
//  ⚠️ Right item order on iOS 26:
//     When multiple `rightBarButtonItems` are used with `hidesSharedBackground`,
//     iOS 26 may render them in reverse order compared to iOS 25 and earlier.
//     The fix below preserves the original array order by re-laying them
//     from right to left based on the `rightBarButtonItems` array sequence.

extension UINavigationBar {

    /// Apply spacing fix for right bar button items only (recommended).
    /// Call once during app setup.
    func applyRightBarButtonItemsFix() {
        guard #available(iOS 26.0, *) else { return }
        swizzleLayoutSubviewsIfNeeded()
        // Store flag so layoutSubviews knows which mode to use
        objc_setAssociatedObject(self, &AssociatedKeys.fixMode, FixMode.rightOnly, .OBJC_ASSOCIATION_RETAIN_NONATOMIC)
    }

    /// Apply spacing fix for both left and right bar button items.
    /// Only use this if your design requires the back button to also have
    /// independent glass backgrounds with zero spacing.
    func applyAllBarButtonItemsFix() {
        guard #available(iOS 26.0, *) else { return }
        swizzleLayoutSubviewsIfNeeded()
        objc_setAssociatedObject(self, &AssociatedKeys.fixMode, FixMode.all, .OBJC_ASSOCIATION_RETAIN_NONATOMIC)
    }

    // MARK: - Swizzling

    private static var hasSwizzled = false

    private func swizzleLayoutSubviewsIfNeeded() {
        guard !Self.hasSwizzled else { return }
        Self.hasSwizzled = true

        let originalSelector = #selector(layoutSubviews)
        let swizzledSelector = #selector(lg_layoutSubviews)

        guard let originalMethod = class_getInstanceMethod(UINavigationBar.self, originalSelector),
              let swizzledMethod = class_getInstanceMethod(UINavigationBar.self, swizzledSelector) else {
            return
        }

        method_exchangeImplementations(originalMethod, swizzledMethod)
    }

    @objc private func lg_layoutSubviews() {
        // Call original (swizzled) implementation
        lg_layoutSubviews()

        guard #available(iOS 26.0, *) else { return }
        guard let mode = objc_getAssociatedObject(self, &AssociatedKeys.fixMode) as? FixMode else { return }

        fixPlatterViewSpace(mode: mode)
    }

    // MARK: - PlatterView Fix

    private func fixPlatterViewSpace(mode: FixMode) {
        var platterViews: [UIView] = []
        collectPlatterViews(in: self, result: &platterViews)
        guard platterViews.count > 0 else { return }

        let navBarWidth = bounds.width
        let midX = navBarWidth / 2.0
        let safeLeft = safeAreaInsets.left
        let safeRight: CGFloat = 5.0  // right padding to avoid screen edge

        var leftViews: [UIView] = []
        var rightViews: [UIView] = []

        for v in platterViews {
            let centerX = v.frame.minX + v.frame.width / 2.0
            if centerX < midX {
                leftViews.append(v)
            } else {
                rightViews.append(v)
            }
        }

        // Left side: ascending by x, pack from safeLeft toward center
        if mode == .all {
            leftViews.sort { $0.frame.minX < $1.frame.minX }
            var leftX = safeLeft
            for v in leftViews {
                fixPlatterView(v, toX: leftX)
                leftX += v.frame.width
            }
        }

        // Right side: descending by original x (rightmost first), pack from right edge inward
        // This preserves the visual order defined in `rightBarButtonItems` array.
        // On iOS 26, multiple right items may appear reversed compared to earlier iOS versions.
        // By sorting descending and placing from right to left, we restore the intended order.
        rightViews.sort { $0.frame.minX > $1.frame.minX }
        var rightX = navBarWidth - safeRight
        for v in rightViews {
            rightX -= v.frame.width
            fixPlatterView(v, toX: rightX)
        }
    }

    private func collectPlatterViews(in view: UIView, result: inout [UIView]) {
        for subview in view.subviews {
            let className = String(describing: type(of: subview))
            if className.contains("PlatterView") {
                result.append(subview)
            } else {
                collectPlatterViews(in: subview, result: &result)
            }
        }
    }

    private func fixPlatterView(_ platterView: UIView, toX x: CGFloat) {
        // 1. Update Leading constraints if any
        if let superview = platterView.superview {
            for constraint in superview.constraints {
                if (constraint.firstItem as? UIView) == platterView && constraint.firstAttribute == .leading {
                    constraint.constant = x
                }
                if (constraint.secondItem as? UIView) == platterView && constraint.secondAttribute == .leading {
                    constraint.constant = -x  // trailing = leading relation
                }
            }
        }

        // 2. Frame fallback
        var frame = platterView.frame
        frame.origin.x = x
        platterView.frame = frame
    }

    // MARK: - Associated Objects

    private enum FixMode: Int {
        case rightOnly = 1
        case all = 2
    }

    private struct AssociatedKeys {
        static var fixMode = "lg_fixMode"
    }
}

// MARK: - Convenience for UINavigationController

extension UINavigationController {

    /// Applies right-only bar button item fix to this navigation controller's bar.
    func applyLiquidGlassRightButtonFix() {
        navigationBar.applyRightBarButtonItemsFix()
    }

    /// Applies full bar button item fix to this navigation controller's bar.
    /// Only use if your design explicitly requires back-button styling changes.
    func applyLiquidGlassAllButtonFix() {
        navigationBar.applyAllBarButtonItemsFix()
    }
}
