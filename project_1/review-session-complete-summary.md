# Review Session Complete Summary

## Course Logistics

### Week 2 Content
- **Guided Learning**: Focuses on RAG (Retrieval-Augmented Generation)
  - Adapting LLMs, fine-tuning vs RAG, prompt engineering
- **Project 2**: Customer support chatbot
  - Runs locally (unlike Project 1 on Colab)
  - Uses lightweight models and higher-level packages (LangChain)
  - Includes Jupyter Notebook, environment config, and sample data
- **Capstone Project**: Guidelines released, dashboard available

### Installation & Setup
- Environment YAML provided with pinned dependencies
- Optional: UV for faster installation
- Recommendation: Use provided versions initially (LangChain v0.x for learning)
- Conda environment: `llm_playground`

---

## Part 1: Tokenization Fundamentals

### Why Tokenization?
- Neural networks operate on numbers, not text
- Tokenization converts text → numbers (IDs) for processing
- Reverse process: numbers → text (decoding)

### Two Phases
1. **Training**: Build vocabulary and mappings (text chunks ↔ IDs)
2. **Inference**: Encode/decode using trained tokenizer

### Tokenizer Types

#### Word Level
- **Chunking**: Split by whitespace, lowercase
- **Vocabulary**: Unique words from corpus
- **Mappings**: Word → ID, ID → Word (sequential IDs: 0, 1, 2...)
- **Special Token**: `<UNK>` for unknown words
- **Limitations**: 
  - Unknown words lose information
  - Vocabulary explosion with many unique words
  - Cannot distinguish different unknown words

#### Character Level
- **Chunking**: Individual characters
- **Vocabulary**: ASCII letters (lowercase + uppercase), optionally punctuation
- **Limitations**: 
  - Loses unknown characters (emojis, special symbols)
  - Very long sequences (one token per character)

#### Subword Level (BPE) - Industry Standard
- **Algorithm**: 
  1. Start with all characters
  2. Iteratively merge most frequent token pairs
  3. Continue until target vocabulary size reached
- **Vocabulary Sizes**:
  - GPT-2: 50,257 tokens
  - GPT-3/4: 100,000 tokens
  - GPT-4o: 200,000 tokens
- **Advantages**:
  - Handles unknown words (splits into subwords)
  - Efficient vocabulary size
  - Works for multilingual text
  - No `<UNK>` token needed (operates at byte level)
- **Special Characters/Emojis**: 
  - BPE works at UTF-8 byte level
  - Frequent byte patterns become tokens
  - Tokenizer doesn't "know" semantic meaning, just patterns

### Implementation Libraries

#### Hugging Face Transformers
- `AutoTokenizer.from_pretrained("gpt2")`
- Access to many pre-trained tokenizers
- GPT-2 special token: `<|endoftext|>`

#### Tiktoken (OpenAI)
- Production-ready library
- Common tokenizers:
  - `cl100k_base`: GPT-4, GPT-4 Turbo, GPT-3.5 Turbo
  - `o200k_base`: GPT-4o family
- Simple encode/decode interface

### Key Tokenization Insights (from Q&A)
- **Token IDs are sequential**: Always 0, 1, 2... based on vocabulary index
- **Vocabulary size ≠ Embedding dimension**: 
  - Vocabulary size: number of unique tokens (determines LM head output)
  - Embedding dimension: size of hidden vectors (e.g., 768)
- **Modern models**: Mostly BPE variants (GPT-4 uses cl100k_base, GPT-4o uses o200k_base)
- **Multilingual support**: Vocabulary size increased (50k→100k→200k) to include multiple languages
- **Languages without spaces**: BPE works at byte/character level, doesn't need whitespace

---

## Part 2: Neural Networks & LLM Architecture

### Neural Networks Basics

#### Core Concept
- Sequences of layers operating on mathematical expressions
- Input → transformations → output

#### Linear Layer
- **Formula**: `output = input × W^T + b`
- **Components**: Weight matrix (W), bias term (b)
- **Shape**: Determined by input/output dimensions
  - Example: 3 inputs → 2 outputs → weight matrix: 3 × 2
- **Implementation**: 
  - PyTorch: `nn.Linear` (pre-built, optimized)
  - Custom: `__init__` creates weights, `forward` implements computation
- **Training**: Weights initialized randomly, updated via backpropagation

### Transformer Architecture

#### Overview
- Most LLMs use **decoder-only transformers**
- Original transformer had encoder-decoder (for translation)
- LLMs use decoder-only (for language generation)

#### Architecture Flow
1. Input: Sequence of token IDs
2. Processing: Linear layers + attention layers
3. Output: Probabilities for next token

### GPT-2 Model Structure

#### Main Components
1. **Transformer**: Core architecture
2. **LM Head**: Final linear layer (vocabulary size output)

#### Detailed Architecture

