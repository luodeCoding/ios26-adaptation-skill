#import <UIKit/UIKit.h>

NS_ASSUME_NONNULL_BEGIN

@interface UINavigationBar (LiquidGlassAdapter)

/// Apply spacing fix for right bar button items only (recommended).
/// Call once during app setup, e.g. after creating your navigation controller.
///
/// ⚠️ Back button (leftBarButtonItems):
///    In most apps the system back button is acceptable under Liquid Glass.
///    Only apply left-side fixes if your design team explicitly requires it,
///    because the back button's chevron has special layout logic that may
///    conflict with manual PlatterView adjustments.
- (void)lg_applyRightBarButtonItemsFix API_AVAILABLE(ios(26.0));

/// Apply spacing fix for both left and right bar button items.
/// Only use this if your design requires the back button to also have
/// independent glass backgrounds with zero spacing.
- (void)lg_applyAllBarButtonItemsFix API_AVAILABLE(ios(26.0));

@end

@interface UINavigationController (LiquidGlassAdapter)

/// Applies right-only bar button item fix to this navigation controller's bar.
- (void)lg_applyLiquidGlassRightButtonFix API_AVAILABLE(ios(26.0));

/// Applies full bar button item fix to this navigation controller's bar.
- (void)lg_applyLiquidGlassAllButtonFix API_AVAILABLE(ios(26.0));

@end

NS_ASSUME_NONNULL_END
