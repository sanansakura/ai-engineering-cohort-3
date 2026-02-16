# Chunk 5 Summary

## Diffusion Training

### Forward and Backward

- Forward: add noise over steps t (1–1000)
- Backward: model predicts noise given noisy image, t, and text
- Loss: MSE between predicted and true noise

### Training Loop

- Sample t; add noise; prepare caption + t; run model; compute MSE; update

## Diffusion Sampling

- Start from random noise at t=1000; iteratively denoise
- DDIM and distillation reduce steps (e.g., 50 → 20)
- Typical: 15–20 steps for quality/speed balance

## Evaluation

### Three Dimensions

1. **Image quality**: perceptual quality of outputs
2. **Diversity**: variety of styles, subjects, compositions
3. **Image–text alignment**: match to prompt

### Metrics

- **Inception Score**: class probabilities from Inception V3; sharp = good quality; flat marginal = good diversity
- **FID**: distance between real and generated image statistics (Inception features)
- **CLIP**: shared text–image space for alignment

## Text-to-Video

### Early Work

- Video Diffusion Models: extend UNet to video (Google)
- Sora (Feb 2024): diffusion-based, compression to latent; few details
- Veo (Google), Kling, Runway, etc.

### T2V vs T2I

- Same conditioning; output = sequence of frames (e.g., 120)
- Much more compute; needs optimization
