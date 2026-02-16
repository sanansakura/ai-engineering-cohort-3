# Chunk 4 Summary

## Model Landscape

### OpenAI

- DALL·E 1 (2021): 256×256, autoregressive
- DALL·E 2 (2022): diffusion, 512–1024, technical paper
- DALL·E 3: 1K, aspect ratios
- GPT-4o, GPT Image 1: strong text rendering; speculated hybrid diffusion + autoregressive

### Google

- Imagen 1–4, Imagen 4 Ultra; high resolution, aspect ratios, multilingual prompts

### Other Providers

- Flux (Black Forest Labs): strong; 200 free credits on BFL website
- Father.ai: leaderboard and model comparison

## Building T2I Models (Diffusion)

### Four Steps

1. **Data**: image–caption pairs (millions)
2. **Architecture**: layers and structure
3. **Training**: objectives and optimization
4. **Sampling**: how to generate

### Data Preparation

- Pairs of images and captions
- Datasets: LAION 5.0, DFN 400M

### Architecture

- **UNet**: encoder–decoder, convolutions, transpose convolutions; text via cross-attention
- **DiT** (Diffusion Transformers, 2023): patchify → transformer → unpatchify
- Patchify: 2D patches → sequence of tokens; 1D or 2D positional encoding
- Conditions: text embeddings and timestep t
- DiT is current standard for T2I
