# 🔮 TarotTara - AI-Powered Tarot Reading Assistant

TarotTara is an intelligent, multilingual tarot reading chatbot that combines traditional tarot wisdom with modern AI technology. It provides personalized tarot readings, timeline predictions, and spiritual guidance through multiple interfaces including CLI, web UI, and REST API.

## ✨ Features

### 🌟 Core Capabilities
- **Multilingual Support**: Detects and responds in multiple languages (English, Hindi, Spanish, French, and more)
- **Multiple Interfaces**: CLI application, Streamlit web UI, and FastAPI REST API
- **Intent Classification**: Intelligently categorizes questions for appropriate responses
- **Caching System**: Redis-based caching for faster response times
- **RAG Integration**: Retrieval-Augmented Generation using PDF knowledge base
- **Conversation Context**: Maintains conversation history for contextual responses
- **Voice Input Support**: Speech-to-text capabilities for hands-free interaction

### 🃏 Tarot Reading Types
- **Yes/No Questions**: Direct answers with card interpretations
- **Timeline Predictions**: Date-specific predictions using seasonal card associations
- **Insight Readings**: Deep understanding and explanations
- **Guidance Readings**: Advice and next steps recommendations
- **Multi-Card Spreads**: Traditional 3-card readings for comprehensive insights
- **Conversational**: Friendly greetings and casual interactions

### 🎯 Question Intent Recognition
- **Conversational**: Greetings and casual interactions
- **Factual**: Information-seeking queries (politely redirected)
- **Timeline**: When/timing questions
- **Insight**: Why/reasoning questions
- **Guidance**: How-to/advice questions
- **Yes/No**: Binary questions
- **General**: Other queries

## 🚀 Installation

### Prerequisites
- Python 3.10 or higher
- Redis server (optional, for caching)
- Groq API key (for LLM inference)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI-Tarot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Set your Groq API key
   export GROQ_API_KEY="your-actual-api-key-here"
   ```

4. **Set up Redis (optional, for caching)**
   ```bash
   # Install Redis (Windows users may need WSL or Docker)
   # Start Redis server
   redis-server
   ```

5. **Initialize the knowledge base**
   ```bash
   python initialize/build_db.py
   ```

## 📁 Project Structure

```
AI-Tarot/
├── core/                    # Core functionality
│   ├── rag.py              # Retrieval-Augmented Generation
│   ├── tarot_reader.py     # Main tarot reading logic
│   └── requirements.txt    # Core dependencies
├── initialize/              # Setup and configuration
│   ├── build_db.py         # Database initialization
│   ├── cache.py            # Redis caching utilities
│   ├── config.py           # Configuration settings
│   └── requirements.txt    # Initialization dependencies
├── utils/                   # Utility modules
│   ├── context.py          # Conversation context management
│   ├── deck.py             # Tarot deck definitions
│   ├── factual.py          # Factual query handling
│   ├── intent.py           # Intent classification
│   ├── pdf_reader.py       # PDF processing
│   ├── voice_assistant.py  # Voice input handling
│   └── requirements.txt    # Utility dependencies
├── pdfFiles/               # Knowledge base PDFs
├── tarot_card_db/          # ChromaDB for card meanings
├── tarot_vectordb/         # Vector database
├── streamlit/              # Streamlit configuration
├── main.py                 # CLI application entry point
├── streamlit_app.py        # Streamlit web UI
├── api.py                  # FastAPI REST API
├── dockerfile              # Docker configuration
└── requirements.txt        # Main Python dependencies
```

## 🎮 Usage

### CLI Application
```bash
python main.py
```

### Streamlit Web UI
```bash
streamlit run streamlit_app.py
```

### FastAPI REST API
```bash
uvicorn api:app --host 0.0.0.0 --port 8080
```

### Docker Deployment
```bash
docker build -t tarottara .
docker run -p 8080:8080 tarottara
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
- **Conversational**: "Hello! How are you today?"
- **General**: "Give me a reading about my career path"

## 🔧 Configuration

### Model Settings (`initialize/config.py`)
```python
MODEL_NAME = "llama3"                    # Model name (currently using Groq API)
VECTOR_DB_DIR = "./tarot_vectordb"       # Vector database directory
PDF_PATHS = ["1.pdf", "2.pdf", ...]      # Knowledge base PDFs
# REDIS_URL = "redis://localhost:6379/0"  # Redis connection URL (optional)
```

### Environment Variables
```bash
GROQ_API_KEY=your-actual-api-key-here      # Required for LLM inference
```

### Supported Languages
- English (en)
- Hindi (hi)
- Spanish (es)
- French (fr)
- Auto-detection for other languages

## 🛠️ Technical Details

### Dependencies
- **groq**: LLM inference via Groq API
- **langchain-groq==0.3.5**: Groq integration
- **sentence-transformers==4.1.0**: Text embeddings
- **redis==6.2.0**: Caching layer (optional)
- **deep-translator==1.11.4**: Language translation
- **langdetect==1.0.9**: Language detection
- **pdfplumber==0.11.7**: PDF text extraction
- **gTTS==2.5.4**: Text-to-speech for voice features
- **speechrecognition==3.14.3**: Speech-to-text
- **streamlit**: Web UI framework
- **fastapi**: REST API framework
- **uvicorn**: ASGI server

### Architecture
- **Intent Classification**: LLM-based question categorization using Groq API
- **RAG System**: PDF-based knowledge retrieval for card meanings
- **Caching**: Redis-based response caching for performance (optional)
- **Translation Pipeline**: Multi-language support with Google Translate
- **Voice Integration**: Speech-to-text and text-to-speech capabilities
- **Conversation Context**: Maintains conversation history for contextual responses
- **Multiple Interfaces**: CLI, Streamlit web UI, and FastAPI REST API

### Tarot Deck Structure
- **78 Cards Total**: 22 Major Arcana + 56 Minor Arcana
- **Seasonal Timing**: Cards mapped to seasonal date ranges
- **Suit Associations**: Cups (Spring), Wands (Summer), Swords (Autumn), Pentacles (Winter)

### API Endpoints
- **POST /ask**: Submit a tarot question
  ```json
  {
    "question": "Will I get the job?",
    "language": "en"
  }
  ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- Traditional tarot wisdom and interpretations
- Groq team for the fast LLM inference API
- ChromaDB for vector database capabilities
- Redis for caching infrastructure
- Streamlit and FastAPI communities for web frameworks

 