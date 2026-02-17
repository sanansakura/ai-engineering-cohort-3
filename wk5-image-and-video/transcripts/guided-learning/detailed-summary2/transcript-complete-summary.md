# Image and Video Generation Complete Summary

Week 5 guided-learning session covering the evolution of generative models from VAEs and GANs to modern diffusion-based text-to-image and text-to-video systems. The lecture explains how these technologies work, how to build them, and how leading companies like OpenAI and Google implement them in production systems.

---

## Key Takeaways

- **Diffusion models** have become the dominant approach for both text-to-image and text-to-video generation, replacing earlier methods like VAEs, GANs, and autoregressive models due to superior quality and training stability.
- **DiT (Diffusion Transformer)** is now the standard architecture, using transformers instead of convolutions to process images as sequences of patches with cross-attention for text conditioning.
- **Latent diffusion** is essential for video generation, using VAEs as compression networks to reduce computational requirements by ~512×, making high-resolution video generation practical.
- **Text conditioning** gives users control over generation, transforming generative models from academic curiosities into practical creative tools. The shift from unconditional to text-to-image generation was crucial for real-world adoption.
- **Quality metrics** (Inception Score, FID, CLIP) help evaluate models across three dimensions: image quality, diversity, and text-image alignment, though human evaluation remains important.

---

## Evolution of Generative Modeling

### VAEs (Variational Autoencoders)

#### Historical Importance
- Introduced in 2013 paper "Auto-Encoding Variational Bayes" (building on 1980s concepts)
- First reasonably capable neural network for image generation
  - Community was initially excited by this breakthrough
  - Demonstrated that neural networks could learn to generate novel images

#### How VAEs Work

##### Architecture
- Two neural network components working together
  - **Encoder**: compresses input images into compact latent representations (typically 1D vectors)
    - Captures essential features needed to reconstruct the image
    - Progressive dimensionality reduction through layers
  - **Decoder**: reconstructs images from latent representations
    - Inverse process of encoder
    - Generates full-sized images from compressed codes

##### Training Process
- Trained end-to-end using reconstruction loss (typically MSE)
  - Measures how well reconstructed image matches original
  - Optimizer adjusts both encoder and decoder parameters
- Creates a meaningful compressed representation of the image space

##### Generation Method
- For generating new images, discard the encoder
  - Sample random vectors from a distribution (e.g., Gaussian)
  - Feed through decoder to produce novel images
  - Images resemble training data but aren't copies
- Example: MNIST digit generation
  - 60,000 training images of 28×28 handwritten digits
  - After training, can generate new realistic digit images

##### Latent Space Structure
- Trained latent space exhibits interesting properties
  - Training examples cluster by category (e.g., all "1"s group together)
  - Natural clustering makes reconstruction easier
  - Smooth interpolation possible between different categories
  - Sampling from "empty" regions generates novel combinations

#### Modern Status

While no longer used for direct generation, VAEs remain crucial:

- **Limitation**: Generated images are blurry and lack fine detail
  - Made them unsuitable for high-quality image generation
- **Current application**: Compression networks in latent diffusion models
  - Transform high-dimensional images to lower-dimensional latent space
  - Enable efficient operation of diffusion models
  - This role is essential in systems like Sora and Stable Diffusion

### GANs (Generative Adversarial Networks)

#### Revolutionary Impact
- Introduced by Ian Goodfellow; became one of the most influential computer vision papers
  - Cited hundreds of thousands of times
- Overcame VAE limitations with much sharper, more detailed images
  - Major leap forward in generation quality

#### Adversarial Training Mechanism

##### Two Competing Networks
- **Generator**: 
  - Takes random vector input
  - Transforms through neural network layers into generated image
  - Goal: fool discriminator into classifying fakes as real
- **Discriminator**:
  - Takes image input (real from dataset or fake from generator)
  - Outputs classification: real or fake
  - Goal: correctly identify authentic vs AI-generated images

##### Training Dynamics
- Both networks trained simultaneously in a competitive game
  - Generator improves at fooling discriminator
  - Discriminator improves at detecting fakes
  - This adversarial competition drives mutual improvement
