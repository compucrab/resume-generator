import streamlit as st
from core.smanager import StateManager
from core.validator import ResumeValidator
from core.suggestions import SuggestionEngine
from datetime import date, datetime

StateManager.initialize()
st.set_page_config(page_title="Resume Generator - Education", layout="wide")


st.markdown("""
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
</style>
""", unsafe_allow_html=True)

StateManager.render_progress_bar(1)

st.title(":material/school: Education Details")
st.caption("Add your educational background (Optional)")
st.info(":material/lightbulb: Education section is optional. Skip if not applicable or add details to strengthen your resume.")
st.divider()

# Sync counter with existing data
existing_edu = st.session_state.form_data.get("education", [])
if "education_count" not in st.session_state:
    st.session_state.education_count = max(len(existing_edu), 1)
else:
    st.session_state.education_count = max(len(existing_edu), st.session_state.education_count)

# Add button (right-aligned)
col_spacer, col_add = st.columns([4, 1])
with col_add:
    if st.button(":material/add: Add", use_container_width=True, type="secondary"):
        st.session_state.education_count += 1
        st.rerun()

st.write("")  

education_entries = []

for i in range(st.session_state.education_count):
    current_data = existing_edu[i] if i < len(existing_edu) else {}
    
    with st.expander(
        f":material/school: Education #{i+1}: {current_data.get('degree', 'New Entry')}", 
        expanded=(i == st.session_state.education_count - 1)
    ):
        if st.session_state.education_count > 1:
            if st.button(
                f":material/delete: Remove Entry #{i+1}", 
                key=f"remove_edu_{i}", 
                type="secondary"
            ):
                StateManager.remove_item("education", i)
                st.session_state.education_count -= 1
                st.rerun()
            st.write("")  

        col1, col2 = st.columns(2, gap="medium")

        with col1:
            inst = st.text_input(
                "Institution *", 
                key=f"edu_inst_{i}", 
                value=current_data.get("institution", ""),
                placeholder="University of California"
            )
            deg = st.text_input(
                "Degree *", 
                key=f"edu_degree_{i}", 
                value=current_data.get("degree", ""),
                placeholder="Bachelor of Science"
            )
            fld = st.text_input(
                "Field of Study", 
                key=f"edu_field_{i}", 
                value=current_data.get("field", ""),
                placeholder="Computer Science"
            )

        with col2:
            s_val = current_data.get("start_date")
            e_val = current_data.get("end_date")
            
            def to_date(d_str):
                try: 
                    return datetime.strptime(d_str, "%Y-%m-%d").date()
                except: 
                    return date.today()

            start = st.date_input(
                "Start Date", 
                key=f"edu_start_{i}", 
                value=to_date(s_val) if s_val else date(2020, 1, 1)
            )
            end = st.date_input(
                "End Date", 
                key=f"edu_end_{i}", 
                value=to_date(e_val) if e_val else date.today()
            )
            gpa = st.text_input(
                "GPA (optional)", 
                key=f"edu_gpa_{i}", 
                value=current_data.get("gpa", ""),
                placeholder="3.8/4.0"
            )

        high = st.text_area(
            "Achievements & Honors", 
            key=f"edu_high_{i}", 
            value=current_data.get("highlights", ""),
            placeholder="Dean's List, Relevant coursework, Awards...",
            height=100
        )

        education_entries.append({
            "institution": inst,
            "degree": deg,
            "field": fld,
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "gpa": gpa,
            "highlights": high,
        })

st.divider()

col1, col2, col3, col4 = st.columns([1.5, 2, 2, 1.5], gap="small")

with col1:
    if st.button(":material/arrow_left_alt: Back", use_container_width=True, type="secondary"):
        StateManager.prev_step(1)

with col4:
    if st.button("Next :material/arrow_right_alt:", use_container_width=True, type="primary"):
        result = ResumeValidator.validate_education(education_entries)
        if not result.is_valid:
            StateManager.show_error_popup(result.errors)
        else:
            StateManager.next_step(1, {"education": education_entries})