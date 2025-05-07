import os
import logging
from typing import List, Dict, Any, Optional
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

logger = logging.getLogger(__name__)

class VectorStoreManager:
    """Manages vector database operations for RAG."""
    
    def __init__(self, 
                 db_directory: str,
                 embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.db_directory = db_directory
        self.embedding_model = embedding_model
        
        # Create directory if it doesn't exist
        os.makedirs(self.db_directory, exist_ok=True)
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model,
            model_kwargs={"device": "cpu"}
        )
        
        # Initialize DB if exists, otherwise it will be created when documents are added
        if os.path.exists(os.path.join(db_directory, "chroma.sqlite3")):
            self.db = Chroma(persist_directory=db_directory, embedding_function=self.embeddings)
        else:
            self.db = None
    
    def add_documents(self, documents: List[Dict[str, Any]], collection_name: Optional[str] = None) -> None:
        """Add documents to the vector store."""
        try:
            # Instantiate a new DB if not exists
            if self.db is None:
                self.db = Chroma.from_documents(
                    documents=documents,
                    embedding=self.embeddings,
                    persist_directory=self.db_directory,
                    collection_name=collection_name
                )
                self.db.persist()
            else:
                # Add to existing DB
                self.db.add_documents(documents)
                self.db.persist()
                
            logger.info(f"Added {len(documents)} documents to vector store")
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {str(e)}")
    
    def similar_documents(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve similar documents to a query."""
        if self.db is None:
            logger.warning("Vector store not initialized. No documents to search.")
            return []
        
        try:
            results = self.db.similarity_search_with_score(query, k=k)
            return [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": score
                } for doc, score in results
            ]
        except Exception as e:
            logger.error(f"Error retrieving similar documents: {str(e)}")
            return []
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store collection."""
        if self.db is None:
            return {"status": "not_initialized", "count": 0}
        
        try:
            count = self.db._collection.count()
            return {
                "status": "active",
                "count": count,
                "embedding_model": self.embedding_model,
                "location": self.db_directory
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {str(e)}")
            return {"status": "error", "message": str(e)}
            
    def clear(self) -> None:
        """Clear all documents from the vector store."""
        if self.db is not None:
            try:
                self.db._collection.delete()
                self.db = None
                logger.info("Vector store cleared successfully")
            except Exception as e:
                logger.error(f"Error clearing vector store: {str(e)}")