- Loss functions create opposing objectives
  - Generator: lower loss when discriminator makes mistakes
  - Discriminator: lower loss when correctly classifying both types

#### Practical Challenges
- Notoriously difficult to train
  - **Mode collapse**: generator produces limited variety
  - **Vanishing gradients**: discriminator dominates, generator can't learn
- Google offers comprehensive GAN training course
  - Covers common problems and mitigation strategies

#### Evolution and Variants

##### StyleGAN's Innovations
- Smooth latent space enables attribute manipulation
  - Gradual movement in latent space produces smooth visual transitions
  - Specific directions correspond to semantic attributes (smile, glasses, etc.)
- Enabled fine-grained control over generated image properties
  - Users can interpolate between different facial expressions
  - Attributes can be added or removed systematically

##### Current Status
- Despite historical importance, GANs less common in modern systems
  - No longer primary technique for text-to-image or text-to-video
  - Most state-of-the-art systems use diffusion instead
  - Important for understanding generative model evolution

### Autoregressive Modeling

#### Core Concept: Sequential Generation

Autoregressive models reformulate image generation as sequence prediction:

- Treat images as sequences of pixels or patches
  - Generate one element at a time
  - Each prediction conditioned on all previous elements
- Fundamentally different from VAEs and GANs
  - VAEs: compress and reconstruct
  - GANs: generate all pixels simultaneously through adversarial process
  - Autoregressive: build images piece by piece

#### Technical Evolution

##### PixelCNN (2016)
- Introduced by van den Oord at DeepMind
- Used CNNs for sequential modeling
  - Each pixel predicted based on local neighborhood context
  - All previously generated pixels inform each new prediction

##### Image Transformer
- Google replaced CNNs with transformer architecture
  - Leveraged self-attention for better long-range dependency modeling
  - Transformers naturally suited for sequence processing

#### Enabling Text-to-Image

##### Cross-Attention for Conditioning
- Transformers include cross-attention layers
  - Can attend to external information (text descriptions)
  - Integrate text guidance into generation process
- Each pixel prediction considers both:
  - Previously generated pixels
  - Text conditioning from prompt

##### DALL·E: Breakthrough System (January 2021)
- OpenAI's first successful text-to-image system
  - Used autoregressive modeling with transformer architecture
  - Generated images token by token, conditioned on text
- Notable results: "armchair in the shape of an avocado"
  - Combined concepts creatively not seen in training
  - Demonstrated semantic understanding across modalities

#### Strengths and Limitations

- **Advantages**: High-quality coherent images; flexible conditioning; excellent global structure
- **Current status**: Not dominant despite capabilities
  - Most state-of-the-art systems use diffusion instead
  - Diffusion models proved more effective for T2I and T2V tasks

### Diffusion Models: Current State-of-the-Art

#### Core Mechanism

Diffusion takes a unique approach through noise addition and removal:

##### Forward Process (Adding Noise)
- Start with clean training image
- Gradually add Gaussian noise over timesteps (typically t=1 to 1000)
  - Higher t means more noise
  - Continue until image is pure random noise
- Deterministic process requiring no learning

##### Backward Process (Learning to Denoise)
- Train neural network to reverse forward process
  - Given noisy image at timestep t, predict the noise
  - Removes noise to produce cleaner image
- Key insight: learning to denoise teaches model about image structure
  - To remove noise successfully, model must understand what realistic images look like

#### Historical Development

##### 2015: Theoretical Foundation
- Original paper introduced mathematical framework
- Defined forward and backward processes
- Showed how to learn data distributions through diffusion

##### 2020: Breakthrough (DDPM)
- "Denoising Diffusion Probabilistic Models" from UC Berkeley
- First successful high-resolution diffusion images (256×256)
  - Demonstrated diffusion could produce high-quality realistic results
- Sparked widespread adoption and rapid improvements

#### Why Diffusion Dominates

Several factors explain diffusion's success:

- **Quality**: Consistently higher visual quality than alternatives
  - More photorealistic appearance
  - Superior fine details and textures
