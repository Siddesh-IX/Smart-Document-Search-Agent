import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv
from backend import get_backend_service

# Load environment variables
load_dotenv()

# Constants
FAISS_PATH = "faiss_index"

# Initialize session state for chat history and file processing
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'input_key' not in st.session_state:
    st.session_state.input_key = 0
if 'files_processed' not in st.session_state:
    st.session_state.files_processed = False
if 'processing_status' not in st.session_state:
    st.session_state.processing_status = None
if 'uploaded_files_info' not in st.session_state:
    st.session_state.uploaded_files_info = None
if 'show_upload_interface' not in st.session_state:
    st.session_state.show_upload_interface = False

def get_backend():
    """Get the backend service instance"""
    backend = get_backend_service()
    if backend.index is None:
        backend.load_index()
    return backend

def escape_html(text):
    """Properly escape HTML characters to prevent display issues."""
    if not text:
        return ""
    import html
    import re
    
    # First escape HTML entities
    escaped = html.escape(text, quote=True)
    
    # Remove any remaining HTML-like tags that might have been generated
    escaped = re.sub(r'<[^>]+>', '', escaped)
    
    # Replace common problematic sequences
    escaped = escaped.replace('&lt;div', '&lt;div')
    escaped = escaped.replace('style=', 'style=')
    
    return escaped

def add_to_chat_history(question, answer, sources):
    """Add a Q&A pair to the chat history."""
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.chat_history.append({
        "question": question,
        "answer": answer,
        "sources": sources,
        "timestamp": timestamp
    })

