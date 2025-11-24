from claim_extractor import ClaimExtractor
from vector_db import VectorDB
from llm_verifier import LLMVerifier
from typing import Dict

class FactChecker:
    def __init__(self, vector_db_path: str = None):
        self.claim_extractor = ClaimExtractor()
        self.vector_db = VectorDB()
        self.llm_verifier = LLMVerifier()
        
        if vector_db_path:
            self.vector_db.load(vector_db_path)
    
    def initialize_facts(self, facts_file: str):
        """Load facts from file and create vector index"""
        with open(facts_file, 'r', encoding='utf-8') as f:
            facts = [line.strip() for line in f if line.strip()]
        
        self.vector_db.create_index(facts)
        self.vector_db.save("fact_index")
    
    def check_fact(self, text: str, top_k: int = 3, threshold: float = 0.3) -> Dict:
        """Main pipeline: extract claim, retrieve evidence, verify"""
        # Use full text as main claim for better context
        main_claim = text
        
        # Check confidence score
        confidence = self.vector_db.get_confidence_score(main_claim, k=top_k)
        
        # If confidence too low, mark as unverifiable immediately
        if confidence < threshold:
            return {
                "verdict": "Unverifiable",
                "evidence": [],
                "reasoning": f"Insufficient relevant evidence found (confidence: {confidence:.2f}). Claim is too vague or outside knowledge base.",
                "confidence": confidence
            }
        
        # Retrieve similar facts
        results = self.vector_db.retrieve(main_claim, k=top_k)
        evidence = [fact for fact, _ in results]
        
        # Verify with LLM
        verification = self.llm_verifier.verify_claim(main_claim, evidence)
        
        # Format output
        return {
            "verdict": verification.get("verdict", "Unverifiable"),
            "evidence": evidence,
            "reasoning": verification.get("reasoning", "No reasoning provided"),
            "confidence": confidence
        }