#!/usr/bin/env python
"""
Enhanced Knowledge Base Builder for Domain-SC

This script provides advanced knowledge collection for multi-agent system architecture:
- Semantic relevance filtering
- Relationship preservation between documents
- Code example extraction and categorization
- Specialized agent architecture pattern recognition
- Resource discovery capabilities
"""

#######################
# CONFIGURATION VARIABLES - Edit these values as needed
#######################

# Relevance thresholds - lower value includes more content (range 0-1)
RELEVANCE_THRESHOLD = 0.35  # Min cosine similarity to be considered relevant

# Rate limiting (requests per second)
RATE_LIMIT = 1

# File type extensions to process
VALID_EXTENSIONS = ['.md', '.txt', '.html', '.pdf', '.doc', '.docx']

# User agent for requests
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"

#######################
# END CONFIGURATION VARIABLES
#######################

import os
import sys
import argparse
import logging
import json
import time
import re
import hashlib
import tempfile
import urllib.parse
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Tuple
from datetime import datetime
import concurrent.futures
import shutil
import networkx as nx
import numpy as np

import requests
from bs4 import BeautifulSoup, Tag
import markdown
from markdownify import markdownify
from urllib.parse import urljoin, urlparse

# If available, use sentence-transformers for semantic processing
try:
    from sentence_transformers import SentenceTransformer
    HAVE_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAVE_SENTENCE_TRANSFORMERS = False

# Add project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

try:
    from src.utils.logger import setup_logger
except ImportError:
    # Fallback logging setup if the import fails
    def setup_logger(name, log_file=None, level=logging.INFO):
        logger = logging.getLogger(name)
        logger.setLevel(level)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        return logger

# Set up logging
logger = setup_logger(__name__, "knowledge_base_builder.log")

# Directory settings
RESOURCES_DIR = os.path.join(project_root, "resources")
TEMP_DIR = os.path.join(project_root, "temp_downloads")
CONFIG_DIR = os.path.join(project_root, "kb_config")
RELATIONSHIP_DIR = os.path.join(project_root, "kb_relationships")
CODE_EXAMPLES_DIR = os.path.join(project_root, "kb_code_examples")

# Architecture patterns to identify
ARCHITECTURE_PATTERNS = {
    # Multi-agent system patterns
    "agent_communication": [
        "message passing", "agent communication", "message format", 
        "communication pattern", "message protocol", "agent messaging"
    ],
    "agent_coordination": [
        "coordination", "orchestration", "agent coordination", "consensus",
        "distributed decision", "coordination pattern", "centralized control"
    ],
    "agent_state_management": [
        "agent state", "state management", "shared state", "state synchronization",
        "state persistence", "state machine", "agent memory"
    ],
    "agent_task_allocation": [
        "task allocation", "workload distribution", "load balancing",
        "task assignment", "job scheduling", "work distribution"
    ],
    "agent_failure_handling": [
        "fault tolerance", "error recovery", "agent failure", "resilience",
        "recovery strategy", "failure detection", "fault handling"
    ],
    
    # General architecture patterns
    "layered_architecture": [
        "layered architecture", "n-tier", "multi-tier", "presentation layer",
        "business layer", "data layer", "separation of concerns"
    ],
    "microservices": [
        "microservice", "service-oriented", "api gateway", "service mesh",
        "domain-driven design", "bounded context", "service discovery"
    ],
    "event_driven": [
        "event-driven", "event sourcing", "message queue", "pub/sub",
        "event stream", "event bus", "message broker", "kafka"
    ],
    "serverless": [
        "serverless", "function as a service", "faas", "lambda",
        "azure functions", "cloud functions", "event triggers"
    ],
    
    # Design patterns
    "creational_patterns": [
        "factory pattern", "abstract factory", "builder pattern", "singleton",
        "prototype pattern", "dependency injection"
    ],
    "structural_patterns": [
        "adapter pattern", "bridge pattern", "composite pattern", "decorator pattern",
        "facade pattern", "flyweight pattern", "proxy pattern"
    ],
    "behavioral_patterns": [
        "observer pattern", "strategy pattern", "command pattern", "state pattern",
        "visitor pattern", "mediator pattern", "memento pattern", "iterator pattern"
    ],
    
    # Data patterns
    "data_storage": [
        "database pattern", "repository pattern", "data access", "orm",
        "nosql", "sharding", "replication", "partitioning", "data lake"
    ],
    "caching": [
        "cache pattern", "distributed cache", "cache invalidation", "cache aside",
        "read-through cache", "write-through cache", "cache eviction"
    ],
    
    # API patterns
    "api_design": [
        "api pattern", "rest", "graphql", "grpc", "api versioning",
        "api gateway", "api documentation", "openapi", "swagger"
    ],
    "api_security": [
        "authentication", "authorization", "oauth", "jwt", "api key",
        "rate limiting", "throttling", "cors"
    ],
    
    # Integration patterns
    "integration": [
        "integration pattern", "enterprise integration", "etl", "data integration",
        "service integration", "api integration", "webhook"
    ],
    
    # Security patterns
    "security": [
        "security pattern", "authorization", "authentication", "encryption",
        "secure design", "zero trust", "principle of least privilege"
    ],
    
    # Scalability patterns
    "scalability": [
        "scalability pattern", "horizontal scaling", "vertical scaling",
        "auto-scaling", "load balancing", "distributed system"
    ],
    
    # Performance patterns
    "performance": [
        "performance pattern", "optimization", "caching", "connection pooling",
        "lazy loading", "pagination", "throttling", "asynchronous processing"
    ]
}

