import re
from typing import List
from pathlib import Path

# transformers and torch (may be heavy). gensim & PyPDF2 are lighter fallbacks for some parts.
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
    import torch
    HF_AVAILABLE = True
except Exception:
    HF_AVAILABLE = False

try:
    from gensim.summarization import summarize as gensim_summarize
    GENSIM_AVAILABLE = True
except Exception:
    GENSIM_AVAILABLE = False

try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except Exception:
    PYPDF2_AVAILABLE = False


def read_txt(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"{path} not found")
    return p.read_text(encoding="utf-8", errors="ignore")


def read_pdf(path: str) -> str:
    if not PYPDF2_AVAILABLE:
        raise RuntimeError("PyPDF2 is not installed. Install it to read PDFs.")
    text_chunks = []
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for i, page in enumerate(reader.pages):
            try:
                text_chunks.append(page.extract_text() or "")
            except Exception:
                continue
    return "\n".join(text_chunks)


def _split_sentences(text: str) -> List[str]:
    # naive sentence split; robust enough for bullets
    parts = re.split(r'(?<=[\.\?\!])\s+', text.strip())
    parts = [p.strip() for p in parts if p.strip()]
    return parts


def _chunk_text(text: str, max_chars: int = 1000) -> List[str]:
    """Split long text into chunks not exceeding max_chars (try not to break sentences)."""
    sentences = _split_sentences(text)
    chunks = []
    current = ""
    for s in sentences:
        if len(current) + len(s) + 1 <= max_chars:
            current = (current + " " + s).strip()
        else:
            if current:
                chunks.append(current)
            current = s
    if current:
        chunks.append(current)
    return chunks


class HFSummarizer:
    def __init__(self, model_name: str = "facebook/bart-large-cnn", device: int = None):
        if not HF_AVAILABLE:
            raise RuntimeError("transformers or torch not available")
        # device: None -> auto (GPU if available)
        if device is None:
            device = 0 if torch.cuda.is_available() else -1
        self.device = device
        # instantiate pipeline lazily to reduce startup overhead
        self.model_name = model_name
        self._pipe = None

    @property
    def pipe(self):
        if self._pipe is None:
            self._pipe = pipeline("summarization", model=self.model_name, device=self.device)
        return self._pipe

    def summarize(self, text: str) -> str:
        # chunk large texts then join partial summaries
        chunks = _chunk_text(text, max_chars=1000)
        results = []
        for c in chunks:
            # adjust min/max lengths reasonably to chunk length
            max_len = min(200, max(30, int(len(c.split()) * 0.6)))
            min_len = min(30, int(max_len * 0.3))
            try:
                out = self.pipe(c, max_length=max_len, min_length=min_len, truncation=True)
                if isinstance(out, list) and out:
                    results.append(out[0]["summary_text"].strip())
            except Exception:
                # on any failure, skip chunk
                continue
        return " ".join(results).strip()


def generate_summary(text: str, num_bullets: int = 4) -> List[str]:
    """
    Generates a concise summary and returns a list of bullet points (num_bullets).
    Strategy:
    - Try HuggingFace summarizer (if available)
    - Fallback to gensim summarizer (TextRank)
    - If both fail, use a naive top-sentences approach
    """
    text = text.strip()
    if not text:
        return []

    # 1) Try HF
    summary_text = ""
    if HF_AVAILABLE:
        try:
            hf = HFSummarizer()
            summary_text = hf.summarize(text)
        except Exception:
            summary_text = ""

    # 2) Fallback to gensim
    if not summary_text and GENSIM_AVAILABLE:
        try:
            # gensim.summarize may fail on very short texts
            # ratio chooses how much to keep; increase ratio if output too short
            summary_text = gensim_summarize(text, ratio=0.2)
        except Exception:
            summary_text = ""

    # 3) Final fallback: naive selection of top sentences (first N sentences)
    if not summary_text:
        sents = _split_sentences(text)
        pick = sents[: max(1, min(len(sents), num_bullets * 2))]
        summary_text = " ".join(pick)

    # Post-process into bullet points: split into sentences and choose up to num_bullets
    sents = _split_sentences(summary_text)
    if len(sents) >= num_bullets:
        bullets = sents[:num_bullets]
    else:
        # if too few sentences, try splitting by semicolons or commas, or split lengthwise
        if len(sents) == 1:
            # break single long sentence into chunks by commas
            parts = [p.strip() for p in re.split(r';|,', sents[0]) if p.strip()]
            bullets = parts[:num_bullets] if parts else [sents[0]]
        else:
            bullets = sents

    # clean bullets
    clean = []
    for b in bullets:
        b = b.strip()
        # ensure ends without trailing weird chars
        b = re.sub(r'\s+', ' ', b)
        clean.append(b)
    return clean


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Text summarizer CLI")
    parser.add_argument("--file", "-f", help="Path to text or pdf file", default=None)
    parser.add_argument("--text", "-t", help="Text string to summarize (wrap in quotes)", default=None)
    parser.add_argument("--bullets", "-b", type=int, default=4, help="Number of bullet points (3-5 recommended)")
    args = parser.parse_args()

    content = ""
    if args.file:
        p = Path(args.file)
        if p.suffix.lower() == ".pdf":
            content = read_pdf(args.file)
        else:
            content = read_txt(args.file)
    elif args.text:
        content = args.text
    else:
        print("No input provided. Use --file or --text")
        exit(1)

    bullets = generate_summary(content, num_bullets=args.bullets)
    for i, b in enumerate(bullets, 1):
        print(f"{i}. {b}")
