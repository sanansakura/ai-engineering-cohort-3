# Chunk 5 Summary

## Commercial Text-to-Image Systems

### OpenAI's Evolution: The DALL·E Family

OpenAI has released multiple generations of text-to-image models:

#### DALL·E 1 (2021)
- First version: 256×256 resolution
- Used autoregressive modeling
- Demonstrated proof-of-concept for text-to-image

#### DALL·E 2 (2022)
- Architectural shift to diffusion models
  - Immediate quality improvement from this change
- Higher resolution: 512 and 1024 pixels
- Released comprehensive technical paper
  - Details on architecture and training
  - Example: "astronaut riding a horse" - semantically meaningful and well-aligned
  - Images showed natural composition and high visual quality

#### DALL·E 3 (2023)
- Further improvements in resolution and features
- Support for different aspect ratios (square, landscape, portrait)
- Limited technical details publicly available

#### GPT-4o and GPT Image 1 (2024-2025)
- Latest models with exceptional text rendering capabilities
  - Earlier models struggled with text in images (misspellings, gibberish)
  - These models render text accurately
- GPT Image 1 is currently their best model
  - Text not only spelled correctly but semantically meaningful
  - Complex representations handled well
- Speculation: hybrid architecture
  - Reverse engineering suggests possible combination of diffusion + autoregressive
  - Autoregressive may handle text rendering
  - Diffusion provides high visual quality

### Google's Competing Systems: Imagen Family

Google followed a similar trajectory with their Imagen models:

#### Progressive Releases
- Imagen 1 (2022): 64×64 starting point
- Imagen 2: 1024 resolution
- Imagen 3: 1024 with multiple aspect ratios
- Imagen 4 and Imagen 4 Ultra: current state-of-the-art
  - Comparable quality to GPT Image 1
  - Excellent text rendering
  - Support for prompts in multiple languages (Korean, Japanese, Spanish, etc.)

#### Comparative Example
- Same prompt tested on both OpenAI and Google models
  - Prompt: person studying machine learning at sunrise with laptop
- Google's Imagen showed impressive results
  - Natural scene composition
  - Accurate details (laptop with diagram visible, books stacked naturally)
  - Better than OpenAI's result for this particular prompt

### Other Notable Providers

#### Flux (Black Forest Labs)
- Recently gaining recognition for high quality
- Offers 200 free credits for experimentation
- Comparable to or better than OpenAI for certain prompts
- Strong performance in current leaderboards

#### Model Leaderboards and Resources
- Father.ai provides comprehensive comparison
  - Current rankings: GPT Image 1 and Imagen 4 at top
  - Flux ranking highly among recent models
- Important to note licensing
  - Many top models are proprietary/closed
  - Some open-source alternatives available but with quality gaps

## Building Text-to-Image Models: The Four Steps

### Comprehensive Framework

Any machine learning model, including text-to-image diffusion models, requires four key components:

#### 1. Data Preparation
- Need millions of image-caption pairs
  - Each image paired with textual description
  - Captions must be accurate and detailed
- Common public datasets
  - LAION 5.0: billions of image-text pairs from web
  - DataComp: curated dataset with quality filtering
- Data quality directly impacts model quality
  - Clean, accurate captions lead to better text-image alignment

#### 2. Architecture Design
- Must decide on model structure
  - What layers to use
  - How to arrange them
  - How to condition on text

#### 3. Training Process
- Define inputs and outputs
  - What the model receives during training
  - What it should predict
- Specify loss function and optimization strategy
  - How to measure model performance
  - How to update parameters to improve

#### 4. Sampling Method
- How to generate new images after training
  - Diffusion sampling: iterative denoising process
  - Number of steps, scheduling, etc.

## Model Architectures for Diffusion

### UNet: The First Architecture

#### Structure
- Encoder-decoder architecture with skip connections
  - Encoder: progressive downsampling with convolutions
    - Image becomes smaller spatially but deeper in channels
    - Example: 64×64 → 32×32 → 16×16 → 4×4, with increasing channel depth
  - Decoder: progressive upsampling with transpose convolutions
    - Reverse process: smaller/deeper → larger/shallower
    - Final output same size as input
  - Skip connections: connect corresponding encoder and decoder layers
    - Help preserve fine details during upsampling

#### Text Conditioning
- Original UNet not designed for conditioning
- Text integration through additional layers
  - Text encoder converts prompts to numerical vectors (embeddings)
  - Cross-attention layers allow model to reference text during generation
  - The denoising process is influenced by text embeddings at multiple stages

### DiT: Diffusion Transformer (2023)

#### Architectural Shift
- Replace convolution-based UNet with transformer-based architecture
- "DiT" = Diffusion Transformer
  - Fully transformer-based processing
  - Leverages success of transformers in other domains

#### Why Transformers?
- More powerful representation learning through self-attention
- Better scalability with more data and compute
  - Performance improves more predictably when scaling up
- Has become the standard for modern text-to-image models
  - All recent state-of-the-art systems use DiT or variants

#### Processing Pipeline
- **Patchify**: convert image to sequence
  - Divide image into patches (e.g., 16×16 pixel patches)
  - Flatten each patch into a vector
  - Project to desired embedding dimension
  - Now have a sequence of patch embeddings
- **Positional Encoding**: add position information
  - Can use 1D encoding (sequential numbering)
  - Or 2D encoding (row, column coordinates)
  - Tells model spatial relationships between patches
- **Transformer Blocks**: process sequence
  - Self-attention allows patches to interact
  - Cross-attention integrates text conditioning
  - Multiple layers progressively refine representations
- **Unpatchify**: convert back to image
  - Reverse of patchify process
  - Sequence of vectors → 2D image
  - Output has same shape as input

#### Conditioning in DiT
- Two types of conditioning inputs
  - Text embeddings from text encoder
  - Timestep t (how noisy the current image is)
- Cross-attention layers integrate these conditions
  - At various depths in the transformer
  - Influences how noise prediction evolves

### Architecture Takeaway

Modern text-to-image systems predominantly use DiT:

- Replaced UNet as the standard architecture
- Better quality and scalability
- All major recent models (Imagen 4, GPT Image 1, etc.) use transformer-based diffusion
