# 📄 Smart Document Search Agent

A powerful Retrieval-Augmented Generation (RAG) application built with Python, Streamlit, and LangChain that allows you to upload documents and ask intelligent questions about their content. The AI will search through your documents and provide answers with proper source citations.

## 🎯 Features

- **Smart Document Search**: Uses semantic similarity search to find relevant content
- **Multiple File Formats**: Supports PDF and TXT files
- **Source Citation**: Always shows which documents contain the answers
- **Interactive Web Interface**: Clean, user-friendly Streamlit interface
- **Vector Store**: Efficient FAISS-based vector storage for fast retrieval
- **OpenAI Integration**: Powered by GPT models and OpenAI embeddings
- **Local Storage**: Documents and indices stored locally for privacy

## � Project Requirements

**Objective**: Upload a small set of documents (5–10). The AI should allow the user to search a query and return the most relevant snippet with source reference.

### **Acceptance Criteria**

- ✅ Upload at least 5 text/PDF docs
- ✅ User types a query → AI returns the best matching snippet
- ✅ Must show source file name with the answer
- ✅ Should work with at least 3 different queries

### **Required Technologies**

- ✅ LangChain + GPT-4
- ✅ Document embeddings (OpenAI)
- ✅ Streamlit UI

## �🛠️ Tech Stack

- **Language**: Python 3.13+
- **Frontend**: Streamlit
- **Orchestration**: LangChain
- **LLM & Embeddings**: OpenAI (GPT-3.5-turbo and text-embedding-ada-002)
- **Vector Store**: FAISS (in-memory, saved to disk)
- **Document Loading**: PyPDFLoader, TextLoader

## 📁 Project Structure

```
Smart Document Search Agent/
├── data/                           # Directory for your documents
│   ├── *.pdf                      # PDF files
│   └── *.txt                      # Text files
├── faiss_index/                   # Generated FAISS vector index (created after ingestion)
├── app.py                         # Main Streamlit application
├── ingest.py                      # Document ingestion script
├── requirements.txt               # Python dependencies
├── .env                          # Environment variables (API keys)
├── .gitignore                    # Git ignore file
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.13 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/account/api-keys))

### Installation

1. **Clone or download the project**

   ```bash
   cd "C:\Projects\Smart Document Search Agent"
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**

   Edit the `.env` file and replace the placeholder with your actual API key:

   ```
   OPENAI_API_KEY="your-actual-api-key-here"
   ```

4. **Add your documents**

   Place your PDF and TXT files in the `data/` folder:

   ```
   data/
   ├── document1.pdf
   ├── document2.pdf
   └── notes.txt
   ```

5. **Create the document index**

   ```bash
   python ingest.py
   ```

6. **Launch the application**

   ```bash
   streamlit run app.py
   ```

7. **Open your browser**

   The app will automatically open at `http://localhost:8501`

## 📖 Usage Guide

### Adding Documents

1. Place your documents (.pdf or .txt files) in the `data/` folder
2. Run the ingestion script: `python ingest.py`
3. The script will process your documents and create a searchable index

### Asking Questions

Once the app is running, you can ask natural language questions such as:

**For HR Policy Documents:**

- "What is the work from home policy?"
- "What are the maternity leave benefits?"
- "How does the referral program work?"
- "What is the PIP policy process?"

**General Questions:**

- "What are the main topics discussed in the documents?"
- "Can you summarize the key findings?"
- "What does the document say about [specific topic]?"

### Understanding Results

The app provides:

- **Answer**: AI-generated response based on your documents
- **Sources**: Which documents were used to generate the answer
- **Document Details**: Expandable section showing the actual text chunks used

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following:

```env
OPENAI_API_KEY="your-openai-api-key"
```

### Customizing the Search

You can modify the following parameters in the code:

**In `ingest.py`:**

- `chunk_size=1000`: Size of text chunks for processing
- `chunk_overlap=200`: Overlap between chunks to maintain context

**In `app.py`:**

- `search_kwargs={"k": 3}`: Number of relevant documents to retrieve
- `temperature=0`: Controls randomness in AI responses (0 = deterministic)

## 🏗️ Architecture

### Document Processing Pipeline

1. **Document Loading**: PDF and TXT files are loaded from the `data/` directory
2. **Text Splitting**: Documents are split into chunks for better retrieval
3. **Embedding Generation**: OpenAI creates vector embeddings for each chunk
4. **Vector Storage**: FAISS stores embeddings for fast similarity search

### Query Processing

1. **User Query**: Natural language question input
2. **Similarity Search**: FAISS finds most relevant document chunks
3. **Context Assembly**: Relevant chunks are formatted for the AI
4. **Answer Generation**: OpenAI generates a response with source attribution

## 🐛 Troubleshooting

### Common Issues

**"No document index found" error:**

- Make sure you've run `python ingest.py` after adding documents
- Check that documents exist in the `data/` folder

**"Authentication Error" from OpenAI:**

- Verify your API key is correct in the `.env` file
- Ensure you have sufficient credits in your OpenAI account

**Import errors:**

- Run `pip install -r requirements.txt` to install all dependencies
- Ensure you're using Python 3.13+

**Port already in use:**

- If port 8501 is busy, run: `streamlit run app.py --server.port 8502`

### Performance Tips

- **Large Documents**: For very large documents, consider increasing `chunk_size` to 1500-2000
- **Many Documents**: The initial indexing may take time but subsequent queries are fast
- **Memory Usage**: FAISS indices are loaded into memory for faster searches

## 🔒 Security & Privacy

- **Local Processing**: All documents are processed and stored locally
- **API Security**: Only text chunks are sent to OpenAI, never full documents
- **Environment Protection**: `.gitignore` prevents accidental API key commits

## 🤝 Contributing

Feel free to contribute to this project by:

1. Adding support for more file formats (Word, Excel, etc.)
2. Implementing advanced search filters
3. Adding document summarization features
4. Improving the UI/UX

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Verify all dependencies are installed correctly
3. Ensure your OpenAI API key is valid and has sufficient credits
4. Check the terminal output for detailed error messages

## 📊 Example Documents Included

This setup includes several HR policy documents for testing:

- Assets Usage and Care Policy
- Compensatory Off Policy
- Learning and Development Policy
- Maternity Leave Policy
- PIP (Performance Improvement Plan) Policy
- Referral Policy
- Work From Home Policy

Try asking questions about these policies to test the system!

---

**Built with ❤️ using Streamlit, LangChain, and OpenAI**
