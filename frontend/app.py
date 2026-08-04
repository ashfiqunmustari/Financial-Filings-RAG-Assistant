import streamlit as st
import requests
import os

USE_API = os.environ.get("API_URL")
if not USE_API:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent / "app"))
    from app.rag import answer_question

def get_answer(question):
    if USE_API:
        response = requests.post(USE_API + "/ask", json={"question": question}, timeout=60)
        response.raise_for_status()
        return response.json()
    else:
        return answer_question(question)

def relevance_badge(distance):
    if distance < 0.8:
        label, bg, fg = "High relevance", "#E1F5EE", "#0F6E56"
    elif distance < 1.2:
        label, bg, fg = "Medium relevance", "#FBEAF0", "#993556"
    else:
        label, bg, fg = "Lower relevance", "#F1EFE8", "#5F5E5A"
    return f'<span style="font-size:12px;padding:3px 10px;border-radius:20px;background:{bg};color:{fg};white-space:nowrap;">{label}</span>'

st.set_page_config(page_title="Filing Insights", page_icon="📄")

st.markdown("""
<style>
html, body, [class*="css"] { font-family: Georgia, 'Times New Roman', serif; }
h1 { font-family: Georgia, serif !important; font-weight: 500 !important; }
.stButton { width: 100%; }
.stButton > button {
    width: 100%;
    background: #D4537E;
    color: #fff;
    border: none;
    border-radius: 8px;
    padding: 12px;
    font-family: Georgia, serif;
    font-size: 24px;
}
.stButton > button:hover { background: #C04670; color: #fff; }
.answer-label {
    font-size: 12px; letter-spacing: 0.1em; text-transform: uppercase;
    color: #993556; margin: 1.5rem 0 0.5rem;
}
.answer-card {
    background: #FBEAF0; border-radius: 14px; padding: 1.25rem 1.5rem;
    font-size: 16px; line-height: 1.7; color: #1A1A1A;
}
.source-section { font-size: 15px; font-weight: 500; color: #1A1A1A; }
.source-preview { font-size: 14px; color: #555; line-height: 1.6; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

st.markdown("# Filing Insights")
st.caption("Ask a question about Microsoft's 2026 annual report (10-K).")

st.write("")
question = st.text_input("Your question", placeholder="What are the main risk factors?", label_visibility="collapsed")

if st.button("Ask", use_container_width=True):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Searching the filing..."):
            result = get_answer(question)

        st.markdown('<div class="answer-label">Answer</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="answer-card">{result["answer"]}</div>', unsafe_allow_html=True)

        sources = result["sources"]

        st.write("")
        with st.expander(f"View sources ({len(sources)})"):
            if not sources:
                st.write("No relevant sections found.")
            else:
                for src in sources:
                    st.markdown(
                        f'<div style="display:flex;justify-content:space-between;align-items:center;margin-top:10px;">'
                        f'<span class="source-section">{src["section"]}</span>{relevance_badge(src["distance"])}</div>',
                        unsafe_allow_html=True,
                    )
                    preview = src.get("text", "")[:200]
                    if preview:
                        st.markdown(f'<div class="source-preview">{preview}…</div>', unsafe_allow_html=True)
                    st.divider()