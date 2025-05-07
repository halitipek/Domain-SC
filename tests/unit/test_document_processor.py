"""
Unit tests for the document processor.
"""

import os
import unittest
import tempfile
from pathlib import Path
import json

# Add project root to Python path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.utils.document_processor import DocumentProcessor


class TestDocumentProcessor(unittest.TestCase):
    """Tests for the DocumentProcessor class."""
    
    def setUp(self):
        """Set up test environment."""
        self.processor = DocumentProcessor(chunk_size=200, chunk_overlap=20)
        self.test_dir = tempfile.mkdtemp()
        
        # Create test files
        self.test_files = {}
        
        # Text file
        self.txt_path = os.path.join(self.test_dir, "test.txt")
        with open(self.txt_path, "w") as f:
            f.write("This is a test document.\nIt has multiple lines.\nThis is used for testing document processing.")
        self.test_files["txt"] = self.txt_path
        
        # Markdown file
        self.md_path = os.path.join(self.test_dir, "test.md")
        with open(self.md_path, "w") as f:
            f.write("# Test Markdown\n\nThis is a **markdown** document.\n\n- Item 1\n- Item 2\n")
        self.test_files["md"] = self.md_path
        
        # JSON file
        self.json_path = os.path.join(self.test_dir, "test.json")
        with open(self.json_path, "w") as f:
            json.dump({"key": "value", "array": [1, 2, 3]}, f)
        self.test_files["json"] = self.json_path
        
    def tearDown(self):
        """Clean up test environment."""
        # Remove test files
        for file_path in self.test_files.values():
            if os.path.exists(file_path):
                os.remove(file_path)
        
        # Remove test directory
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)
    
    def test_initialization(self):
        """Test initialization of the DocumentProcessor."""
        self.assertEqual(self.processor.chunk_size, 200)
        self.assertEqual(self.processor.chunk_overlap, 20)
        self.assertIsNotNone(self.processor.text_splitter)
    
    def test_load_document_txt(self):
        """Test loading a text document."""
        docs = self.processor.load_document(self.txt_path)
        
        # Verify docs are loaded
        self.assertGreater(len(docs), 0)
        
        # Verify metadata
        for doc in docs:
            self.assertEqual(doc.metadata["source"], self.txt_path)
            self.assertEqual(doc.metadata["file_type"], ".txt")
            self.assertEqual(doc.metadata["filename"], "test.txt")
    
    def test_load_document_md(self):
        """Test loading a markdown document."""
        docs = self.processor.load_document(self.md_path)
        
        # Verify docs are loaded
        self.assertGreater(len(docs), 0)
        
        # Verify metadata
        for doc in docs:
            self.assertEqual(doc.metadata["source"], self.md_path)
            self.assertEqual(doc.metadata["file_type"], ".md")
            self.assertEqual(doc.metadata["filename"], "test.md")
    
    def test_load_document_json(self):
        """Test loading a JSON document."""
        docs = self.processor.load_document(self.json_path)
        
        # Verify docs are loaded
        self.assertGreater(len(docs), 0)
        
        # Verify metadata
        for doc in docs:
            self.assertEqual(doc.metadata["source"], self.json_path)
            self.assertEqual(doc.metadata["file_type"], ".json")
            self.assertEqual(doc.metadata["filename"], "test.json")
    
    def test_load_nonexistent_document(self):
        """Test loading a nonexistent document."""
        docs = self.processor.load_document("/path/to/nonexistent/file.txt")
        self.assertEqual(len(docs), 0)
    
    def test_chunk_documents(self):
        """Test chunking documents."""
        # Load a document
        docs = self.processor.load_document(self.txt_path)
        
        # Chunk the document
        chunked_docs = self.processor.chunk_documents(docs)
        
        # Verify chunking
        self.assertGreaterEqual(len(chunked_docs), len(docs))
    
    def test_extract_metadata(self):
        """Test extracting metadata from documents."""
        # Load documents
        docs1 = self.processor.load_document(self.txt_path)
        docs2 = self.processor.load_document(self.md_path)
        all_docs = docs1 + docs2
        
        # Extract metadata
        metadata = self.processor.extract_metadata(all_docs)
        
        # Verify metadata
        self.assertEqual(metadata["total_documents"], len(all_docs))
        self.assertIn(".txt", metadata["document_types"])
        self.assertIn(".md", metadata["document_types"])
        self.assertIn(self.txt_path, metadata["document_sources"])
        self.assertIn(self.md_path, metadata["document_sources"])
        self.assertEqual(metadata["total_chunks"], len(all_docs))
        self.assertGreater(metadata["average_chunk_length"], 0)
    
    def test_process_files(self):
        """Test processing multiple files."""
        # Process files
        file_paths = [self.txt_path, self.md_path, self.json_path]
        chunked_docs, metadata = self.processor.process_files(file_paths)
        
        # Verify chunked documents
        self.assertGreater(len(chunked_docs), 0)
        
        # Verify metadata
        self.assertEqual(metadata["total_documents"], len(chunked_docs))
        self.assertIn(".txt", metadata["document_types"])
        self.assertIn(".md", metadata["document_types"])
        self.assertIn(".json", metadata["document_types"])
        self.assertIn(self.txt_path, metadata["document_sources"])
        self.assertIn(self.md_path, metadata["document_sources"])
        self.assertIn(self.json_path, metadata["document_sources"])
        self.assertEqual(metadata["total_chunks"], len(chunked_docs))
        self.assertGreater(metadata["average_chunk_length"], 0)


if __name__ == "__main__":
    unittest.main()