import streamlit as st
from core.validator import ResumeValidator, PersonalInfo
from core.smanager import StateManager

StateManager.initialize()
st.set_page_config(page_title="Resume Generator", layout="wide")

StateManager.render_progress_bar(0)

st.title("Provide personal info")
st.divider()


formget = st.session_state.form_data.get
col1, col2 = st.columns(2)
summary = st.text_area("Professional Summary *", value=formget("summary", ""), height=150)

with col1:
    name = st.text_input("Full Name *", value=formget("name", ""))
    email = st.text_input("Email *", value=formget("email", ""))
    phone = st.text_input("Phone", value=formget("phone", ""))

with col2:
    title = st.text_input("Professional Title", value=formget("title", ""))
    website = st.text_input("Website", value=formget("website", ""))
    location = st.text_input("Location", value=formget("location", ""))
    
st.divider()

left_btn, spacer, right_btn = st.columns([2, 4, 1])

with left_btn:
    if st.button("Give suggestions", icon=":material/lightbulb_2:"):
        StateManager.show_suggestions("Hello")

with right_btn:
    if st.button("Next", icon=":material/arrow_forward:"):
        info = PersonalInfo(
            name=str(name),
            email=str(email),
            phone=phone,
            location=location,
            title=title,
            website=website,
            summary=summary,
        )
        result = ResumeValidator.validate_personal_info(info)

        if not result.is_valid:
                StateManager.show_error_popup(result.errors)
        else:
            StateManager.next_step(0, vars(info))