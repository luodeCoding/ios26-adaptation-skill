#!/usr/bin/env python3
"""Generate professional cover images and diagrams for iOS 26 adaptation skill."""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

def get_font(size, bold=False):
    candidates = [
        "/System/Library/AssetsV2/com_apple_MobileAsset_Font7/3419f2a427639ad8c8e139149a287865a90fa17e.asset/AssetData/PingFang.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                if "PingFang" in path:
                    # PingFang ttc index: 0=Light, 1=Regular, 2=Semibold, 3=Medium, 4=Thin, 5=Ultralight
                    idx = 2 if bold else 1
                    return ImageFont.truetype(path, size, index=idx)
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

def get_en_font(size, bold=False):
    candidates = [
        "/System/Library/AssetsV2/com_apple_MobileAsset_Font7/2a8b9118cdff69e8ba88a0fe6e7c42860e3c01a5.asset/AssetData/SF-Pro.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return get_font(size, bold)

# iOS style colors
BLUE = (0, 122, 255)
INDIGO = (88, 86, 214)
PURPLE = (175, 82, 222)
TEAL = (48, 209, 165)
GREEN = (52, 199, 89)
ORANGE = (255, 149, 0)
PINK = (255, 55, 95)
RED = (255, 59, 48)
GRAY = (142, 142, 147)
LIGHT_GRAY = (229, 229, 234)
DARK_BG = (20, 20, 35)
CARD_BG = (35, 35, 55)
WHITE = (255, 255, 255)

def gradient_bg(img, color1, color2):
    draw = ImageDraw.Draw(img)
    w, h = img.size
    for y in range(h):
        ratio = y / h
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

def draw_card(draw, x, y, w, h, radius=20, fill=CARD_BG, border=None):
    draw.rounded_rectangle([x, y, x+w, y+h], radius=radius, fill=fill, outline=border, width=2 if border else 0)

def draw_badge(draw, x, y, text, color, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad_x, pad_y = 16, 8
    draw.rounded_rectangle([x, y, x+tw+pad_x*2, y+th+pad_y*2], radius=18, fill=color)
    draw.text((x+pad_x, y+pad_y), text, fill=WHITE, font=font)

# ==================== Cover ====================
def gen_cover(filename, title_line1, title_line2, platform):
    W, H = 1200, 630
    img = Image.new("RGB", (W, H))
    gradient_bg(img, (15, 18, 40), (45, 30, 80))
    draw = ImageDraw.Draw(img)

    # Decorative glow circles (blurred)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse([700, -80, 1100, 320], fill=(88, 86, 214, 40))
    glow_draw.ellipse([850, 350, 1250, 750], fill=(0, 122, 255, 30))
    glow_draw.ellipse([-100, 200, 250, 550], fill=(48, 209, 165, 25))
    img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Platform badge
    f_badge = get_font(20)
    badge_text = f"{platform} 独家"
    draw_badge(draw, 60, 40, badge_text, BLUE, f_badge)

    # Title
    f_title = get_font(72, bold=True)
    f_title2 = get_font(56, bold=True)
    draw.text((60, 130), title_line1, fill=WHITE, font=f_title)
    if title_line2:
        draw.text((60, 220), title_line2, fill=WHITE, font=f_title2)

    # Subtitle line
    draw.rectangle([60, 310, 220, 316], fill=BLUE)

    # Features with icons
    f_feat = get_font(24)
    features = [
        ("🔍", "20+ 自动化扫描规则", BLUE),
        ("📦", "Swift / OC 双语言模板", TEAL),
        ("🧪", "两轮 QA 深度排查", PURPLE),
    ]
    fx, fy = 60, 350
    for icon, text, color in features:
        draw.text((fx, fy), icon, fill=WHITE, font=f_feat)
        draw.text((fx + 40, fy), text, fill=(200, 200, 220), font=f_feat)
        fy += 50

    # Right side: iOS 26 badge
    draw.rounded_rectangle([800, 140, 1120, 460], radius=30, fill=CARD_BG, outline=(88, 86, 214, 80), width=2)
    f_ios = get_en_font(120, bold=True)
    draw.text((830, 170), "iOS", fill=WHITE, font=f_ios)
    draw.text((830, 300), "26", fill=BLUE, font=get_en_font(180, bold=True))
    draw.text((830, 500), "ADAPTATION", fill=GRAY, font=get_en_font(20))

    # Bottom bar
    draw.rectangle([0, 570, W, 630], fill=(10, 12, 30))
    f_bottom = get_font(18)
    draw.text((60, 588), "GitHub: luodeCoding/ios26-adaptation-skill", fill=GRAY, font=f_bottom)
    draw.text((750, 588), "开源 · 免费 · 生产可用", fill=(100, 100, 120), font=f_bottom)

    img.save(filename, quality=95)
    print(f"Generated: {filename}")

# ==================== What Is This Project ====================
def gen_project_overview(filename):
    W, H = 1200, 800
    img = Image.new("RGB", (W, H), (250, 250, 255))
    draw = ImageDraw.Draw(img)

    f_title = get_font(42, bold=True)
    f_sub = get_font(26)
    f_num = get_en_font(64, bold=True)
    f_label = get_font(20)

    draw.text((60, 40), "这个项目能帮你做什么？", fill=DARK_BG, font=f_title)
    draw.rectangle([60, 100, 200, 106], fill=BLUE)

    # 4 capability cards
    cards = [
        ("01", "自动扫描废弃 API", "一行命令检测 20+ 种 iOS 26 废弃/移除 API，输出 Markdown 报告", BLUE),
        ("02", "直接可用的代码模板", "Swift / Objective-C / 混合项目三套模板，复制到项目即可用", TEAL),
        ("03", "完整的适配文档", "30 个 FAQ、测试指南、SDK 兼容性速查表，覆盖全流程", PURPLE),
        ("04", "持续维护更新", "两轮 QA 排查已修复 15 项差距，持续跟踪 Apple 最新变更", ORANGE),
    ]

    cx, cy = 60, 140
    for num, title, desc, color in cards:
        draw_card(draw, cx, cy, 520, 260, fill=WHITE, border=LIGHT_GRAY)
        # Color strip
        draw.rectangle([cx, cy, cx+6, cy+260], fill=color)
        # Number
        draw.text((cx+30, cy+20), num, fill=color, font=f_num)
        # Title
        draw.text((cx+30, cy+100), title, fill=DARK_BG, font=f_sub)
        # Desc (wrap)
        words = desc
        draw.text((cx+30, cy+150), words[:20], fill=GRAY, font=f_label)
        draw.text((cx+30, cy+180), words[20:40], fill=GRAY, font=f_label)
        draw.text((cx+30, cy+210), words[40:], fill=GRAY, font=f_label)

        cx += 560
        if cx > 700:
            cx = 60
            cy += 300

    # Bottom highlight
    draw.rounded_rectangle([60, 720, 1140, 780], radius=16, fill=(230, 242, 255))
    draw.text((90, 738), "💡 适用场景：", fill=DARK_BG, font=get_font(24, bold=True))
    draw.text((220, 740), "iOS 26 SDK 适配 deadline 临近 / 团队缺乏系统适配方案 / 需要自动化检测工具", fill=(60, 60, 80), font=f_label)

    img.save(filename, quality=95)
    print(f"Generated: {filename}")

# ==================== Scanner Demo ====================
def gen_scanner_demo(filename):
    W, H = 1200, 700
    img = Image.new("RGB", (W, H), DARK_BG)
    draw = ImageDraw.Draw(img)

    f_title = get_font(36, bold=True)
    f_code = get_font(18)
    f_header = get_font(22, bold=True)

    draw.text((60, 30), "扫描效果演示", fill=WHITE, font=f_title)
    draw.text((60, 80), "python3 scripts/ios26-scanner.py /path/to/your/project", fill=GREEN, font=f_code)

    # Terminal window
    draw.rounded_rectangle([60, 130, 1140, 660], radius=16, fill=(28, 28, 45))
    # Terminal header
    draw.rounded_rectangle([60, 130, 1140, 170], radius=16, fill=(40, 40, 60))
    draw.rectangle([60, 150, 1140, 170], fill=(40, 40, 60))
    # Window dots
    for i, c in enumerate([RED, ORANGE, GREEN]):
        draw.ellipse([80 + i*25, 142, 96 + i*25, 158], fill=c)

    lines = [
        ("# iOS 26 Adaptation Scan Report", GRAY),
        ("", WHITE),
        ("Files Scanned: 247", WHITE),
        ("Total Issues: 12  (Errors: 3, Warnings: 9)", WHITE),
        ("", WHITE),
        ("## Issues", BLUE),
        ("", WHITE),
        ("| Rule ID     | Severity | File           | Line | Message                         |", WHITE),
        ("|-------------|----------|----------------|------|---------------------------------|", WHITE),
        ("| WINDOW-001  | ERROR    | LoginVC.swift  | 45   | Deprecated keyWindow usage      |", RED),
        ("| STOREKIT-001| ERROR    | IAPManager.m   | 128  | StoreKit 1 API removed          |", RED),
        ("| PRIVACY-001 | ERROR    | ./             | 0    | Missing PrivacyInfo.xcprivacy   |", RED),
        ("| SCREEN-001  | WARNING  | HomeVC.swift   | 88   | Deprecated UIScreen.main usage  |", ORANGE),
        ("| SWIFTUI-001 | WARNING  | Profile.swift  | 32   | NavigationView is deprecated    |", ORANGE),
        ("", WHITE),
        ("Run with --format json for structured output", GRAY),
    ]

    y = 190
    for text, color in lines:
        draw.text((80, y), text, fill=color, font=f_code)
        y += 28

    img.save(filename, quality=95)
    print(f"Generated: {filename}")

# ==================== Template Structure ====================
def gen_template_tree(filename):
    W, H = 1200, 750
    img = Image.new("RGB", (W, H), (250, 250, 255))
    draw = ImageDraw.Draw(img)

    f_title = get_font(36, bold=True)
    f_folder = get_font(22, bold=True)
    f_file = get_font(20)
    f_badge = get_font(16)

    draw.text((60, 30), "模板目录结构", fill=DARK_BG, font=f_title)
    draw.rectangle([60, 85, 220, 90], fill=BLUE)

    # Tree structure
    tree = [
        ("templates/", None, 0),
        ("swift/", BLUE, 1),
        ("UIApplication+MainWindow.swift", GRAY, 2),
        ("SceneDelegate.swift", GRAY, 2),
        ("AppDelegate+Setup.swift", GRAY, 2),
        ("UNNotificationOptions+Adapter.swift", GRAY, 2),
        ("Swift6ConcurrencyAdapter.swift", GREEN, 2),
        ("objc/", TEAL, 1),
        ("UIApplication+MainWindow.h/.m", GRAY, 2),
        ("SceneDelegate.h/.m", GRAY, 2),
        ("AppDelegate+Setup.h/.m", GRAY, 2),
        ("UNNotificationOptionsAdapter.h/.m", GRAY, 2),
        ("mixed/", PURPLE, 1),
        ("README.md", GRAY, 2),
        ("PrivacyInfo.xcprivacy", ORANGE, 1),
    ]

    y = 120
    for name, color, level in tree:
        x = 60 + level * 40
        if color and level <= 1:
            # Folder with color badge
            draw.rounded_rectangle([x, y, x + 280, y + 36], radius=8, fill=color)
            draw.text((x + 12, y + 4), "📁 " + name, fill=WHITE, font=f_folder)
        else:
            # File
            draw.text((x + 12, y), "📄 " + name, fill=(60, 60, 80) if color == GRAY else color, font=f_file)
        y += 42

    # Legend
    lx, ly = 500, 130
    draw.text((lx, ly), "图例说明:", fill=DARK_BG, font=get_font(22, bold=True))
    items = [
        (BLUE, "Swift 模板"),
        (TEAL, "Objective-C 模板"),
        (PURPLE, "混合项目指南"),
        (ORANGE, "Privacy Manifest"),
        (GREEN, "Swift 6 并发适配"),
    ]
    for color, label in items:
        ly += 40
        draw.rectangle([lx, ly+8, lx+20, ly+28], fill=color)
        draw.text((lx+30, ly), label, fill=(60, 60, 80), font=f_badge)

    # Bottom note
    draw.rounded_rectangle([60, 680, 1140, 730], radius=12, fill=(230, 242, 255))
    draw.text((80, 695), "使用方法：根据项目语言选择目录，复制文件到主项目并修改类名和逻辑", fill=(40, 60, 100), font=get_font(20))

    img.save(filename, quality=95)
    print(f"Generated: {filename}")

# ==================== Main ====================
if __name__ == "__main__":
    gen_cover("cover-juejin-v2.png", "iOS 26 适配完全指南", "自动化扫描 + 20+ 规则 + 踩坑实录", "掘金")
    gen_cover("cover-csdn-v2.png", "iOS 26 SDK 适配完整方案", "含自动化扫描脚本与代码模板", "CSDN")
    gen_project_overview("project-overview.png")
    gen_scanner_demo("scanner-demo.png")
    gen_template_tree("template-tree.png")
    print("\nAll v2 images generated!")
