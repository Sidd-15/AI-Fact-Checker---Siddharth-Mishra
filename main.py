from fact_checker import FactChecker

# Initialize fact checker
checker = FactChecker()

# Load and index facts (run once)
checker.initialize_facts("facts.txt")

# Test with sample input
test_claim = "The Indian government has announced free electricity to all farmers starting July 2025."

result = checker.check_fact(test_claim)

print("\n" + "="*60)
print("FACT CHECK RESULT")
print("="*60)
print(f"\nClaim: {test_claim}")
print(f"\nVerdict: {result['verdict']}")
print(f"\nReasoning: {result['reasoning']}")
print(f"\nEvidence:")
for i, evidence in enumerate(result['evidence'], 1):
    print(f"  {i}. {evidence}")
print("\n" + "="*60)