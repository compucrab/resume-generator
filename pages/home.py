import streamlit as st
from core.smanager import StateManager

st.set_page_config(
    page_title="AI Resume Generator", layout="wide", initial_sidebar_state="collapsed"
)

st.markdown(
    """
<style>
    /* Main container styling */
    .main > div {
        padding-top: 2rem;
    }
    
    /* Button styling */
    .stButton > button {
        height: 3rem;
        font-size: 1rem;
        font-weight: 500;
    }
    
    /* Remove extra padding */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
    }
    
    /* Center content */
    .center-content {
        max-width: 900px;
        margin: 0 auto;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown("<div class='center-content'>", unsafe_allow_html=True)
st.title(":material/robot_2: AI Powered Resume Generator")
st.markdown("### Transform your experience into a recruiter-ready resume in minutes")
st.divider()

try:
    resume_index = st.session_state.visited.index(False)
except (ValueError, AttributeError):
    resume_index = len(StateManager.STEPS) - 1

if any(st.session_state.get("visited", [])):
    st.info(
        f":material/lightbulb: Progress detected! Resuming at Step {resume_index + 1}: **{StateManager.STEPS[resume_index]}**"
    )
    st.write("")  

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button(
        ":material/restart_alt: Reset Session",
        use_container_width=True,
        type="secondary",
    ):
        st.session_state.form_data = {}
        st.session_state.visited = [False] * len(StateManager.STEPS)
        if hasattr(StateManager, "ls") and StateManager.ls:
            StateManager.ls.deleteAll()
        st.rerun()


with col3:
    has_progress = any(st.session_state.get("visited", []))
    btn_label = (
        "Continue :material/arrow_right_alt:"
        if has_progress
        else "Start Building :material/arrow_right_alt:"
    )

    if st.button(btn_label, use_container_width=True, type="primary"):
        st.switch_page(StateManager.get_page_path(resume_index))

st.write("")


feat_col1, feat_col2, feat_col3 = st.columns(3)

with feat_col1:
    st.markdown("**📝 Smart Suggestions**")
    st.caption("AI-powered tips to improve your resume")

with feat_col2:
    st.markdown("**🎯 ATS-Optimized**")
    st.caption("Formatted for applicant tracking systems")

with feat_col3:
    st.markdown("**⚡ Quick & Easy**")
    st.caption("Generate professional PDFs in minutes")

st.markdown("</div>", unsafe_allow_html=True)
