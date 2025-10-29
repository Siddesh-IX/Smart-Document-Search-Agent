# 📄 Smart Document Search Agent

A powerful Retrieval-Augmented Generation (RAG) application built with Python, Streamlit, and LangChain that allows you to upload documents and ask intelligent questions about their content. The AI will search through your documents and provide answers with proper source citations.

## ✨ Key Features

### 🚀 **Dynamic Document Processing**

- **Runtime Upload**: Upload 1-10 documents directly through the web interface
- **Multi-Format Support**: PDF and Word (.doc, .docx) documents
- **Real-Time Processing**: Automatic FAISS index creation after upload
- **File Validation**: Size limits, type checking, and comprehensive error handling

### 🎯 **Intelligent Search & AI**

- **Semantic Search**: Vector embeddings for intelligent content matching using OpenAI embeddings
- **Anti-Hallucination**: Built-in validation to prevent AI assumptions and general knowledge responses
- **Source Citation**: Always shows which documents contain the answers with proper references
- **Context-Aware**: Chunk-based processing with overlap for content continuity

### 🎨 **Modern User Interface**

- **3-Section Layout**: Fixed title header, scrollable chat area, and always-visible input section
- **Responsive Design**: Mobile-friendly interface with proper viewport handling
- **Purple Theme**: Modern gradient design with smooth hover animations
- **Session Management**: Persistent chat history and document status tracking

### 🔒 **Privacy & Security**

- **Local Processing**: Documents processed and stored locally for privacy
- **Secure API**: Only relevant text chunks sent to OpenAI, never full documents
- **Session Isolation**: Each user session maintains separate document context

## 🎯 Project Evolution & Requirements

### **Original Requirements Met & Enhanced**

**Enhanced Objective**: Dynamic upload of 1-10 documents with intelligent question-answering and proper source attribution.

### **Acceptance Criteria - All Enhanced ✅**

- ✅ **Dynamic Upload**: 1-10 PDF/Word docs via web interface (enhanced from static folder)
- ✅ **Intelligent Search**: AI returns contextually relevant answers with source snippets
- ✅ **Source Attribution**: Shows document names and relevant text chunks used
- ✅ **Multi-Query Support**: Handles unlimited queries with chat history
- ✅ **Anti-Hallucination**: Prevents AI from providing general knowledge responses

### **Technology Stack - Enhanced**

- ✅ **LangChain Framework**: Complete RAG pipeline with document processing
- ✅ **OpenAI Integration**: GPT-3.5-turbo + text-embedding-ada-002
- ✅ **Modern Streamlit UI**: 3-section responsive layout with custom CSS
- ✅ **FAISS Vector Store**: Efficient similarity search with persistent storage

## 🛠️ Technology Stack

### **Core Technologies**

- **Language**: Python 3.13+
- **Frontend**: Streamlit with custom CSS (3-section responsive layout)
- **AI Framework**: LangChain for RAG pipeline orchestration
- **LLM**: OpenAI GPT-3.5-turbo for answer generation
- **Embeddings**: OpenAI text-embedding-ada-002 for semantic search
- **Vector Store**: FAISS with local persistence for fast similarity search

### **Document Processing**

- **PDF Support**: PyPDF for PDF document processing
- **Word Support**: python-docx for .doc/.docx files
- **Text Processing**: RecursiveCharacterTextSplitter for intelligent chunking
- **File Handling**: Comprehensive validation and error management

## 📁 Project Structure

```
Smart Document Search Agent/
├── app.py                         # Main Streamlit application with 3-section layout
├── backend.py                     # Document processing & AI backend service
├── ingest.py                      # Legacy document ingestion script (optional)
├── requirements.txt               # Python dependencies
├── .env                          # Environment variables (OpenAI API key)
├── faiss_index/                   # Auto-generated FAISS vector index
│   └── index.faiss               # Vector store file (created after upload)
├── __pycache__/                  # Python cache files
├── data/                         # Legacy static documents folder (optional)
├── .gitignore                    # Git ignore configuration
└── README.md                     # This documentation
```

### **File Descriptions**

- **app.py**: Modern Streamlit UI with dynamic file upload, chat interface, and session management
- **backend.py**: Core RAG functionality including document processing, FAISS operations, and AI integration
- **requirements.txt**: All Python dependencies including Streamlit, LangChain, OpenAI, FAISS, and document processors

## 🚀 Quick Start

### Prerequisites

