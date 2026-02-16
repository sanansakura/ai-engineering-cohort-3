# Chunk 2 Summary

## VAEs Continued

### MNIST Example

- 60K 28×28 grayscale digits; learn digit distribution, then sample new digits

### Implementation (PyTorch)

- VAE as nn.Module; encoder/decoder as sequences of linear layers
- Encoder outputs mean and log-variance (2D latent in example)
- Sampling: z = mean + std * epsilon, epsilon ~ N(0,1)
- Loss: binary cross-entropy or similar
- Standard training loop: batches, optimizer, backward

### Latent Space Visualization

- Encoded points form clusters (e.g., digit classes)
- Sampling in empty regions yields novel digits
- Interpolation between clusters can be ambiguous

### VAEs Today

- Not used for image generation (blurry outputs)
- Still used in diffusion pipelines (e.g., compression/encoding)

## GANs (Generative Adversarial Networks)

### Introduction

- Generator + discriminator; game-theoretic setup
- Generator: random vector → image; discriminator: real vs fake
- Major improvement over VAEs (clearer, more detailed images)

### Training

- Generator: fool discriminator; discriminator: classify real vs fake
- Cross-entropy losses; joint optimization
- Challenges: mode collapse, vanishing gradients (see Google GAN course)

### Inference

- Use generator only; sample latent from same distribution as training

### Variants

- Conditional GANs, StyleGAN, BigGAN, etc.
- StyleGAN: attribute control (smile, glasses) via smooth latent space
