import requests
import json
from typing import Dict, List

class LLMVerifier:
    def __init__(self, model: str = "mistral", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
    
    def verify_claim(self, claim: str, evidence: List[str]) -> Dict:
        """Verify claim against retrieved evidence using LLM"""
        prompt = f"""You are a fact-checking assistant. Analyze the claim against the evidence and provide a verdict.

Claim: {claim}

Evidence:
{chr(10).join(f"{i+1}. {e}" for i, e in enumerate(evidence))}

Based on the evidence, classify this claim as:
- "Likely True" if evidence strongly supports it
- "Likely False" if evidence contradicts it
- "Unverifiable" if evidence is insufficient

Respond in JSON format:
{{
  "verdict": "Likely True/Likely False/Unverifiable",
  "reasoning": "Brief explanation of your decision"
}}"""

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={"model": self.model, "prompt": prompt, "stream": False}
        )
        
        result_text = response.json()['response']
        
        # Extract JSON from response
        try:
            start = result_text.find('{')
            end = result_text.rfind('}') + 1
            result = json.loads(result_text[start:end])
        except:
            result = {"verdict": "Unverifiable", "reasoning": "Could not parse LLM response"}
        
        return result