- **Stability**: More stable training than GANs
  - Fewer failure modes
  - More predictable convergence
- **Scalability**: Better than autoregressive at scale
  - Efficiently leverages powerful architectures
- **Active optimization**: Research continues to address speed
  - Many techniques to reduce inference steps
  - Practical systems use 15-20 steps instead of 1000

---

## From Unconditional to Text-to-Image Generation

### The Control Problem

Early generative models generated random samples with no user control:

#### Limitations of Unconditional Generation
- Models sample randomly from learned distribution
  - Example: "This Person Does Not Exist" website generates random faces
  - Users cannot specify desired attributes (gender, age, accessories)
- Severely limits practical utility
  - Users typically have specific needs
  - Random outputs rarely meet those needs

### Text-to-Image as Solution

The industry shifted toward conditional generation:

#### How T2I Works
- Extends underlying techniques (diffusion, autoregressive, etc.) with text conditioning
  - User provides text description
  - Model generates images matching that description
- Gives users precise control while maintaining quality

#### Why T2I Became Standard
- Much more useful for practical applications
  - Content creation, design, prototyping
  - Users iteratively refine prompts to achieve desired results
- All modern systems focus on T2I
  - DALL·E, Midjourney, Stable Diffusion, Imagen all text-conditioned

---

## Commercial Text-to-Image Systems

### OpenAI's DALL·E Evolution

#### DALL·E 1 (2021)
- 256×256 resolution; autoregressive modeling
- Proof-of-concept for text-to-image generation

#### DALL·E 2 (2022)
- Switched from autoregressive to diffusion
  - Immediate and substantial quality improvement
- Higher resolutions (512, 1024 pixels)
- Released comprehensive technical paper with architectural details
- Example: "astronaut riding a horse" showed natural composition and alignment

#### DALL·E 3 (2023)
- Further quality and feature improvements
- Multiple aspect ratio support
- Limited technical details publicly available

#### GPT-4o and GPT Image 1 (2024-2025)
- Exceptional text rendering capabilities
  - Earlier models struggled with text (misspellings, gibberish)
  - These models render text accurately and semantically meaningfully
- GPT Image 1 is OpenAI's current best model
- Speculation suggests hybrid architecture
  - Possibly combines diffusion (visual quality) + autoregressive (text rendering)

### Google's Imagen Family

#### Progressive Development
- Imagen 1 (2022): 64×64 starting point
- Imagen 2: 1024 resolution
- Imagen 3: 1024 with multiple aspect ratios
- Imagen 4 and Imagen 4 Ultra: current state-of-the-art
  - Quality comparable to GPT Image 1
  - Excellent text rendering
  - Multilingual prompt support (Korean, Japanese, Spanish, etc.)

### Other Notable Systems

#### Flux (Black Forest Labs)
- Recently gaining recognition for high quality output
- Offers 200 free credits for experimentation
- Ranks highly in current leaderboards

#### Model Comparison Resources
- Father.ai provides comprehensive leaderboard
  - Current top: GPT Image 1 and Imagen 4
- Important to note licensing
  - Many top models proprietary/closed
  - Quality gap exists with open-source alternatives

---

## Building Text-to-Image Diffusion Models

### The Four-Step Framework

Building any ML model, including T2I diffusion, requires four components:

#### 1. Data Preparation
- Need millions of image-caption pairs
  - Each image with accurate textual description
- Common public datasets
  - LAION 5.0: billions of web-scraped pairs
  - DataComp: quality-filtered dataset
- Data quality directly impacts model quality

#### 2. Architecture Design
- Must choose model structure, layers, and arrangement
- How to condition on text effectively

#### 3. Training Process  
- Define inputs, outputs, loss function, optimization strategy
- How to measure and improve performance

#### 4. Sampling Method
- How to generate new images from trained model
- For diffusion: iterative denoising process

### Architecture: From UNet to DiT

#### UNet: First Architecture

