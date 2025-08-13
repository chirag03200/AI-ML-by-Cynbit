import streamlit as st
from io import StringIO
import summarizer
from pathlib import Path

st.set_page_config(page_title="Text Summarizer", layout="centered")

st.title("📝 Text Summarizer")
st.write("Paste text or upload a .txt/.pdf file. Choose number of bullets and click **Summarize**.")

uploaded = st.file_uploader("Upload .txt or .pdf", type=["txt", "pdf"])
text_input = st.text_area("Or paste text here", height=250)

cols = st.columns([1, 2, 1])
with cols[0]:
    num_bullets = st.number_input("Bullets", min_value=1, max_value=8, value=4, step=1)
with cols[1]:
    run_btn = st.button("Summarize")
with cols[2]:
    clear_btn = st.button("Clear")

if clear_btn:
    st.experimental_rerun()

content = ""
if uploaded is not None:
    # read uploaded file
    try:
        b = uploaded.read()
        suffix = Path(uploaded.name).suffix.lower()
        if suffix == ".pdf":
            # write to temp file and use read_pdf
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(b)
                tmp_path = tmp.name
            content = summarizer.read_pdf(tmp_path)
        else:
            try:
                content = b.decode("utf-8")
            except Exception:
                content = b.decode("latin-1", errors="ignore")
    except Exception as e:
        st.error(f"Failed to read file: {e}")

# If user typed/pasted text, prefer that
if text_input and text_input.strip():
    content = text_input

if run_btn:
    if not content or not content.strip():
        st.warning("Please paste text or upload a file first.")
    else:
        with st.spinner("Summarizing..."):
            try:
                bullets = summarizer.generate_summary(content, num_bullets=int(num_bullets))
            except Exception as e:
                st.error(f"Summarization failed: {e}")
                bullets = []

        if bullets:
            st.markdown("### Summary")
            for b in bullets:
                st.write(f"- {b}")
            # provide a download button
            summary_text = "\n".join(f"- {b}" for b in bullets)
            st.download_button("Download summary (.txt)", summary_text, file_name="summary.txt")
        else:
            st.info("No summary generated. Try a longer input or check logs.")
