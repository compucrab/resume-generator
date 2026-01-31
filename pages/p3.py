import streamlit as st
from core.smanager import StateManager
from core.validator import ResumeValidator
from core.suggestions import SuggestionEngine
from datetime import date, datetime

StateManager.initialize()
st.set_page_config(page_title="Resume Generator - Experience", layout="wide")

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

StateManager.render_progress_bar(2)

st.title(":material/work: Work Experience")
st.caption("Showcase your professional journey")
st.divider()

existing_exp = st.session_state.form_data.get("experience", [])
if "experience_count" not in st.session_state:
    st.session_state.experience_count = max(len(existing_exp), 1)
else:
    st.session_state.experience_count = max(len(existing_exp), st.session_state.experience_count)

col_spacer, col_add = st.columns([4, 1])
with col_add:
    if st.button(":material/add: Add", use_container_width=True, type="secondary"):
        st.session_state.experience_count += 1
        st.rerun()

st.write("")

experience_entries = []

for i in range(st.session_state.experience_count):
    current_data = existing_exp[i] if i < len(existing_exp) else {}
    
    with st.expander(
        f":material/work: Experience #{i+1}: {current_data.get('position', 'New Entry')}", 
        expanded=(i == st.session_state.experience_count - 1)
    ):
        if st.session_state.experience_count > 1:
            if st.button(
                f":material/delete: Remove Entry #{i+1}", 
                key=f"remove_exp_{i}", 
                type="secondary"
            ):
                StateManager.remove_item("experience", i)
                st.session_state.experience_count -= 1
                st.rerun()
            st.write("")  

        col1, col2 = st.columns(2, gap="medium")

        with col1:
            company = st.text_input(
                "Company *", 
                key=f"exp_company_{i}", 
                value=current_data.get("company", ""),
                placeholder="Acme Corporation"
            )
            position = st.text_input(
                "Position *", 
                key=f"exp_position_{i}", 
                value=current_data.get("position", ""),
                placeholder="Senior Software Engineer"
            )
            location = st.text_input(
                "Location", 
                key=f"exp_location_{i}", 
                value=current_data.get("location", ""),
                placeholder="San Francisco, CA"
            )

        with col2:
            def to_date(d_str):
                try: 
                    return datetime.strptime(d_str, "%Y-%m-%d").date()
                except: 
                    return date.today()

            start = st.date_input(
                "Start Date", 
                key=f"exp_start_{i}", 
                value=to_date(current_data.get("start_date"))
            )
            end = st.date_input(
                "End Date", 
                key=f"exp_end_{i}", 
                value=to_date(current_data.get("end_date"))
            )
            
            st.write("")

        highlights = st.text_area(
            "Key Achievements & Responsibilities", 
            key=f"exp_high_{i}", 
            value=current_data.get("highlights", ""),
            placeholder="• Led team of 5 engineers\n• Increased system performance by 40%\n• Developed microservices architecture",
            height=150
        )

        experience_entries.append({
            "company": company,
            "position": position,
            "location": location,
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "highlights": highlights,
        })

st.divider()

col1, col2, col3 = st.columns([1.5, 2.5, 1.5], gap="small")

with col1:
    if st.button(":material/arrow_left_alt: Back", use_container_width=True, type="secondary"):
        StateManager.prev_step(2)

with col2:
    if st.button(":material/lightbulb: Get Suggestions", use_container_width=True, type="secondary"):
        suggestions_md = SuggestionEngine.analyze_experience(experience_entries)
        StateManager.show_suggestions(suggestions_md)

with col3:
    if st.button("Next :material/arrow_right_alt:", use_container_width=True, type="primary"):
        result = ResumeValidator.validate_experience(experience_entries)
        if not result.is_valid:
            StateManager.show_error_popup(result.errors)
        else:
            StateManager.next_step(2, {"experience": experience_entries})