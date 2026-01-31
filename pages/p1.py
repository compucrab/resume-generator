import streamlit as st
from core.validator import ResumeValidator, PersonalInfo
from core.smanager import StateManager
from core.suggestions import SuggestionEngine

StateManager.initialize()
st.set_page_config(page_title="Resume Generator", layout="wide")

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

StateManager.render_progress_bar(0)

st.title(":material/add_notes: Personal Information")
st.caption("Let's start with your basic details")

formget = st.session_state.form_data.get

summary = st.text_area(
    "Professional Summary *", 
    value=formget("summary", ""), 
    height=120,
    placeholder="A brief overview of your professional background and key strengths..."
)

st.write("")

col1, col2 = st.columns(2, gap="medium")

with col1:
    name = st.text_input(
        "Full Name *", 
        value=formget("name", ""),
        placeholder="Your Name"
    )
    email = st.text_input(
        "Email *", 
        value=formget("email", ""),
        placeholder="name@example.com"
    )
    phone = st.text_input(
        "Phone *", 
        value=formget("phone", ""),
        placeholder="+91 1234567890"
    )

with col2:
    title = st.text_input(
        "Professional Title *", 
        value=formget("title", ""),
        placeholder="Senior Software Engineer"
    )
    location = st.text_input(
        "Location *", 
        value=formget("location", ""),
        placeholder="Jodhpur, Rajasthan"
    )
    website = st.text_input(
        "Website / LinkedIn", 
        value=formget("website", ""),
        placeholder="linkedin.com/in/name"
    )
    
st.divider()

col_sug, col_spacer, col_next = st.columns([2, 3, 1.5])

with col_sug:
    if st.button(":material/lightbulb: Get Suggestions", use_container_width=True, type="secondary"):
        current_data = {
            "name": str(name),
            "email": str(email),
            "phone": phone,
            "location": location,
            "title": title,
            "website": website,
            "summary": summary,
        }
        suggestions_md = SuggestionEngine.analyze_personal_info(current_data)
        StateManager.show_suggestions(suggestions_md)

with col_next:
    if st.button("Next :material/arrow_right_alt:", use_container_width=True, type="primary"):
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