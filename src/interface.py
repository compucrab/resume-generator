import streamlit as st
from src.validator import ResumeValidator, PersonalInfo


class UI:
    def __init__(self) -> None:
        # Initialize the step counter
        if "active_step" not in st.session_state:
            st.session_state.active_step = 0

        # Initialize a dictionary to keep data when moving between pages
        if "form_data" not in st.session_state:
            st.session_state.form_data = {}

        st.title("AI powered Resume Generator")

        self.steps = [
            "Personal Info",
            "Education",
            "Experience",
            "Projects & Skills",
            "Custom Sections",
        ]

    def run(self):
        # Progress Bar / Step Indicator
        st.progress((st.session_state.active_step + 1) / len(self.steps))
        st.write(
            f"**Step {st.session_state.active_step + 1}: {self.steps[st.session_state.active_step]}**"
        )
        st.divider()

        # Routing logic (Which page to show?)
        if st.session_state.active_step == 0:
            self.render_personal_info()
        elif st.session_state.active_step == 1:
            self.render_education()
        elif st.session_state.active_step == 2:
            self.render_experience()

    def render_personal_info(self):
        col1, col2 = st.columns(2)
        with col1:
            # We use 'value=' to pull existing data if the user clicked 'Previous'
            name = str(
                st.text_input(
                    "Full Name *", value=st.session_state.form_data.get("name", "")
                )
            )
            email = str(
                st.text_input(
                    "Email *", value=st.session_state.form_data.get("email", "")
                )
            )
            phone = st.text_input(
                "Phone", value=st.session_state.form_data.get("phone", "")
            )
            location = st.text_input(
                "Location", value=st.session_state.form_data.get("location", "")
            )
        with col2:
            label = st.text_input(
                "Professional Title", value=st.session_state.form_data.get("label", "")
            )
            website = st.text_input(
                "Website", value=st.session_state.form_data.get("website", "")
            )
            linkedin = st.text_input(
                "LinkedIn", value=st.session_state.form_data.get("linkedin", "")
            )
            github = st.text_input(
                "GitHub", value=st.session_state.form_data.get("github", "")
            )

        summary = st.text_area(
            "Professional Summary",
            value=st.session_state.form_data.get("summary", ""),
            height=150,
        )

        # Navigation Buttons
        st.divider()
        _, next_col = st.columns([5, 1])

        if next_col.button("Next ➡️"):
            # 1. Collect and Map
            info = PersonalInfo(
                name=name,
                email=email,
                phone=phone,
                location=location,
                label=label,
                website=website,
                linkedin=linkedin,
                github=github,
                summary=summary,
            )
            # 2. Validate ONLY when Next is clicked
            result = ResumeValidator.validate_personal_info(info)

            if not result.is_valid:
                for error in result.errors:
                    st.error(f"**{error.field_name.title()}**: {error.message}")
            else:
                # 3. Save to state and Increment Step
                st.session_state.form_data.update(vars(info))
                st.session_state.active_step += 1
                st.rerun()  # Refresh to show next page

    def render_education(self):
        st.header("Education History")
        # Example input
        univ = st.text_input(
            "University Name", value=st.session_state.form_data.get("univ", "")
        )

        st.divider()
        prev_col, next_col = st.columns([1, 5])

        if prev_col.button("⬅️ Previous"):
            st.session_state.active_step -= 1
            st.rerun()

        if next_col.button("Next ➡️"):
            # Validation logic for Education would go here
            st.session_state.form_data["univ"] = univ
            st.session_state.active_step += 1
            st.rerun()

    def render_experience(self):
        st.header("Work Experience")
        # Navigation
        st.divider()
        if st.button("⬅️ Previous"):
            st.session_state.active_step -= 1
            st.rerun()


if __name__ == "__main__":
    ui = UI()
    ui.run()
