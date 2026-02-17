# Chunk 6 Summary

## Diffusion Training Process

### Forward and Backward Processes

The training of diffusion models involves two complementary processes:

#### Forward Process: Adding Noise
- Take a clean image from training data
- Gradually add Gaussian noise over timesteps t (typically 1-1000)
  - t=1: almost no noise
  - t=1000: pure random noise
  - Higher t means more noise
- This process requires no learning - it's just noise addition
  - Provides the noisy training examples for the model

#### Backward Process: Learning to Denoise
- The diffusion model learns to reverse the forward process
  - Given a noisy image at timestep t, predict the noise
  - Or equivalently, predict a denoised version
- Training objective: predict noise accurately
  - Better predictions mean better understanding of image structure

### Detailed Training Loop

Each training iteration involves several steps:

#### Step 1: Add Noise
- Take a clean training image
- Randomly sample timestep t (between 1 and 1000)
  - Different noise levels provide varied training examples
- Apply forward process to create noisy image x_t

#### Step 2: Prepare Conditions
- Text conditioning: encode the caption
  - Use a text encoder (e.g., CLIP or T5)
  - Get sequence of text embedding vectors
- Timestep conditioning: represent t as an embedding
  - Tells model how noisy the input is
  - Critical for successful denoising

#### Step 3: Predict Noise
- Feed noisy image, text embeddings, and timestep to diffusion model
  - Model processes through transformer layers
  - Cross-attention integrates text and timestep information
  - Output: predicted noise

#### Step 4: Calculate Loss
- Compare predicted noise with actual noise added
  - Use Mean Squared Error (MSE) loss
  - Measure pixel-wise differences
- This simple loss function works remarkably well

#### Step 5: Update Parameters
- Backpropagate the loss
- Optimizer updates model parameters
  - Improves noise prediction accuracy over time

### Why This Works

The denoising objective implicitly learns the data distribution:

- To predict noise accurately, model must know what "real" images look like
- Different noise levels provide complementary information
  - High noise (large t): learn global structure
  - Low noise (small t): learn fine details
- Text conditioning ensures generated images match prompts

## Diffusion Sampling (Generation)

### Basic Sampling Process

After training, generate new images through iterative denoising:

#### Starting Point
- Begin with pure random noise
  - Sampled from standard Gaussian distribution
  - This represents timestep t=1000

#### Iterative Denoising
- Pass noisy image, desired text prompt, and current timestep to model
  - Model predicts the noise in current image
- Subtract predicted noise to get slightly cleaner image
  - Move from x_t to x_{t-1}
- Repeat for many steps
  - Gradually refine from noise to clear image

#### Final Output
- After all steps (traditionally 1000), arrive at x_0
  - This is the final generated image
  - Should be high quality and match text prompt

### Optimizing Sampling Speed

Traditional 1000-step sampling is very slow:

#### The Speed Problem
- Each step requires a full forward pass through the model
- 1000 steps takes significant time
  - Major bottleneck for practical deployment

#### Solutions and Techniques
- **DDIM (Denoising Diffusion Implicit Models)**
  - Enables skipping steps without quality loss
  - Can reduce to ~50 steps
- **Distillation**
  - Train smaller/faster models to mimic the original
  - Can achieve high quality in 10-20 steps
- **Extreme cases**: 1-2 step models
  - Research direction: maintain quality with minimal steps

#### Practical Trade-offs
- Most deployed systems use 15-20 steps
  - Good balance of quality and speed
  - Much faster than 1000 steps
  - Still maintains high visual quality

## Evaluation Metrics

### Three Dimensions of Quality

Text-to-image models must be evaluated across multiple aspects:

#### 1. Image Quality
- Are the generated images visually appealing?
  - Sharp details, realistic textures
  - Proper composition and lighting

#### 2. Diversity
- Can the model generate varied outputs?
  - Different styles, subjects, compositions
  - Not stuck producing similar images

#### 3. Text-Image Alignment
- Do generated images match the prompts?
  - All elements from prompt present
  - Semantic relationships correct

### Key Metrics

#### Inception Score (Quality + Diversity)
- Uses pre-trained Inception V3 classifier
  - Originally trained on ImageNet (1000 classes)
- Process:
  1. Generate images with the model
  2. Run through Inception to get class probabilities
  3. Check if distributions are "sharp" (confident predictions)
    - Sharp distributions indicate clear, recognizable subjects (quality)
  4. Calculate marginal distribution (average across images)
    - Flat marginal indicates variety across classes (diversity)
  5. Compute KL divergence between individual and marginal
    - High divergence = good quality + diversity

#### FID (Fréchet Inception Distance)
- Compares statistics of real vs. generated images
- Process:
  1. Extract features from real images using Inception
    - Get mean and covariance of feature distributions
  2. Extract features from generated images
    - Same process for fake images
  3. Calculate distance between the two distributions
    - Lower FID = generated images more similar to real
- Measures both quality and diversity in a single score

#### CLIP Score (Text-Image Alignment)
- Uses CLIP's shared embedding space
  - CLIP trained to map text and images to same space
  - Similar text-image pairs are close in embedding space
- Process:
  1. Encode text prompt with CLIP text encoder
  2. Encode generated image with CLIP image encoder
  3. Calculate cosine similarity between embeddings
    - Higher similarity = better alignment

### Evaluation Considerations

All these metrics are proxies for human judgment:

- Inception-based metrics (IS, FID) may not capture all aspects of quality
  - Depend on Inception's biases
- CLIP score limited by CLIP's understanding
  - May miss nuanced semantic relationships
- Human evaluation still important
  - Especially for subjective quality assessment
- Multiple metrics together give better picture than any single metric

## Summary of Text-to-Image Pipeline

### Complete System

Building a text-to-image diffusion model requires:

1. **Data**: Clean image-caption pairs (LAION, DataComp, etc.)
2. **Architecture**: DiT (Diffusion Transformer) is current standard
   - Patchify → Transformer → Unpatchify
   - Cross-attention for text conditioning
3. **Training**: Forward-backward diffusion with MSE loss
   - Add noise (forward), learn to denoise (backward)
   - Condition on text and timestep
4. **Sampling**: Iterative denoising from noise to image
   - 15-20 steps typical with optimizations
5. **Evaluation**: IS, FID for quality/diversity; CLIP for alignment

This foundation extends to text-to-video, which will be covered next.