# Comprehensive architecture reference text for relevance comparison
ARCHITECTURE_REFERENCE = """
Software architecture encompasses the high-level structures of a software system, the discipline of 
creating such structures, and the documentation of these structures. These structures are needed to 
reason about the software system. Each structure comprises software elements, relations among them, 
and properties of both elements and relations.

SOFTWARE ARCHITECTURE PATTERNS

1. Layered Architecture:
   - Organizes a system into layers with specific responsibilities
   - Enforces separation of concerns
   - Examples: OSI model, traditional web applications (presentation, business, data)

2. Microservices Architecture:
   - Structures an application as a collection of loosely coupled services
   - Enables independent deployment and scaling
   - Emphasizes domain-driven design and bounded contexts
   - Requires API gateways, service discovery, and distributed monitoring

3. Event-Driven Architecture:
   - Uses events to trigger and communicate between decoupled services
   - Supports asynchronous operations through message brokers
   - Patterns include event sourcing, CQRS, pub/sub

4. Serverless Architecture:
   - Focuses on functions triggered by events
   - Eliminates the need to manage infrastructure
   - Enables automatic scaling based on demand

5. Multi-Agent Systems:
   - Computational systems where multiple autonomous agents interact
   - Agents work together through communication, coordination, and sometimes competition
   - Characteristics: autonomy, local views, decentralization
   - Components: message passing, coordination mechanisms, task allocation
   - LLM implementations use specialized agents with different capabilities

6. Service-Oriented Architecture (SOA):
   - Organizes functionality as a collection of interoperable services
   - Uses service contracts and enterprise service bus
   - Focuses on business capabilities as services

7. Monolithic Architecture:
   - Single-tiered software application with all components combined
   - Simplifies deployment but can become complex over time

DESIGN PATTERNS

1. Creational Patterns:
   - Factory, Abstract Factory, Builder, Singleton, Prototype
   - Solve object creation problems and increase flexibility

2. Structural Patterns:
   - Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy
   - Handle relationships between entities and structure composition

3. Behavioral Patterns:
   - Observer, Strategy, Command, State, Visitor, Mediator
   - Define communication patterns between objects

DATA ARCHITECTURE PATTERNS

1. Data Storage:
   - Relational databases, NoSQL databases, data lakes
   - Patterns: repository, data mapper, active record
   - Strategies: sharding, replication, partitioning

2. Caching:
   - Cache-aside, read-through, write-through, write-behind
   - Distributed caching, invalidation strategies

API DESIGN PATTERNS

1. REST (Representational State Transfer):
   - Resource-based with CRUD operations
   - Stateless communication using HTTP verbs
   - Leverages HTTP status codes for responses

2. GraphQL:
   - Query language for APIs with client-specified data retrieval
   - Single endpoint with flexible data fetching

3. gRPC:
   - High-performance RPC framework using Protocol Buffers
   - Supports streaming and bidirectional communication

INTEGRATION PATTERNS

1. Enterprise Integration:
   - Message queues, service buses, API gateways
   - ETL processes, webhooks, adapters

SECURITY PATTERNS

1. Authentication/Authorization:
   - OAuth, JWT, SAML, OpenID Connect
   - RBAC, ABAC, principle of least privilege

2. Secure Design:
   - Zero trust architecture, defense in depth
   - Secure by design principles

SCALABILITY PATTERNS

1. Horizontal/Vertical Scaling:
   - Load balancing, auto-scaling, sharding
   - Stateless design, distributed caching

2. Performance Optimization:
   - Connection pooling, lazy loading, asynchronous processing
   - Caching, pagination, throttling

CLOUD ARCHITECTURE PATTERNS

1. Infrastructure as Code (IaC):
   - Declarative infrastructure definitions
   - Versioned and automated deployment

2. Containerization and Orchestration:
   - Docker containers, Kubernetes orchestration
   - Service mesh for enhanced network communication
"""

