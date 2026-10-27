"""Draw Tea Stall episode 1 on the GridShare GPU. No words inside the picture."""
import torch
from diffusers import StableDiffusionXLPipeline
from pathlib import Path

OUT = Path("/workspace/out/raw")
OUT.mkdir(parents=True, exist_ok=True)
MODEL = "/workspace/Illustrious-XL-v2.0.safetensors"

SELLER = (
    "1man, adult, late twenties, black hair tied back, short beard, "
    "cream kurta, brown apron, red thread bracelet on left wrist"
)
STYLE = (
    "masterpiece, best quality, manhwa panel, clean lineart, soft night lighting, "
    "detailed background, vertical composition"
)
NEG = (
    "text, letters, watermark, signature, logo, child, loli, sword, weapon, blood, "
    "extra fingers, extra arms, bad anatomy, blurry, lowres, cropped head"
)

PANELS = [
    ("01 night stall", f"{STYLE}, wide shot, small wooden tea stall at night, warm lantern, quiet Indian street, {SELLER} standing behind the counter"),
    ("02 wiping", f"{STYLE}, medium shot, {SELLER} wiping a wooden tea counter with a cloth, clay cups stacked beside him"),
    ("03 kettle", f"{STYLE}, close shot, large metal tea kettle pouring steam, warm lantern light, wooden stall"),
    ("04 customer", f"{STYLE}, tired adult man in a simple shirt stops in front of the tea stall at night, {SELLER} looks up"),
    ("05 pour", f"{STYLE}, {SELLER} pours hot tea from a metal kettle into a small clay cup"),
    ("06 worried", f"{STYLE}, adult customer holding a clay cup of tea with both hands, worried face, night stall behind him"),
    ("07 listen", f"{STYLE}, {SELLER} leans on the counter and listens, kind eyes, customer across the counter"),
    ("08 bracelet", f"{STYLE}, close-up of a left wrist with a thin red thread bracelet beside a clay tea cup on wood"),
    ("09 cardamom", f"{STYLE}, {SELLER} drops one green cardamom pod into a clay cup of tea"),
    ("10 relax", f"{STYLE}, adult customer drinks tea, shoulders relaxed, a small smile, night stall"),
    ("11 coins", f"{STYLE}, a few Indian coins on the wooden counter, clay cup empty beside them, {SELLER} hand nearby"),
    ("12 smile", f"{STYLE}, {SELLER} alone behind the stall, small quiet smile, lantern still lit, empty night street"),
]


def main() -> None:
    pipe = StableDiffusionXLPipeline.from_single_file(
        MODEL, torch_dtype=torch.float16, use_safetensors=True
    )
    pipe.to("cuda")
    if hasattr(pipe.vae, "enable_tiling"):
        pipe.vae.enable_tiling()
    for index, (name, prompt) in enumerate(PANELS, start=1):
        dest = OUT / f"{index:02d}.png"
        if dest.exists() and dest.stat().st_size > 100_000:
            print("skip", dest.name, flush=True)
            continue
        image = pipe(
            prompt=prompt,
            negative_prompt=NEG,
            width=832,
            height=1216,
            num_inference_steps=24,
            guidance_scale=5.5,
            generator=torch.Generator("cuda").manual_seed(4100 + index),
        ).images[0]
        image.save(dest)
        print("saved", name, dest.stat().st_size, flush=True)


if __name__ == "__main__":
    main()
