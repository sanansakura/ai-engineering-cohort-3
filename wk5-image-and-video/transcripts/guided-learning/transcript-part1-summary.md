# Chunk 1 Summary

## Overview

Week 5 guided-learning session on image and video generation. Covers four generative modeling approaches (VAEs, GANs, autoregressive, diffusion), then focuses on diffusion-based text-to-image and text-to-video models, including architecture, training, sampling, evaluation, and system design.

## Generative Modeling Approaches

### VAEs (Variational Autoencoders)

- Introduced in 2013 (Auto-Encoding Variational Bayes); earlier simpler versions in 1980s
- Two components: encoder and decoder (both neural networks)
- Encoder compresses input image into compact vector; decoder reconstructs image
- Trained with reconstruction loss (e.g., MSE) to minimize difference between input and reconstruction
- For generation: discard encoder, sample random vector from distribution (e.g., Gaussian), pass to decoder
- Latent space: encoded training examples cluster by category (e.g., MNIST digits)
- Samples often blurry; not used for image generation today; still used in diffusion models for compression

### GANs (Generative Adversarial Networks)

- Introduced by Ian Goodfellow; highly influential paper
- Two components: generator (creates images from random vector) and discriminator (classifies real vs. fake)
- Adversarial training: generator minimizes discriminator accuracy; discriminator maximizes it
- Training challenges: mode collapse, vanishing gradients; many variants (StyleGAN, BigGAN, etc.)
- StyleGAN allowed manipulation of facial features (smile, glasses) via smooth latent space
- Not used in state-of-the-art text-to-image/video models today

### Autoregressive Modeling

- Formulates image generation as sequence generation (pixels or patches, one by one)
- Each pixel/patch conditioned on previously generated ones
- Image Transformer (Google): replaced CNN with self-attention for conditional image generation
- DALL·E (OpenAI, Jan 2021): first successful text-to-image using transformers; conditions on text tokens
- Advantage: flexible conditioning (text, category); high quality, coherent images
- Not the dominant approach; most state-of-the-art models use diffusion

### Diffusion Models

- Formulate generation as iterative denoising: add noise (forward process), train model to denoise (backward process)
- Training: add noise to images, train model to predict noise or denoised version
- Inference: start from random noise, iteratively denoise to generate new image
- DDPM (2020): first high-resolution diffusion images (256×256)
- Dominant for text-to-image and text-to-video; quality leap from autoregressive (e.g., DALL·E 1 → DALL·E 2)

## Image vs. Text-to-Image Generation

- Unconditional generation: no user control over output
- Text-to-image (T2I): user provides text prompt; model generates conditioned on text
- Industry shifted to T2I for controllability

## Model Landscape

### OpenAI

- DALL·E 1 (2021): 256×256, autoregressive
- DALL·E 2 (2022): diffusion, 512–1024 resolution
- DALL·E 3 (2023): 1K, aspect ratios
- GPT-4o / o1 image, GPT Image 1 (2025): best text rendering; speculative hybrid diffusion + autoregressive

### Google

- Imagen 1–4, Imagen 4 Ultra; improved resolution, aspect ratios, multilingual prompts

### Others

- Flux (Black Forest Labs): strong performance; free credits on BFL website
- Leaderboards: GPT Image 1, Imagen 4, Flux rank highly; sites like Father.ai for comparison

## Building Text-to-Image Models (Diffusion-Based)

### Data Preparation

- Need image–caption pairs (millions); e.g., LAION 5.0, DFN 400M
- Clean captions; standardize format

### Model Architecture

- UNet: encoder–decoder with skip connections; text encoded and injected via cross-attention
- DiT (Diffusion Transformer, 2023): replaces convolutions with patchify → transformer → unpatchify
- Patchify: divide image into patches (e.g., 16×16), flatten, project to embedding; add positional encoding (1D or 2D)
- DiT is current standard; scales better with data and compute

### Training

- Forward process: add noise to image over steps t (e.g., t = 1 to 1000)
- Backward process: diffusion model predicts noise given noisy image, timestep t, and conditions (text)
- Loss: MSE between predicted and true noise
- Conditions: text embeddings (CLIP/T5), timestep t

### Sampling

- Start from random noise at t=1000; iteratively denoise using model
- Traditionally 1000 steps; optimizations (DDIM, distillation) reduce to ~20–50 steps
- Trade-off: fewer steps = faster but possibly lower quality

## Evaluation

- Image quality and diversity: Inception Score, FID (compare fake vs. real image stats via Inception/CLIP)
- Image–text alignment: CLIP similarity (shared embedding space for text and images)

## Text-to-Video

### Differences from Text-to-Image

- Output: sequence of frames (e.g., 120) instead of single image
- Much more compute; requires efficiency

### Latent Diffusion

- Operate in latent space, not pixel space
- VAE or similar compression: encoder maps video to latent; decoder maps back
- Compression (e.g., 8× spatially and temporally) can reduce 110M pixels to ~216K (≈512× efficiency)
- Sora blog mentions compression/encoding to latent space

### Data and Training

- Need video–caption pairs; less data than images
- Mitigations: train on images + videos (images = 1-frame videos); or pretrain on images, finetune on video
- Precompute latent representations before training
- Separate models: base video model, spatial upsampler (4×), temporal upsampler (2× for frame rate)

### Model Architecture (Video DiT)

- 3D patchify: patches across space and time (cubes)
- 3D positional encoding (spatial + temporal)
- 3D unpatchify for output
- Same transformer + cross-attention for conditions

### Generation Pipeline

1. Random 3D noise → diffusion model ( conditioned on text) → denoised latent
2. VAE decoder → pixel video
3. Optional: spatial resolution model, temporal resolution model
4. Safety checks on prompt and output

### System Design (Sora-like)

- Autocomplete / prompt suggestions
- Safety service (prompt filtering)
- Prompt enhancer (paraphrase, add details)
- Generation component (diffusion in latent space)
- VAE decoder
- Output safety check
- Spatial resolution model
- Temporal resolution model
- Final video

## Key Takeaways

- Diffusion models dominate image and video generation
- DiT (Diffusion Transformer) is standard architecture
- Latent diffusion essential for video (efficiency)
- VAEs used for compression in diffusion pipelines, not for direct generation
- Data: image/video–caption pairs; captions must be clean
- Evaluation: quality/diversity (FID, IS), alignment (CLIP)
