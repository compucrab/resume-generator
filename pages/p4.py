import streamlit as st
from core.smanager import StateManager
from core.validator import ResumeValidator
from datetime import date, datetime

# 1. Page Setup & State Sync
StateManager.initialize()
st.set_page_config(page_title="Resume Generator - Projects", layout="wide")
StateManager.render_progress_bar(3) # Index 3

st.title("Projects")

# 2. Dynamic Counter Setup (Synced with form_data)
existing_projects = st.session_state.form_data.get("projects", [])
if "project_count" not in st.session_state:
    st.session_state.project_count = max(len(existing_projects), 1)
else:
    # Ensure count reflects items potentially deleted or added in storage
    st.session_state.project_count = max(len(existing_projects), st.session_state.project_count)

# Header with Add Button
col_h, col_btn = st.columns([3, 1])
with col_btn:
    if st.button("➕ Add Project", use_container_width=True):
        st.session_state.project_count += 1
        st.rerun()

project_entries = []

# 3. Form Rendering
for i in range(st.session_state.project_count):
    # Fetch existing data for this index if it exists
    current = existing_projects[i] if i < len(existing_projects) else {}
    
    with st.expander(f"🚀 Project #{i+1}", expanded=(i == st.session_state.project_count - 1)):
        # --- REMOVAL LOGIC ---
        if st.session_state.project_count > 1:
            if st.button(f"Remove Project #{i+1}", key=f"remove_proj_{i}", type="secondary", icon=":material/delete:"):
                StateManager.remove_item("projects", i)
                st.session_state.project_count -= 1
                st.rerun()
        # ---------------------

        name = st.text_input("Project Name *", key=f"proj_name_{i}", value=current.get("name", ""))
        
        c1, c2 = st.columns(2)
        with c1:
            # Date Handling
            d_val = current.get("date")
            try: 
                default_d = datetime.strptime(str(d_val), "%Y-%m-%d").date()
            except: 
                default_d = date.today()
            proj_date = st.date_input("Completion Date", key=f"proj_date_{i}", value=default_d)
        
        with c2:
            url = st.text_input("Project URL (optional)", key=f"proj_url_{i}", value=current.get("url", ""))
            
        desc = st.text_area("Description", key=f"proj_desc_{i}", value=current.get("description", ""), height=100)

        project_entries.append({
            "name": name,
            "date": proj_date.isoformat(),
            "url": url,
            "description": desc
        })

st.divider()

# 4. Navigation
l_btn, spacer, r_btn = st.columns([1, 4, 1])
with l_btn:
    if st.button("Back"): 
        StateManager.prev_step(3)

with r_btn:
    if st.button("Next"):
        result = ResumeValidator.validate_projects(project_entries)
        if not result.is_valid:
            StateManager.show_error_popup(result.errors)
        else:
            # next_step handles LocalStorage setItem automatically
            StateManager.next_step(3, {"projects": project_entries})