**1. Embeddings**
- **Text Embeddings (WTE)**: 
  - Maps token IDs → vectors
  - Shape: `[vocab_size, hidden_dim]` (GPT-2: 50,257 × 768)
  - Each row = embedding for one token (lookup table)
- **Position Embeddings (WPE)**: 
  - Adds position information
  - Same hidden dimension (768)
- **Combined**: Text + Position embeddings

**2. Transformer Blocks** (12 blocks in GPT-2)
- Each block contains:
  - Layer normalization
  - Multi-head attention
  - Layer normalization
  - MLP (feed-forward network)
- **MLP Structure**: 
  - Two linear layers
  - Expands then contracts: 768 → 3072 → 768

**3. LM Head**
- Final linear layer
- Converts hidden dimension → vocabulary size
- Shape: `[hidden_dim, vocab_size]` (GPT-2: 768 × 50,257)

### Forward Pass Example: "hello my name"

1. **Tokenization**: Text → 3 token IDs
2. **Embedding**: IDs → vectors (3 × 768)
3. **Position Embedding**: Add position info (still 3 × 768)
4. **Transformer Blocks**: Process through 12 blocks (still 3 × 768)
5. **LM Head**: Transform to vocab size (3 × 50,257)
6. **Extract Last Token**: Take last vector (50,257)
7. **Softmax**: Convert logits → probabilities (50,257)
8. **Select Token**: Highest probability (e.g., "is" at 77%)

### Key Dimensions & Shapes

#### Hyperparameters (GPT-2)
- **Vocabulary Size**: 50,257
- **Hidden Dimension**: 768
- **Number of Layers**: 12
- **Sequence Length**: Variable (max 1024 for GPT-2)

#### Shape Transformations
- Input IDs: `[batch_size, sequence_length]`
- Embeddings: `[batch_size, sequence_length, hidden_dim]`
- After transformer: `[batch_size, sequence_length, hidden_dim]`
- After LM head: `[batch_size, sequence_length, vocab_size]`
- Last token logits: `[batch_size, vocab_size]`

#### Example Flow
- Input: "hello my name" (3 tokens)
- Embeddings: 3 × 768
- Through transformer: 3 × 768
- LM head output: 3 × 50,257
- Last token probabilities: 50,257

### Important Concepts

#### Parameters vs Hyperparameters
- **Parameters**: Weights in model (learnable, updated during training)
  - Example: GPT-2 has 117M parameters
- **Hyperparameters**: Design choices (fixed, set before training)
  - Example: `hidden_dim=768`, `num_layers=12`, `vocab_size=50,257`

#### Embedding Dimension
- Each token becomes a vector of size `hidden_dim`
- GPT-2: 768 dimensions
- GPT-3: 12,288 dimensions
- Larger = more capacity but more parameters

#### Sequence Length
- Variable input lengths
- Padding for shorter sequences
- Modern models: 4k, 8k, 32k, even millions (with Ring Attention)

### Architecture Q&A Insights

**Q: Embedding matrix dimensions?**
- Shape: `[vocab_size, hidden_dim]` (GPT-2: 50,257 × 768)
- Each row = embedding for one token
- Lookup table: ID → embedding vector

**Q: How does 768 → 50,257 transformation work?**
- Final linear layer (LM head)
- Weight matrix: 768 × 50,257
- Matrix multiplication transforms dimensions
- One probability per vocabulary token

**Q: Multi-head attention dimensions?**
- Query, Key, Value matrices (each is a linear layer)
- Input/Output: `[seq_len, hidden_dim]` (usually same)
- GPT-2: 768 × 768 for each Q/K/V
- GPT-3: 12,288 × 12,288

**Q: What do embedding numbers mean?**
- Learned representations, not interpretable by humans
- Meaning emerges from training
- Focus on shapes, not individual values

---

## Part 3: Text Generation & Decoding

### Text Generation Process

#### End-to-End Flow
1. **Input**: User prompt (text)
2. **Tokenization**: Text → token IDs
3. **Embedding**: IDs → embedding vectors
4. **Transformer**: Process through layers
5. **Output**: Probabilities for next token
6. **Decoding**: Select next token
7. **Repeat**: Append token and continue
8. **Stop**: End token or max length reached

#### Basic Generation Loop
1. Start with prompt
2. Tokenize → IDs
3. Pass through model → logits
4. Apply softmax → probabilities
5. Select next token (greedy or sampling)
6. Append to prompt
7. Repeat until end token or max length

### Implementation

#### Hugging Face Generate
- Simple call: `model.generate(input_ids)`
- Handles entire loop automatically
- Parameters:
  - `max_new_tokens`: Maximum tokens to generate (e.g., 80)
  - `do_sample`: Enable/disable sampling
  - `top_k`: Number of top tokens to consider
  - `top_p`: Nucleus sampling threshold

### Decoding Strategies

