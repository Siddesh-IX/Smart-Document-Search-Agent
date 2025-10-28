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

@st.cache_resource
def get_backend():
    """Get the backend service instance (cached)"""
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
        st.subheader("💬 Conversation History")
        
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

# Add custom CSS for better chat appearance
st.markdown("""
<style>
/* Chat container styling */
.chat-container {
    max-height: 600px;
    overflow-y: auto;
    padding: 10px 0;
}

/* Hide Streamlit default elements */
.stApp > header {
    background-color: transparent;
}

/* Custom scrollbar */
.chat-container::-webkit-scrollbar {
    width: 8px;
}

.chat-container::-webkit-scrollbar-track {
    background: #1E1E1E;
    border-radius: 4px;
}

.chat-container::-webkit-scrollbar-thumb {
    background: #404040;
    border-radius: 4px;
}

.chat-container::-webkit-scrollbar-thumb:hover {
    background: #555555;
}

/* Improve button styling */
.stButton > button {
    background-color: #007ACC !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    padding: 8px 16px !important;
    min-height: 40px !important;
}

.stButton > button:hover {
    background-color: #005A9E !important;
    transform: scale(1.02) !important;
    transition: all 0.2s !important;
}

.stButton > button:focus {
    outline: none !important;
    box-shadow: 0 0 0 2px rgba(0, 122, 204, 0.3) !important;
}

/* Sidebar improvements */
.css-1d391kg {
    background-color: #1E1E1E;
}
</style>
""", unsafe_allow_html=True)

st.title("📄 Smart Document Search Agent")

# Add main content wrapper to prevent overlap with sticky input
st.markdown('<div class="main-content">', unsafe_allow_html=True)

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
        st.markdown("""
        <div style="
            background-color: #262730;
            padding: 30px;
            border-radius: 15px;
            border: 2px dashed #007ACC;
            margin: 20px 0;
            text-align: center;
        ">
        """, unsafe_allow_html=True)
        
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
        
        # Instructions
        st.markdown("""
        <div style="
            background-color: #1E1E1E;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        ">
            <h4 style="color: #007ACC;">💡 How it works:</h4>
            <ol style="color: #B0B0B0; line-height: 1.6;">
                <li>Upload 1-10 PDF or Word documents</li>
                <li>Click "Process Documents" to create search index</li>
                <li>Start asking questions about your documents</li>
                <li>Get AI-powered answers with source references</li>
            </ol>
            
            <h4 style="color: #007ACC; margin-top: 20px;">🔒 Privacy:</h4>
            <p style="color: #B0B0B0; margin: 0;">Your documents are processed locally and securely. Files are temporarily stored only during processing.</p>
            
            <h4 style="color: #007ACC; margin-top: 20px;">🎯 AI Behavior:</h4>
            <p style="color: #B0B0B0; margin: 0;">The AI will only answer based on your uploaded documents. If information isn't found, it will clearly state this instead of guessing.</p>
        </div>
        """, unsafe_allow_html=True)

else:
    # Chat Interface (existing code with modifications)
    # Show processing status if files were just processed
    if st.session_state.processing_status and st.session_state.uploaded_files_info:
        st.success(f"✅ Successfully processed {len(st.session_state.uploaded_files_info)} documents!")
        
        with st.expander("📊 Processing Details", expanded=False):
            st.write(f"**Files processed:** {', '.join(st.session_state.uploaded_files_info)}")
            st.write(f"**Total chunks created:** {st.session_state.processing_status.get('total_chunks', 'N/A')}")
            
            if st.button("🔄 Upload New Documents", use_container_width=True):
                # Reset session state to go back to upload interface
                st.session_state.files_processed = False
                st.session_state.processing_status = None
                st.session_state.uploaded_files_info = None
                st.session_state.chat_history = []
                st.session_state.show_upload_interface = True
                st.session_state.input_key += 1  # Reset input field as well
                st.rerun()
    
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
            - "What is the main topic of these documents?"
            - "Summarize the key points"
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
                if st.button("🗑️ Clear Chat", use_container_width=True):
                    st.session_state.chat_history = []
                    st.session_state.input_key += 1
                    st.rerun()
            
            with col2:
                if st.button("📁 New Upload", use_container_width=True):
                    # Clear all session state for fresh upload
                    st.session_state.files_processed = False
                    st.session_state.processing_status = None
                    st.session_state.uploaded_files_info = None
                    st.session_state.chat_history = []
                    st.session_state.show_upload_interface = True
                    st.session_state.input_key += 1  # Reset input field as well
                    st.rerun()
    
    # Display chat history
    display_chat_history()
    
    # Fixed input at the bottom with modern styling
    st.markdown("---")
    
    # Sticky search bar at the bottom with responsive design
    st.markdown("""
    <style>
    /* Sticky input container */
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #0E1117;
        padding: 15px 20px 20px 20px;
        border-top: 1px solid #262730;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.3);
        z-index: 1000;
    }
    
    /* Remove outer border and keep only inner */
    .stTextInput > div {
        border: none !important;
        padding: 0 !important;
    }
    
    .stTextInput > div > div {
        border: none !important;
    }
    
    .stTextInput > div > div > input {
        background-color: #262730 !important;
        border: 1px solid #404040 !important;
        border-radius: 25px !important;
        padding: 12px 20px !important;
        color: #FAFAFA !important;
        outline: none !important;
        box-shadow: none !important;
        font-size: 16px !important; /* Prevents zoom on mobile */
    }
    
    .stTextInput > div > div > input:focus {
        border: 1px solid #007ACC !important;
        box-shadow: 0 0 0 1px #007ACC !important;
        outline: none !important;
    }
    
    .stTextInput > div > div > input:focus-visible {
        outline: none !important;
        border: 1px solid #007ACC !important;
        box-shadow: 0 0 0 1px #007ACC !important;
    }
    
    /* Remove red borders completely */
    .stTextInput > div > div > input:invalid,
    .stTextInput > div > div > input:required {
        border: 1px solid #404040 !important;
        box-shadow: none !important;
    }
    
    /* Add bottom margin to main content to prevent overlap with sticky input */
    .main-content {
        margin-bottom: 100px;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .input-container {
            padding: 10px 15px 15px 15px;
        }
        
        .stTextInput > div > div > input {
            padding: 10px 15px !important;
            font-size: 16px !important;
        }
        
        /* Adjust column widths on mobile */
        .stColumns {
            gap: 5px;
        }
        
        /* Chat bubbles responsive */
        .main-content {
            margin-bottom: 120px;
            padding: 0 10px;
        }
        
        /* Make chat bubbles full width on mobile */
        [data-testid="column"] {
            min-width: 0;
        }
    }
    
    @media (max-width: 480px) {
        .input-container {
            padding: 8px 10px 12px 10px;
        }
        
        .stTextInput > div > div > input {
            padding: 8px 12px !important;
            font-size: 16px !important;
        }
        
        .main-content {
            margin-bottom: 110px;
            padding: 0 5px;
        }
        
        /* Stack columns on very small screens */
        .stColumns {
            flex-direction: column;
            gap: 2px;
        }
        
        /* Hide sidebar on mobile for more space */
        .css-1d391kg {
            display: none;
        }
    }
    
    /* Ensure text is readable on all devices */
    @media (min-width: 1200px) {
        .main-content {
            max-width: 1200px;
            margin: 0 auto 100px auto;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Wrap input in container with sticky class
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    with st.container():
        # Create responsive columns
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
    
    st.markdown('</div>', unsafe_allow_html=True)
    
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

# Close main content wrapper
st.markdown('</div>', unsafe_allow_html=True)