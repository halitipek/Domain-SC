#!/usr/bin/env python
"""
URL Extraction and Scraping Tool for Domain-SC

This script extracts URLs from input files, scrapes their content,
and adds it to the RAG knowledge base. It also optionally processes
the input files themselves for RAG knowledge.
"""

import os
import sys
import re
import argparse
import logging
import json
import tempfile
import io
from pathlib import Path
from typing import List, Dict, Any, Set, Tuple
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify

# Try to import PDF libraries, but make them optional
try:
    from PyPDF2 import PdfReader
    HAVE_PYPDF2 = True
except ImportError:
    HAVE_PYPDF2 = False
    
try:
    import pdfplumber
    HAVE_PDFPLUMBER = True
except ImportError:
    HAVE_PDFPLUMBER = False

# Add project root to path
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

# Import from Domain-SC
from src.utils.logger import setup_logger
from enhanced_knowledge_base import EnhancedKnowledgeBaseBuilder, RESOURCES_DIR, CONFIG_DIR

# Set up logging
logger = setup_logger("url_extractor", "extract_and_scrape.log")

class URLExtractorAndScraper:
    """Extracts URLs from files and scrapes them for RAG knowledge."""
    
    def __init__(self, resources_dir: str = RESOURCES_DIR, config_dir: str = CONFIG_DIR):
        """Initialize the extractor and scraper.
        
        Args:
            resources_dir: Directory to save processed resources
            config_dir: Directory containing configuration files
        """
        self.resources_dir = resources_dir
        self.config_dir = config_dir
        self.temp_dir = os.path.join(project_root, "temp_extracts")
        
        # Create directories if they don't exist
        for directory in [resources_dir, config_dir, self.temp_dir]:
            os.makedirs(directory, exist_ok=True)
        
        # Initialize the knowledge base builder
        self.kb_builder = EnhancedKnowledgeBaseBuilder(
            resources_dir=resources_dir,
            config_dir=config_dir
        )
        
        # Tracked URLs to avoid duplicates
        self.extracted_urls = set()
        self.processed_urls = set()
        self.processed_files = set()
        
        logger.info("URL Extractor and Scraper initialized")
    
    def _is_valid_url(self, url: str) -> bool:
        """Check if a URL is valid."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    def extract_urls_from_text(self, text: str) -> Set[str]:
        """Extract URLs from text content."""
        # Pattern for matching URLs
        url_pattern = r'https?://[^\s()<>[\]"\']+(?:\([^\s()<>[\]"\']*\)|[^\s`!()\[\]{};:\'".,<>?«»""''])*'
        
        # Find all matches
        urls = set(re.findall(url_pattern, text))
        
        # Filter valid URLs
        valid_urls = set(url for url in urls if self._is_valid_url(url))
        
        # Add to tracked URLs
        self.extracted_urls.update(valid_urls)
        
        return valid_urls
    
    def extract_urls_from_file(self, file_path: str) -> Set[str]:
        """Extract URLs from a file based on its type."""
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return set()
        
        _, extension = os.path.splitext(file_path)
        extension = extension.lower()
        
        try:
            # Handle different file types
            if extension in ['.md', '.txt']:
                # Simple text file
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return self.extract_urls_from_text(content)
                
            elif extension in ['.html', '.htm']:
                # HTML file
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Use BeautifulSoup to extract URLs from href and src attributes
                soup = BeautifulSoup(content, 'html.parser')
                urls = set()
                
                # Extract from links
                for a_tag in soup.find_all('a', href=True):
                    href = a_tag['href']
                    if href.startswith(('http://', 'https://')):
                        urls.add(href)
                
                # Extract from images, scripts, etc.
                for tag in soup.find_all(['img', 'script', 'iframe'], src=True):
                    src = tag['src']
                    if src.startswith(('http://', 'https://')):
                        urls.add(src)
                
                # Also scan text for URLs
                urls.update(self.extract_urls_from_text(soup.get_text()))
                
                return urls
                
            elif extension in ['.pdf']:
                # PDF file
                urls = set()
                
                # Try PyPDF2 first
                if HAVE_PYPDF2:
                    try:
                        with open(file_path, 'rb') as f:
                            pdf = PdfReader(f)
                            text = ""
                            for page in pdf.pages:
                                page_text = page.extract_text()
                                if page_text:
                                    text += page_text + "\n"
                            
                            # Extract URLs from the text
                            urls.update(self.extract_urls_from_text(text))
                            logger.info(f"Extracted URLs from PDF using PyPDF2: {len(urls)}")
                    except Exception as e:
                        logger.warning(f"Error extracting text with PyPDF2: {str(e)}")
                
                # Try pdfplumber if PyPDF2 failed or found no URLs
                if HAVE_PDFPLUMBER and (not HAVE_PYPDF2 or len(urls) == 0):
                    try:
                        with pdfplumber.open(file_path) as pdf:
                            text = ""
                            for page in pdf.pages:
                                page_text = page.extract_text()
                                if page_text:
                                    text += page_text + "\n"
                            
                            # Extract URLs from the text
                            urls.update(self.extract_urls_from_text(text))
                            logger.info(f"Extracted URLs from PDF using pdfplumber: {len(urls)}")
                    except Exception as e:
                        logger.warning(f"Error extracting text with pdfplumber: {str(e)}")
                
                if not HAVE_PYPDF2 and not HAVE_PDFPLUMBER:
                    logger.warning("PDF support requires PyPDF2 or pdfplumber. Install with: pip install PyPDF2 pdfplumber")
                
                return urls
                
            elif extension in ['.json']:
                # JSON file
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Convert to string and extract URLs
                content = json.dumps(data)
                return self.extract_urls_from_text(content)
                
            elif extension in ['.py', '.js', '.java', '.c', '.cpp', '.h', '.cs']:
                # Code file - just extract from text
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return self.extract_urls_from_text(content)
                
            else:
                logger.warning(f"Unsupported file type: {extension}")
                # Try as text file anyway
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    return self.extract_urls_from_text(content)
                except Exception as e:
                    logger.error(f"Could not read file as text: {str(e)}")
                    return set()
                    
        except Exception as e:
            logger.error(f"Error extracting URLs from {file_path}: {str(e)}")
            return set()
    
    def process_file_for_rag(self, file_path: str) -> bool:
        """Process a file directly for RAG knowledge (without scraping)."""
        if file_path in self.processed_files:
            logger.info(f"File already processed: {file_path}")
            return False
            
        try:
            # Copy file to temp directory
            filename = os.path.basename(file_path)
            temp_path = os.path.join(self.temp_dir, filename)
            
            with open(file_path, 'r', encoding='utf-8') as src, open(temp_path, 'w', encoding='utf-8') as dst:
                content = src.read()
                dst.write(content)
            
            logger.info(f"Copied {file_path} to {temp_path} for processing")
            
            # Process the file with the knowledge base builder
            processed = self.kb_builder.process_files([temp_path])
            
            if processed > 0:
                logger.info(f"Successfully processed file for RAG: {file_path}")
                self.processed_files.add(file_path)
                return True
            else:
                logger.warning(f"File not processed (may not be relevant): {file_path}")
                return False
                
        except Exception as e:
            logger.error(f"Error processing file for RAG: {str(e)}")
            return False
    
    def scrape_url(self, url: str) -> bool:
        """Scrape a URL and process its content for RAG."""
        if url in self.processed_urls:
            logger.info(f"URL already processed: {url}")
            return False
        
        try:
            # Use the knowledge base builder to fetch and process the URL
            file_path = self.kb_builder.fetch_web_article(url)
            
            if file_path:
                logger.info(f"Successfully scraped and processed URL: {url}")
                self.processed_urls.add(url)
                return True
            else:
                logger.warning(f"URL not processed (may not be relevant): {url}")
                return False
                
        except Exception as e:
            logger.error(f"Error scraping URL: {str(e)}")
            return False
    
    def process_directory(self, directory: str, include_files: bool = True) -> Tuple[int, int]:
        """Process all files in a directory to extract and scrape URLs."""
        if not os.path.isdir(directory):
            logger.error(f"Directory not found: {directory}")
            return 0, 0
        
        extracted_count = 0
        processed_count = 0
        
        # Walk through the directory
        for root, _, files in os.walk(directory):
            for filename in files:
                file_path = os.path.join(root, filename)
                
                # Skip large files
                if os.path.getsize(file_path) > 10 * 1024 * 1024:  # 10 MB
                    logger.warning(f"Skipping large file: {file_path}")
                    continue
                
                # Extract URLs from the file
                urls = self.extract_urls_from_file(file_path)
                extracted_count += len(urls)
                
                # Process the file itself if requested
                if include_files:
                    if self.process_file_for_rag(file_path):
                        processed_count += 1
                
                # Process each extracted URL
                for url in urls:
                    if self.scrape_url(url):
                        processed_count += 1
        
        return extracted_count, processed_count
    
    def process_files(self, file_paths: List[str], include_files: bool = True) -> Tuple[int, int]:
        """Process specific files to extract and scrape URLs."""
        extracted_count = 0
        processed_count = 0
        
        for file_path in file_paths:
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                continue
            
            if os.path.isdir(file_path):
                ext_count, proc_count = self.process_directory(file_path, include_files)
                extracted_count += ext_count
                processed_count += proc_count
                continue
            
            # Skip large files
            if os.path.getsize(file_path) > 10 * 1024 * 1024:  # 10 MB
                logger.warning(f"Skipping large file: {file_path}")
                continue
            
            # Extract URLs from the file
            urls = self.extract_urls_from_file(file_path)
            extracted_count += len(urls)
            
            # Process the file itself if requested
            if include_files:
                if self.process_file_for_rag(file_path):
                    processed_count += 1
            
            # Process each extracted URL
            for url in urls:
                if self.scrape_url(url):
                    processed_count += 1
        
        return extracted_count, processed_count
    
    def save_extracted_urls(self, output_file: str = None) -> str:
        """Save the list of extracted URLs to a file."""
        if not output_file:
            output_file = os.path.join(self.config_dir, "extracted_urls.json")
        
        try:
            data = {
                "extracted_urls": list(self.extracted_urls),
                "processed_urls": list(self.processed_urls),
                "processed_files": list(self.processed_files)
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
                
            logger.info(f"Saved extracted URLs to {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"Error saving URLs: {str(e)}")
            return None

def main():
    """Main function to run the URL extractor and scraper."""
    parser = argparse.ArgumentParser(description="Extract URLs from files and scrape them for RAG knowledge")
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--files', '-f', nargs='+', help="Specific files to process")
    input_group.add_argument('--directory', '-d', help="Directory to process recursively")
    
    # Processing options
    parser.add_argument('--include-files', action='store_true', default=True, 
                        help="Process the input files themselves for RAG (default: True)")
    parser.add_argument('--output', '-o', help="Output file for extracted URLs")
    parser.add_argument('--resources-dir', help="Directory to save processed resources")
    parser.add_argument('--config-dir', help="Directory containing configuration files")
    parser.add_argument('--relevance-threshold', type=float, default=0.35,
                        help="Minimum relevance score threshold (default: 0.35)")
    
    args = parser.parse_args()
    
    # Initialize the extractor with custom directories if provided
    extractor = URLExtractorAndScraper(
        resources_dir=args.resources_dir or RESOURCES_DIR,
        config_dir=args.config_dir or CONFIG_DIR
    )
    
    # Set relevance threshold if specified
    if args.relevance_threshold:
        extractor.kb_builder.RELEVANCE_THRESHOLD = args.relevance_threshold
    
    # Process input
    if args.directory:
        print(f"Processing directory: {args.directory}")
        extracted, processed = extractor.process_directory(
            args.directory, 
            include_files=args.include_files
        )
    elif args.files:
        print(f"Processing {len(args.files)} files")
        extracted, processed = extractor.process_files(
            args.files,
            include_files=args.include_files
        )
    
    # Save the extracted URLs
    output_file = extractor.save_extracted_urls(args.output)
    
    # Print summary
    print("\nExtraction and Scraping Summary:")
    print(f"URLs extracted: {len(extractor.extracted_urls)}")
    print(f"URLs processed: {len(extractor.processed_urls)}")
    print(f"Files processed: {len(extractor.processed_files)}")
    print(f"Extracted URLs saved to: {output_file}")
    print(f"Processed resources saved to: {extractor.resources_dir}")
    
    # Set up RAG index with the new knowledge
    setup_cmd = f"python src/setup.py --setup-rag --resource-dir {extractor.resources_dir}"
    print(f"\nTo set up the RAG index with the new knowledge, run:\n{setup_cmd}")

if __name__ == "__main__":
    main()