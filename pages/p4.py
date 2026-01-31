import streamlit as st
from core.smanager import StateManager
from core.validator import ResumeValidator
from core.suggestions import SuggestionEngine
from datetime import date, datetime

StateManager.initialize()
st.set_page_config(page_title="Resume Generator - Projects", layout="wide")


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

StateManager.render_progress_bar(3)

st.title(":material/folder_open: Projects")
st.caption("Highlight your notable projects (Optional)")
st.divider()

# Sync counter
existing_projects = st.session_state.form_data.get("projects", [])
if "project_count" not in st.session_state:
    st.session_state.project_count = max(len(existing_projects), 1)
else:
    st.session_state.project_count = max(len(existing_projects), st.session_state.project_count)

# Add button
col_spacer, col_add = st.columns([4, 1])
with col_add:
    if st.button(":material/add: Add", use_container_width=True, type="secondary"):
        st.session_state.project_count += 1
        st.rerun()

st.write("")  

project_entries = []

for i in range(st.session_state.project_count):
    current = existing_projects[i] if i < len(existing_projects) else {}
    
    with st.expander(
        f":material/rocket_launch: Project #{i+1}: {current.get('name', 'New Entry')}", 
        expanded=(i == st.session_state.project_count - 1)
    ):
        if st.session_state.project_count > 1:
            if st.button(
                f":material/delete: Remove Project #{i+1}", 
                key=f"remove_proj_{i}", 
                type="secondary"
            ):
                StateManager.remove_item("projects", i)
                st.session_state.project_count -= 1
                st.rerun()
            st.write("")

        name = st.text_input(
            "Project Name *", 
            key=f"proj_name_{i}", 
            value=current.get("name", ""),
            placeholder="E-commerce Platform"
        )
        
        col1, col2 = st.columns(2, gap="medium")
        
        with col1:
            d_val = current.get("date")
            try: 
                default_d = datetime.strptime(str(d_val), "%Y-%m-%d").date()
            except: 
                default_d = date.today()
            
            proj_date = st.date_input(
                "Completion Date", 
                key=f"proj_date_{i}", 
                value=default_d
            )
        
        with col2:
            url = st.text_input(
                "Project URL (optional)", 
                key=f"proj_url_{i}", 
                value=current.get("url", ""),
                placeholder="github.com/username/project"
            )
            
        desc = st.text_area(
            "Description & Technologies", 
            key=f"proj_desc_{i}", 
            value=current.get("description", ""),
            placeholder="Built a full-stack e-commerce platform using React, Node.js, and MongoDB...",
            height=120
        )

        project_entries.append({
            "name": name,
            "date": proj_date.isoformat(),
            "url": url,
            "description": desc
        })

st.divider()

# Navigation buttons
col1, col2, col3 = st.columns([1.5, 2.5, 1.5], gap="small")

with col1:
    if st.button(":material/arrow_left_alt: Back", use_container_width=True, type="secondary"): 
        StateManager.prev_step(3)

with col2:
    if st.button(":material/lightbulb: Get Suggestions", use_container_width=True, type="secondary"):
        suggestions_md = SuggestionEngine.analyze_projects(project_entries)
        StateManager.show_suggestions(suggestions_md)

with col3:
    if st.button("Next :material/arrow_right_alt:", use_container_width=True, type="primary"):
        result = ResumeValidator.validate_projects(project_entries)
        if not result.is_valid:
            StateManager.show_error_popup(result.errors)
        else:
            StateManager.next_step(3, {"projects": project_entries})