import streamlit as st
import time
import re
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain
 
# PAGE CONFIG 
st.set_page_config(
    page_title="ResearchAI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)
 
# GLOBAL STYLES 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap');
 
/* Root reset */
html, body, [class*="css"]  {
    font-family: 'DM Sans', sans-serif;
    background-color: #0b0c10;
    color: #e2e8f0;
}
 
/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { 
    padding: 2rem 3rem 4rem 3rem; 
    max-width: 900px;
    margin: 0 auto;
}
 
/* ── HERO ── */
.hero-wrap {
    text-align: center;
    padding: 3.5rem 1rem 2rem;
    position: relative;
}
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.22em;
    color: #64ffda;
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2.8rem, 6vw, 4.4rem);
    line-height: 1.1;
    background: linear-gradient(135deg, #e2e8f0 30%, #64ffda 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 1rem;
}
.hero-subtitle {
    color: #94a3b8;
    font-size: 1.05rem;
    font-weight: 300;
    max-width: 560px;
    margin: 0 auto 2.5rem;
    line-height: 1.65;
    text-align: center;
    display: block;
    width: 100%;
}
 
/* ── INPUT CARD ── */
.input-card {
    background: linear-gradient(135deg, #141820 0%, #1a1f2e 100%);
    border: 1px solid #1e2740;
    border-radius: 16px;
    padding: 2rem 2.4rem;
    margin-bottom: 2rem;
    box-shadow: 0 8px 40px rgba(0,0,0,0.4);
}
 
/* ── Streamlit input override ── */
div[data-testid="stTextInput"] input {
    background: #0d1117 !important;
    border: 1.5px solid #1e2740 !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #64ffda !important;
    box-shadow: 0 0 0 3px rgba(100,255,218,0.1) !important;
}
div[data-testid="stTextInput"] label {
    color: #94a3b8 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em;
}
 
/* ── BUTTON ── */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #0fbbaa, #064e45) !important;
    color: #0b0c10 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.06em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 2.2rem !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
    box-shadow: 0 4px 18px rgba(100,255,218,0.2) !important;
    cursor: pointer !important;
    white-space: nowrap !important;
    height: 48px !important;
    min-width: 160px !important;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(100,255,218,0.35) !important;
}
 
/* ── STEP BADGES ── */
.step-header {
    display: flex;
    align-items: center;
    gap: 0.9rem;
    margin: 2rem 0 0.8rem;
}
.step-badge {
    background: rgba(100,255,218,0.12);
    border: 1px solid rgba(100,255,218,0.3);
    color: #64ffda;
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    padding: 0.25rem 0.65rem;
    border-radius: 100px;
    letter-spacing: 0.1em;
    white-space: nowrap;
}
.step-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.25rem;
    color: #e2e8f0;
    margin: 0;
}
 
/* ── RESULT CARDS ── */
.result-card {
    background: #111520;
    border: 1px solid #1e2740;
    border-left: 3px solid #64ffda;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    font-size: 0.93rem;
    line-height: 1.75;
    color: #cbd5e1;
    font-family: 'DM Sans', sans-serif;
    white-space: pre-wrap;
    word-break: break-word;
}
 
