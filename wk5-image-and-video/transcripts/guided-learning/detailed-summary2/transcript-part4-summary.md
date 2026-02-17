# Chunk 4 Summary

## Diffusion Models: The Current State-of-the-Art

### Core Mechanism

Diffusion models take a fundamentally different approach from previous methods:

#### Forward Process (Adding Noise)
- Start with a clean image from the training data
- Gradually add noise over multiple steps
  - Each step makes the image slightly noisier
  - Continue until the image is pure random noise
- This process is deterministic and requires no learning

#### Backward Process (Denoising)
- Train a neural network to reverse the forward process
  - Given a noisy image, predict the noise that was added
  - Or equivalently, predict a slightly denoised version
- The model learns to remove noise step by step
  - Through this denoising process, it learns the data distribution

### Generation Through Denoising

Once trained, generation is intuitive:

- Start with pure random noise
- Apply the diffusion model iteratively to remove noise
  - Each step produces a slightly cleaner image
  - After many steps, arrive at a high-quality generated image
- The key insight: learning to denoise teaches the model about image structure
  - To remove noise successfully, the model must know what realistic images look like

### Historical Development

#### 2015: Theoretical Foundation
- Original diffusion models paper introduced the mathematical framework
  - Defined the forward and backward processes
  - Showed how to learn data distributions through diffusion

#### 2020: Breakthrough (DDPM)
- "Denoising Diffusion Probabilistic Models" from UC Berkeley
  - First successful high-resolution diffusion-generated images (256×256)
  - Demonstrated that diffusion could produce high-quality, realistic images
- This paper sparked widespread adoption
  - Community recognized diffusion's potential
  - Led to rapid improvements and variants

### OpenAI's Pivot: DALL·E 1 to DALL·E 2

The transition from DALL·E 1 to DALL·E 2 highlights diffusion's advantages:

#### DALL·E 1 (2021)
- Used autoregressive modeling approach
- Generated 256×256 images
- While impressive, had limitations in quality

#### DALL·E 2 (2022)
- OpenAI switched from autoregressive to diffusion
  - This architectural change brought substantial quality improvements
- Could generate higher resolutions (512, 1024 pixels)
  - Images were sharper and more detailed
  - Better aligned with text prompts
- Included technical paper with architectural details
  - Showed specific techniques like CLIP embeddings for text conditioning

### Quality Comparison

The lecture emphasizes the remarkable progress:

- VAEs to diffusion in just a few years
  - From blurry MNIST digits to photorealistic high-resolution images
- This rapid improvement demonstrates diffusion's superiority
  - Better quality than VAEs
  - More stable training than GANs
  - Better scalability than autoregressive methods

## Comparing Generative Approaches

### Quality vs. Speed Trade-offs

Different approaches have different characteristics:

#### VAEs and GANs
- Quality: lower by modern standards
  - VAEs produce blurry outputs
  - GANs better but still limited
- Speed: fast generation
  - Single forward pass produces an image
- Status: not competitive for current applications

#### Autoregressive and Diffusion
- Quality: excellent, high-resolution, coherent
  - Both can produce photorealistic images
  - Strong semantic understanding
- Speed: slower than VAEs/GANs
  - Autoregressive: generate one token at a time
  - Diffusion: require many denoising steps (traditionally 1000)
- Status: diffusion dominates for T2I and T2V

### Why Diffusion Won

Several factors explain diffusion's dominance:

- Consistently higher visual quality
  - More photorealistic appearance
  - Better fine details and textures
- More stable training than GANs
  - Fewer failure modes
  - More predictable convergence
- Better scalability than autoregressive
  - Can leverage powerful architectures efficiently
- Active research continues to address speed
  - Many techniques to reduce inference steps
  - 15-20 steps often sufficient instead of 1000

## From Unconditional to Text-to-Image

### The Control Problem

Early generative models lacked user control:

#### Unconditional Generation Issues
- Models generate random samples from learned distribution
  - No way to specify what you want
  - Example: "This Person Does Not Exist" website
    - Each refresh generates a random face
    - Cannot request specific attributes (gender, glasses, etc.)
- This limitation makes models less useful for practical applications
  - Users typically have specific needs
  - Random generation doesn't meet those needs

### Text-to-Image as a Solution

The industry shifted toward conditional generation:

#### Text-to-Image (T2I) Models
- Extend the same underlying techniques (diffusion, autoregressive, etc.)
- Add conditioning on text prompts
  - User provides text description
  - Model generates images matching that description
- This gives users control while maintaining quality
  - Can specify exactly what image is needed
  - Model generates based on those specifications

#### Why T2I Became Standard
- Much more useful for practical applications
  - Design, content creation, prototyping
  - Users can iteratively refine prompts to get desired outputs
- Most modern systems focus on T2I rather than unconditional generation
  - DALL·E, Midjourney, Stable Diffusion, etc. all text-conditioned
  - This lecture will focus on building T2I systems
