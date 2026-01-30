import streamlit as st
from core.smanager import StateManager
from core.validator import ResumeValidator
from datetime import date, datetime

StateManager.initialize()
st.set_page_config(page_title="Resume Generator - Education", layout="wide")
StateManager.render_progress_bar(1)

st.title("Education Details")

# Sync counter with existing data
existing_edu = st.session_state.form_data.get("education", [])
if "education_count" not in st.session_state:
    st.session_state.education_count = max(len(existing_edu), 1)
else:
    # Ensure count doesn't fall behind if items were added elsewhere
    st.session_state.education_count = max(len(existing_edu), st.session_state.education_count)

col_title, col_add = st.columns([3, 1])
with col_add:
    if st.button("Add Education :material/add:", use_container_width=True):
        st.session_state.education_count += 1
        st.rerun()

education_entries = []

for i in range(st.session_state.education_count):
    # Get current data if it exists for this index
    current_data = existing_edu[i] if i < len(existing_edu) else {}
    
    with st.expander(f"🎓 Education #{i+1}", expanded=(i == st.session_state.education_count - 1)):
        # Removal UI
        if st.session_state.education_count > 1:
            if st.button(f"Remove Entry #{i+1}", key=f"remove_edu_{i}", type="secondary", icon=":material/delete:"):
                StateManager.remove_item("education", i)
                st.session_state.education_count -= 1
                st.rerun()

        col1, col2 = st.columns(2)

        with col1:
            inst = st.text_input("Institution *", key=f"edu_inst_{i}", 
                                value=current_data.get("institution", ""))
            deg = st.text_input("Degree *", key=f"edu_degree_{i}", 
                               value=current_data.get("degree", ""))
            fld = st.text_input("Field of Study", key=f"edu_field_{i}", 
                               value=current_data.get("field", ""))

        with col2:
            s_val = current_data.get("start_date")
            e_val = current_data.get("end_date")
            
            def to_date(d_str):
                try: return datetime.strptime(d_str, "%Y-%m-%d").date()
                except: return date.today()

            start = st.date_input("Start Date", key=f"edu_start_{i}", 
                                 value=to_date(s_val) if s_val else date(2020, 1, 1))
            end = st.date_input("End Date", key=f"edu_end_{i}", 
                               value=to_date(e_val) if e_val else date.today())
            gpa = st.text_input("GPA (optional)", key=f"edu_gpa_{i}", 
                               value=current_data.get("gpa", ""))

        high = st.text_area("Achievements", key=f"edu_high_{i}", 
                           value=current_data.get("highlights", ""))

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
l_btn, spacer, r_btn = st.columns([1, 4, 1])

with l_btn:
    if st.button(":material/arrow_back: Back"):
        StateManager.prev_step(1)

with r_btn:
    if st.button("Next :material/arrow_forward:"):
        result = ResumeValidator.validate_education(education_entries)
        if not result.is_valid:
            StateManager.show_error_popup(result.errors)
        else:
            StateManager.next_step(1, {"education": education_entries})