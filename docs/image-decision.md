# Image decision — 26 Oct 2026, 6:03 PM IST

The fight pages for The F-Rank Tea Seller cannot be drawn on the current VPS, and Pollinations is not the uploader.

## What we checked

- Cloudflare Workers AI (FLUX.2 klein and FLUX.1 schnell) refuses swords, blood, and monster fights. That filter cannot be turned off. Those prompts are the comic.
- `46.28.44.225` is a 2-core, 8 GB CPU server with no NVIDIA GPU. It already runs `mt5`, `gold-dashboard`, and `smc-paper-bot`. Leave it as the trading and calendar box.
- The only Hugging Face model that ran there is `nota-ai/bk-sdm-tiny`. One 512×512 picture took about 3 minutes and came out a gray sketch. Animagine XL 4.0 does not fit in the free memory.
- Google Flow is a website, 50 credits a day, Nano Banana. Same kind of filter as Cloudflare. No official API, and a headless browser on this VPS is the wrong place for a Google login.
- Pollinations classic API did draw a sword, free, no key: 576×1024, their logo in the corner, one image every 45 seconds. It skipped the character details. It cannot make an 800×1280 WEBTOON slice or keep one face across 40 panels.

## What will actually make an episode

One of these, then download the files onto the existing VPS:

1. Rent a GPU for the draw and turn it off after. Animagine XL 4.0 or Illustrious XL v2.0. An RTX 3060 12 GB was about $0.06 an hour on 26 Oct 2026. Forty panels are a few minutes.
2. Pay for an API and call it from the VPS. Hypereal is about $0.02 a picture (about $0.80 for 40). Sogni Unlimited is $20 a month and includes Animagine XL 4.0, with a 3-day trial of up to 120 pictures a day.

Do not use NoobAI-XL if the WEBTOON might earn money. Its card forbids selling the pictures.

Lettering stays in our own code. The model should not paint the words.
