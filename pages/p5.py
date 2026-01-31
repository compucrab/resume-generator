import streamlit as st
from core.smanager import StateManager
from core.generator import Generator
from core.suggestions import SuggestionEngine
import os
from datetime import datetime

StateManager.initialize()
st.set_page_config(page_title="Resume Generator - Final Review", layout="wide")


st.markdown(
    """
<style>
    .stButton > button {
        height: 3rem;
        font-weight: 500;
    }
    .block-container {
        padding-top: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    .big-button > button {
        height: 4rem !important;
        font-size: 1.1rem !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

StateManager.render_progress_bar(4)

st.title("✨ Custom Sections & Final Review")
st.caption("Add any additional sections and generate your resume")
st.info(
    ":material/lightbulb: Add sections like Certifications, Awards, Publications, Volunteer Work, etc."
)
col_tex, col_add, _ = st.columns(3)

st.divider()

existing_custom = st.session_state.get("form_data", {}).get("custom_sections", [])

if "custom_count" not in st.session_state:
    st.session_state.custom_count = max(len(existing_custom), 0)

with col_add:
    if st.button(
        ":material/add: Add Section",
        key="add_custom_btn",
        use_container_width=True,
        type="secondary",
    ):
        st.session_state.custom_count += 1
        st.rerun()

st.write("")

custom_sections_data = []

for i in range(st.session_state.custom_count):
    current = existing_custom[i] if i < len(existing_custom) else {}

    with st.expander(f"✨ {current.get('title', f'Section #{i+1}')}", expanded=True):
        if st.button(
            f":material/delete: Remove Section #{i+1}",
            key=f"remove_custom_{i}",
            type="secondary",
        ):
            StateManager.remove_item("custom_sections", i)
            st.session_state.custom_count = max(0, st.session_state.custom_count - 1)
            st.rerun()

        st.write("")  

        section_title = st.text_input(
            "Section Title",
            key=f"custom_title_{i}",
            value=current.get("title", ""),
            placeholder="e.g., Certifications, Awards, Publications",
        )

        section_content = st.text_area(
            "Content",
            key=f"custom_content_{i}",
            value=current.get("content", ""),
            placeholder="• AWS Certified Solutions Architect\n• Google Cloud Professional\n• CompTIA Security+",
            height=120,
        )

        custom_sections_data.append(
            {"title": section_title, "content": section_content}
        )


col1 = st.columns(1)[0]

# Center the generate button with better prominence
col_left, col_center, col_right = st.columns([1, 2, 1])
with col_center:
    if st.button(
        ":material/search: Analyze Resume Strength", use_container_width=True, type="secondary"
    ):
        analysis_data = st.session_state.form_data.copy()
        analysis_data["custom_sections"] = custom_sections_data
        score, feedback = SuggestionEngine.analyze_overall_resume(analysis_data)
        StateManager.show_suggestions(feedback)

# Center the generate button with better prominence
col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    st.markdown('<div class="big-button">', unsafe_allow_html=True)
    if st.button(":material/rocket_launch: Generate PDF Resume", use_container_width=True, type="primary"):
        with st.spinner("✨ Crafting your professional resume..."):
            st.session_state.form_data["custom_sections"] = custom_sections_data
            pdf_path, error = Generator.generate_pdf(st.session_state.form_data)

            if error:
                st.error(f":material/error: Generation failed: {error}")
            elif pdf_path and os.path.exists(pdf_path):
                st.success(":material/check_circle: Resume Generated Successfully!")

                with open(pdf_path, "rb") as f:
                    pdf_bytes = f.read()

                st.write("")  
                st.download_button(
                    label=":material/download: Download PDF",
                    data=pdf_bytes,
                    file_name=f"Resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    type="primary",
                )
    st.markdown("</div>", unsafe_allow_html=True)
