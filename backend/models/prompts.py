"""
models/prompts.py
Dynamic prompt builder for interior design generation.
Combines room type, style, density, and detected furniture
into rich positive + negative prompts for Stable Diffusion.
"""

# ── Style modifiers ───────────────────────────────────────────────────────────
STYLE_MODIFIERS = {
    "modern":            "sleek modern, clean lines, contemporary",
    "minimalist":        "minimalist, uncluttered, Zen, negative space",
    "scandinavian":      "Scandinavian, hygge, light wood, neutral tones",
    "industrial":        "industrial loft, exposed brick, metal accents",
    "bohemian":          "bohemian eclectic, warm textures, layered rugs",
    "mid-century modern": "mid-century modern, organic shapes, teak wood",
    "traditional":       "traditional classic, rich wood tones, ornate details",
    "japandi":           "Japandi, wabi-sabi, natural materials, serene",
    "coastal":           "coastal beach house, light airy, natural linen",
    "art deco":          "art deco, geometric patterns, gold accents, glamorous",
}

# ── Density modifiers ─────────────────────────────────────────────────────────
DENSITY_MODIFIERS = {
    "minimal":  "minimal furniture, open space, breathing room",
    "moderate": "tastefully furnished, balanced layout",
    "dense":    "richly furnished, layered decor, cozy and full",
}

# ── Lighting modifiers ────────────────────────────────────────────────────────
LIGHTING_MODIFIERS = {
    "bedroom":        "warm soft lighting, bedside lamps",
    "living room":    "natural daylight, ambient lighting",
    "kitchen":        "bright task lighting, under-cabinet lights",
    "bathroom":       "clean white lighting, spa-like",
    "dining room":    "warm pendant lighting over table",
    "home office":    "cool daylight, desk lamp",
    "nursery":        "soft warm lighting, gentle atmosphere",
    "studio apartment": "multifunctional lighting, warm and bright",
}

# ── Negative prompt (shared across all styles) ────────────────────────────────
BASE_NEGATIVE_PROMPT = (
    "ugly, distorted, blurry, low quality, watermark, text, logo, "
    "deformed, bad anatomy, disfigured, extra limbs, cropped, "
    "worst quality, jpeg artifacts, overexposed, underexposed, "
    "people, person, human, face, hands, cluttered mess"
)


# ── Builder ───────────────────────────────────────────────────────────────────
def build_prompt(
    room_type: str,
    style: str,
    density: str,
    furniture: list[str],
) -> tuple[str, str]:
    """
    Build positive and negative prompts for Stable Diffusion.

    Args:
        room_type:  e.g. "living room"
        style:      e.g. "modern"
        density:    "minimal" | "moderate" | "dense"
        furniture:  list of detected furniture labels from segmentation

    Returns:
        (positive_prompt, negative_prompt)

    Example output:
        "sleek modern, clean lines, contemporary living room interior,
         tastefully furnished, balanced layout, sofa, coffee table, lamp,
         natural daylight, ambient lighting, professional interior design
         photography, realistic lighting, high quality, 8k,
         architectural digest, beautiful composition"
    """
    style_key = style.lower()
    style_mod = STYLE_MODIFIERS.get(style_key, style)

    density_key = density.lower()
    density_mod = DENSITY_MODIFIERS.get(density_key, "tastefully furnished")

    lighting = LIGHTING_MODIFIERS.get(room_type.lower(), "beautiful natural lighting")

    # Use up to 4 detected furniture items
    furniture_str = (
        ", ".join(furniture[:4]) if furniture else "carefully selected furniture"
    )

    positive_prompt = (
        f"{style_mod} {room_type} interior, "
        f"{density_mod}, {furniture_str}, "
        f"{lighting}, "
        f"professional interior design photography, realistic lighting, "
        f"high quality, 8k, architectural digest, beautiful composition, "
        f"photorealistic"
    )

    return positive_prompt, BASE_NEGATIVE_PROMPT


def describe_prompt(
    room_type: str,
    style: str,
    density: str,
    furniture: list[str],
) -> str:
    """
    Returns a human-readable one-liner describing the generation settings.
    Used in the Streamlit UI.
    """
    furniture_str = ", ".join(furniture[:3]) if furniture else "auto-detected furniture"
    return (
        f"{style.title()} {room_type} · {density} furnishing · "
        f"detected: {furniture_str}"
    )
