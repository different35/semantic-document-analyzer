import streamlit as st
import sys
sys.path.append("..")
from knowledge_base import AMDOptimizedKnowledgeBase

st.set_page_config(page_title="Semantik Arama", page_icon="🔍", layout="wide")

@st.cache_resource
def load_system():
    return AMDOptimizedKnowledgeBase(use_gpu=True)

kb = load_system()
st.title("🔍 Semantik Doküman Arama")

with st.sidebar:
    st.header("📁 Doküman Yükleme")
    uploaded_files = st.file_uploader("Dosyaları seçin", accept_multiple_files=True)

col1, col2 = st.columns(2)
with col1:
    keyword1 = st.text_input("Kelime 1")
with col2:
    keyword2 = st.text_input("Kelime 2")

if st.button("🔍 Ara"):
    if keyword1 and keyword2:
        results = kb.search_semantic(keyword1, keyword2)
        st.write(results)
