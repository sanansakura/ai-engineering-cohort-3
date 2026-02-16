# Chunk 3 Summary

## Autoregressive Modeling

### Idea

- Image as sequence of pixels/patches; predict next conditioned on previous
- Paper: PixelCNN / conditional image generation with CNNs (van den Oord, 2016)
- Image Transformer (Google): replace CNN with self-attention

### Conditioning

- Cross-attention layer: condition on category or text
- Enables text-to-image; DALL·E (OpenAI, Jan 2021) first strong T2I with transformers

### Strengths and Limits

- High-quality, coherent images; flexible conditioning
- Not dominant; most state-of-the-art T2I/T2V use diffusion

## Diffusion Models

### Mechanism

- Forward: add noise to images
- Backward: train model to denoise (predict noise or clean image)
- Inference: start from random noise, iteratively denoise

### Papers

- 2015: initial diffusion formulation
- 2020 DDPM: first high-res diffusion images (256×256)
- DALL·E 2 (2022): OpenAI switched from autoregressive to diffusion; large quality jump

## Recap and Comparison

### Quality vs Speed

- VAEs, GANs: lower quality, faster
- Autoregressive, diffusion: higher quality, slower
- Diffusion preferred for top T2I/T2V models

### Image vs Text-to-Image

- Unconditional: random outputs (e.g., thispersondoesnotexist.com)
- T2I: user controls generation via text prompts
