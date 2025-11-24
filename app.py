import streamlit as st
from fact_checker import FactChecker
import json

# Page config
st.set_page_config(page_title="Fact Checker", page_icon="🔍", layout="centered")

# Custom CSS
st.markdown("""
<style>
    .main-header {text-align: center; color: #1f77b4; margin-bottom: 2rem;}
    .verdict-likely true {background: #d4edda; padding: 1rem; border-radius: 8px; border-left: 4px solid #28a745; color: #155724;}
    .verdict-likely false {background: #f8d7da; padding: 1rem; border-radius: 8px; border-left: 4px solid #dc3545; color: #721c24;}
    .verdict-unverifiable {background: #fff3cd; padding: 1rem; border-radius: 8px; border-left: 4px solid #ffc107; color: #856404;}
    .evidence-box {background: #e9ecef; padding: 1rem; margin: 0.5rem 0; border-radius: 5px; font-size: 0.95rem; color: #212529; border: 1px solid #dee2e6;}
</style>
""", unsafe_allow_html=True)

# Initialize
@st.cache_resource
def load_checker():
    checker = FactChecker()
    try:
        checker.vector_db.load("fact_index")
    except:
        checker.initialize_facts("facts.txt")
    return checker

checker = load_checker()

# Header
st.markdown("<h1 class='main-header'>🔍 AI Fact Checker</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Verify claims against trusted sources using AI</p>", unsafe_allow_html=True)

# Input
claim_input = st.text_area("Enter a claim to verify:", 
                           placeholder="e.g., The Indian government has announced free electricity to all farmers starting July 2025.",
                           height=100)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    check_button = st.button("🔍 Check Fact", use_container_width=True, type="primary")

# Process
if check_button and claim_input:
    with st.spinner("Analyzing claim..."):
        result = checker.check_fact(claim_input)
    
    # Display verdict
    verdict = result['verdict']
    confidence = result.get('confidence', 0)
    verdict_class = f"verdict-{verdict.lower()}"
    
    if verdict == "Likely True":
        emoji = "✅"
    elif verdict == "Likely False":
        emoji = "❌"
    else:
        emoji = "⚠️"
    
    st.markdown(f"<div class='{verdict_class}'><h3>{emoji} {verdict}</h3><p style='margin:0; font-size:0.9rem;'>Confidence: {confidence:.2%}</p></div>", unsafe_allow_html=True)
    
    # Reasoning
    st.markdown("### 💭 Reasoning")
    st.write(result['reasoning'])
    
    # Evidence
    st.markdown("### 📚 Evidence")
    for i, evidence in enumerate(result['evidence'], 1):
        st.markdown(f"<div class='evidence-box'><strong>{i}.</strong> {evidence}</div>", unsafe_allow_html=True)
    
    # Feedback
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👍 Helpful"):
            st.success("Thanks for your feedback!")
    with col2:
        if st.button("👎 Not Helpful"):
            st.info("Thanks! We'll improve.")

elif check_button:
    st.warning("⚠️ Please enter a claim to check.")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #999; font-size: 0.85rem;'>Powered by Mistral LLM & Sentence Transformers</p>", unsafe_allow_html=True)