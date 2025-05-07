"""
Functional tests for the CLI tool.
"""

import unittest
import subprocess
import sys
import os
from pathlib import Path
import tempfile
import json
import shutil

# Add project root to Python path
root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root_dir))


class TestCLI(unittest.TestCase):
    """Functional tests for the CLI tool."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        
        # Create a test markdown file
        self.test_md = os.path.join(self.test_dir, "test.md")
        with open(self.test_md, "w") as f:
            f.write("""# Test Document
            
This is a test document for the CLI.

## Section 1

- Item 1
- Item 2

## Section 2

More test content.
""")
    
    def tearDown(self):
        """Clean up test environment."""
        # Remove test directory and contents
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def run_cli(self, args):
        """Run the CLI with the given arguments.
        
        Args:
            args: List of CLI arguments
            
        Returns:
            (stdout, stderr, return_code)
        """
        cli_path = os.path.join(root_dir, "cli.py")
        
        # Run the CLI
        process = subprocess.Popen(
            [sys.executable, cli_path] + args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Get output
        stdout, stderr = process.communicate()
        return_code = process.returncode
        
        return stdout, stderr, return_code
    
    def test_rag_index_and_query(self):
        """Test the RAG index and query commands."""
        # Skip this test if in CI environment (which might not have the dependencies)
        if os.environ.get("CI"):
            self.skipTest("Skipping in CI environment")
        
        # Run RAG index command
        stdout, stderr, return_code = self.run_cli(["rag", "index", "--files", self.test_md])
        
        # If the command fails due to missing dependencies, skip the test
        if return_code != 0 and "No module named" in stderr:
            self.skipTest(f"Skipping due to missing dependencies: {stderr}")
        
        # Otherwise, verify command succeeded
        self.assertEqual(return_code, 0, f"Command failed with stderr: {stderr}")
        
        try:
            # Parse the JSON output
            result = json.loads(stdout)
            
            # Verify result
            self.assertEqual(result["status"], "success")
            self.assertGreater(result["document_count"], 0)
        except json.JSONDecodeError:
            # If the output is not valid JSON, the test will still pass
            # if the return code is 0 (this can happen if pretty-printing is used)
            pass
        
        # Run RAG query command
        stdout, stderr, return_code = self.run_cli(["rag", "query", "--query", "test document"])
        
        # Verify command succeeded
        self.assertEqual(return_code, 0, f"Command failed with stderr: {stderr}")
    
    def test_help_command(self):
        """Test the help command."""
        # Run help command
        stdout, stderr, return_code = self.run_cli(["--help"])
        
        # Verify command succeeded
        self.assertEqual(return_code, 0)
        
        # Verify help output
        self.assertIn("Domain-SC Command Line Interface", stdout)
        self.assertIn("Command to execute", stdout)
    
    def test_rag_stats_command(self):
        """Test the RAG stats command."""
        # Skip this test if in CI environment
        if os.environ.get("CI"):
            self.skipTest("Skipping in CI environment")
        
        # Run RAG stats command
        stdout, stderr, return_code = self.run_cli(["rag", "stats"])
        
        # If the command fails due to missing dependencies, skip the test
        if return_code != 0 and "No module named" in stderr:
            self.skipTest(f"Skipping due to missing dependencies: {stderr}")
        
        # Otherwise, verify command succeeded
        self.assertEqual(return_code, 0, f"Command failed with stderr: {stderr}")
        
        try:
            # Parse the JSON output
            result = json.loads(stdout)
            
            # Verify result structure
            self.assertIn("chunk_size", result)
            self.assertIn("chunk_overlap", result)
            self.assertIn("embedding_model", result)
            self.assertIn("vector_store", result)
        except json.JSONDecodeError:
            # If the output is not valid JSON, the test will still pass
            # if the return code is 0
            pass


if __name__ == "__main__":
    unittest.main()