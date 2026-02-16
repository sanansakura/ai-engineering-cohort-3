# Chunk 6 Summary

## Latent Diffusion for Video

### Compression

- VAE: video → latent; diffusion in latent space; VAE decoder → video
- Example: 1280×720×120 frames → 8× spatial + temporal compression → ~512× fewer pixels
- Sora blog mentions compression to latent space

### Data and Training

- Video–caption pairs; precompute latents
- Two strategies: (1) joint image+video training, or (2) pretrain on images, finetune on video
- Separate models: spatial upsampler (4×), temporal upsampler (2× frame rate)

### Video DiT

- 3D patchify (spatial + temporal)
- 3D positional encoding
- Same transformer + cross-attention

### Generation Pipeline

- Random 3D noise → diffusion (text-conditioned) → denoised latent → VAE decoder → optional upsampling

### System Design (Sora-like)

1. Prompt autocomplete
2. Safety (prompt filtering)
3. Prompt enhancer (paraphrase, add detail)
4. Diffusion generation (latent)
5. VAE decoder
6. Output safety
7. Spatial resolution model
8. Temporal resolution model
9. Final video

### Projects

- Load models and generate images/videos
- Chat UI: route to text, image, or video generation by intent