#### Greedy Decoding
- Always picks highest probability token
- `do_sample=False`
- **Pros**: Deterministic, fast
- **Cons**: Can be repetitive, less creative

#### Top-k Sampling
- Considers top k most likely tokens
- Samples from this subset
- `do_sample=True, top_k=50`
- **Pros**: More diverse outputs, ignores very unlikely tokens
- **Cons**: May include irrelevant tokens if k is too large

#### Top-p (Nucleus) Sampling
- Considers tokens until cumulative probability ≥ p
- Dynamic token set size
- `do_sample=True, top_p=0.9`
- **Pros**: Balances diversity and quality
- **Cons**: Less predictable than greedy

### Model Comparison

#### GPT-2
- **Parameters**: 117M
- **Year**: 2019 (early model)
- **Capabilities**: Limited
- **Example**: "What is 2+2?" → poor answer (treats as continuation)

#### Qwen 3
- **Parameters**: 600M
- **Year**: More recent
- **Capabilities**: Better performance
- **Example**: "What is 2+2?" → "4" (correct)

#### Key Insight
- Same architecture, different sizes
- Larger models = more parameters = better performance
- Easy to swap models (same interface)

---

## Advanced Topics & Q&A

### Normalization Layers

#### Purpose
- Normalizes activations at each layer
- Prevents values from becoming too large/small
- Helps with training stability

#### Why Needed?
- **Vanishing Gradients**: Values too small → gradients disappear
- **Exploding Gradients**: Values too large → gradients explode
- Normalization keeps activations in controlled range
- Makes training more stable

#### Additional Context
- Used in cosine similarity calculations
- Dot product vs normalized dot product have different use cases
- Important in recommendation systems (popularity bias considerations)

### Batch Processing

#### Parallel Requests
- LLMs support batch processing
- First dimension is `batch_size`
- Send multiple prompts at once
- Model processes batch in parallel
- APIs support batching

### Context Window Limitations

#### Long Context Challenges
- Models may focus on beginning/end of context
- Middle content sometimes less influential
- Ongoing research area
- Evaluation tests for long-context recall

#### Solutions
- **RAG** (Retrieval-Augmented Generation): Pull relevant information dynamically
- **Dynamic Context Building**: File-based storage and retrieval
- **Tool Calling**: Agentic systems that open files when needed
- **MCP** (Model Context Protocol): Standard for context management
- **Ring Attention**: Research from Berkeley enabling millions of tokens

### Sequence Length Handling

#### Variable Length Inputs
- Padding with special tokens for shorter sequences
- Truncation if too long
- Max sequence length limit (GPT-2: 1024)
- Handled during preprocessing

#### Modern Advances
- **Ring Attention**: Enables millions of tokens
- Used by modern long-context models
- Allows processing very long documents (books, PDFs)

### Model Internals

#### Inspecting Layers
- Can print layer structures
- Inspect weight shapes
- Understand dimensions
- Values themselves not meaningful (learned representations)

---

## Key Takeaways

### For Learning
- **Tokenization is fundamental**: Text must become numbers
- **BPE is industry standard**: Handles unknowns better than word/character level
- **Neural networks = sequences of layers**: Linear transformations
- **All LLMs follow similar architecture**: Decoder-only transformers
- **Generation = iterative token prediction**: Loop until stop condition

### For Future Projects
- **Don't need all details**: Can treat models as black boxes
- **Higher-level libraries**: LangChain abstracts complexity
- **Foundation helps**: Understanding helps with technical reports
- **Project 1**: Deep dive into fundamentals
- **Project 2+**: Use higher-level tools

### For Development
- **Focus on applications**: Use pre-trained models
- **Understand high-level concepts**: Details matter for research, less for applications
- **Easy model swapping**: Same interface, different capabilities
- **Modern tools**: APIs and libraries handle complexity

### Learning Path
- **Project 1**: Deep dive into fundamentals (this session)
- **Project 2+**: Higher-level libraries and tools
- **Understanding helps but not required**: Can revisit details later
- **Building vs Research**: Different levels of detail needed

---

## Resources

- **Hugging Face Transformers**: Documentation and model hub
- **Tiktoken**: OpenAI's production tokenizer library
- **Ring Attention Paper**: Berkeley research on long context
- **Layer Normalization**: Video by Andrej Karpathy
- **Cosine Similarity**: Important in recommendation systems

---

## Summary Flow

1. **Text Input** → Tokenizer → **Token IDs**
2. **Token IDs** → Embeddings → **Embedding Vectors**
3. **Embedding Vectors** → Transformer Blocks → **Processed Vectors**
4. **Processed Vectors** → LM Head → **Logits (vocab_size)**
5. **Logits** → Softmax → **Probabilities**
6. **Probabilities** → Decoding Strategy → **Next Token**
7. **Repeat** until end token or max length

**Key Insight**: Everything is just numbers and mathematical transformations. The "intelligence" emerges from the learned weights and the architecture design.

