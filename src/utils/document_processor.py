"""
Document processing utilities for Domain-SC.
Handles text extraction, chunking, and preparation for vector indexing.
"""

import os
import hashlib
import logging
from typing import List, Dict, Any, Tuple
import re

from utils.logger import setup_logger

logger = setup_logger(__name__, "document_processor.log")

def process_files(file_paths: List[str], chunk_size: int = 1000, chunk_overlap: int = 200) -> Tuple[List[str], List[Dict[str, Any]], List[str]]:
    """
    Process text files for indexing.
    
    Args:
        file_paths: List of paths to files to process
        chunk_size: Size of text chunks
        chunk_overlap: Overlap between chunks
        
    Returns:
        Tuple of (documents, metadatas, ids)
    """
    documents = []
    metadatas = []
    ids = []
    
    for file_path in file_paths:
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                logger.warning(f"File not found: {file_path}")
                continue
                
            # Extract text based on file type
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext == '.md':
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
            elif file_ext == '.txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
            else:
                logger.warning(f"Unsupported file type: {file_ext} - skipping {file_path}")
                continue
                
            # Generate chunks
            chunks = _chunk_text(text, chunk_size, chunk_overlap)
            
            # Create metadata and IDs
            for i, chunk in enumerate(chunks):
                # Generate a consistent ID
                chunk_id = hashlib.md5(f"{file_path}_{i}".encode()).hexdigest()
                
                documents.append(chunk)
                metadatas.append({
                    "source": file_path,
                    "chunk": i,
                    "total_chunks": len(chunks)
                })
                ids.append(chunk_id)
                
            logger.info(f"Processed {file_path}: {len(chunks)} chunks")
            
        except Exception as e:
            logger.error(f"Error processing {file_path}: {str(e)}")
    
    return documents, metadatas, ids
    
def _chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
    """
    Split text into overlapping chunks.
    
    Args:
        text: Text to split
        chunk_size: Maximum chunk size
        chunk_overlap: Overlap between chunks
        
    Returns:
        List of text chunks
    """
    # Clean text
    text = re.sub(r'\s+', ' ', text).strip()
    
    # If text is shorter than chunk size, return as single chunk
    if len(text) <= chunk_size:
        return [text]
        
    chunks = []
    start = 0
    
    while start < len(text):
        # Find end of chunk
        end = start + chunk_size
        
        # If we're at the end, just use the remaining text
        if end >= len(text):
            chunks.append(text[start:])
            break
            
        # Try to break at paragraph or sentence
        if end < len(text):
            # First try to find paragraph break
            paragraph_break = text.rfind("\n\n", start, end)
            
            if paragraph_break != -1 and paragraph_break > start + chunk_size // 2:
                # Found a good paragraph break
                end = paragraph_break
            else:
                # Try to find sentence break
                sentence_break = text.rfind(". ", start, end)
                if sentence_break != -1 and sentence_break > start + chunk_size // 2:
                    end = sentence_break + 1  # Include the period
        
        # Add the chunk
        chunks.append(text[start:end])
        
        # Move to next chunk with overlap
        start = end - chunk_overlap
        
    return chunks