#!/usr/bin/env python3
"""Generate cover images and diagrams for iOS 26 adaptation skill."""

from PIL import Image, ImageDraw, ImageFont
import os

# Font setup
def get_font(size, bold=False):
    """Try to find a suitable font with CJK support."""
    candidates = [
        "/System/Library/AssetsV2/com_apple_MobileAsset_Font7/3419f2a427639ad8c8e139149a287865a90fa17e.asset/AssetData/PingFang.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        "/System/Library/Fonts/PingFang.ttc",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                if bold:
                    return ImageFont.truetype(path, size, index=2)  # Semibold
                return ImageFont.truetype(path, size, index=1)  # Regular
            except Exception:
                try:
                    return ImageFont.truetype(path, size)
                except Exception:
                    continue
    return ImageFont.load_default()

# Colors
BG_TOP = (30, 40, 80)
BG_BOTTOM = (80, 40, 120)
ACCENT = (0, 200, 255)
WHITE = (255, 255, 255)
GRAY = (180, 180, 200)
GREEN = (50, 200, 100)
ORANGE = (255, 150, 50)
RED = (255, 80, 80)

def draw_gradient_bg(draw, width, height, top_color, bottom_color):
    """Draw vertical gradient background."""
    for y in range(height):
        ratio = y / height
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    """Draw rounded rectangle."""
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

# ============== Cover Image ==============
def generate_cover(filename, title, subtitle, platform):
    W, H = 1200, 600
    img = Image.new("RGB", (W, H), BG_TOP)
    draw = ImageDraw.Draw(img)
    draw_gradient_bg(draw, W, H, BG_TOP, BG_BOTTOM)

    # Decorative circles
    draw.ellipse([800, -100, 1100, 200], outline=(100, 80, 160), width=3)
    draw.ellipse([900, 400, 1200, 700], outline=(80, 100, 160), width=2)
    draw.ellipse([-100, 300, 200, 600], outline=(100, 80, 160), width=2)

    # Platform badge
    font_badge = get_font(20)
    badge_text = f"{platform} | iOS 26 Adaptation"
    draw.rounded_rectangle([60, 40, 60 + len(badge_text) * 22, 80], radius=20, fill=(255, 255, 255, 30))
    draw.text((75, 45), badge_text, fill=ACCENT, font=font_badge)

    # Main title
    font_title = get_font(64, bold=True)
    # Wrap title if too long
    lines = []
    if len(title) > 14:
        mid = len(title) // 2
        lines = [title[:mid], title[mid:]]
    else:
        lines = [title]

    y = 180
    for line in lines:
        draw.text((60, y), line, fill=WHITE, font=font_title)
        y += 90

    # Subtitle
    font_sub = get_font(32)
    draw.text((60, y + 20), subtitle, fill=GRAY, font=font_sub)

    # Decorative line
    draw.rectangle([60, y + 90, 300, y + 95], fill=ACCENT)

    # Bottom info
    font_info = get_font(22)
    draw.text((60, 520), "GitHub: luodeCoding/ios26-adaptation-skill", fill=GRAY, font=font_info)
    draw.text((60, 555), "Last Updated: 2026-05-06", fill=GRAY, font=font_info)

    # Right side decorative blocks
    blocks = [
        ("20+", "Scanner Rules"),
        ("3", "Language Templates"),
        ("15", "QA Gaps Fixed"),
    ]
    bx, by = 850, 200
    for num, label in blocks:
        draw.rounded_rectangle([bx, by, bx + 280, by + 90], radius=12, fill=(255, 255, 255, 20))
        font_num = get_font(42, bold=True)
        font_label = get_font(18)
        draw.text((bx + 20, by + 10), num, fill=ACCENT, font=font_num)
        draw.text((bx + 20, by + 60), label, fill=GRAY, font=font_label)
        by += 110

    img.save(filename, quality=95)
    print(f"Generated: {filename}")

# ============== Phase Flow Diagram ==============
def generate_phase_flow(filename):
    W, H = 1200, 500
    img = Image.new("RGB", (W, H), (245, 247, 250))
    draw = ImageDraw.Draw(img)

    font_title = get_font(36, bold=True)
    font_header = get_font(28, bold=True)
    font_text = get_font(20)
    font_date = get_font(18)

    draw.text((60, 30), "iOS 26 两阶段适配流程", fill=(40, 40, 60), font=font_title)
    draw.rectangle([60, 85, 200, 88], fill=ACCENT)

    # Phase 1 box
    p1_x, p1_y = 60, 120
    draw.rounded_rectangle([p1_x, p1_y, p1_x + 520, p1_y + 320], radius=16, fill=WHITE, outline=ACCENT, width=3)
    draw.rounded_rectangle([p1_x, p1_y, p1_x + 520, p1_y + 50], radius=16, fill=ACCENT)
    draw.text((p1_x + 20, p1_y + 8), "Phase 1: SDK 构建适配", fill=WHITE, font=font_header)
    draw.text((p1_x + 380, p1_y + 12), "Before 2026-04-28", fill=WHITE, font=font_date)

    tasks1 = [
        "修复废弃 API (keyWindow, delegate.window)",
        "SceneDelegate 架构迁移",
        "StoreKit 1 → StoreKit 2 迁移",
        "添加 PrivacyInfo.xcprivacy",
        "临时禁用 Liquid Glass",
    ]
    y = p1_y + 70
    for task in tasks1:
        draw.text((p1_x + 20, y), "✓ " + task, fill=(50, 50, 70), font=font_text)
        y += 45

    # Arrow
    draw.polygon([(620, 270), (660, 250), (660, 290)], fill=ORANGE)
    draw.rectangle([600, 265, 640, 275], fill=ORANGE)

    # Phase 2 box
    p2_x, p2_y = 660, 120
    draw.rounded_rectangle([p2_x, p2_y, p2_x + 480, p2_y + 320], radius=16, fill=WHITE, outline=GREEN, width=3)
    draw.rounded_rectangle([p2_x, p2_y, p2_x + 480, p2_y + 50], radius=16, fill=GREEN)
    draw.text((p2_x + 20, p2_y + 8), "Phase 2: Liquid Glass 适配", fill=WHITE, font=font_header)
    draw.text((p2_x + 340, p2_y + 12), "Before Xcode 27", fill=WHITE, font=font_date)

    tasks2 = [
        "移除 UIDesignRequiresCompatibility",
        "处理浮动 TabBar safeArea 变化",
        "移除自定义背景色",
        "验证 UIDropShadowView 影响",
    ]
    y = p2_y + 70
    for task in tasks2:
        draw.text((p2_x + 20, y), "✓ " + task, fill=(50, 50, 70), font=font_text)
        y += 45

    # Deadline badge
    draw.rounded_rectangle([400, 460, 800, 490], radius=20, fill=(255, 230, 230), outline=RED, width=2)
    draw.text((430, 465), "⚠️  Deadline: 2026-04-28 之后不合规提交将被拒审", fill=RED, font=font_date)

    img.save(filename, quality=95)
    print(f"Generated: {filename}")

# ============== Scanner Rules Overview ==============
def generate_scanner_rules(filename):
    W, H = 1200, 700
    img = Image.new("RGB", (W, H), (245, 247, 250))
    draw = ImageDraw.Draw(img)

    font_title = get_font(36, bold=True)
    font_cat = get_font(22, bold=True)
    font_rule = get_font(18)

    draw.text((60, 30), "iOS 26 Scanner 规则覆盖图", fill=(40, 40, 60), font=font_title)
    draw.rectangle([60, 85, 280, 88], fill=ACCENT)

    categories = [
        ("窗口访问", ["WINDOW-001 keyWindow", "WINDOW-002 [UIApplication keyWindow]", "WINDOW-003 delegate.window",
                      "WINDOW-004 AppDelegate.window", "WINDOW-005 .window.rootViewController", "WINDOW-006 .window.visibleViewController"], ACCENT),
        ("通知 & 网络", ["NOTIF-001 UNNotificationPresentationOptionAlert", "TLS-001 TLS 1.0/1.1"], ORANGE),
        ("框架迁移", ["STOREKIT-001 StoreKit 1 API", "SIRIKIT-001 SiriKit Intent", "COREDATA-001 Ubiquitous keys",
                      "PHOTOS-001 UIImagePickerController", "WEB-001 UIWebView"], GREEN),
        ("SwiftUI", ["SWIFTUI-001 NavigationView", "SWIFTUI-002 .cornerRadius()", "SWIFTUI-003 .foregroundColor()"], (200, 100, 255)),
        ("其他", ["SWIFT6-001 Swift 6 并发", "STATUS-001~003 statusBarStyle", "PRIVACY-001 Privacy Manifest"], RED),
    ]

    x, y = 60, 120
    for cat_name, rules, color in categories:
        box_h = 50 + len(rules) * 32
        draw.rounded_rectangle([x, y, x + 350, y + box_h], radius=12, fill=WHITE, outline=color, width=2)
        draw.rounded_rectangle([x, y, x + 350, y + 36], radius=12, fill=color)
        draw.text((x + 12, y + 4), cat_name, fill=WHITE, font=font_cat)

        ry = y + 45
        for rule in rules:
            draw.text((x + 15, ry), "• " + rule, fill=(60, 60, 80), font=font_rule)
            ry += 32

        x += 380
        if x > 900:
            x = 60
            y += box_h + 30

    # Summary
    draw.rounded_rectangle([60, 620, 1140, 670], radius=12, fill=(230, 245, 255), outline=ACCENT, width=2)
    font_sum = get_font(22)
    draw.text((80, 630), "总计 20+ 条规则，覆盖 error / warning / info 三个级别", fill=(40, 60, 100), font=font_sum)
    draw.text((80, 650), "使用方法: python3 scripts/ios26-scanner.py /your/project/path", fill=(80, 100, 140), font=font_sum)

    img.save(filename, quality=95)
    print(f"Generated: {filename}")

# ============== Tech Stack Diagram ==============
def generate_tech_stack(filename):
    W, H = 1000, 400
    img = Image.new("RGB", (W, H), (245, 247, 250))
    draw = ImageDraw.Draw(img)

    font_title = get_font(32, bold=True)
    font_label = get_font(20, bold=True)
    font_desc = get_font(16)

    draw.text((60, 25), "项目技术栈", fill=(40, 40, 60), font=font_title)

    stacks = [
        ("Swift", "iOS 13+ 模板、SwiftUI、Swift 6 并发", (255, 90, 50), 60, 100),
        ("Objective-C", "iOS 12 兼容模板、混合项目桥接", (50, 120, 200), 360, 100),
        ("Python 3", "扫描脚本、单元测试、CI 流水线", (50, 160, 80), 660, 100),
        ("Markdown", "文档、FAQ、测试指南、检查清单", (120, 80, 180), 360, 260),
    ]

    for name, desc, color, x, y in stacks:
        draw.rounded_rectangle([x, y, x + 280, y + 130], radius=14, fill=WHITE, outline=color, width=3)
        draw.rounded_rectangle([x, y, x + 280, y + 40], radius=14, fill=color)
        draw.text((x + 15, y + 8), name, fill=WHITE, font=font_label)
        # Wrap desc
        words = desc.split("、")
        line1 = "、".join(words[:2])
        line2 = "、".join(words[2:]) if len(words) > 2 else ""
        draw.text((x + 15, y + 55), line1, fill=(60, 60, 80), font=font_desc)
        if line2:
            draw.text((x + 15, y + 80), line2, fill=(60, 60, 80), font=font_desc)

    img.save(filename, quality=95)
    print(f"Generated: {filename}")

# ============== Main ==============
if __name__ == "__main__":
    os.makedirs(".", exist_ok=True)

    generate_cover("cover-juejin.png",
                   "iOS 26 适配完全指南",
                   "自动化扫描 + 20+ 规则 + 踩坑实录",
                   "掘金")

    generate_cover("cover-csdn.png",
                   "iOS 26 SDK 适配完整方案",
                   "含自动化扫描脚本与代码模板",
                   "CSDN")

    generate_phase_flow("phase-flow.png")
    generate_scanner_rules("scanner-rules.png")
    generate_tech_stack("tech-stack.png")

    print("\nAll images generated successfully!")