/* ── REPORT CARD ── */
.report-card {
    background: linear-gradient(160deg, #111827 0%, #0d1420 100%);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 2rem 2.4rem;
    color: #dde4ef;
    font-size: 0.97rem;
    line-height: 1.85;
    white-space: pre-wrap;
    word-break: break-word;
}
.report-card h3 {
    font-family: 'DM Serif Display', serif;
    color: #e2e8f0;
    margin-top: 1.4rem;
}
 
/* ── CRITIC SCORECARD ── */
.score-box {
    display: inline-block;
    background: linear-gradient(135deg, #0fbbaa22, #0fbbaa11);
    border: 2px solid #0fbbaa;
    border-radius: 14px;
    padding: 0.6rem 1.4rem;
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: #64ffda;
    margin-bottom: 1rem;
}
.critic-section {
    background: #0d1117;
    border: 1px solid #1e2740;
    border-radius: 12px;
    padding: 1.2rem 1.6rem;
    margin-bottom: 0.8rem;
    color: #94a3b8;
    font-size: 0.92rem;
    line-height: 1.75;
    white-space: pre-wrap;
}
.critic-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.15em;
    color: #64ffda;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
 
/* ── VERDICT ── */
.verdict-box {
    background: linear-gradient(135deg, #1a2740, #0f1a30);
    border: 1px solid #2563eb55;
    border-radius: 12px;
    padding: 1rem 1.6rem;
    font-style: italic;
    color: #93c5fd;
    font-size: 1rem;
    margin-top: 0.5rem;
}
 
/* ── DIVIDER ── */
.fancy-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1e2740 30%, #64ffda44 50%, #1e2740 70%, transparent);
    margin: 2.5rem 0;
}
 
/* ── STATUS SPINNER ── */
div[data-testid="stStatusWidget"] {
    background: #111520 !important;
    border: 1px solid #1e2740 !important;
    border-radius: 12px !important;
}
 
/* ── SUCCESS / INFO ── */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: 1px solid #1e2740 !important;
}
 
/* ── DOWNLOAD BUTTON ── */
div[data-testid="stDownloadButton"] > button {
    background: #141820 !important;
    color: #64ffda !important;
    border: 1px solid #64ffda55 !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
    transition: background 0.15s, box-shadow 0.15s !important;
}
div[data-testid="stDownloadButton"] > button:hover {
    background: #1e2740 !important;
    box-shadow: 0 4px 14px rgba(100,255,218,0.15) !important;
}
 
/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0b0c10; }
::-webkit-scrollbar-thumb { background: #1e2740; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)
 
 
# HELPERS 
 
def parse_critic(feedback: str):
    """Extract score, strengths, areas, verdict from critic output."""
    score_match = re.search(r"Score:\s*(\d+(?:\.\d+)?)/10", feedback)
    score = score_match.group(1) if score_match else "?"
 
    strengths_match = re.search(
        r"Strengths:\s*(.*?)(?:Areas to Improve:|$)", feedback, re.DOTALL | re.IGNORECASE)
    strengths = strengths_match.group(1).strip() if strengths_match else ""
 
    areas_match = re.search(
        r"Areas to Improve:\s*(.*?)(?:One line verdict:|$)", feedback, re.DOTALL | re.IGNORECASE)
    areas = areas_match.group(1).strip() if areas_match else ""
 
    verdict_match = re.search(r"One line verdict:\s*(.*?)$", feedback, re.DOTALL | re.IGNORECASE)
    verdict = verdict_match.group(1).strip() if verdict_match else ""
 
    return score, strengths, areas, verdict
 
 
def score_color(score_str: str) -> str:
    try:
        s = float(score_str)
        if s >= 8: return "#64ffda"
        if s >= 6: return "#fbbf24"
        return "#f87171"
    except:
        return "#64ffda"
 
 
# HERO 
st.markdown("""
<div class="hero-wrap">
    <div class="hero-eyebrow">⚡ AI-Powered Research Engine</div>
    <h1 class="hero-title">ResearchAI</h1>
    <p class="hero-subtitle">
        Enter any topic. Our multi-agent pipeline searches the web, scrapes deep content, writes a structured report, and critiques it — automatically.
    </p>
</div>
""", unsafe_allow_html=True)
 
# INPUT 
st.markdown('<div class="input-card">', unsafe_allow_html=True)
col1, col2 = st.columns([5, 1], vertical_alignment="bottom")
with col1:
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Impact of quantum computing on cryptography",
        label_visibility="visible",
    )