def display_chat_history():
    """Display the chat history in a conversational format."""
    if st.session_state.chat_history:
        # Display chat messages without redundant title since we have title section at top
        for i, chat in enumerate(st.session_state.chat_history):
            # User question (right side with grey background)
            # Responsive columns: mobile-friendly layout
            col1, col2, col3 = st.columns([0.5, 1.5, 2])
            with col3:
                st.markdown(f"""
                <div style="
                    background-color: #3A3A3A;
                    padding: 10px 15px;
                    border-radius: 15px 15px 5px 15px;
                    margin: 5px 0;
                    text-align: left;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                ">
                    <div style="
                        font-size: 0.8em;
                        color: #B0B0B0;
                        margin-bottom: 3px;
                    ">
                        👤 You • {chat['timestamp']}
                    </div>
                    <div style="
                        color: white;
                        font-size: 0.95em;
                        line-height: 1.4;
                        white-space: pre-wrap;
                    ">
                        {escape_html(chat['question'])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # AI answer (left side without box)
            # Responsive columns for AI answers
            col1, col2, col3 = st.columns([3, 1, 0.5])
            with col1:
                # Display AI header
                st.markdown(f"""
                <div style="
                    font-size: 0.8em;
                    color: #B0B0B0;
                    margin-bottom: 8px;
                ">
                    🤖 AI Assistant • {chat['timestamp']}
                </div>
                """, unsafe_allow_html=True)
                
                # Display the answer as clean text using st.write
                st.write(chat['answer'])
                
                # Display sources in italics
                if chat['sources']:
                    st.markdown("*Sources:*")
                    
                    # Create source boxes without copy buttons
                    for source in chat['sources']:
                        st.markdown(f"""
                        <div style="
                            background-color: rgba(0, 122, 204, 0.1);
                            padding: 8px 12px;
                            border-radius: 8px;
                            border-left: 3px solid #007ACC;
                            margin: 4px 0;
                            font-size: 0.9em;
                            color: #FAFAFA;
                        ">
                            📄 {escape_html(source)}
                        </div>
                        """, unsafe_allow_html=True)
            
            # Add space between conversations
            st.markdown("<br>", unsafe_allow_html=True)
        
        # Add some space before the input
        st.markdown("")
        st.markdown("")

# Streamlit UI
st.set_page_config(
    page_title="Smart Document Search", 
    layout="wide",
    page_icon="📄"
)

# Clean up old CSS and prepare for 3-section layout

# Load the backend service
backend = get_backend()

# Check if we need to show file upload or chat interface
index_status = backend.get_index_status()
# Show upload interface if user clicked new upload (files_processed = False) OR if no index exists
# Show chat interface if index exists AND user hasn't requested new upload AND files were processed
show_chat_interface = (index_status['loaded'] or st.session_state.files_processed) and st.session_state.get('show_upload_interface', False) != True

if not show_chat_interface:
    # File Upload Interface
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #007ACC, #005A9E);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(0, 122, 204, 0.3);
    ">
        <h2 style="color: white; margin: 0;">📄 Smart Document Search Agent</h2>
        <p style="color: #E6F3FF; margin: 10px 0 0 0;">Upload your documents to get started with intelligent search</p>
    </div>
    """, unsafe_allow_html=True)
    
    # File Upload Section
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        # st.markdown("""
        # <div style="
        #     background-color: #262730;
        #     padding: 30px;
        #     border-radius: 15px;
        #     border: 2px dashed #007ACC;
        #     margin: 20px 0;
        #     text-align: center;
        # ">
        # """, unsafe_allow_html=True)
        
        st.markdown("### 📁 Upload Your Documents")
        st.markdown("**Supported formats:** PDF, Word (.doc, .docx)")
        st.markdown("**File limit:** 1-10 files")
        
        # File uploader
        uploaded_files = st.file_uploader(
            "Choose your documents",
            accept_multiple_files=True,
            type=['pdf', 'doc', 'docx'],
            help="Select between 1-10 PDF or Word documents to search through"
        )
        
        # Display uploaded files info
        if uploaded_files:
            st.markdown("#### 📋 Selected Files:")
            for i, file in enumerate(uploaded_files, 1):
                file_size = len(file.getvalue()) / (1024 * 1024)  # Size in MB
                st.markdown(f"**{i}.** `{file.name}` ({file_size:.2f} MB)")
            
            # Validation messages
            if len(uploaded_files) < 1:
                st.error("⚠️ Please select at least 1 file.")
            elif len(uploaded_files) > 10:
                st.error("⚠️ Maximum 10 files allowed. Please remove some files.")
            else:
                st.success(f"✅ {len(uploaded_files)} file(s) ready for processing")
                
                # Process files button
                if st.button("🚀 Process Documents", use_container_width=True, type="primary"):
                    with st.spinner("🔄 Processing documents and creating search index..."):
                        # Process the uploaded files
                        result = backend.process_uploaded_files(uploaded_files)
                        
                        if result['success']:
                            st.session_state.files_processed = True
                            st.session_state.processing_status = result
                            st.session_state.uploaded_files_info = [f.name for f in uploaded_files]
                            st.session_state.show_upload_interface = False  # Switch back to chat interface
                            st.success(result['message'])
                            st.balloons()  # Celebration animation
                            st.rerun()
                        else:
                            st.error(f"❌ Processing failed: {result['error']}")
                            if 'errors' in result and result['errors']:
                                st.markdown("**File-specific errors:**")
                                for error in result['errors']:
                                    st.error(f"• {error}")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Instructions using native Streamlit components
        with st.container():
            st.markdown("#### 💡 How it works:")
            st.markdown("""
            1. Upload 1-10 PDF or Word documents
            2. Click "Process Documents" to create search index
            3. Start asking questions about your documents
            4. Get AI-powered answers with source references
            """)
            
            st.markdown("#### 🔒 Privacy:")
            st.info("Your documents are processed locally and securely. Files are temporarily stored only during processing.")
            
            st.markdown("#### 🎯 AI Behavior:")
            st.info("The AI will only answer based on your uploaded documents. If information isn't found, it will clearly state this instead of guessing.")

