#!/usr/bin/env python3
"""
Test script to verify backend functionality
"""

import os
from dotenv import load_dotenv
from backend import get_backend_service

def main():
    print("=== Backend Test ===")
    
    # Load environment variables
    load_dotenv()
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"✓ API Key loaded: {api_key[:20]}...{api_key[-5:]}")
    else:
        print("✗ No API key found!")
        return
    
    # Test backend initialization
    try:
        backend = get_backend_service()
        print(f"✓ Backend created: {backend}")
        print(f"✓ Backend index: {backend.index}")
        
        # Get index status
        status = backend.get_index_status()
        print(f"✓ Index status: {status}")
        
        if status['loaded']:
            print("✓ Ready to test search!")
            
            # Test a simple query
            test_query = "What is this document about?"
            result = backend.process_query(test_query)
            
            if result['success']:
                print(f"✓ Search test successful!")
                print(f"  Answer preview: {result['answer'][:100]}...")
                print(f"  Sources: {result['sources']}")
            else:
                print(f"✗ Search test failed: {result['error']}")
        else:
            print("! Index not loaded - upload some files first")
            
    except Exception as e:
        print(f"✗ Backend test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()