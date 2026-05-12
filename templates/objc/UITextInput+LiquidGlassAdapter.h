#import <UIKit/UIKit.h>

NS_ASSUME_NONNULL_BEGIN

/// Keyboard Input Accessory View Liquid Glass Adapter (iOS 26+)
///
/// iOS 26 Liquid Glass applies glassmorphism effects to the keyboard's default
/// input accessory view (the toolbar above the keyboard). If your design team
/// finds this effect visually disruptive, use this adapter to clear the default
/// accessory view on iOS 26+.
///
/// ⚠️ This is an OPTIONAL adjustment. Only apply if:
///    - Your testers report the glass toolbar looks "ugly" or clashes with UI
///    - You have custom text fields / text views that should not show the effect
///    - Your design system requires a consistent non-glass appearance
///
/// Usage:
/// 1. For individual text fields (e.g. in viewDidLoad or cell configuration):
///    [textField lg_clearLiquidGlassAccessoryIfNeeded];
///
/// 2. In custom UITextField / UITextView subclasses, call in init or awakeFromNib.
///
/// 3. Prefer per-control application. Global sweeping is discouraged because
///    some text inputs may legitimately need the accessory view.

@interface UITextField (LiquidGlassAdapter)

/// Clears the default input accessory view on iOS 26+ to avoid Liquid Glass toolbar effects.
- (void)lg_clearLiquidGlassAccessoryIfNeeded;

@end

@interface UITextView (LiquidGlassAdapter)

/// Clears the default input accessory view on iOS 26+ to avoid Liquid Glass toolbar effects.
- (void)lg_clearLiquidGlassAccessoryIfNeeded;

@end

NS_ASSUME_NONNULL_END