else:
    # Chat Interface with proper 3-section layout
    st.markdown('<div class="main-app-container">', unsafe_allow_html=True)
    
    # SECTION 1: Title/Header (Fixed at top)
    st.markdown('<div class="title-section">', unsafe_allow_html=True)
    st.markdown("### 📄 Smart Document Search Agent")
    
    # Show processing status if files were just processed
    if st.session_state.processing_status and st.session_state.uploaded_files_info:
        st.success(f"✅ Successfully processed {len(st.session_state.uploaded_files_info)} documents!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # SECTION 2: Chat/Conversation (Scrollable middle section)
    st.markdown('<div class="chat-section">', unsafe_allow_html=True)
    
    # Display chat history within scrollable area
    display_chat_history()
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close chat-section
    
    # Sidebar with instructions and examples
    with st.sidebar:
            st.header("📋 Instructions")
            st.markdown("""
            1. Upload your documents using the file uploader
            2. Wait for processing to complete  
            3. Ask questions in the input box at the bottom
            4. The AI will search through your documents and provide answers with sources
            5. **Important**: If information is not found in your documents, the AI will clearly state this and suggest contacting an administrator
            6. Your conversation history will appear above
            """)
            
            st.header("💡 Example Questions")
            st.markdown("""
            - "What are the important policies mentioned?"
            - "Find information about specific procedures"
            - "What are the main conclusions?"
            """)
            
            st.header("📊 Document Status")
            status = backend.get_index_status()
            if status['loaded']:
                st.success(f"✅ {status['document_count']} document chunks ready!")
            else:
                st.info("📁 Upload documents to get started")
            
            # Action buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Clear Chat", use_container_width=True):
                    st.session_state.chat_history = []
                    st.session_state.input_key += 1
                    st.rerun()
            
            with col2:
                if st.button("New Upload", use_container_width=True):
                    # Clear all session state for fresh upload
                    st.session_state.files_processed = False
                    st.session_state.processing_status = None
                    st.session_state.uploaded_files_info = None
                    st.session_state.chat_history = []
                    st.session_state.show_upload_interface = True
                    st.session_state.input_key += 1  # Reset input field as well
                    st.rerun()
            
            # Clear Documents button (full width)
            if status['loaded']:  # Only show if documents are loaded
                st.markdown("---")  # Separator line
                st.markdown("⚠️ **Danger Zone**")
                
                # Initialize confirmation state
                if 'confirm_clear_docs' not in st.session_state:
                    st.session_state.confirm_clear_docs = False
                
                if not st.session_state.confirm_clear_docs:
                    if st.button("Clear All Document Chunks", use_container_width=True, type="secondary"):
                        st.session_state.confirm_clear_docs = True
                        st.rerun()
                else:
                    st.warning("⚠️ This will permanently delete all document chunks!")
                    col_confirm1, col_confirm2 = st.columns(2)
                    
                    with col_confirm1:
                        if st.button("✅ Yes, Clear", use_container_width=True, type="primary"):
                            # Clear documents from backend
                            result = backend.clear_documents()
                            
                            if result['success']:
                                # Reset backend service to reload fresh state
                                from backend import reset_backend_service
                                reset_backend_service()
                                
                                # Clear all session state
                                st.session_state.files_processed = False
                                st.session_state.processing_status = None
                                st.session_state.uploaded_files_info = None
                                st.session_state.chat_history = []
                                st.session_state.show_upload_interface = True
                                st.session_state.input_key += 1
                                st.session_state.confirm_clear_docs = False
                                
                                st.success("✅ All documents cleared successfully!")
                                st.rerun()
                            else:
                                st.error(f"❌ Error clearing documents: {result.get('error', 'Unknown error')}")
                                st.session_state.confirm_clear_docs = False
                    
                    with col_confirm2:
                        if st.button("❌ Cancel", use_container_width=True):
                            st.session_state.confirm_clear_docs = False
                            st.rerun()
    
    # 3-Section Layout CSS
    st.markdown("""
    <style>
    /* Main parent container - exactly 100vh */
    .main-app-container {
        height: 100vh !important;
        display: flex !important;
        flex-direction: column !important;
        overflow: hidden !important;
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
    }
    
    /* Section 1: Title/Header - Fixed height at top */
    .title-section {
        height: 80px !important;
        flex-shrink: 0 !important;
        padding: 15px 20px !important;
        background-color: #0E1117 !important;
        border-bottom: 1px solid #262730 !important;
        display: flex !important;
        align-items: center !important;
        z-index: 100 !important;
        position: relative !important;
    }
    
    /* Section 2: Chat/Conversation - Flexible with scroll */
    .chat-section {
        flex: 1 !important;
        overflow-y: auto !important;
        overflow-x: hidden !important;
        padding: 20px !important;
        background-color: #0E1117 !important;
        min-height: 0 !important; /* Critical for flex children */
    }
    
    /* Section 3: Input - Fixed height at bottom */
    .input-section {
        height: 100px !important;
        flex-shrink: 0 !important;
        padding: 15px 20px !important;
        background-color: #0E1117 !important;
        border-top: 1px solid #262730 !important;
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
        z-index: 100 !important;
        position: relative !important;
    }
    
    /* Custom scrollbar for chat section */
    .chat-section::-webkit-scrollbar {
        width: 8px;
    }
    
    .chat-section::-webkit-scrollbar-track {
        background: #1E1E1E;
        border-radius: 4px;
    }
    
    .chat-section::-webkit-scrollbar-thumb {
        background: #404040;
        border-radius: 4px;
    }
    
    .chat-section::-webkit-scrollbar-thumb:hover {
        background: #555555;
    }
    
    /* Input styling */
    .input-section .stTextInput > div {
        border: none !important;
        padding: 0 !important;
        width: 100% !important;
    }
    
    .input-section .stTextInput > div > div {
        border: none !important;
    }
    
    .input-section .stTextInput > div > div > input {
        background-color: #262730 !important;
        border: 1px solid #404040 !important;
        border-radius: 25px !important;
        padding: 12px 20px !important;
        color: #FAFAFA !important;
        outline: none !important;
        box-shadow: none !important;
        font-size: 16px !important;
        width: 100% !important;
    }
    
    .input-section .stTextInput > div > div > input:focus {
        border: 1px solid #007ACC !important;
        box-shadow: 0 0 0 1px #007ACC !important;
        outline: none !important;
    }
    
    /* Button styling */
    .input-section .stButton > button {
        background-color: #007ACC !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 12px 30px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        height: 50px !important;
        min-width: 80px !important;
    }
    
    .input-section .stButton > button:hover {
        background-color: #005A9E !important;
        transform: translateY(-1px) !important;
    }
    
    /* Hide Streamlit's default app structure */
    .stApp > div:first-child {
        overflow: hidden !important;
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .title-section {
            height: 70px !important;
            padding: 10px 15px !important;
        }
        
        .input-section {
            height: 90px !important;
            padding: 10px 15px !important;
        }
        
        .chat-section {
            padding: 15px !important;
        }
    }
    
    @media (max-width: 480px) {
        .title-section {
            height: 60px !important;
            padding: 8px 10px !important;
        }
        
        .input-section {
            height: 80px !important;
            padding: 8px 10px !important;
        }
        
        .chat-section {
            padding: 10px !important;
        }
        
        .input-section .stTextInput > div > div > input {
            padding: 8px 12px !important;
            font-size: 14px !important;
        }
        
        .input-section .stButton > button {
            padding: 8px 20px !important;
            font-size: 14px !important;
            height: 40px !important;
        }
    }
    
    /* Process Documents Button - Purple Theme */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button[kind="primary"]:active {
        transform: translateY(0px) !important;
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # SECTION 3: Input (Fixed at bottom)
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    
    # Create responsive columns for input
    col1, col2 = st.columns([4, 1])
    
    with col1:
        query = st.text_input(
            "Ask a question about your documents:",
            placeholder="💬 Type your question here...",
            key=f"query_input_{st.session_state.input_key}",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("Ask", use_container_width=True, help="Ask question")
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close input-section
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close main-app-container
    
    # Process the question when user submits
    if (query and send_button) or (query and query not in [chat['question'] for chat in st.session_state.chat_history]):
        if query.strip():  # Make sure query is not empty
            with st.spinner("🔍 Searching and thinking..."):
                # Process question using backend service
                result = backend.process_query(query)
                
                if result["success"]:
                    # Add to chat history
                    add_to_chat_history(query, result["answer"], result["sources"])
                    
                    # Show success message temporarily
                    success_placeholder = st.success("✅ Answer generated!")
                    
                    # Clear the input and increment key to reset the input field
                    st.session_state.input_key += 1
                    
                    # Rerun to update the display
                    st.rerun()
                    
                else:
                    st.error(f"An error occurred: {result['error']}")
                    st.info("Please check your OpenAI API key and try again.")