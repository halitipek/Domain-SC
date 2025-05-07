#!/usr/bin/env python
"""
Knowledge Base Builder for Domain-SC

This script downloads, processes, and prepares architectural documentation for the RAG system.
It collects content from various sources including GitHub repositories, official documentation,
and engineering blogs.
"""

import os
import sys
import argparse
import logging
import json
import time
import re
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import concurrent.futures
import shutil

import requests
from bs4 import BeautifulSoup
import markdown
from markdownify import markdownify
from urllib.parse import urljoin, urlparse

# Add project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

from src.utils.logger import setup_logger

# Set up logging
logger = setup_logger(__name__, "knowledge_base_builder.log")

# Directory settings
RESOURCES_DIR = os.path.join(project_root, "resources")
TEMP_DIR = os.path.join(project_root, "temp_downloads")
CONFIG_DIR = os.path.join(project_root, "kb_config")

# User agent for requests
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"

# Rate limiting (requests per second)
RATE_LIMIT = 1

# File type extensions to process
VALID_EXTENSIONS = ['.md', '.txt', '.html', '.pdf', '.doc', '.docx']


class KnowledgeBaseBuilder:
    """Builder for the Domain-SC knowledge base."""
    
    def __init__(self, resources_dir: str = RESOURCES_DIR, config_dir: str = CONFIG_DIR, temp_dir: str = TEMP_DIR):
        """Initialize the knowledge base builder.
        
        Args:
            resources_dir: Directory to save processed knowledge resources
            config_dir: Directory containing source configurations
            temp_dir: Directory for temporary downloads
        """
        self.resources_dir = resources_dir
        self.config_dir = config_dir
        self.temp_dir = temp_dir
        
        # Create directories if they don't exist
        os.makedirs(resources_dir, exist_ok=True)
        os.makedirs(config_dir, exist_ok=True)
        os.makedirs(temp_dir, exist_ok=True)
        
        # Keep track of processed documents
        self.processed_docs = []
        self.failed_sources = []
        
        # Load existing sources for tracking
        self.sources_file = os.path.join(config_dir, "processed_sources.json")
        self.sources = self._load_sources()
        
    def _load_sources(self) -> Dict[str, Any]:
        """Load previously processed sources."""
        if os.path.exists(self.sources_file):
            try:
                with open(self.sources_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logger.warning(f"Error loading sources file {self.sources_file}, creating new one")
                return {"sources": [], "last_update": ""}
        return {"sources": [], "last_update": ""}
    
    def _save_sources(self):
        """Save processed sources for future reference."""
        self.sources["last_update"] = datetime.now().isoformat()
        with open(self.sources_file, 'w') as f:
            json.dump(self.sources, f, indent=2)
    
    def _source_already_processed(self, url: str) -> bool:
        """Check if a source has already been processed."""
        return url in [s.get("url") for s in self.sources.get("sources", [])]
    
    def _add_processed_source(self, url: str, title: str, doc_type: str, status: str = "success"):
        """Add a source to the processed list."""
        source_info = {
            "url": url,
            "title": title,
            "type": doc_type,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
        self.sources.setdefault("sources", []).append(source_info)
        
    def download_file(self, url: str, output_path: str) -> bool:
        """Download a file from a URL."""
        try:
            headers = {"User-Agent": USER_AGENT}
            response = requests.get(url, headers=headers, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(output_path, 'wb') as out_file:
                for chunk in response.iter_content(chunk_size=8192):
                    out_file.write(chunk)
            return True
        except Exception as e:
            logger.error(f"Error downloading {url}: {str(e)}")
            return False
    
    def fetch_github_repo(self, repo_url: str, branch: str = "main", 
                         subdirectory: str = None, patterns: List[str] = None) -> List[str]:
        """Fetch documentation files from a GitHub repository."""
        if not repo_url.endswith("/"):
            repo_url += "/"
        
        # Extract owner and repo name
        match = re.match(r"https://github\.com/([^/]+)/([^/]+)", repo_url)
        if not match:
            logger.error(f"Invalid GitHub URL: {repo_url}")
            return []
            
        owner, repo = match.groups()
        
        # Construct API URL
        api_base = f"https://api.github.com/repos/{owner}/{repo}/contents"
        if subdirectory:
            api_base += f"/{subdirectory}"
        
        # Set up parameters
        params = {"ref": branch}
        
        # Make the request
        headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/vnd.github.v3+json"
        }
        
        # Check if GitHub token is available for higher rate limits
        github_token = os.environ.get("GITHUB_TOKEN")
        if github_token:
            headers["Authorization"] = f"token {github_token}"
        
        try:
            response = requests.get(api_base, headers=headers, params=params)
            response.raise_for_status()
            contents = response.json()
            
            downloaded_files = []
            
            # Create a directory for this repo
            repo_dir = os.path.join(self.temp_dir, f"{owner}_{repo}")
            os.makedirs(repo_dir, exist_ok=True)
            
            for item in contents:
                # Only process files, not directories
                if item["type"] != "file":
                    continue
                    
                # Check if file matches patterns
                name = item["name"]
                _, ext = os.path.splitext(name)
                
                if ext.lower() not in VALID_EXTENSIONS:
                    continue
                    
                if patterns and not any(re.search(pattern, name, re.IGNORECASE) for pattern in patterns):
                    continue
                
                # Download the file
                download_url = item["download_url"]
                output_path = os.path.join(repo_dir, name)
                
                if self.download_file(download_url, output_path):
                    downloaded_files.append(output_path)
                    logger.info(f"Downloaded {name} from {repo_url}")
                
                # Respect rate limiting
                time.sleep(1/RATE_LIMIT)
            
            return downloaded_files
            
        except Exception as e:
            logger.error(f"Error fetching GitHub repo {repo_url}: {str(e)}")
            self.failed_sources.append({"url": repo_url, "error": str(e)})
            return []
    
    def fetch_web_article(self, url: str) -> Optional[str]:
        """Fetch an article from a website and convert to markdown."""
        try:
            headers = {"User-Agent": USER_AGENT}
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted elements
            for element in soup.select('nav, header, footer, aside, script, style, [role="navigation"]'):
                element.decompose()
            
            # Extract the title
            title_tag = soup.find('title')
            title = title_tag.text if title_tag else "Untitled"
            
            # Find the main content
            main_content = None
            for selector in ['main', 'article', '.post-content', '.article-content', '.content']:
                main_content = soup.select_one(selector)
                if main_content:
                    break
            
            if not main_content:
                main_content = soup.find('body')
            
            # Convert HTML to markdown
            markdown_content = markdownify(str(main_content))
            
            # Create a clean title for the filename
            clean_title = re.sub(r'[^\w\s-]', '', title).strip().lower()
            clean_title = re.sub(r'[-\s]+', '-', clean_title)
            
            # Create a unique filename
            url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
            filename = f"{clean_title}-{url_hash}.md"
            
            # Add title and source to the markdown content
            final_content = f"# {title}\n\nSource: {url}\n\n{markdown_content}"
            
            # Save the content
            output_path = os.path.join(self.temp_dir, filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(final_content)
            
            self._add_processed_source(url, title, "article")
            return output_path
            
        except Exception as e:
            logger.error(f"Error fetching article {url}: {str(e)}")
            self.failed_sources.append({"url": url, "error": str(e)})
            return None
    
    def process_documentation_site(self, base_url: str, include_paths: List[str] = None, 
                                  exclude_patterns: List[str] = None, depth: int = 2) -> List[str]:
        """Process a documentation website by crawling it."""
        processed_urls = set()
        queue = [(base_url, 0)]  # (url, depth)
        downloaded_files = []
        
        while queue:
            url, current_depth = queue.pop(0)
            
            # Skip if already processed
            if url in processed_urls:
                continue
                
            processed_urls.add(url)
            
            # Skip if exceeds depth
            if current_depth > depth:
                continue
                
            # Skip if URL matches exclude patterns
            if exclude_patterns and any(re.search(pattern, url) for pattern in exclude_patterns):
                continue
                
            # Skip if include_paths specified and URL doesn't match any of them
            if include_paths and not any(path in url for path in include_paths):
                continue
            
            try:
                logger.info(f"Processing {url}")
                headers = {"User-Agent": USER_AGENT}
                response = requests.get(url, headers=headers, timeout=30)
                response.raise_for_status()
                
                # Save the page content
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract title
                title_tag = soup.find('title')
                title = title_tag.text if title_tag else "Untitled"
                
                # Create a filename
                parsed_url = urlparse(url)
                path_parts = parsed_url.path.strip('/').split('/')
                filename = '-'.join(path_parts) if path_parts and path_parts[0] else parsed_url.netloc
                url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
                filename = f"{filename}-{url_hash}.md"
                
                # Find the main content
                main_content = None
                for selector in ['main', 'article', '.documentation', '.docs-content', '.content']:
                    main_content = soup.select_one(selector)
                    if main_content:
                        break
                
                if not main_content:
                    main_content = soup.find('body')
                
                # Convert to markdown
                markdown_content = markdownify(str(main_content))
                
                # Add title and source
                final_content = f"# {title}\n\nSource: {url}\n\n{markdown_content}"
                
                # Save the content
                output_path = os.path.join(self.temp_dir, filename)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(final_content)
                
                downloaded_files.append(output_path)
                self._add_processed_source(url, title, "documentation")
                
                # Find links on the page
                if current_depth < depth:
                    for a_tag in soup.find_all('a', href=True):
                        link = a_tag['href']
                        
                        # Skip fragment links
                        if link.startswith('#'):
                            continue
                            
                        # Create absolute URL
                        absolute_url = urljoin(url, link)
                        
                        # Only follow links on the same domain
                        if urlparse(absolute_url).netloc == urlparse(base_url).netloc:
                            queue.append((absolute_url, current_depth + 1))
                
                # Respect rate limiting
                time.sleep(1/RATE_LIMIT)
                
            except Exception as e:
                logger.error(f"Error processing {url}: {str(e)}")
                self.failed_sources.append({"url": url, "error": str(e)})
        
        return downloaded_files
    
    def process_files(self, files: List[str]) -> int:
        """Process downloaded files into knowledge base format."""
        processed_count = 0
        
        for file_path in files:
            try:
                # Get file extension
                _, ext = os.path.splitext(file_path)
                
                # Get output filename
                filename = os.path.basename(file_path)
                
                # If not markdown, convert to markdown
                if ext.lower() != '.md':
                    # Handle different formats
                    if ext.lower() in ['.html', '.htm']:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            html_content = f.read()
                        content = markdownify(html_content)
                        
                        # Create a new filename
                        filename = os.path.splitext(filename)[0] + '.md'
                    else:
                        # Just copy the file for now
                        logger.warning(f"Unsupported file format for conversion: {ext}")
                        content = None
                else:
                    # Already markdown, just read it
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                
                # Write processed content if available
                if content:
                    output_path = os.path.join(self.resources_dir, filename)
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    processed_count += 1
                    logger.info(f"Processed {filename}")
                else:
                    # Just copy the file
                    output_path = os.path.join(self.resources_dir, filename)
                    shutil.copy(file_path, output_path)
                    processed_count += 1
                    logger.info(f"Copied {filename}")
                    
            except Exception as e:
                logger.error(f"Error processing file {file_path}: {str(e)}")
        
        return processed_count
    
    def build_knowledge_base(self, github_repos: List[Dict] = None, articles: List[str] = None, 
                           docs_sites: List[Dict] = None, local_docs: List[str] = None) -> Dict[str, Any]:
        """Build the knowledge base from multiple sources."""
        all_files = []
        results = {
            "github_repos": 0,
            "articles": 0,
            "docs_sites": 0,
            "local_docs": 0,
            "processed_files": 0,
            "failed_sources": 0
        }
        
        # Process GitHub repositories
        if github_repos:
            logger.info(f"Processing {len(github_repos)} GitHub repositories...")
            for repo_config in github_repos:
                repo_url = repo_config.get("url")
                branch = repo_config.get("branch", "main")
                subdirectory = repo_config.get("subdirectory")
                patterns = repo_config.get("patterns")
                
                if self._source_already_processed(repo_url):
                    logger.info(f"Skipping already processed repo: {repo_url}")
                    continue
                
                files = self.fetch_github_repo(repo_url, branch, subdirectory, patterns)
                all_files.extend(files)
                results["github_repos"] += 1
        
        # Process web articles
        if articles:
            logger.info(f"Processing {len(articles)} web articles...")
            for article_url in articles:
                if self._source_already_processed(article_url):
                    logger.info(f"Skipping already processed article: {article_url}")
                    continue
                    
                file_path = self.fetch_web_article(article_url)
                if file_path:
                    all_files.append(file_path)
                    results["articles"] += 1
        
        # Process documentation sites
        if docs_sites:
            logger.info(f"Processing {len(docs_sites)} documentation sites...")
            for site_config in docs_sites:
                base_url = site_config.get("url")
                include_paths = site_config.get("include_paths")
                exclude_patterns = site_config.get("exclude_patterns")
                depth = site_config.get("depth", 2)
                
                if self._source_already_processed(base_url):
                    logger.info(f"Skipping already processed documentation site: {base_url}")
                    continue
                
                files = self.process_documentation_site(base_url, include_paths, exclude_patterns, depth)
                all_files.extend(files)
                results["docs_sites"] += 1
        
        # Process local document directories
        if local_docs:
            logger.info(f"Processing {len(local_docs)} local document directories...")
            for doc_dir in local_docs:
                if not os.path.exists(doc_dir):
                    logger.warning(f"Local document directory does not exist: {doc_dir}")
                    continue
                    
                # Get all files with valid extensions
                for root, _, files in os.walk(doc_dir):
                    for filename in files:
                        _, ext = os.path.splitext(filename)
                        if ext.lower() in VALID_EXTENSIONS:
                            file_path = os.path.join(root, filename)
                            all_files.append(file_path)
                            
                results["local_docs"] += 1
        
        # Process all the collected files
        results["processed_files"] = self.process_files(all_files)
        results["failed_sources"] = len(self.failed_sources)
        
        # Save the sources file
        self._save_sources()
        
        logger.info(f"Knowledge base building complete. Processed {results['processed_files']} files.")
        return results

def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from a JSON file."""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading config from {config_path}: {str(e)}")
        return {}

def create_default_config(config_path: str):
    """Create a default configuration file if none exists."""
    default_config = {
        "github_repos": [
            {
                "url": "https://github.com/donnemartin/system-design-primer",
                "branch": "master",
                "patterns": [".md$"]
            },
            {
                "url": "https://github.com/kamranahmedse/design-patterns-for-humans",
                "branch": "master",
                "patterns": [".md$"]
            },
            {
                "url": "https://github.com/brendangregg/FlameGraph",
                "branch": "master",
                "subdirectory": "docs",
                "patterns": [".md$"]
            }
        ],
        "articles": [
            "https://martinfowler.com/articles/microservices.html",
            "https://docs.microsoft.com/en-us/azure/architecture/patterns/",
            "https://12factor.net/",
            "https://samnewman.io/patterns/architectural/bff/",
            "https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/"
        ],
        "docs_sites": [
            {
                "url": "https://docs.microsoft.com/en-us/azure/architecture/patterns/",
                "include_paths": ["/azure/architecture/patterns/"],
                "depth": 1
            },
            {
                "url": "https://www.patterns.dev/posts",
                "depth": 1
            }
        ],
        "local_docs": []
    }
    
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w') as f:
        json.dump(default_config, f, indent=2)
    
    logger.info(f"Created default configuration file at {config_path}")
    return default_config

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Build knowledge base for Domain-SC")
    parser.add_argument(
        "--config", "-c",
        default=os.path.join(CONFIG_DIR, "kb_sources.json"),
        help="Path to configuration file"
    )
    parser.add_argument(
        "--resources-dir", "-r",
        default=RESOURCES_DIR,
        help="Directory to save processed resources"
    )
    parser.add_argument(
        "--temp-dir", "-t",
        default=TEMP_DIR,
        help="Directory for temporary downloads"
    )
    parser.add_argument(
        "--github-only", 
        action="store_true",
        help="Only process GitHub repositories"
    )
    parser.add_argument(
        "--articles-only", 
        action="store_true",
        help="Only process web articles"
    )
    parser.add_argument(
        "--docs-only", 
        action="store_true",
        help="Only process documentation sites"
    )
    parser.add_argument(
        "--local-only", 
        action="store_true",
        help="Only process local documents"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean temporary directory before processing"
    )
    parser.add_argument(
        "--force-refresh",
        action="store_true",
        help="Force refresh of all sources, even if already processed"
    )
    
    args = parser.parse_args()
    
    # Check if config file exists, create default if not
    if not os.path.exists(args.config):
        config = create_default_config(args.config)
    else:
        config = load_config(args.config)
    
    # Clean temp directory if requested
    if args.clean and os.path.exists(args.temp_dir):
        shutil.rmtree(args.temp_dir)
        os.makedirs(args.temp_dir, exist_ok=True)
        logger.info(f"Cleaned temporary directory: {args.temp_dir}")
    
    # Initialize builder
    builder = KnowledgeBaseBuilder(
        resources_dir=args.resources_dir,
        config_dir=os.path.dirname(args.config),
        temp_dir=args.temp_dir
    )
    
    # If force refresh, clear the sources tracking
    if args.force_refresh:
        builder.sources = {"sources": [], "last_update": ""}
        logger.info("Forcing refresh of all sources")
    
    # Filter sources based on arguments
    github_repos = config.get("github_repos", []) if not args.articles_only and not args.docs_only and not args.local_only else []
    articles = config.get("articles", []) if not args.github_only and not args.docs_only and not args.local_only else []
    docs_sites = config.get("docs_sites", []) if not args.github_only and not args.articles_only and not args.local_only else []
    local_docs = config.get("local_docs", []) if not args.github_only and not args.articles_only and not args.docs_only else []
    
    # Build knowledge base
    results = builder.build_knowledge_base(
        github_repos=github_repos,
        articles=articles,
        docs_sites=docs_sites,
        local_docs=local_docs
    )
    
    # Print summary
    print("\nKnowledge Base Building Summary:")
    print(f"GitHub Repositories: {results['github_repos']}")
    print(f"Web Articles: {results['articles']}")
    print(f"Documentation Sites: {results['docs_sites']}")
    print(f"Local Document Directories: {results['local_docs']}")
    print(f"Total Files Processed: {results['processed_files']}")
    print(f"Failed Sources: {results['failed_sources']}")
    print(f"\nResources saved to: {args.resources_dir}")
    
    # Run the RAG index setup
    print("\nSetting up RAG index with the new knowledge base...")
    setup_cmd = f"python src/setup.py --setup-rag --resource-dir {args.resources_dir}"
    os.system(setup_cmd)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())