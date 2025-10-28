"""
Backend API module for Smart Document Search Agent
Handles all OpenAI API calls and document processing
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
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
        
    def load_index(self):
        """Load the FAISS index"""
        try:
            embeddings = OpenAIEmbeddings()
            self.index = FAISS.load_local(
                self.faiss_path, 
                embeddings, 
                allow_dangerous_deserialization=True
            )
            return True
        except Exception as e:
            print(f"Error loading FAISS index: {e}")
            return False
    
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
        template = """Answer the question based only on the following context. 
        Be conversational and helpful. Always mention the source documents when relevant.

        Context:
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
    
    def process_query(self, query):
        """Main function to process a user query"""
        try:
            # Search for relevant documents
            relevant_docs = self.search_documents(query)
            
            # Format context
            context = self.format_docs(relevant_docs)
            
            # Generate answer
            answer = self.generate_answer(query, context)
            
            # Extract sources
            sources = set()
            for doc in relevant_docs:
                source = doc.metadata.get('source', 'Unknown')
                sources.add(os.path.basename(source) if source != 'Unknown' else 'Unknown')
            
            return {
                "success": True,
                "answer": answer,
                "sources": list(sources),
                "relevant_docs": relevant_docs,
                "context_length": len(context)
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