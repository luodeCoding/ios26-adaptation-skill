#import "UITextInput+LiquidGlassAdapter.h"

@implementation UITextField (LiquidGlassAdapter)

- (void)lg_clearLiquidGlassAccessoryIfNeeded {
    if (@available(iOS 26.0, *)) {
        self.inputAccessoryView = [[UIView alloc] init];
    }
}

@end

@implementation UITextView (LiquidGlassAdapter)

- (void)lg_clearLiquidGlassAccessoryIfNeeded {
    if (@available(iOS 26.0, *)) {
        self.inputAccessoryView = [[UIView alloc] init];
    }
}

@end
