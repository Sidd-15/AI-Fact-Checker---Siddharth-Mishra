
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple
import pickle

class VectorDB:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.facts = []
    
    def create_index(self, facts: List[str]):
        """Create FAISS index from facts"""
        self.facts = facts
        embeddings = self.model.encode(facts, convert_to_numpy=True)
        
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings.astype('float32'))
    
    def retrieve(self, query: str, k: int = 3) -> List[Tuple[str, float]]:
        """Retrieve top-k similar facts"""
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_embedding.astype('float32'), k)
        
        results = [(self.facts[idx], float(distances[0][i])) 
                   for i, idx in enumerate(indices[0]) if idx < len(self.facts)]
        return results
    
    def get_confidence_score(self, query: str, k: int = 3) -> float:
        """Calculate confidence score based on retrieval similarity"""
        results = self.retrieve(query, k)
        if not results:
            return 0.0
        avg_distance = sum(dist for _, dist in results) / len(results)
        # Convert distance to similarity score (0-1)
        confidence = max(0, 1 - (avg_distance / 10))
        return confidence
    
    def save(self, path: str):
        """Save index and facts"""
        faiss.write_index(self.index, f"{path}.index")
        with open(f"{path}.pkl", 'wb') as f:
            pickle.dump(self.facts, f)
    
    def load(self, path: str):
        """Load index and facts"""
        self.index = faiss.read_index(f"{path}.index")
        with open(f"{path}.pkl", 'rb') as f:
            self.facts = pickle.load(f)