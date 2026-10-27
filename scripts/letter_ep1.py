"""Make WEBTOON files from the raw panels. Words are added here, not by the model."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

RAW = Path("/workspace/out/raw")
OUT = Path("/workspace/out/webtoon")
OUT.mkdir(parents=True, exist_ok=True)

LINES = [
    "Night. The stall is open.",
    "He wipes the counter clean.",
    "The kettle is ready.",
    "A tired man stops.",
    "One clay cup.",
    "He holds it, and says nothing.",
    "The seller listens.",
    "A red thread, and a warm cup.",
    "Cardamom, for the worry.",
    "The shoulders drop.",
    "Coins on the wood.",
    "The lamp stays lit.",
]

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]


def font(size: int) -> ImageFont.ImageFont:
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def panel(src: Path, line: str, dest: Path) -> None:
    art = Image.open(src).convert("RGB")
    canvas = Image.new("RGB", (800, 1280), (28, 18, 12))
    art = art.resize((800, 1100), Image.Resampling.LANCZOS)
    canvas.paste(art, (0, 0))
    draw = ImageDraw.Draw(canvas)
    pen = font(36)
    box = draw.textbbox((0, 0), line, font=pen)
    width = box[2] - box[0]
    draw.text(((800 - width) / 2, 1148), line, fill=(255, 236, 210), font=pen)
    for quality in (90, 85, 80, 75, 70):
        canvas.save(dest, "JPEG", quality=quality, optimize=True)
        if dest.stat().st_size < 2_000_000:
            break


def thumb(src: Path, size: tuple[int, int], dest: Path, limit: int) -> None:
    from PIL import ImageOps

    image = ImageOps.fit(Image.open(src).convert("RGB"), size, Image.Resampling.LANCZOS)
    for quality in (90, 85, 80, 75, 65, 55):
        image.save(dest, "JPEG", quality=quality, optimize=True)
        if dest.stat().st_size < limit:
            break


def main() -> None:
    first = None
    for index, line in enumerate(LINES, start=1):
        src = RAW / f"{index:02d}.png"
        dest = OUT / f"{index:02d}.jpg"
        panel(src, line, dest)
        first = first or dest
        print("page", dest.name, dest.stat().st_size, flush=True)
    thumb(RAW / "01.png", (1080, 1080), OUT / "thumb-square.jpg", 500_000)
    thumb(RAW / "01.png", (1080, 1920), OUT / "thumb-vertical.jpg", 700_000)
    thumb(RAW / "01.png", (160, 151), OUT / "thumb-episode.jpg", 200_000)
    print("thumbs", flush=True)


if __name__ == "__main__":
    main()
