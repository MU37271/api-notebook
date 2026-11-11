"""Generate PWA icons matching the pastel collage look."""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)

CREAM = (251, 247, 240, 255)
PINK = (243, 205, 198, 255)
BLUE = (201, 220, 238, 255)
MINT = (205, 231, 214, 255)
ACC1 = (237, 165, 147, 255)
ACC2 = (201, 115, 95, 255)


def font(size):
    for name in ("arialbd.ttf", "Arialbd.ttf", "segoeuib.ttf"):
        p = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    try:
        return ImageFont.load_default(size=size)
    except Exception:
        return ImageFont.load_default()


def build(size, maskable=False):
    """Draw at 3x then downscale for smooth edges."""
    S = size * 3
    img = Image.new("RGBA", (S, S), CREAM)
    d = ImageDraw.Draw(img)

    # polka dots
    step = int(S / 16)
    r = max(2, int(S / 210))
    for gy in range(-1, 18):
        for gx in range(-1, 18):
            x = gx * step
            y = gy * step + (step // 2 if gx % 2 else 0)
            col = PINK if (gx + gy) % 3 == 0 else (BLUE if (gx + gy) % 3 == 1 else MINT)
            d.ellipse([x - r, y - r, x + r, y + r], fill=col)

    # centre disc (maskable keeps it inside the 80% safe zone)
    cr = int(S * (0.235 if maskable else 0.30))
    cx = cy = S // 2
    steps = cr
    for i in range(steps, 0, -1):
        t = i / steps
        col = tuple(int(ACC1[k] * t + ACC2[k] * (1 - t)) for k in range(3)) + (255,)
        rr = int(cr * t)
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col)

    # white K
    f = font(int(cr * 1.25))
    box = d.textbbox((0, 0), "K", font=f)
    w, h = box[2] - box[0], box[3] - box[1]
    d.text((cx - w / 2 - box[0], cy - h / 2 - box[1]), "K", font=f, fill=(255, 255, 255, 255))

    return img.resize((size, size), Image.LANCZOS)


targets = [
    ("icon-192.png", 192, False),
    ("icon-512.png", 512, False),
    ("icon-512-maskable.png", 512, True),
    ("apple-touch-icon.png", 180, False),
    ("favicon-64.png", 64, False),
]

for name, size, maskable in targets:
    im = build(size, maskable)
    path = os.path.join(OUT, name)
    im.convert("RGB").save(path, "PNG", optimize=True)
    print(f"{name:26s} {size}x{size}  {os.path.getsize(path)} bytes")

print("done ->", OUT)