##### Structure
- Encoder-decoder with skip connections
  - **Encoder**: progressive downsampling with convolutions
    - Image becomes smaller spatially, deeper in channels
    - Example: 64×64 → 32×32 → 16×16 → 4×4 with increasing depth
  - **Decoder**: progressive upsampling with transpose convolutions
    - Reverse process: smaller/deeper → larger/shallower
  - **Skip connections**: preserve fine details during upsampling

##### Text Conditioning in UNet
- Text encoder converts prompts to numerical embeddings
- Cross-attention layers allow model to reference text
- Denoising process influenced by text at multiple stages

#### DiT: Diffusion Transformer (2023)

##### Architectural Shift
- Replace convolution-based UNet with fully transformer-based architecture
- Leverages transformer success from other domains (NLP, etc.)

##### Why Transformers Won
- More powerful representation learning through self-attention
- Better scalability with data and compute
  - Performance improves predictably when scaling
- Now standard for modern T2I models
  - All recent state-of-the-art systems use DiT or variants

##### DiT Processing Pipeline

**Patchify**: Convert image to sequence
- Divide image into patches (e.g., 16×16 pixels)
- Flatten each patch into vector
- Project to desired embedding dimension
- Result: sequence of patch embeddings

**Positional Encoding**: Add spatial information
- Can use 1D encoding (sequential numbering)
- Or 2D encoding (row, column coordinates)
- Tells model spatial relationships between patches

**Transformer Blocks**: Process sequence
- Self-attention allows patches to interact
- Cross-attention integrates text conditioning
- Multiple layers progressively refine representations

**Unpatchify**: Convert back to image
- Reverse patchify process
- Sequence of vectors → 2D image
- Output matches input shape

##### Conditioning in DiT
- Two conditioning inputs
  - Text embeddings from text encoder
  - Timestep t (indicates noise level)
- Cross-attention layers integrate conditions throughout processing

### Training Diffusion Models

#### Forward and Backward Processes

##### Forward: Adding Noise
- Take clean image from training data
- Add Gaussian noise over timesteps t (1-1000)
- Deterministic process, no learning required

##### Backward: Learning to Denoise
- Diffusion model learns to reverse forward process
- Given noisy image at timestep t, predict the noise
- Better predictions indicate better understanding of image structure

#### Detailed Training Loop

Each iteration involves:

**Step 1: Add Noise**
- Take clean training image
- Randomly sample timestep t (1-1000)
- Apply forward process to create noisy image x_t

**Step 2: Prepare Conditions**
- Text: encode caption using text encoder (CLIP, T5, etc.)
- Timestep: represent t as embedding (tells model noise level)

**Step 3: Predict Noise**
- Feed noisy image, text, timestep to diffusion model
- Process through transformer with cross-attention
- Output: predicted noise

**Step 4: Calculate Loss**
- Compare predicted noise with actual added noise
- Use MSE (Mean Squared Error) loss
- Measure pixel-wise differences

**Step 5: Update Parameters**
- Backpropagate loss
- Optimizer updates model parameters
- Improves noise prediction accuracy

#### Why Denoising Works

The denoising objective implicitly learns data distribution:

- To predict noise accurately, model must know what real images look like
- Different noise levels provide complementary information
  - High noise (large t): learn global structure
  - Low noise (small t): learn fine details
- Text conditioning ensures outputs match prompts

### Sampling (Generation)

#### Basic Sampling Process

Generate new images through iterative denoising:

**Starting Point**
- Begin with pure random noise (timestep t=1000)

**Iterative Denoising**
- Pass noisy image, text prompt, current timestep to model
- Model predicts noise in current image
- Subtract predicted noise to get cleaner image
- Move from x_t to x_{t-1}
- Repeat for many steps

**Final Output**
- After all steps, arrive at x_0 (final generated image)
- Should be high quality and match text prompt

#### Optimizing Sampling Speed

Traditional 1000-step sampling is slow:

**The Speed Problem**
- Each step requires full forward pass through model
- Major bottleneck for deployment

**Solutions**
- **DDIM**: Skip steps without quality loss (reduces to ~50 steps)
- **Distillation**: Train faster models that mimic original (10-20 steps)
- **Extreme cases**: Research on 1-2 step models

