import streamlit as st
from streamlit_local_storage import LocalStorage
from typing import Optional


class StateManager:
    STEPS = ["Personal Info", "Education", "Experience", "Projects", "Skills"]
    ls: Optional[LocalStorage] = None

    @staticmethod
    def initialize():
        if StateManager.ls is None:
            StateManager.ls = LocalStorage()

        if "form_data" not in st.session_state:
            st.session_state.form_data = {}
        if "visited" not in st.session_state:
            st.session_state.visited = [False] * len(StateManager.STEPS)

        stored_data = StateManager.ls.getItem("resume_form_data")
        if stored_data and not st.session_state.form_data:
            st.session_state.form_data = stored_data
            st.session_state.visited = (
                StateManager.ls.getItem("resume_visited") or st.session_state.visited
            )

    @staticmethod
    def render_progress_bar(current_index: int):
        """Displays a progress bar and step indicator."""
        progress = (current_index + 1) / len(StateManager.STEPS)
        st.progress(progress)

        cols = st.columns(len(StateManager.STEPS))
        for i, step in enumerate(StateManager.STEPS):
            with cols[i]:
                if i < current_index:
                    st.caption(f"✅ {step}")
                elif i == current_index:
                    st.markdown(f"**🔵 {step}**")
                else:
                    st.caption(f"⚪ {step}")
        st.divider()

    @staticmethod
    def next_step(current_index: int, data: dict):
        # Update Session State
        for key, value in data.items():
            st.session_state.form_data[key] = value

        st.session_state.visited[current_index] = True

        if StateManager.ls:
            StateManager.ls.setItem(
                "resume_form_data", st.session_state.form_data, key="save_form"
            )

            StateManager.ls.setItem(
                "resume_visited", st.session_state.visited, key="save_visited"
            )

        next_idx = current_index + 1
        if next_idx < len(StateManager.STEPS):
            st.switch_page(StateManager.get_page_path(next_idx))

    @staticmethod
    def get_page_path(index: int) -> str:
        """Returns the file path for a specific step index."""
        return f"pages/p{index + 1}.py"

    @staticmethod
    def prev_step(current_index: int):
        """Moves to the previous page index or back to app.py if at p1."""
        if current_index == 0:
            st.switch_page("app.py")
        else:
            prev_idx = current_index - 1
            st.session_state.active_step = prev_idx
            st.switch_page(StateManager.get_page_path(prev_idx))

    @staticmethod
    @st.dialog("Validation Errors")
    def show_error_popup(errors):
        st.write("⚠️ Please fix these issues:")
        for error in errors:
            st.error(f"{error.message}")

    @staticmethod
    @st.dialog("AI Suggestions")
    def show_suggestions(markdown):
        st.markdown(markdown)

    @staticmethod
    def remove_item(category: str, index: int):
        """Removes an item from a list in form_data and updates storage."""
        if category in st.session_state.form_data:
            items = st.session_state.form_data[category]
            if 0 <= index < len(items):
                items.pop(index)
                st.session_state.form_data[category] = items

                # Update LocalStorage
                if StateManager.ls:
                    StateManager.ls.setItem(
                        "resume_form_data", st.session_state.form_data, key="save_form"
                    )