with col2:
    run = st.button("🔬  Run Research", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
 
# PIPELINE 
if run:
    if not topic.strip():
        st.warning("Please enter a research topic before running.")
        st.stop()
 
    state = {}
 
    # STEP 1 
    st.markdown("""
    <div class="step-header">
        <span class="step-badge">STEP 01</span>
        <span class="step-title">Web Search Agent</span>
    </div>
    """, unsafe_allow_html=True)
 
    with st.status("🔍  Searching the web for relevant sources…", expanded=True) as status:
        st.write("Querying Tavily search API with your topic…")
        search_agent = build_search_agent()
        search_result = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
        })
        state["search_results"] = search_result["messages"][-1].content
        st.write("✅  Search complete — top results retrieved.")
        status.update(label="✅  Search complete", state="complete", expanded=False)
 
    st.markdown(f'<div class="result-card">{state["search_results"]}</div>', unsafe_allow_html=True)
 
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
 
    # STEP 2
    st.markdown("""
    <div class="step-header">
        <span class="step-badge">STEP 02</span>
        <span class="step-title">Deep-Read Agent</span>
    </div>
    """, unsafe_allow_html=True)
 
    with st.status("📖  Scraping the most relevant source…", expanded=True) as status:
        st.write("Picking the best URL from search results and scraping full content…")
        reader_agent = build_reader_agent()
        reader_result = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:800]}"
            )]
        })
        state["scraped_content"] = reader_result["messages"][-1].content
        st.write("✅  Content scraped and cleaned.")
        status.update(label="✅  Scraping complete", state="complete", expanded=False)
 
    st.markdown(f'<div class="result-card">{state["scraped_content"]}</div>', unsafe_allow_html=True)
 
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
 
    # STEP 3
    st.markdown("""
    <div class="step-header">
        <span class="step-badge">STEP 03</span>
        <span class="step-title">Report Writer</span>
    </div>
    """, unsafe_allow_html=True)
 
    with st.status("✍️  Drafting research report…", expanded=True) as status:
        st.write("Combining search results + scraped content → structured report…")
        research_combined = (
            f"SEARCH RESULTS:\n{state['search_results']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
        )
        state["report"] = writer_chain.invoke({
            "topic": topic,
            "research": research_combined,
        })
        st.write("✅  Report drafted.")
        status.update(label="✅  Report ready", state="complete", expanded=False)
 
    st.markdown(f'<div class="report-card">{state["report"]}</div>', unsafe_allow_html=True)
 
    # Download button
    st.download_button(
        label="⬇  Download Report (.txt)",
        data=state["report"],
        file_name=f"report_{topic[:40].replace(' ','_')}.txt",
        mime="text/plain",
    )
 
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
 
    # STEP 4 
    st.markdown("""
    <div class="step-header">
        <span class="step-badge">STEP 04</span>
        <span class="step-title">Critic Review</span>
    </div>
    """, unsafe_allow_html=True)
 
    with st.status("🧐  Critic is evaluating the report…", expanded=True) as status:
        st.write("Sending report to the critic agent for scoring and feedback…")
        state["feedback"] = critic_chain.invoke({"report": state["report"]})
        st.write("✅  Review complete.")
        status.update(label="✅  Critique done", state="complete", expanded=False)
 
    score, strengths, areas, verdict = parse_critic(state["feedback"])
    clr = score_color(score)
 
    # Score pill
    st.markdown(
        f'<div class="score-box" style="border-color:{clr}; color:{clr};">'
        f'Score &nbsp;{score}<span style="font-size:1rem;opacity:0.5">/10</span>'
        f'</div>',
        unsafe_allow_html=True
    )
 
    col_s, col_a = st.columns(2)
    with col_s:
        st.markdown('<div class="critic-label">💚 Strengths</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="critic-section">{strengths}</div>', unsafe_allow_html=True)
    with col_a:
        st.markdown('<div class="critic-label">⚠️ Areas to Improve</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="critic-section">{areas}</div>', unsafe_allow_html=True)
 
    if verdict:
        st.markdown(f'<div class="verdict-box">🗣️ &nbsp;{verdict}</div>', unsafe_allow_html=True)
 
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
 
    st.success("🎉  Research pipeline completed successfully!", icon="✅")