**Practical Deployment**
- Most systems use 15-20 steps
  - Good balance of quality and speed
  - Much faster than 1000 steps
  - Maintains high visual quality

### Evaluation Metrics

#### Three Quality Dimensions

Text-to-image models evaluated across:

1. **Image Quality**: Visual appeal, sharpness, realism
2. **Diversity**: Variety in styles, subjects, compositions
3. **Text-Image Alignment**: Match between images and prompts

#### Key Metrics

##### Inception Score (Quality + Diversity)
- Uses pre-trained Inception V3 classifier
- Process:
  - Generate images, run through Inception for class probabilities
  - Sharp distributions indicate clear subjects (quality)
  - Flat marginal distribution indicates variety (diversity)
  - Compute KL divergence between individual and marginal

##### FID (Fréchet Inception Distance)
- Compares statistics of real vs. generated images
- Process:
  - Extract Inception features from both real and generated
  - Calculate distance between distributions
  - Lower FID = more similar to real images

##### CLIP Score (Text-Image Alignment)
- Uses CLIP's shared embedding space
- Process:
  - Encode text prompt with CLIP text encoder
  - Encode generated image with CLIP image encoder
  - Calculate cosine similarity between embeddings
  - Higher similarity = better alignment

#### Evaluation Considerations
- All metrics are proxies for human judgment
- Inception-based metrics depend on Inception's biases
- CLIP score limited by CLIP's understanding
- Human evaluation remains important for subjective quality
- Multiple metrics together give better picture than any single one

---

## Text-to-Video Generation

### Extending T2I to T2V

Text-to-video is similar to text-to-image but with added complexity:

#### Key Difference
- T2I output: single image
- T2V output: sequence of frames (e.g., 120 frames)
  - When played sequentially, forms a video
- Much more computationally expensive
  - Model must generate hundreds of images instead of one
  - Requires significant optimization to make practical

### Latent Diffusion: Essential for Video

#### The Efficiency Challenge

Operating in pixel space is prohibitively expensive:

- Example: 1280×720 video with 120 frames
  - Total: ~110 million pixels to generate
  - Diffusion in pixel space would be extremely slow

#### Solution: Latent Space Compression

Use VAE as compression network:

**Encoder**: Video → Latent Representation
- Compress both spatially and temporally
- Example: 8× compression factor in each dimension
  - 1280 → 160 width
  - 720 → 90 height  
  - 120 → 15 frames
- Result: ~216,000 latent "pixels" instead of 110 million
- Approximately 512× more efficient

**Diffusion in Latent Space**
- Train diffusion model to operate on compressed representations
- Much more computationally manageable

**Decoder**: Latent → Video
- VAE decoder transforms back to pixel space
- Produces final video output

**Real-World Application**
- Sora blog explicitly mentions using compression to latent space
- This technique makes high-resolution video generation practical

### Video Data and Training

#### Data Challenges

Video data is more scarce than image data:

**The Scarcity Problem**
- Image datasets: billions of pairs (e.g., LAION 5.0)
- Video datasets: much smaller scale
- High-quality video-caption pairs harder to obtain

**Mitigation Strategies**

Two common approaches:

1. **Joint Image+Video Training**
   - Images can be treated as 1-frame videos
   - Combine both data types in training
   - Leverage abundant image data

2. **Pretrain then Finetune**
   - Pretrain on images to learn spatial information
     - Colors, objects, compositions, textures
   - Finetune on video to learn temporal information
     - Motion, actions, dynamics
   - Often faster than joint training

#### Efficiency Techniques

**Precompute Latent Representations**
- Use trained VAE to encode all training videos
- Store compressed latents for training
- Avoids encoding during each training iteration

**Separate Resolution Models**
- Base model generates low-resolution video in latent space
- **Spatial upsampler**: increases resolution (e.g., 4× spatial)
  - Keeps frame count constant
- **Temporal upsampler**: increases frame rate (e.g., 2× temporal)
  - Keeps spatial resolution constant
  - Example: 12 fps → 24 fps
