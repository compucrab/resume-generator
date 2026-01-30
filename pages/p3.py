import streamlit as st
from core.smanager import StateManager
from core.validator import ResumeValidator
from datetime import date, datetime

StateManager.initialize()
st.set_page_config(page_title="Resume Generator - Experience", layout="wide")
StateManager.render_progress_bar(2)

st.title("Work Experience")

# Sync counter with existing data
existing_exp = st.session_state.form_data.get("experience", [])
if "experience_count" not in st.session_state:
    st.session_state.experience_count = max(len(existing_exp), 1)
else:
    st.session_state.experience_count = max(len(existing_exp), st.session_state.experience_count)

col_title, col_add = st.columns([3, 1])
with col_add:
    if st.button("Add Experience :material/add:", use_container_width=True):
        st.session_state.experience_count += 1
        st.rerun()

experience_entries = []

for i in range(st.session_state.experience_count):
    current_data = existing_exp[i] if i < len(existing_exp) else {}
    
    with st.expander(f"💼 Experience #{i+1}", expanded=(i == st.session_state.experience_count - 1)):
        # Removal UI
        if st.session_state.experience_count > 1:
            if st.button(f"Remove Entry #{i+1}", key=f"remove_exp_{i}", type="secondary", icon=":material/delete:"):
                StateManager.remove_item("experience", i)
                st.session_state.experience_count -= 1
                st.rerun()

        col1, col2 = st.columns(2)

        with col1:
            company = st.text_input("Company *", key=f"exp_company_{i}", 
                                   value=current_data.get("company", ""))
            position = st.text_input("Position *", key=f"exp_position_{i}", 
                                    value=current_data.get("position", ""))
            location = st.text_input("Location", key=f"exp_location_{i}", 
                                    value=current_data.get("location", ""))

        with col2:
            def to_date(d_str):
                try: return datetime.strptime(d_str, "%Y-%m-%d").date()
                except: return date.today()

            start = st.date_input("Start Date", key=f"exp_start_{i}", 
                                 value=to_date(current_data.get("start_date")))
            end = st.date_input("End Date", key=f"exp_end_{i}", 
                               value=to_date(current_data.get("end_date")))

        highlights = st.text_area("Key Achievements", key=f"exp_high_{i}", 
                                 value=current_data.get("highlights", ""), height=150)

        experience_entries.append({
            "company": company,
            "position": position,
            "location": location,
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "highlights": highlights,
        })

st.divider()
l_btn, spacer, r_btn = st.columns([1, 4, 1])

with l_btn:
    if st.button(":material/arrow_back: Back"):
        StateManager.prev_step(2)

with r_btn:
    if st.button("Next :material/arrow_forward:"):
        result = ResumeValidator.validate_experience(experience_entries)
        if not result.is_valid:
            StateManager.show_error_popup(result.errors)
        else:
            StateManager.next_step(2, {"experience": experience_entries})