# Chunk 1 Summary

## Overview

Week 5 intro: image and video generation. Preview of four approaches (VAEs, GANs, autoregressive, diffusion), plus live demo of system-design diagram generation.

## Session Introduction

### Topics to Cover

- Four generative approaches: VAEs, GANs, autoregressive modeling, diffusion
- Text-to-image (T2I) models
- Forward/backward process in diffusion, sampling
- Text-to-video (T2V) models and best practices

### Live Demo

- Challenging prompt: "diagram showing system design of the model"
- Diagram generation is harder than cats/dogs; layout and logic must be consistent
- Model produced useful diagrams (environment, policy, value function, arrows)
- Default behavior: two images per prompt for fallback options

## VAEs (Variational Autoencoders)

### Introduction

- Early generative approach; first practical NN image generator
- Paper: Auto-Encoding Variational Bayes (2013); roots in 1980s
- Probabilistic model; learns data distribution for sampling

### Architecture

- Encoder: image → compact latent vector (1D)
- Decoder: latent vector → reconstructed image
- Loss: reconstruction (e.g., MSE)
- For generation: discard encoder, sample latent from Gaussian, decode