- Training separate models more efficient than single high-res model

### Video DiT Architecture

Extend image DiT to handle 3D (spatial + temporal) data:

#### 3D Patchify
- Images: divide into 2D patches
- Videos: divide into 3D patches (cubes)
  - Patches across both spatial dimensions and time
- Each 3D patch flattened to vector
- Apply projection to get desired embedding size
- Result: longer sequence than image (due to temporal dimension)

#### 3D Positional Encoding
- Images: 1D or 2D positional encoding
- Videos: add temporal dimension
  - Can use 1D: sequential numbering across all patches
  - Or 3D: (column, row, time) coordinates
- Informs model of spatial and temporal relationships

#### Same Transformer Core
- Process sequence with transformer blocks
  - Self-attention allows all patches to interact
  - Cross-attention integrates text and timestep conditions
- Architecture fundamentally same as image DiT
  - Just handles longer sequences with temporal information

#### 3D Unpatchify
- Convert sequence back to 3D output (video)
- Ensures output has same shape as input

### Generation Pipeline

Complete text-to-video generation workflow:

#### Step 1: Base Generation (Latent Space)
- Start with random 3D noise
- Apply diffusion model conditioned on text prompt
- Iteratively denoise in latent space
- Result: denoised latent representation

#### Step 2: Decode to Pixels
- Use VAE decoder to convert latent to pixel video
- This produces viewable video but at base resolution

#### Step 3: Spatial Upsampling (Optional)
- Pass through spatial resolution model
- Increases resolution 4× while keeping frame count constant

#### Step 4: Temporal Upsampling (Optional)
- Pass through temporal resolution model
- Increases frame rate 2× while keeping resolution constant

#### Step 5: Final Video
- High-resolution, high-frame-rate video matching text prompt

### Production System Design (Sora-Like)

Complete system includes multiple components beyond diffusion model:

#### 1. Prompt Autocomplete
- Suggests completions as user types
- Improves user experience (like Google Search)

#### 2. Safety Service (Prompt Filtering)
- Analyzes submitted prompt for inappropriate requests
- Rejects unsafe prompts before generation
- Prevents misuse of system

#### 3. Prompt Enhancer
- Improves user-provided prompts
  - Fixes spelling and grammar issues
  - Adds detail for ambiguous descriptions
  - Paraphrases for clarity
- Results in better generation quality

#### 4. Diffusion Generation
- Core model generates video in latent space
- Conditioned on enhanced prompt and timestep
- Output: latent representation of video

#### 5. VAE Decoder
- Converts latent representation to pixel video
- Makes video viewable

#### 6. Output Safety Check
- Analyzes generated video content
- Rejects inappropriate outputs even if prompt was acceptable
- Final safety layer before user sees result

#### 7. Spatial Resolution Model
- Increases spatial resolution (e.g., 4×)
- Maintains frame count

#### 8. Temporal Resolution Model
- Increases frame rate (e.g., 2×)
- Maintains spatial resolution

#### 9. Final Delivery
- High-quality video delivered to user
- Matches original text prompt

### Commercial T2V Systems

#### Sora (OpenAI, February 2024)
- Limited technical details publicly available
- Known: diffusion-based with compression to latent space
- Generates impressive high-quality videos

#### Veo (Google)
- Veo 1, 2, 3 progressive releases
- Veo 3 can generate video with synchronized audio
- Accessible through interface for testing

#### Other Providers
- Kling, Runway, Pika, and others
- Leaderboards (similar to T2I) track quality
- Most top models are proprietary/closed source

---

## Summary

Modern image and video generation relies on diffusion models operating in latent space with transformer architectures (DiT). Text conditioning via cross-attention enables user control, making these systems practical for creative applications. The evolution from VAEs (blurry) to GANs (training instability) to autoregressive (sequential slowness) to diffusion (high quality + stable training) represents significant progress. Production systems require not just the core diffusion model but also safety filtering, prompt enhancement, VAE compression, and resolution upsampling to deliver high-quality results. As research continues, focus areas include faster sampling, better text-image alignment, and more efficient video generation.
