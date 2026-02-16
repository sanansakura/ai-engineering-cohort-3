# Guided Learning Complete Summary

Week 5 guided-learning session on image and video generation. Covers generative modeling (VAEs, GANs, autoregressive, diffusion), diffusion-based text-to-image and text-to-video models, architecture, training, sampling, evaluation, and system design.

---

## Key Takeaways

- **Diffusion models** are the dominant approach for image and video generation; most state-of-the-art models are diffusion-based.
- **DiT (Diffusion Transformer)** is the standard architecture, replacing UNets.
- **Latent diffusion** is essential for video: operate in compressed latent space for efficiency.
- **VAEs** are used for compression in diffusion pipelines, not for direct image generation.
- **Data**: Image/video–caption pairs; captions must be clean and detailed.
- **Evaluation**: Quality/diversity (FID, Inception Score), alignment (CLIP).

---

## Generative Modeling Approaches

### VAEs (Variational Autoencoders)

- Introduced in 2013 (Auto-Encoding Variational Bayes); earlier versions in 1980s
- Encoder compresses image to latent vector; decoder reconstructs
- Trained with reconstruction loss (e.g., MSE)
- For generation: sample random vector, pass through decoder
- Latent space clusters by category (e.g., MNIST digits)
- Not used for image generation today (blurry outputs); still used for compression in diffusion models

### GANs (Generative Adversarial Networks)

- Generator creates images; discriminator distinguishes real vs. fake
- Adversarial training; challenges include mode collapse, vanishing gradients
- StyleGAN enabled attribute manipulation (smile, glasses) via smooth latent space
- Not used in current text-to-image/video models

### Autoregressive Modeling

- Image as sequence of pixels/patches; each conditioned on previous
- Image Transformer, DALL·E (2021): text-to-image with transformers
- Flexible conditioning; high quality; not dominant today

### Diffusion Models

- Forward: add noise; backward: denoise iteratively
- Train model to predict noise (or denoised image); MSE loss
- Inference: start from random noise, denoise step by step
- DDPM (2020): first high-resolution diffusion images
- Dominant for T2I and T2V

---

## Image vs. Text-to-Image

- Unconditional generation: no control over output
- Text-to-image: user prompt conditions generation; industry standard
- Landscape: OpenAI (DALL·E 1–3, GPT Image 1), Google (Imagen 1–4), Flux, others
- Leaderboards: Father.ai; GPT Image 1, Imagen 4, Flux rank highly

---

## Building Text-to-Image Models (Diffusion)

### Data

- Image–caption pairs (millions); LAION 5.0, DFN 400M
- Clean captions; standardize format

### Architecture

- **UNet**: encoder–decoder, text injected via cross-attention
- **DiT**: patchify → transformer → unpatchify; 2D positional encoding
- DiT is current standard; scales with data and compute

### Training

- Forward: add noise over steps t (1–1000)
- Backward: model predicts noise given noisy image, t, and text
- Loss: MSE between predicted and true noise
- Conditions: text embeddings (CLIP/T5), timestep t

### Sampling

- Start from random noise at t=1000; iteratively denoise
- Optimizations (DDIM, distillation): ~20–50 steps typical
- Trade-off: fewer steps = faster, possibly lower quality

### Evaluation

- Quality/diversity: Inception Score, FID
- Alignment: CLIP similarity

---

## Text-to-Video

### Latent Diffusion for Video

- Operate in latent space (compression 8× spatially and temporally)
- VAE encoder/decoder; ~512× efficiency vs. pixel space
- Sora uses compression to latent space

### Architecture (Video DiT)

- 3D patchify (spatial + temporal patches)
- 3D positional encoding
- Same transformer + cross-attention; output 3D latent

### Data and Training

- Video–caption pairs; less data than images
- Mitigations: train on images + videos; or pretrain on images, finetune on video
- Precompute latents before training
- Separate models: base, spatial upsampler (4×), temporal upsampler (2× frame rate)

### Generation Pipeline

1. Random 3D noise → diffusion model (text-conditioned) → denoised latent
2. VAE decoder → pixel video
3. Optional: spatial then temporal resolution models
4. Safety on prompt and output

### System Design (Sora-like)

- Autocomplete / prompt suggestions
- Safety service (prompt filtering)
- Prompt enhancer (paraphrase, add details)
- Generation (diffusion in latent space)
- VAE decoder
- Output safety
- Spatial resolution model
- Temporal resolution model
- Final video

---

## References Mentioned

- VAE: Auto-Encoding Variational Bayes (2013)
- GAN: Goodfellow et al.
- Autoregressive: PixelCNN, Image Transformer, DALL·E
- Diffusion: DDPM (2020)
- DiT: Diffusion Transformers (2023)
- Sora, Veo, Open Sora
- Leaderboards: Father.ai, Chatbot Arena
