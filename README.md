# 🔮 TarotTara - AI-Powered Tarot Reading Assistant

TarotTara is an intelligent, multilingual tarot reading chatbot that combines traditional tarot wisdom with modern AI technology. It provides personalized tarot readings, timeline predictions, and spiritual guidance through both text and voice interactions.

## ✨ Features

### 🌟 Core Capabilities
- **Multilingual Support**: Detects and responds in multiple languages (English, Hindi, Spanish, French, and more)
- **Voice & Text Input**: Choose between voice commands or text chat for your questions
- **Intent Classification**: Intelligently categorizes questions for appropriate responses
- **Caching System**: Redis-based caching for faster response times
- **RAG Integration**: Retrieval-Augmented Generation using PDF knowledge base

### 🃏 Tarot Reading Types
- **Yes/No Questions**: Direct answers with card interpretations
- **Timeline Predictions**: Date-specific predictions using seasonal card associations
- **Insight Readings**: Deep understanding and explanations
- **Guidance Readings**: Advice and next steps recommendations
- **Multi-Card Spreads**: Traditional 3-card readings for comprehensive insights

### 🎯 Question Intent Recognition
- **Conversational**: Greetings and casual interactions
- **Factual**: Information-seeking queries (politely redirected)
- **Timeline**: When/timing questions
- **Insight**: Why/reasoning questions
- **Guidance**: How-to/advice questions
- **General**: Other queries

## 🚀 Installation

### Prerequisites
- Python 3.10 or higher
- Redis server
- Ollama with LLaMA 3 model

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd NEW-CHATBOT
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   # or using uv (recommended)
   uv sync
   ```

3. **Set up Redis**
   ```bash
   # Install Redis (Windows users may need WSL or Docker)
   # Start Redis server
   redis-server
   ```

4. **Install and configure Ollama**
   ```bash
   # Install Ollama from https://ollama.ai
   # Pull LLaMA 3 model
   ollama pull llama3
   ```

5. **Initialize the knowledge base**
   ```bash
   python initialize/build_db.py
   ```

## 📁 Project Structure

```
NEW CHATBOT/
├── core/                    # Core functionality
│   ├── rag.py              # Retrieval-Augmented Generation
│   └── tarot_reader.py     # Main tarot reading logic
├── initialize/              # Setup and configuration
│   ├── build_db.py         # Database initialization
│   ├── cache.py            # Redis caching utilities
│   └── config.py           # Configuration settings
├── utils/                   # Utility modules
│   ├── deck.py             # Tarot deck definitions
│   ├── factual.py          # Factual query handling
│   ├── intent.py           # Intent classification
│   ├── pdf_reader.py       # PDF processing
│   └── voice_assistant.py  # Voice input handling
├── pdfFiles/               # Knowledge base PDFs
├── tarot_card_db/          # ChromaDB for card meanings
├── tarot_vectordb/         # Vector database
├── main.py                 # Main application entry point
└── requirements.txt        # Python dependencies
```

## 🎮 Usage

### Starting the Application
```bash
python main.py
```

### Interactive Session
1. **Select Language**: Choose your preferred language (en, hi, es, fr)
2. **Choose Input Method**: Select 'voice' or 'chat' for question input
3. **Ask Your Question**: Pose your tarot-related question
4. **Receive Reading**: Get personalized interpretation with cards and insights
5. **Continue or Exit**: Ask more questions or type 'exit' to quit

### Example Questions
- **Timeline**: "When will I find my dream job?"
- **Yes/No**: "Will I get the promotion?"
- **Insight**: "Why am I feeling stuck in my relationship?"
- **Guidance**: "What should I focus on for personal growth?"
- **General**: "Give me a reading about my career path"

## 🔧 Configuration

### Model Settings (`initialize/config.py`)
```python
MODEL_NAME = "llama3"                    # Ollama model name
VECTOR_DB_DIR = "./tarot_vectordb"       # Vector database directory
PDF_PATHS = ["1.pdf", "2.pdf", ...]      # Knowledge base PDFs
REDIS_URL = "redis://localhost:6379/0"   # Redis connection URL
```

### Supported Languages
- English (en)
- Hindi (hi)
- Spanish (es)
- French (fr)
- Auto-detection for other languages

## 🛠️ Technical Details

### Dependencies
- **chromadb==1.0.12**: Vector database for embeddings
- **langchain-ollama==0.3.3**: LLM integration
- **sentence-transformers==4.1.0**: Text embeddings
- **redis>=6.2.0**: Caching layer
- **deep-translator==1.11.4**: Language translation
- **langdetect==1.0.9**: Language detection
- **pdfplumber==0.11.7**: PDF text extraction
- **gtts>=2.5.4**: Text-to-speech for voice features

### Architecture
- **Intent Classification**: LLM-based question categorization
- **RAG System**: PDF-based knowledge retrieval for card meanings
- **Caching**: Redis-based response caching for performance
- **Translation Pipeline**: Multi-language support with Google Translate
- **Voice Integration**: Speech-to-text and text-to-speech capabilities

### Tarot Deck Structure
- **78 Cards Total**: 22 Major Arcana + 56 Minor Arcana
- **Seasonal Timing**: Cards mapped to seasonal date ranges
- **Suit Associations**: Cups (Spring), Wands (Summer), Swords (Autumn), Pentacles (Winter)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## 🙏 Acknowledgments

- Traditional tarot wisdom and interpretations
- Ollama team for the local LLM framework
- ChromaDB for vector database capabilities
- Redis for caching infrastructure

 