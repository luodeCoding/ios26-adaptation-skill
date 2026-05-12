import UIKit

// MARK: - Keyboard Input Accessory View Liquid Glass Adapter (iOS 26+)
//
//  iOS 26 Liquid Glass applies glassmorphism effects to the keyboard's default
//  input accessory view (the toolbar above the keyboard). If your design team
//  finds this effect visually disruptive, use this adapter to clear the default
//  accessory view on iOS 26+.
//
//  ⚠️ This is an OPTIONAL adjustment. Only apply if:
//     - Your testers report the glass toolbar looks "ugly" or clashes with UI
//     - You have custom text fields / text views that should not show the effect
//     - Your design system requires a consistent non-glass appearance
//
//  Usage:
//  1. For individual text fields (e.g. in viewDidLoad or cell configuration):
//     textField.lg_clearLiquidGlassAccessoryIfNeeded()
//
//  2. In custom UITextField / UITextView subclasses, call in init or awakeFromNib:
//     override func awakeFromNib() {
//         super.awakeFromNib()
//         lg_clearLiquidGlassAccessoryIfNeeded()
//     }
//
//  3. Prefer per-control application. Global sweeping is discouraged because
//     some text inputs may legitimately need the accessory view (e.g. custom
//     toolbars with done/next buttons).

extension UITextField {

    /// Clears the default input accessory view on iOS 26+ to avoid Liquid Glass toolbar effects.
    /// Safe to call on any iOS version — no-op below iOS 26.
    func lg_clearLiquidGlassAccessoryIfNeeded() {
        if #available(iOS 26.0, *) {
            self.inputAccessoryView = UIView()
        }
    }
}

extension UITextView {

    /// Clears the default input accessory view on iOS 26+ to avoid Liquid Glass toolbar effects.
    /// Safe to call on any iOS version — no-op below iOS 26.
    func lg_clearLiquidGlassAccessoryIfNeeded() {
        if #available(iOS 26.0, *) {
            self.inputAccessoryView = UIView()
        }
    }
}
