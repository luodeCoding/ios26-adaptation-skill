#import "UINavigationBar+LiquidGlassAdapter.h"
#import <objc/runtime.h>

static const char *kLGFixModeKey = "lg_fixMode";

typedef NS_ENUM(NSInteger, LGFixMode) {
    LGFixModeRightOnly = 1,
    LGFixModeAll = 2
};

@implementation UINavigationBar (LiquidGlassAdapter)

#pragma mark - Public

- (void)lg_applyRightBarButtonItemsFix {
    if (@available(iOS 26.0, *)) {
        [self lg_swizzleLayoutSubviewsIfNeeded];
        objc_setAssociatedObject(self, kLGFixModeKey, @(LGFixModeRightOnly), OBJC_ASSOCIATION_RETAIN_NONATOMIC);
    }
}

- (void)lg_applyAllBarButtonItemsFix {
    if (@available(iOS 26.0, *)) {
        [self lg_swizzleLayoutSubviewsIfNeeded];
        objc_setAssociatedObject(self, kLGFixModeKey, @(LGFixModeAll), OBJC_ASSOCIATION_RETAIN_NONATOMIC);
    }
}

#pragma mark - Swizzling

static BOOL lg_hasSwizzled = NO;

- (void)lg_swizzleLayoutSubviewsIfNeeded {
    @synchronized (UINavigationBar.class) {
        if (lg_hasSwizzled) return;
        lg_hasSwizzled = YES;

        SEL originalSelector = @selector(layoutSubviews);
        SEL swizzledSelector = @selector(lg_layoutSubviews);

        Method originalMethod = class_getInstanceMethod(UINavigationBar.class, originalSelector);
        Method swizzledMethod = class_getInstanceMethod(UINavigationBar.class, swizzledSelector);

        if (!originalMethod || !swizzledMethod) return;

        method_exchangeImplementations(originalMethod, swizzledMethod);
    }
}

- (void)lg_layoutSubviews {
    // Call original (swizzled) implementation
    [self lg_layoutSubviews];

    if (@available(iOS 26.0, *)) {
        NSNumber *modeValue = objc_getAssociatedObject(self, kLGFixModeKey);
        if (modeValue) {
            [self lg_fixPlatterViewSpaceWithMode:(LGFixMode)modeValue.integerValue];
        }
    }
}

#pragma mark - PlatterView Fix

- (void)lg_fixPlatterViewSpaceWithMode:(LGFixMode)mode {
    NSMutableArray<UIView *> *platterViews = [NSMutableArray array];
    [self lg_collectPlatterViews:self result:platterViews];

    if (platterViews.count == 0) return;

    CGFloat navBarWidth = self.frame.size.width;
    CGFloat midX = navBarWidth / 2.0;
    CGFloat safeLeft = self.safeAreaInsets.left;
    CGFloat safeRight = 5.0;

    NSMutableArray<UIView *> *leftViews = [NSMutableArray array];
    NSMutableArray<UIView *> *rightViews = [NSMutableArray array];

    for (UIView *v in platterViews) {
        CGFloat centerX = v.frame.origin.x + v.frame.size.width / 2.0;
        if (centerX < midX) {
            [leftViews addObject:v];
        } else {
            [rightViews addObject:v];
        }
    }

    // Left side: ascending by x, pack from safeLeft toward center
    if (mode == LGFixModeAll) {
        [leftViews sortUsingComparator:^NSComparisonResult(UIView *a, UIView *b) {
            return a.frame.origin.x > b.frame.origin.x ? NSOrderedDescending : NSOrderedAscending;
        }];
        CGFloat leftX = safeLeft;
        for (UIView *v in leftViews) {
            [self lg_fixPlatterView:v toX:leftX];
            leftX += v.frame.size.width;
        }
    }

    // Right side: descending by original x (rightmost first), pack from right edge inward.
    // This preserves the visual order defined in `rightBarButtonItems` array.
    // On iOS 26, multiple right items may appear reversed compared to earlier iOS versions.
    // By sorting descending and placing from right to left, we restore the intended order.
    [rightViews sortUsingComparator:^NSComparisonResult(UIView *a, UIView *b) {
        return a.frame.origin.x < b.frame.origin.x ? NSOrderedDescending : NSOrderedAscending;
    }];
    CGFloat rightX = navBarWidth - safeRight;
    for (UIView *v in rightViews) {
        rightX -= v.frame.size.width;
        [self lg_fixPlatterView:v toX:rightX];
    }
}

- (void)lg_collectPlatterViews:(UIView *)view result:(NSMutableArray<UIView *> *)result {
    for (UIView *subview in view.subviews) {
        NSString *className = NSStringFromClass(subview.class);
        if ([className containsString:@"PlatterView"]) {
            [result addObject:subview];
        } else {
            [self lg_collectPlatterViews:subview result:result];
        }
    }
}

- (void)lg_fixPlatterView:(UIView *)platterView toX:(CGFloat)x {
    // 1. Update Leading constraints if any
    UIView *superview = platterView.superview;
    if (superview) {
        for (NSLayoutConstraint *constraint in superview.constraints) {
            if (constraint.firstItem == platterView && constraint.firstAttribute == NSLayoutAttributeLeading) {
                constraint.constant = x;
            }
            if (constraint.secondItem == platterView && constraint.secondAttribute == NSLayoutAttributeLeading) {
                constraint.constant = -x;
            }
        }
    }

    // 2. Frame fallback
    CGRect frame = platterView.frame;
    frame.origin.x = x;
    platterView.frame = frame;
}

@end

#pragma mark - UINavigationController Convenience

@implementation UINavigationController (LiquidGlassAdapter)

- (void)lg_applyLiquidGlassRightButtonFix {
    [self.navigationBar lg_applyRightBarButtonItemsFix];
}

- (void)lg_applyLiquidGlassAllButtonFix {
    [self.navigationBar lg_applyAllBarButtonItemsFix];
}

@end