- **Python 3.13+** ([Download here](https://www.python.org/downloads/))
- **OpenAI API Key** ([Get one here](https://platform.openai.com/account/api-keys))
- **Git** (optional, for cloning)

### Installation & Setup

1. **Clone or Download the Project**

   ```bash
   git clone https://github.com/Siddesh-IX/Smart-Document-Search-Agent.git
   cd "Smart-Document-Search-Agent"
   ```

2. **Install Python Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure OpenAI API Key**

   Create a `.env` file in the project root:

   ```env
   OPENAI_API_KEY="your-actual-api-key-here"
   ```

4. **Launch the Application**

   ```bash
   streamlit run app.py
   ```

5. **Access the Web Interface**

   - The app opens automatically at `http://localhost:8502`
   - If port 8502 is busy, Streamlit will use the next available port

### First Time Usage

1. **Upload Documents**: Use the web interface to upload 1-10 PDF or Word files
2. **Process Files**: Click "🚀 Process Documents" to create the search index
3. **Start Chatting**: Ask questions about your uploaded documents
4. **View Sources**: Each answer includes references to source documents

## 📖 Usage Guide

### 🔄 Dynamic Document Management

#### **Upload Process**

1. **Access Upload Interface**: If no documents are loaded, you'll see the upload screen
2. **Select Files**: Choose 1-10 PDF or Word documents using the file picker
3. **Validate Files**: The system checks file types and sizes automatically
4. **Process Documents**: Click the purple "🚀 Process Documents" button
5. **Index Creation**: Wait for automatic FAISS index generation (with progress indicator)

#### **Document Controls**

- **Clear Chat**: Remove conversation history while keeping documents
- **New Upload**: Start fresh with new documents
- **Clear All Documents**: Permanently remove all uploaded documents and index

### 💬 Intelligent Question-Answering

#### **Sample Questions**

**For Business/HR Documents:**

- "What is the work from home policy?"
- "What are the maternity leave benefits?"
- "How does the referral program work?"
- "What is the performance improvement process?"

**General Analysis:**

- "What are the main topics discussed in the documents?"
- "Can you summarize the key findings?"
- "What does the document say about [specific topic]?"
- "Find information about specific procedures"

#### **Understanding Responses**

The AI provides:

- **Contextual Answer**: Generated from your specific documents only
- **Source References**: Shows which documents were used with file names
- **No Hallucination**: If information isn't found, the AI clearly states this
- **Chat History**: Persistent conversation with timestamps

## ⚙️ Configuration & Customization

### Environment Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY="your-openai-api-key-here"
```

### Advanced Configuration Options

#### **Document Processing (backend.py)**

```python
# Text splitting configuration
chunk_size=1000              # Size of text chunks for processing
chunk_overlap=200            # Overlap between chunks for context continuity

# Search parameters
search_kwargs={"k": 3}       # Number of relevant documents to retrieve
temperature=0                # AI response randomness (0 = deterministic)
```

#### **File Upload Limits (app.py)**

```python
# File validation settings
MAX_FILES = 10               # Maximum files per upload
SUPPORTED_FORMATS = ['pdf', 'doc', 'docx']
MAX_FILE_SIZE = "200MB"      # Per file size limit
```

#### **UI Customization**

The 3-section layout uses custom CSS that can be modified:

- **Title Section**: 80px fixed height at top
- **Chat Section**: Flexible scrollable middle area
- **Input Section**: 100px fixed height at bottom

## 🏗️ System Architecture

### 🔄 **RAG Pipeline Architecture**

```
User Upload → Document Processing → Vector Storage → Query Processing → AI Response
```

#### **Document Processing Pipeline**

1. **Upload Validation**: File type, size, and count validation
2. **Temporary Storage**: Secure temporary file handling during processing
3. **Document Loading**: PDF/Word documents loaded using specialized loaders
4. **Text Chunking**: Intelligent text splitting with configurable overlap
5. **Embedding Generation**: OpenAI creates vector embeddings for semantic search
6. **FAISS Indexing**: Vector storage with local persistence for fast retrieval

#### **Query Processing Flow**

1. **User Input**: Natural language question through web interface
2. **Semantic Search**: FAISS similarity search to find relevant document chunks
3. **Context Assembly**: Retrieved chunks formatted as context for the AI
4. **AI Generation**: GPT-3.5-turbo generates contextual response
5. **Response Validation**: Anti-hallucination checks to ensure answer accuracy
6. **Source Attribution**: Document sources attached to the final response

### 🎨 **Frontend Architecture**

#### **3-Section Responsive Layout**

- **Section 1**: Fixed title header with processing status
- **Section 2**: Scrollable chat area with conversation history
- **Section 3**: Fixed input section always visible at bottom

#### **Session Management**

- **Persistent State**: Chat history, document status, and file information
- **Dynamic Interface**: Switches between upload and chat modes
- **Error Handling**: Comprehensive validation and user feedback

## � Troubleshooting

### Common Issues & Solutions

#### **🔑 API Key Issues**

```
Error: "Authentication Error" from OpenAI
```

**Solutions:**

- Verify `.env` file contains correct OpenAI API key
- Check API key format: `OPENAI_API_KEY="sk-..."`
- Ensure sufficient credits in your OpenAI account
- Restart the application after updating `.env`

#### **📁 Document Processing Issues**

```
Error: "Processing failed" or "File validation error"
```

**Solutions:**

- Ensure files are PDF or Word (.doc/.docx) format only
- Check file sizes are reasonable (under 50MB per file)
- Upload 1-10 files maximum per session
- Try processing fewer files if encountering memory issues

#### **🌐 Connection Issues**

```
Error: Port already in use
```

**Solutions:**

- Kill existing Streamlit processes: `taskkill /f /im streamlit.exe`
- Use different port: `streamlit run app.py --server.port 8503`
- Check if another application is using the port

#### **📦 Installation Issues**

```
Error: Module not found or import errors
```

**Solutions:**

- Install dependencies: `pip install -r requirements.txt`
- Upgrade pip: `python -m pip install --upgrade pip`
- Use virtual environment to avoid conflicts
- Ensure Python 3.13+ is being used

### 🚀 Performance Optimization

- **Large Documents**: Increase `chunk_size` to 1500-2000 for better context
- **Many Files**: Initial processing takes time, but queries are fast afterward
- **Memory Management**: FAISS indices load into memory for optimal search speed
- **Browser Performance**: Clear browser cache if UI becomes sluggish

## 🔒 Security & Privacy

- **Local Processing**: All documents are processed and stored locally
- **API Security**: Only text chunks are sent to OpenAI, never full documents
- **Environment Protection**: `.gitignore` prevents accidental API key commits

## 🔒 Security & Privacy

### **Data Protection**

- **Local Processing**: All documents processed and stored locally on your machine
- **API Security**: Only relevant text chunks sent to OpenAI, never full documents
- **No Data Persistence**: OpenAI doesn't store your data when using the API
- **Session Isolation**: Each browser session maintains separate document context

### **Best Practices**

- Keep your OpenAI API key secure and never commit it to version control
- Regularly clear uploaded documents if processing sensitive information
- Monitor your OpenAI API usage and costs through their dashboard

## 🛣️ Roadmap & Future Enhancements

### **Planned Features**

- [ ] Support for additional file formats (Excel, PowerPoint, etc.)
- [ ] Advanced search filters and query refinement
- [ ] Document summarization and key insights extraction
- [ ] Multi-language document support
- [ ] Integration with cloud storage services
- [ ] Advanced analytics and usage metrics

### **Recent Improvements**

- ✅ Dynamic file upload system (replaced static folder approach)
- ✅ Anti-hallucination validation system
- ✅ 3-section responsive UI layout
- ✅ Word document support (.doc/.docx)
- ✅ Real-time processing with progress indicators
- ✅ Session management and chat history

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### **Ways to Contribute**

1. **Bug Reports**: Submit issues with detailed reproduction steps
2. **Feature Requests**: Suggest new functionality or improvements
3. **Code Contributions**: Fork, develop, and submit pull requests
4. **Documentation**: Improve README, add examples, or create tutorials
5. **Testing**: Test with different document types and provide feedback

### **Development Setup**

```bash
git clone https://github.com/Siddesh-IX/Smart-Document-Search-Agent.git
cd Smart-Document-Search-Agent
pip install -r requirements.txt
# Make your changes
# Test thoroughly
# Submit pull request
```

## � License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🆘 Support & Community

### **Getting Help**

1. **📖 Documentation**: Check this README and inline code comments
2. **🐛 Issues**: Search existing GitHub issues or create a new one
3. **💬 Discussions**: Use GitHub Discussions for questions and ideas
4. **🔍 Troubleshooting**: Follow the comprehensive troubleshooting guide above

### **Quick Support Checklist**

- ✅ Check troubleshooting section
- ✅ Verify Python 3.13+ and all dependencies installed
- ✅ Ensure OpenAI API key is valid with sufficient credits
- ✅ Review terminal output for detailed error messages
- ✅ Try with different documents to isolate issues

## 🎯 Project Stats

- **Language**: Python 3.13+
- **Framework**: Streamlit + LangChain
- **AI Model**: OpenAI GPT-3.5-turbo
- **Vector Store**: FAISS with local persistence
- **File Support**: PDF, Word (.doc/.docx)
- **UI**: 3-section responsive layout with custom CSS
- **Architecture**: RAG (Retrieval-Augmented Generation)

---

## ⭐ Acknowledgments

- **Streamlit** for the amazing web app framework
- **LangChain** for the comprehensive RAG pipeline tools
- **OpenAI** for powerful language models and embeddings
- **FAISS** for efficient vector similarity search
- **Python Community** for excellent document processing libraries

---

**🚀 Built with ❤️ using Streamlit, LangChain, and OpenAI**

_Transform your documents into intelligent, searchable knowledge with the power of AI!_
