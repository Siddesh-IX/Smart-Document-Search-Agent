"""
Backend API module for Smart Document Search Agent
Handles all OpenAI API calls and document processing
"""

import os
import tempfile
import shutil
from io import BytesIO
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.document_loaders.word_document import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

class DocumentSearchBackend:
    """Backend service for document search operations"""
    
    def __init__(self, faiss_path="faiss_index"):
        self.faiss_path = faiss_path
        self.index = None
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
    def load_index(self):
        """Load the FAISS index"""
        try:
            self.index = FAISS.load_local(
                self.faiss_path, 
                self.embeddings, 
                allow_dangerous_deserialization=True
            )
            return True
        except Exception as e:
            print(f"Error loading FAISS index: {e}")
            return False
    
    def validate_file_type(self, file_name: str) -> Dict[str, Any]:
        """Validate if file is PDF or Word document"""
        valid_extensions = {
            '.pdf': 'PDF',
            '.doc': 'Word',
            '.docx': 'Word',
            '.txt': 'Text'
        }
        
        file_ext = os.path.splitext(file_name.lower())[1]
        
        if file_ext in valid_extensions:
            return {
                'valid': True,
                'type': valid_extensions[file_ext],
                'extension': file_ext
            }
        else:
            return {
                'valid': False,
                'type': None,
                'extension': file_ext,
                'error': f'Unsupported file type: {file_ext}. Only PDF, Word (.doc, .docx), and Text files are supported.'
            }
    
    def process_uploaded_files(self, uploaded_files) -> Dict[str, Any]:
        """Process uploaded files and create/update FAISS index"""
        try:
            # Validate file count
            if len(uploaded_files) < 1:
                return {
                    'success': False,
                    'error': 'At least 1 file is required.',
                    'processed_count': 0
                }
            
            if len(uploaded_files) > 10:
                return {
                    'success': False,
                    'error': 'Maximum 10 files allowed.',
                    'processed_count': 0
                }
            
            documents = []
            processed_files = []
            errors = []
            
            # Create temporary directory for file processing
            with tempfile.TemporaryDirectory() as temp_dir:
                
                for uploaded_file in uploaded_files:
                    try:
                        # Validate file type
                        validation = self.validate_file_type(uploaded_file.name)
                        if not validation['valid']:
                            errors.append(f"{uploaded_file.name}: {validation['error']}")
                            continue
                        
                        # Save uploaded file temporarily
                        temp_file_path = os.path.join(temp_dir, uploaded_file.name)
                        with open(temp_file_path, 'wb') as f:
                            f.write(uploaded_file.getvalue())
                        
                        # Load document based on file type
                        file_docs = self._load_document(temp_file_path, validation['extension'])
                        documents.extend(file_docs)
                        processed_files.append(uploaded_file.name)
                        
                    except Exception as e:
                        errors.append(f"{uploaded_file.name}: Error processing file - {str(e)}")
                        continue
            
            if not documents:
                return {
                    'success': False,
                    'error': 'No documents could be processed successfully.',
                    'errors': errors,
                    'processed_count': 0
                }
            
            # Split documents into chunks
            docs = self.text_splitter.split_documents(documents)
            
            # Create new FAISS index
            self.index = FAISS.from_documents(docs, self.embeddings)
            
            # Save the index
            if os.path.exists(self.faiss_path):
                shutil.rmtree(self.faiss_path)
            self.index.save_local(self.faiss_path)
            
            return {
                'success': True,
                'message': f'Successfully processed {len(processed_files)} files with {len(docs)} chunks.',
                'processed_files': processed_files,
                'total_chunks': len(docs),
                'errors': errors,
                'processed_count': len(processed_files)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error during file processing: {str(e)}',
                'processed_count': 0
            }
    
    def _load_document(self, file_path: str, file_extension: str):
        """Load document based on file type"""
        try:
            if file_extension == '.pdf':
                loader = PyPDFLoader(file_path)
            elif file_extension in ['.doc', '.docx']:
                loader = Docx2txtLoader(file_path)
            elif file_extension == '.txt':
                loader = TextLoader(file_path, encoding='utf-8')
            else:
                raise ValueError(f"Unsupported file extension: {file_extension}")
            
            return loader.load()
            
        except Exception as e:
            raise Exception(f"Failed to load document {os.path.basename(file_path)}: {str(e)}")
    
    def get_index_status(self) -> Dict[str, Any]:
        """Get current index status and information"""
        if self.index is None:
            return {
                'loaded': False,
                'document_count': 0,
                'message': 'No index loaded. Please upload documents to get started.'
            }
        else:
            return {
                'loaded': True,
                'document_count': self.index.index.ntotal,
                'message': f'Index ready with {self.index.index.ntotal} document chunks.'
            }
    
    def format_docs(self, docs):
        """Format retrieved documents for the prompt"""
        formatted = []
        for i, doc in enumerate(docs):
            source = doc.metadata.get('source', 'Unknown')
            content = doc.page_content
            formatted.append(f"Document {i+1} (Source: {os.path.basename(source)}):\n{content}")
        return "\n\n".join(formatted)
    
    def search_documents(self, query, k=3):
        """Search for relevant documents"""
        if not self.index:
            raise ValueError("Index not loaded. Call load_index() first.")
        
        retriever = self.index.as_retriever(search_kwargs={"k": k})
        relevant_docs = retriever.invoke(query)
        return relevant_docs
    
    def generate_answer(self, query, context):
        """Generate answer using OpenAI API"""
        template = """Answer the question based STRICTLY on the following context from the provided documents. 

        IMPORTANT INSTRUCTIONS:
        - Only use information that is explicitly mentioned in the context below
        - Do NOT make assumptions, guesses, or add information not present in the documents
        - If the answer is not found in the provided context, clearly state: "I cannot find information about this topic in the provided documents. Please contact the administrator for more details."
        - When information is available, be conversational and helpful
        - Always mention the source documents when providing answers
        - Do not provide general knowledge that isn't in the documents

        Context from documents:
        {context}

        Question: {question}

        Answer: """
        
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | self.llm | StrOutputParser()
        
        answer = chain.invoke({
            "context": context, 
            "question": query
        })
        
        return answer
    
    def _validate_answer(self, answer, context):
        """Validate answer to prevent hallucinations"""
        # Check for common patterns that indicate the AI is providing general knowledge
        hallucination_indicators = [
            "generally", "typically", "usually", "commonly", "often",
            "in most cases", "generally speaking", "as a rule",
            "it is known that", "studies show", "research indicates",
            "experts believe", "it is widely accepted"
        ]
        
        # Convert to lowercase for checking
        answer_lower = answer.lower()
        
        # If the answer contains hallucination indicators and doesn't reference the documents
        if any(indicator in answer_lower for indicator in hallucination_indicators):
            if "document" not in answer_lower and "provided" not in answer_lower:
                return "I cannot find information about this topic in the provided documents. Please contact the administrator for more details."
        
        # If the answer is very generic and doesn't mention sources or documents
        if len(answer) > 200 and "document" not in answer_lower and "source" not in answer_lower:
            # Check if the answer content actually appears in the context
            context_lower = context.lower()
            answer_words = set(answer_lower.split())
            context_words = set(context_lower.split())
            
            # If less than 30% of answer words appear in context, it might be hallucinated
            overlap = len(answer_words.intersection(context_words)) / len(answer_words) if answer_words else 0
            if overlap < 0.3:
                return "I cannot find information about this topic in the provided documents. Please contact the administrator for more details."
        
        return answer
    
    def process_query(self, query):
        """Main function to process a user query"""
        try:
            # Search for relevant documents
            relevant_docs = self.search_documents(query)
            
            # Check if we found any documents
            if not relevant_docs:
                return {
                    "success": True,
                    "answer": "I cannot find any relevant information about this topic in the provided documents. Please contact the administrator for more details.",
                    "sources": [],
                    "relevant_docs": [],
                    "context_length": 0
                }
            
            # Format context
            context = self.format_docs(relevant_docs)
            
            # Check if context is meaningful (not just empty or very short)
            if len(context.strip()) < 50:  # If context is too short, it's likely not relevant
                return {
                    "success": True,
                    "answer": "I cannot find sufficient information about this topic in the provided documents. Please contact the administrator for more details.",
                    "sources": [],
                    "relevant_docs": [],
                    "context_length": 0
                }
            
            # Generate answer
            answer = self.generate_answer(query, context)
            
            # Post-process answer to catch potential hallucinations
            answer = self._validate_answer(answer, context)
            
            # Check if the answer indicates no information was found
            no_info_indicators = [
                "cannot find information",
                "cannot find any relevant information", 
                "cannot find sufficient information",
                "cannot find specific information",
                "no information available",
                "not found in the provided documents"
            ]
            
            answer_lower = answer.lower()
            no_info_found = any(indicator in answer_lower for indicator in no_info_indicators)
            
            # Extract sources only if information was actually found
            sources = []
            used_docs = []
            context_length = 0
            
            if not no_info_found:
                # Only extract sources when we have a real answer
                sources_set = set()
                for doc in relevant_docs:
                    source = doc.metadata.get('source', 'Unknown')
                    sources_set.add(os.path.basename(source) if source != 'Unknown' else 'Unknown')
                sources = list(sources_set)
                used_docs = relevant_docs
                context_length = len(context)
            
            return {
                "success": True,
                "answer": answer,
                "sources": sources,
                "relevant_docs": used_docs,
                "context_length": context_length
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "answer": None,
                "sources": [],
                "relevant_docs": [],
                "context_length": 0
            }

# Global backend instance
backend_service = None

def get_backend_service():
    """Get or create the backend service instance"""
    global backend_service
    if backend_service is None:
        backend_service = DocumentSearchBackend()
        backend_service.load_index()
    return backend_service