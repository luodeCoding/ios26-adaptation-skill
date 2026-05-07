#!/usr/bin/env python3
"""
Gemini 自动生图脚本
读取 prompts/*.md 中的提示词，调用 Gemini API 生成图片

使用方式:
    export GEMINI_API_KEY="你的API密钥"
    python3 generate_with_gemini.py

可选参数:
    --prompts-dir  指定 prompt 文件目录 (默认: ./prompts)
    --output-dir   指定输出目录 (默认: ./gemini_outputs)
    --model        指定模型 (默认: gemini-2.0-flash-exp-image-generation)
    --file         只生成指定文件，如 01-cover
"""

import os
import sys
import re
import argparse
from pathlib import Path


def extract_gemini_prompt(md_content: str) -> str:
    """从 markdown 内容中提取 Gemini 提示词"""
    # 优先提取 ## Gemini 提示词 或 ## Gemini Prompt 下面的代码块
    patterns = [
        r'##\s*Gemini[\s\w]*\n+```\n(.*?)\n```',
        r'##\s*Gemini[\s\w]*\n+(.*?)(?=\n##|\Z)',
    ]
    for pattern in patterns:
        match = re.search(pattern, md_content, re.DOTALL | re.IGNORECASE)
        if match:
            prompt = match.group(1).strip()
            # 去掉可能的代码块标记
            prompt = re.sub(r'^```\w*\n?', '', prompt)
            prompt = re.sub(r'\n?```$', '', prompt)
            return prompt.strip()
    return ""


def generate_image_with_gemini(prompt: str, api_key: str, model: str) -> bytes:
    """
    调用 Gemini API 生成图片
    使用 google-generativeai SDK 或直接用 HTTP 请求
    """
    try:
        # 方案1: 使用 google-generativeai SDK（推荐）
        import google.generativeai as genai

        genai.configure(api_key=api_key)

        # 使用支持图像生成的模型
        model_instance = genai.GenerativeModel(model)

        response = model_instance.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_modalities=["Text", "Image"]
            )
        )

        # 从响应中提取图片数据
        for part in response.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                return part.inline_data.data

        raise RuntimeError("响应中没有找到图片数据")

    except ImportError:
        # 方案2: 使用纯 HTTP 请求（无需额外依赖）
        return _generate_via_http(prompt, api_key, model)


def _generate_via_http(prompt: str, api_key: str, model: str) -> bytes:
    """通过 HTTP 直接调用 Gemini API"""
    import json
    import urllib.request
    import urllib.error

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"]
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise RuntimeError(f"API 请求失败: {e.code} - {error_body}")

    # 解析响应，提取图片
    candidates = data.get("candidates", [])
    for candidate in candidates:
        content = candidate.get("content", {})
        parts = content.get("parts", [])
        for part in parts:
            if "inlineData" in part:
                import base64
                image_data = part["inlineData"].get("data", "")
                mime_type = part["inlineData"].get("mimeType", "image/png")
                return base64.b64decode(image_data)

    raise RuntimeError("响应中没有找到图片数据，原始响应:\n" + json.dumps(data, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="Gemini 自动生图")
    parser.add_argument("--prompts-dir", default="./prompts", help="prompt 文件目录")
    parser.add_argument("--output-dir", default="./gemini_outputs", help="输出目录")
    parser.add_argument("--model", default="gemini-2.0-flash-exp-image-generation",
                        help="Gemini 模型名称")
    parser.add_argument("--file", help="只生成指定的 prompt 文件（不含 .md 后缀）")
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ 错误: 请设置环境变量 GEMINI_API_KEY")
        print("   获取方式: https://aistudio.google.com/app/apikey")
        sys.exit(1)

    prompts_dir = Path(args.prompts_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 收集要处理的 prompt 文件
    if args.file:
        md_files = [prompts_dir / f"{args.file}.md"]
    else:
        md_files = sorted(prompts_dir.glob("*.md"))

    if not md_files:
        print(f"❌ 在 {prompts_dir} 中没有找到 .md 文件")
        sys.exit(1)

    print(f"🎨 Gemini 生图脚本")
    print(f"   模型: {args.model}")
    print(f"   输出: {output_dir.absolute()}")
    print(f"   共 {len(md_files)} 个 prompt 文件\n")

    success_count = 0
    fail_count = 0

    for md_file in md_files:
        if not md_file.exists():
            print(f"⚠️ 跳过: {md_file.name} (文件不存在)")
            continue

        name = md_file.stem
        content = md_file.read_text(encoding="utf-8")
        prompt = extract_gemini_prompt(content)

        if not prompt:
            print(f"⚠️ 跳过: {md_file.name} (未提取到提示词)")
            continue

        output_path = output_dir / f"{name}.png"
        print(f"🔄 生成中: {md_file.name} → {output_path.name}")
        print(f"   提示词长度: {len(prompt)} 字符")

        try:
            image_data = generate_image_with_gemini(prompt, api_key, args.model)
            output_path.write_bytes(image_data)
            file_size = len(image_data) / 1024
            print(f"   ✅ 完成 ({file_size:.1f} KB)\n")
            success_count += 1

        except Exception as e:
            print(f"   ❌ 失败: {e}\n")
            fail_count += 1

    print("=" * 50)
    print(f"📊 生成完成: {success_count} 成功, {fail_count} 失败")
    print(f"📁 输出目录: {output_dir.absolute()}")

    if fail_count > 0:
        print("\n💡 失败排查:")
        print("   1. 检查 API Key 是否有效")
        print("   2. 确认模型支持图像生成 (gemini-2.0-flash-exp-image-generation)")
        print("   3. 检查网络连接")
        sys.exit(1)


if __name__ == "__main__":
    main()
