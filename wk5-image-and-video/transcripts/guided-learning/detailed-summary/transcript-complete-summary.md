# Detailed Summary Complete Summary

Week 5 guided-learning on image and video generation: four generative approaches (VAEs, GANs, autoregressive, diffusion), diffusion-based T2I and T2V, architecture, training, sampling, evaluation, and system design.

---

## Key Takeaways

- **Diffusion models** dominate image and video generation; most state-of-the-art models are diffusion-based.
- **DiT** is the standard architecture for T2I and T2V.
- **Latent diffusion** (VAE compression) is essential for video to reduce compute.
- **VAEs** are used for compression in diffusion pipelines, not for direct generation.
- **Data**: image/video–caption pairs; datasets like LAION 5.0, DFN 400M.
- **Evaluation**: quality/diversity (Inception Score, FID), alignment (CLIP).

---

## Generative Modeling Approaches

### VAEs

- Encoder compresses image to latent; decoder reconstructs; trained with MSE
- For generation: sample latent, decode
- MNIST example: 28×28 digits; PyTorch encoder outputs mean and log-variance
- Not used for image generation (blurry); used in diffusion for compression

### GANs

- Generator + discriminator; adversarial training
- Variants: StyleGAN (attribute control), conditional GANs
- No longer used in top T2I/T2V models

### Autoregressive

- Image as sequence of pixels/patches; predict next conditioned on previous
- DALL·E (2021): first strong T2I with transformers
- Flexible conditioning; not dominant for T2I/T2V today

### Diffusion

- Forward: add noise; backward: denoise; inference: start from noise, iteratively denoise
- DDPM (2020): first high-res diffusion images
- Dominant for T2I and T2V

---

## Image vs Text-to-Image

- Unconditional: random outputs
- T2I: user controls via text prompts; industry standard

---

## Model Landscape

- **OpenAI**: DALL·E 1–3, GPT Image 1
- **Google**: Imagen 1–4
- **Others**: Flux, Father.ai leaderboard

---

## Building T2I Models (Diffusion)

### Data

- Image–caption pairs (millions); LAION 5.0, DFN 400M

### Architecture

- **UNet**: encoder–decoder, text via cross-attention
- **DiT**: patchify → transformer → unpatchify; 2D positional encoding; cross-attention for text
- DiT is current standard

### Training

- Forward: add noise over t (1–1000)
- Backward: model predicts noise; loss = MSE
- Conditions: text embeddings, timestep t

### Sampling

- Start from random noise at t=1000; iteratively denoise
- DDIM/distillation: ~15–20 steps typical

### Evaluation

- Quality/diversity: Inception Score, FID
- Alignment: CLIP similarity

---

## Text-to-Video

### Latent Diffusion

- VAE compresses video; diffusion in latent space; decoder produces video
- ~512× efficiency vs pixel space
- Sora uses compression to latent space

### Video DiT

- 3D patchify, 3D positional encoding
- Same transformer + cross-attention

### Data and Training

- Video–caption pairs; precompute latents
- Joint image+video training or image pretrain + video finetune
- Separate spatial (4×) and temporal (2×) upsamplers

### Generation Pipeline

- Random 3D noise → diffusion (text-conditioned) → denoised latent → VAE decoder → optional upsampling

### System Design (Sora-like)

1. Prompt autocomplete
2. Safety (prompt filtering)
3. Prompt enhancer
4. Diffusion generation (latent)
5. VAE decoder
6. Output safety
7. Spatial resolution model
8. Temporal resolution model
9. Final video

---

## References

- VAE: Auto-Encoding Variational Bayes (2013)
- GAN: Goodfellow et al.
- Diffusion: DDPM (2020), DiT (2023)
- Sora, Veo, Open Sora
- Father.ai, BFL (Flux)
