# RAG Knowledge Enhancement Tools

This document explains how to use the URL extraction and scraping tools to enhance your RAG knowledge base with content from external sources and provided files.

## Extract and Scrape URLs Tool

The `extract_and_scrape.py` script automatically extracts URLs from input files, scrapes their content, and processes both the input files and the scraped content for your RAG knowledge base.

### Basic Usage

```bash
# Process specific files and scrape URLs found within them
python extract_and_scrape.py --files file1.md file2.txt documentation.html

# Process an entire directory recursively
python extract_and_scrape.py --directory /path/to/documents

# Save extracted URLs to a specific file
python extract_and_scrape.py --files file1.md file2.txt --output extracted_urls.json

# Adjust the relevance threshold (0.0-1.0)
python extract_and_scrape.py --files file1.md --relevance-threshold 0.3
```

### Advanced Options

```bash
# Process URLs only, but not the files themselves
python extract_and_scrape.py --files file1.md --include-files false

# Specify a custom resources directory
python extract_and_scrape.py --files file1.md --resources-dir /custom/resources/dir

# Specify a custom config directory
python extract_and_scrape.py --files file1.md --config-dir /custom/config/dir
```

### How It Works

1. **URL Extraction**: The script analyzes each file to extract valid URLs.
   - Supports multiple file formats (markdown, text, HTML, JSON, PDF, code files)
   - Uses regex and BeautifulSoup to extract URLs from different contexts
   - PDF support requires additional libraries (PyPDF2 or pdfplumber)

2. **File Processing**: Input files are also processed for the RAG knowledge base.
   - Files are analyzed for relevance to architecture patterns
   - Only files that meet the relevance threshold are added

3. **URL Scraping**: Each extracted URL is scraped for content.
   - Content is downloaded, cleaned, and converted to markdown format
   - Relevance filtering ensures only architecture-related content is added

4. **RAG Integration**: Processed content is saved to the resources directory.
   - Ready to be indexed by the RAG system
   - Architecture patterns are automatically identified

## Enhanced Knowledge Base Builder

For more fine-grained control, you can use the enhanced knowledge base builder directly. See [ENHANCED_KB_GUIDE.md](ENHANCED_KB_GUIDE.md) for more details.

## Typical Workflow

A typical workflow for enhancing your RAG knowledge base:

1. Collect architecture-related documents in a directory
2. Run the URL extraction and scraping tool:
   ```bash
   python extract_and_scrape.py --directory /path/to/docs
   ```
3. Set up the RAG index with the newly added content:
   ```bash
   python src/setup.py --setup-rag
   ```
4. Test the enhanced RAG capabilities:
   ```bash
   python src/integrate_improvements.py --test-rag
   ```

## Best Practices

1. **Start with Quality Sources**: Use documentation with high-quality links to architecture resources
2. **Adjust Relevance Threshold**: Default (0.35) is balanced, but can be tuned:
   - Lower (0.2-0.3) to be more inclusive but less focused
   - Higher (0.5-0.7) to be more selective but might miss relevant content
3. **Check Extracted URLs**: Review the generated JSON file to see what URLs were found
4. **Incremental Enhancement**: Add small batches of content and test the RAG system after each addition
5. **PDF Processing**: For PDF support, install the required libraries:
   ```bash
   pip install PyPDF2 pdfplumber
   ```