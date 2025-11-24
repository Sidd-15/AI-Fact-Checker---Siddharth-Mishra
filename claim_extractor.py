import spacy
from typing import List

class ClaimExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
    
    def extract_claims(self, text: str) -> List[str]:
        """Extract key claims and entities from input text"""
        doc = self.nlp(text)
        
        # Extract named entities
        entities = [ent.text for ent in doc.ents]
        
        # Extract noun chunks as potential claims
        noun_chunks = [chunk.text for chunk in doc.noun_chunks]
        
        # Combine and deduplicate
        claims = list(set(entities + noun_chunks + [text]))
        
        return claims