class EnhancedKnowledgeBaseBuilder:
    """Enhanced builder for the Domain-SC knowledge base with advanced features."""
    
    def __init__(self, resources_dir: str = RESOURCES_DIR, config_dir: str = CONFIG_DIR, 
                 temp_dir: str = TEMP_DIR, relationship_dir: str = RELATIONSHIP_DIR,
                 code_examples_dir: str = CODE_EXAMPLES_DIR):
        """Initialize the enhanced knowledge base builder.
        
        Args:
            resources_dir: Directory to save processed knowledge resources
            config_dir: Directory containing source configurations
            temp_dir: Directory for temporary downloads
            relationship_dir: Directory to store relationship data
            code_examples_dir: Directory to store extracted code examples
        """
        self.resources_dir = resources_dir
        self.config_dir = config_dir
        self.temp_dir = temp_dir
        self.relationship_dir = relationship_dir
        self.code_examples_dir = code_examples_dir
        
        # Create directories if they don't exist
        for directory in [resources_dir, config_dir, temp_dir, relationship_dir, code_examples_dir]:
            os.makedirs(directory, exist_ok=True)
        
        # Initialize semantic model if available
        self.semantic_model = None
        if HAVE_SENTENCE_TRANSFORMERS:
            try:
                self.semantic_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
                logger.info("Loaded sentence transformer model for semantic filtering")
            except Exception as e:
                logger.warning(f"Failed to load sentence transformer: {str(e)}")
        
        # Compute reference embedding for architecture knowledge
        self.reference_embedding = None
        if self.semantic_model:
            self.reference_embedding = self.semantic_model.encode(ARCHITECTURE_REFERENCE)
        
        # Initialize relationship graph
        self.relationship_graph = nx.DiGraph()
        
        # Track processed documents and their relevance scores
        self.processed_docs = []
        self.relevance_scores = {}
        self.failed_sources = []
        self.code_examples = {}
        
        # Load existing sources for tracking
        self.sources_file = os.path.join(config_dir, "processed_sources.json")
        self.sources = self._load_sources()
        
        # Load relationship graph if it exists
        self.graph_file = os.path.join(relationship_dir, "knowledge_graph.json")
        self._load_relationship_graph()

        # Load existing code examples if any
        self.code_examples_file = os.path.join(code_examples_dir, "code_examples.json")
        self._load_code_examples()
    
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
    
    def _load_relationship_graph(self):
        """Load the relationship graph from disk if it exists."""
        if os.path.exists(self.graph_file):
            try:
                with open(self.graph_file, 'r') as f:
                    graph_data = json.load(f)
                
                # Create graph from the JSON data
                self.relationship_graph = nx.node_link_graph(graph_data)
                logger.info(f"Loaded relationship graph with {len(self.relationship_graph.nodes)} nodes and {len(self.relationship_graph.edges)} edges")
            except Exception as e:
                logger.warning(f"Error loading relationship graph: {str(e)}")
                self.relationship_graph = nx.DiGraph()
    
    def _save_relationship_graph(self):
        """Save the relationship graph to disk."""
        try:
            # Convert graph to JSON-serializable format
            graph_data = nx.node_link_data(self.relationship_graph)
            
            with open(self.graph_file, 'w') as f:
                json.dump(graph_data, f, indent=2)
            
            logger.info(f"Saved relationship graph with {len(self.relationship_graph.nodes)} nodes and {len(self.relationship_graph.edges)} edges")
        except Exception as e:
            logger.error(f"Error saving relationship graph: {str(e)}")
    
    def _load_code_examples(self):
        """Load previously extracted code examples."""
        if os.path.exists(self.code_examples_file):
            try:
                with open(self.code_examples_file, 'r') as f:
                    self.code_examples = json.load(f)
                logger.info(f"Loaded {len(self.code_examples)} code examples")
            except Exception as e:
                logger.warning(f"Error loading code examples: {str(e)}")
                self.code_examples = {}
    
    def _save_code_examples(self):
        """Save extracted code examples."""
        try:
            with open(self.code_examples_file, 'w') as f:
                json.dump(self.code_examples, f, indent=2)
            logger.info(f"Saved {len(self.code_examples)} code examples")
        except Exception as e:
            logger.error(f"Error saving code examples: {str(e)}")
    
    def _source_already_processed(self, url: str) -> bool:
        """Check if a source has already been processed."""
        return url in [s.get("url") for s in self.sources.get("sources", [])]
    
    def _add_processed_source(self, url: str, title: str, doc_type: str, relevance_score: float = 0.0, status: str = "success"):
        """Add a source to the processed list."""
        source_info = {
            "url": url,
            "title": title,
            "type": doc_type,
            "relevance_score": relevance_score,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
        self.sources.setdefault("sources", []).append(source_info)
    
    def _calculate_relevance(self, text: str) -> float:
        """Calculate the relevance of text to multi-agent systems architecture."""
        if not self.semantic_model or self.reference_embedding is None:
            # If semantic model not available, use keyword-based scoring
            return self._keyword_relevance(text)
        
        try:
            # Get embedding for the text
            text_embedding = self.semantic_model.encode(text[:10000])  # Limit to first 10k chars
            
            # Calculate cosine similarity with reference
            similarity = np.dot(text_embedding, self.reference_embedding) / (
                np.linalg.norm(text_embedding) * np.linalg.norm(self.reference_embedding)
            )
            
            return float(similarity)
        except Exception as e:
            logger.warning(f"Error calculating semantic relevance: {str(e)}")
            return self._keyword_relevance(text)
    
    def _keyword_relevance(self, text: str) -> float:
        """Calculate relevance based on keyword presence when semantic model not available."""
        # List of keywords relevant to multi-agent architectures
        keywords = [
            "agent", "multi-agent", "autonomous agent", "agent communication", 
            "agent orchestration", "agent coordination", "distributed agents",
            "message passing", "agent state", "agent memory", "task allocation",
            "agent architecture", "agent pattern", "multi-agent system",
            "LLM agent", "agent workflow", "agent framework", "agent design pattern"
        ]
        
        # Count keyword occurrences
        text_lower = text.lower()
        count = sum(text_lower.count(kw.lower()) for kw in keywords)
        
        # Normalize by text length and keyword count
        text_length = max(len(text.split()), 1)  # Avoid division by zero
        normalized_score = min(count / (text_length * 0.01), 1.0)
        
        return normalized_score
    
    def _identify_architecture_patterns(self, text: str) -> Dict[str, List[str]]:
        """Identify architecture patterns in the text across multiple categories."""
        results = {}
        text_lower = text.lower()
        
        for pattern_type, pattern_keywords in ARCHITECTURE_PATTERNS.items():
            matches = []
            
            # Search for each keyword in the pattern type
            for keyword in pattern_keywords:
                if keyword.lower() in text_lower:
                    # Find the context around the keyword (sentence or paragraph)
                    try:
                        # Try to find a sentence containing the keyword
                        sentences = re.split(r'(?<=[.!?])\s+', text)
                        for sentence in sentences:
                            if keyword.lower() in sentence.lower():
                                matches.append(sentence.strip())
                    except Exception:
                        # If regex fails, just take the surrounding text
                        keyword_pos = text_lower.find(keyword.lower())
                        if keyword_pos >= 0:
                            start_pos = max(0, keyword_pos - 100)
                            end_pos = min(len(text), keyword_pos + len(keyword) + 100)
                            context = text[start_pos:end_pos].strip()
                            matches.append(context)
            
            if matches:
                # Deduplicate matches while preserving order
                unique_matches = []
                seen = set()
                for match in matches:
                    match_hash = hashlib.md5(match.encode()).hexdigest()
                    if match_hash not in seen:
                        seen.add(match_hash)
                        unique_matches.append(match)
                
                # Only keep the first 5 matches to avoid overwhelming
                results[pattern_type] = unique_matches[:5]
        
        return results
    
    def _extract_code_blocks(self, content: str, source: str) -> List[Dict[str, Any]]:
        """Extract code blocks from markdown or HTML content."""
        code_blocks = []
        
        # Extract markdown-style code blocks
        markdown_pattern = r'```(?P<language>\w*)\n(?P<code>.*?)\n```'
        for match in re.finditer(markdown_pattern, content, re.DOTALL):
            language = match.group('language') or 'unknown'
            code = match.group('code')
            
            # Analyze the code to determine what it demonstrates
            patterns = self._identify_architecture_patterns(code)
            
            code_blocks.append({
                'language': language,
                'code': code,
                'source': source,
                'patterns': patterns
            })
        
        # Extract HTML code blocks if BeautifulSoup is available
        try:
            soup = BeautifulSoup(content, 'html.parser')
            for pre in soup.find_all('pre'):
                code_tag = pre.find('code')
                if code_tag:
                    language = code_tag.get('class', ['unknown'])[0].replace('language-', '')
                    code = code_tag.text
                    
                    # Analyze the code
                    patterns = self._identify_architecture_patterns(code)
                    
                    code_blocks.append({
                        'language': language,
                        'code': code,
                        'source': source,
                        'patterns': patterns
                    })
        except Exception as e:
            logger.debug(f"Error parsing HTML code blocks: {str(e)}")
        
        return code_blocks
    
    def _add_to_relationship_graph(self, url: str, title: str, links: List[str], relevance: float):
        """Add a document and its relationships to the graph."""
        # Clean and normalize the URL
        url = url.strip()
        
        # Add the document node if it doesn't exist
        if url not in self.relationship_graph:
            self.relationship_graph.add_node(url, title=title, relevance=relevance, type="document")
        
        # Add edges for each outgoing link
        for link in links:
            link = link.strip()
            if link and link != url:  # Avoid self-links
                if link not in self.relationship_graph:
                    self.relationship_graph.add_node(link, title="", relevance=0.0, type="reference")
                
                # Add the edge from document to link
                self.relationship_graph.add_edge(url, link)
    
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
            
            # Process the contents
            if isinstance(contents, list):
                items = contents
            else:
                items = [contents]
                
            for item in items:
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
                    
                    # Add to relationship graph - all files in repo are related
                    repo_node = f"github.com/{owner}/{repo}"
                    self._add_to_relationship_graph(
                        url=repo_node,
                        title=f"{owner}/{repo} GitHub Repository",
                        links=[download_url],
                        relevance=0.8  # Assume GitHub repos in our list are relevant
                    )
                    
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
            
            # Extract all links before removing elements
            links = []
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                if href.startswith('#'):
                    continue
                
                # Convert to absolute URL
                abs_link = urljoin(url, href)
                links.append(abs_link)
            
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
            
            # Calculate relevance to multi-agent systems
            relevance = self._calculate_relevance(final_content)
            logger.info(f"Article relevance score: {relevance:.4f} for {url}")
            
            # Only process if it meets the relevance threshold
            if relevance >= RELEVANCE_THRESHOLD:
                # Extract code examples
                code_blocks = self._extract_code_blocks(final_content, url)
                if code_blocks:
                    for block in code_blocks:
                        block_id = hashlib.md5(block['code'].encode()).hexdigest()[:16]
                        self.code_examples[block_id] = block
                    logger.info(f"Extracted {len(code_blocks)} code blocks from {url}")
                
                # Add to relationship graph
                self._add_to_relationship_graph(
                    url=url,
                    title=title,
                    links=links,
                    relevance=relevance
                )
                
                # Identify architecture patterns
                patterns = self._identify_architecture_patterns(final_content)
                
                # Save the content
                output_path = os.path.join(self.temp_dir, filename)
                with open(output_path, 'w', encoding='utf-8') as f:
                    # Add pattern metadata to the top of the file
                    if patterns:
                        f.write(f"# {title}\n\nSource: {url}\n\n")
                        f.write("## Identified Architecture Patterns\n\n")
                        for pattern_type, examples in patterns.items():
                            f.write(f"### {pattern_type.replace('_', ' ').title()}\n\n")
                            for example in examples[:3]:  # Limit to 3 examples per pattern
                                f.write(f"- {example}\n")
                            f.write("\n")
                        f.write("\n---\n\n")
                        f.write(markdown_content)
                    else:
                        f.write(final_content)
                
                self._add_processed_source(url, title, "article", relevance)
                self.relevance_scores[output_path] = relevance
                return output_path
            else:
                logger.info(f"Skipping irrelevant article: {url} (score: {relevance:.4f})")
                self._add_processed_source(url, title, "article", relevance, status="skipped_irrelevant")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching article {url}: {str(e)}")
            self.failed_sources.append({"url": url, "error": str(e)})
            return None
    
    def process_documentation_site(self, base_url: str, include_paths: List[str] = None, 
                                  exclude_patterns: List[str] = None, depth: int = 2) -> List[str]:
        """Process a documentation website by crawling it with semantic filtering."""
        processed_urls = set()
        queue = [(base_url, 0)]  # (url, depth)
        downloaded_files = []
        link_structure = {}  # Keep track of page relationships
        
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
                
                # Extract links first
                soup = BeautifulSoup(response.text, 'html.parser')
                links = []
                
                for a_tag in soup.find_all('a', href=True):
                    link = a_tag['href']
                    
                    # Skip fragment links
                    if link.startswith('#'):
                        continue
                        
                    # Create absolute URL
                    absolute_url = urljoin(url, link)
                    
                    # Only consider links on the same domain
                    if urlparse(absolute_url).netloc == urlparse(base_url).netloc:
                        links.append(absolute_url)
                        
                        # Add to queue if not yet processed and within depth
                        if absolute_url not in processed_urls and current_depth < depth:
                            queue.append((absolute_url, current_depth + 1))
                
                # Store link structure
                link_structure[url] = links
                
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
                
                # Calculate relevance
                relevance = self._calculate_relevance(markdown_content)
                logger.info(f"Doc site page relevance score: {relevance:.4f} for {url}")
                
                # Only process if it meets the relevance threshold
                if relevance >= RELEVANCE_THRESHOLD:
                    # Extract code examples
                    code_blocks = self._extract_code_blocks(markdown_content, url)
                    if code_blocks:
                        for block in code_blocks:
                            block_id = hashlib.md5(block['code'].encode()).hexdigest()[:16]
                            self.code_examples[block_id] = block
                        logger.info(f"Extracted {len(code_blocks)} code blocks from {url}")
                    
                    # Identify architecture patterns
                    patterns = self._identify_architecture_patterns(markdown_content)
                    
                    # Add to relationship graph
                    self._add_to_relationship_graph(
                        url=url,
                        title=title,
                        links=links,
                        relevance=relevance
                    )
                    
                    # Add title and source
                    final_content = f"# {title}\n\nSource: {url}\n\n"
                    
                    # Add pattern metadata if found
                    if patterns:
                        final_content += "## Identified Architecture Patterns\n\n"
                        for pattern_type, examples in patterns.items():
                            final_content += f"### {pattern_type.replace('_', ' ').title()}\n\n"
                            for example in examples[:3]:  # Limit to 3 examples per pattern
                                final_content += f"- {example}\n"
                            final_content += "\n"
                        final_content += "\n---\n\n"
                    
                    final_content += markdown_content
                    
                    # Save the content
                    output_path = os.path.join(self.temp_dir, filename)
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(final_content)
                    
                    downloaded_files.append(output_path)
                    self.relevance_scores[output_path] = relevance
                    self._add_processed_source(url, title, "documentation", relevance)
                else:
                    logger.info(f"Skipping irrelevant documentation page: {url} (score: {relevance:.4f})")
                    self._add_processed_source(url, title, "documentation", relevance, status="skipped_irrelevant")
                
                # Respect rate limiting
                time.sleep(1/RATE_LIMIT)
                
            except Exception as e:
                logger.error(f"Error processing {url}: {str(e)}")
                self.failed_sources.append({"url": url, "error": str(e)})
        
        return downloaded_files
    
    def process_files(self, files: List[str]) -> int:
        """Process downloaded files into knowledge base format with semantic filtering."""
        processed_count = 0
        
        for file_path in files:
            try:
                # Skip if file doesn't exist
                if not os.path.exists(file_path):
                    logger.warning(f"File does not exist: {file_path}")
                    continue
                
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
                
                # Check relevance if we have content
                if content and file_path not in self.relevance_scores:
                    relevance = self._calculate_relevance(content)
                    self.relevance_scores[file_path] = relevance
                    logger.info(f"File relevance score: {relevance:.4f} for {file_path}")
                else:
                    # Use pre-calculated relevance if available
                    relevance = self.relevance_scores.get(file_path, 0.0)
                
                # Only process files that meet the relevance threshold
                if relevance >= RELEVANCE_THRESHOLD:
                    # Extract code examples
                    if content:
                        code_blocks = self._extract_code_blocks(content, file_path)
                        if code_blocks:
                            for block in code_blocks:
                                block_id = hashlib.md5(block['code'].encode()).hexdigest()[:16]
                                self.code_examples[block_id] = block
                            logger.info(f"Extracted {len(code_blocks)} code blocks from {file_path}")
                        
                        # Identify architecture patterns
                        patterns = self._identify_architecture_patterns(content)
                        
                        # Add pattern metadata if found
                        if patterns:
                            pattern_text = "## Identified Architecture Patterns\n\n"
                            for pattern_type, examples in patterns.items():
                                pattern_text += f"### {pattern_type.replace('_', ' ').title()}\n\n"
                                for example in examples[:3]:  # Limit to 3 examples per pattern
                                    pattern_text += f"- {example}\n"
                                pattern_text += "\n"
                            pattern_text += "\n---\n\n"
                            
                            # Find the right place to insert pattern metadata
                            lines = content.split('\n')
                            title_line = -1
                            for i, line in enumerate(lines):
                                if line.startswith('# '):
                                    title_line = i
                                    break
                            
                            if title_line >= 0 and title_line + 1 < len(lines):
                                # Insert after title and first few lines
                                insert_at = min(title_line + 5, len(lines))
                                content = '\n'.join(lines[:insert_at]) + '\n\n' + pattern_text + '\n'.join(lines[insert_at:])
                    
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
                else:
                    logger.info(f"Skipping irrelevant file: {file_path} (score: {relevance:.4f})")
                    
            except Exception as e:
                logger.error(f"Error processing file {file_path}: {str(e)}")
        
        return processed_count
    
    def discover_related_resources(self, seed_urls: List[str], max_discoveries: int = 10) -> List[Dict[str, Any]]:
        """Discover additional resources related to multi-agent systems.
        This is an advanced feature that tries to find new resources not in the initial configuration.
        """
        discovered = []
        
        # Implementation uses a simple approach:
        # 1. Visit each seed URL
        # 2. Extract outgoing links that seem relevant (based on text around the link)
        # 3. Visit those links and assess their relevance
        
        for seed_url in seed_urls[:5]:  # Limit to first 5 seeds to avoid too much crawling
            try:
                headers = {"User-Agent": USER_AGENT}
                response = requests.get(seed_url, headers=headers, timeout=30)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find links with promising anchor text
                for a_tag in soup.find_all('a', href=True):
                    if len(discovered) >= max_discoveries:
                        break
                        
                    link_text = a_tag.get_text().strip().lower()
                    href = a_tag['href']
                    
                    # Skip non-http links and fragments
                    if not href.startswith(('http://', 'https://')) or href.startswith('#'):
                        continue
                    
                    # Check if the link text suggests relevance to multi-agent systems
                    if any(term in link_text for term in ['agent', 'multi-agent', 'architecture', 'pattern']):
                        # Only process each URL once
                        if href not in [d['url'] for d in discovered] and not self._source_already_processed(href):
                            # Visit the link to check its relevance
                            try:
                                link_response = requests.get(href, headers=headers, timeout=10)
                                if link_response.status_code == 200:
                                    link_soup = BeautifulSoup(link_response.text, 'html.parser')
                                    link_title = link_soup.find('title')
                                    title_text = link_title.get_text() if link_title else href
                                    
                                    # Get main content
                                    main_content = None
                                    for selector in ['main', 'article', '.content']:
                                        main_content = link_soup.select_one(selector)
                                        if main_content:
                                            break
                                    
                                    if not main_content:
                                        main_content = link_soup.find('body')
                                    
                                    # Convert to text and calculate relevance
                                    if main_content:
                                        main_text = main_content.get_text()
                                        relevance = self._calculate_relevance(main_text)
                                        
                                        if relevance >= RELEVANCE_THRESHOLD:
                                            discovered.append({
                                                'url': href,
                                                'title': title_text,
                                                'relevance': relevance,
                                                'source': seed_url
                                            })
                                            logger.info(f"Discovered relevant resource: {href} (score: {relevance:.4f})")
                            except Exception as e:
                                logger.debug(f"Error checking discovered link {href}: {str(e)}")
                            
                            # Respect rate limiting
                            time.sleep(1/RATE_LIMIT)
                
            except Exception as e:
                logger.error(f"Error during resource discovery from {seed_url}: {str(e)}")
        
        return discovered
    
    def generate_knowledge_report(self) -> Dict[str, Any]:
        """Generate a report about the knowledge base."""
        total_docs = len([f for f in os.listdir(self.resources_dir) if os.path.isfile(os.path.join(self.resources_dir, f))])
        code_examples_count = len(self.code_examples)
        
        # Count documents by pattern type
        pattern_counts = {}
        for pattern_type in ARCHITECTURE_PATTERNS.keys():
            pattern_counts[pattern_type] = 0
        
        # Analyze the relationship graph
        graph_stats = {
            "total_nodes": len(self.relationship_graph.nodes),
            "total_edges": len(self.relationship_graph.edges),
            "highest_relevance_nodes": [],
            "most_connected_nodes": []
        }
        
        # Find nodes with highest relevance
        if self.relationship_graph.nodes:
            nodes_by_relevance = sorted(
                self.relationship_graph.nodes(data=True),
                key=lambda x: x[1].get('relevance', 0),
                reverse=True
            )
            graph_stats["highest_relevance_nodes"] = [
                {"url": node[0], "title": node[1].get('title', ''), "relevance": node[1].get('relevance', 0)}
                for node in nodes_by_relevance[:5]  # Top 5
            ]
            
            # Find most connected nodes
            nodes_by_connections = sorted(
                self.relationship_graph.nodes,
                key=lambda x: len(list(self.relationship_graph.neighbors(x))),
                reverse=True
            )
            graph_stats["most_connected_nodes"] = [
                {"url": node, "title": self.relationship_graph.nodes[node].get('title', ''), 
                 "connections": len(list(self.relationship_graph.neighbors(node)))}
                for node in nodes_by_connections[:5]  # Top 5
            ]
        
        # Count code examples by pattern
        code_examples_by_pattern = {}
        for pattern_type in ARCHITECTURE_PATTERNS.keys():
            code_examples_by_pattern[pattern_type] = 0
        
        for example in self.code_examples.values():
            for pattern_type in example.get('patterns', {}):
                if pattern_type in code_examples_by_pattern:
                    code_examples_by_pattern[pattern_type] += 1
        
        report = {
            "total_documents": total_docs,
            "code_examples": code_examples_count,
            "code_examples_by_pattern": code_examples_by_pattern,
            "pattern_coverage": pattern_counts,
            "relationship_graph": graph_stats,
            "failed_sources": len(self.failed_sources),
            "generated_at": datetime.now().isoformat()
        }
        
        # Save the report
        report_path = os.path.join(self.config_dir, "knowledge_report.json")
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def build_knowledge_base(self, github_repos: List[Dict] = None, articles: List[str] = None, 
                           docs_sites: List[Dict] = None, local_docs: List[str] = None,
                           discover_resources: bool = False, max_discoveries: int = 10) -> Dict[str, Any]:
        """Build the knowledge base from multiple sources with semantic filtering."""
        all_files = []
        results = {
            "github_repos": 0,
            "articles": 0,
            "docs_sites": 0,
            "local_docs": 0,
            "discovered_resources": 0,
            "processed_files": 0,
            "failed_sources": 0,
            "code_examples": 0
        }
        
        # Discovered resources
        discovered_resources = []
        
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
            seed_urls = []  # Collect URLs for resource discovery
            
            for article_url in articles:
                if self._source_already_processed(article_url):
                    logger.info(f"Skipping already processed article: {article_url}")
                    continue
                    
                file_path = self.fetch_web_article(article_url)
                if file_path:
                    all_files.append(file_path)
                    seed_urls.append(article_url)
                    results["articles"] += 1
            
            # If resource discovery is enabled, find more relevant resources
            if discover_resources and seed_urls:
                logger.info(f"Discovering additional resources from {len(seed_urls)} seed URLs...")
                discovered_resources = self.discover_related_resources(seed_urls, max_discoveries)
                
                # Process discovered resources
                for resource in discovered_resources:
                    file_path = self.fetch_web_article(resource['url'])
                    if file_path:
                        all_files.append(file_path)
                        results["discovered_resources"] += 1
        
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
        results["code_examples"] = len(self.code_examples)
        
        # Save relationships
        self._save_relationship_graph()
        
        # Save code examples
        self._save_code_examples()
        
        # Save the sources file
        self._save_sources()
        
        # Generate knowledge report
        knowledge_report = self.generate_knowledge_report()
        results["knowledge_report"] = knowledge_report
        
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
                "url": "https://github.com/microsoft/autogen",
                "branch": "main",
                "subdirectory": "docs",
                "patterns": [".md$"]
            }
        ],
        "articles": [
            "https://martinfowler.com/articles/microservices.html",
            "https://12factor.net/",
            "https://en.wikipedia.org/wiki/Multi-agent_system"
        ],
        "docs_sites": [
            {
                "url": "https://learn.microsoft.com/en-us/azure/architecture/patterns/",
                "include_paths": ["/azure/architecture/patterns/"],
                "depth": 1
            },
            {
                "url": "https://python.langchain.com/docs/modules/agents/",
                "depth": 2
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
    parser = argparse.ArgumentParser(description="Enhanced Knowledge Base Builder for Domain-SC")
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
        "--relationship-dir",
        default=RELATIONSHIP_DIR,
        help="Directory to store relationship data"
    )
    parser.add_argument(
        "--code-examples-dir",
        default=CODE_EXAMPLES_DIR,
        help="Directory to store extracted code examples"
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
        "--discover-resources",
        action="store_true",
        help="Discover additional resources from seed URLs"
    )
    parser.add_argument(
        "--max-discoveries",
        type=int,
        default=10,
        help="Maximum number of resources to discover (default: 10)"
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
    parser.add_argument(
        "--relevance-threshold",
        type=float,
        default=0.45,  # Lowered threshold to include more resources
        help=f"Minimum relevance score threshold (default: 0.45)"
    )
    parser.add_argument(
        "--skip-rag-setup",
        action="store_true",
        help="Skip running the RAG setup after building the knowledge base"
    )
    
    args = parser.parse_args()
    
    # Update relevance threshold if specified
    RELEVANCE_THRESHOLD = args.relevance_threshold
    
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
    builder = EnhancedKnowledgeBaseBuilder(
        resources_dir=args.resources_dir,
        config_dir=os.path.dirname(args.config),
        temp_dir=args.temp_dir,
        relationship_dir=args.relationship_dir,
        code_examples_dir=args.code_examples_dir
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
        local_docs=local_docs,
        discover_resources=args.discover_resources,
        max_discoveries=args.max_discoveries
    )
    
    # Print summary
    print("\nEnhanced Knowledge Base Building Summary:")
    print(f"GitHub Repositories: {results['github_repos']}")
    print(f"Web Articles: {results['articles']}")
    print(f"Documentation Sites: {results['docs_sites']}")
    print(f"Local Document Directories: {results['local_docs']}")
    print(f"Discovered Resources: {results['discovered_resources']}")
    print(f"Total Files Processed: {results['processed_files']}")
    print(f"Code Examples Extracted: {results['code_examples']}")
    print(f"Failed Sources: {results['failed_sources']}")
    print(f"\nResources saved to: {args.resources_dir}")
    print(f"Relationship data saved to: {args.relationship_dir}")
    print(f"Code examples saved to: {args.code_examples_dir}")
    
    # Run the RAG index setup if not skipped
    if not args.skip_rag_setup:
        print("\nSetting up RAG index with the new knowledge base...")
        setup_cmd = f"python src/setup.py --setup-rag --resource-dir {args.resources_dir}"
        os.system(setup_cmd)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())