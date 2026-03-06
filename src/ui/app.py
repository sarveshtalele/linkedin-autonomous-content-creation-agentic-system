from __future__ import annotations
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))


import asyncio

import streamlit as st

from src.ingestion.pipeline import ingest
from src.pipeline.runner import run_pipeline


st.set_page_config(page_title="LinkedIn Autonomous Content Creation Agentic System", layout="wide")
st.title("LinkedIn Autonomous Content Agent")
st.caption("Powered by Ollama phi3 + Hybrid RAG + Reviewer Rewrite Loop")


topic = st.text_input("Post Topic", placeholder="e.g. How AI agents improve GTM execution")
uploaded_files = st.file_uploader("Upload files", accept_multiple_files=True)
urls_raw = st.text_area("Web URLs (one per line)", placeholder="https://example.com/blog-post")

col1, col2 = st.columns(2)
with col1:
    generate = st.button("Generate LinkedIn Post", type="primary", use_container_width=True)
with col2:
    st.empty()


if generate:
    if not topic.strip():
        st.error("Enter a topic before generating.")
        st.stop()

    url_list = [line.strip() for line in urls_raw.splitlines() if line.strip()]

    with st.spinner("Ingesting sources..."):
        data = ingest(uploaded_files or [], url_list)

    if not data:
        st.error("No usable content found from uploaded files or URLs.")
        st.stop()

    with st.spinner("Running autonomous pipeline..."):
        result = asyncio.run(run_pipeline(topic.strip(), data))

    st.subheader("LinkedIn Post")
    st.markdown(result.get("linkedin_post", ""))

    score = int(result.get("score", 0))
    st.metric("Review Score", score)

    with st.expander("Reviewer Feedback"):
        st.write(result.get("review", "No feedback available."))

    with st.expander("Detected Keywords"):
        st.write(result.get("keywords", []))

    with st.expander("Ingested Sources"):
        st.write([item.get("source") for item in data])
