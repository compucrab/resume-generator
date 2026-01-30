import streamlit as st
from core.smanager import StateManager
from core.generator import Generator

import os
from datetime import datetime

StateManager.initialize()

st.header("Custom Sections")
st.info("Add additional sections like Certifications, Awards, Publications, etc.")

existing_custom = st.session_state.get("form_data", {}).get("custom_sections", [])

if "custom_count" not in st.session_state:
    st.session_state.custom_count = max(len(existing_custom), 0)

if st.button("➕ Add Custom Section", key="add_custom_btn"):
    st.session_state.custom_count += 1
    st.rerun()

custom_sections_data = []

for i in range(st.session_state.custom_count):
    current = existing_custom[i] if i < len(existing_custom) else {}
    
    with st.expander(f"✨ Section #{i+1}: {current.get('title', 'New Section')}", expanded=True):
        # --- REMOVAL LOGIC ---
        if st.button(f"Remove Section #{i+1}", key=f"remove_custom_{i}", type="secondary", icon=":material/delete:"):
            StateManager.remove_item("custom_sections", i)
            st.session_state.custom_count = max(0, st.session_state.custom_count - 1)
            st.rerun()

        section_title = st.text_input(
            "Section Title",
            key=f"custom_title_{i}",
            value=current.get("title", ""),
            placeholder="e.g., Certifications",
        )
        
        section_content = st.text_area(
            "Content",
            key=f"custom_content_{i}",
            value=current.get("content", ""),
            placeholder="AWS Certified Solutions Architect\nGoogle Cloud Professional",
            height=150,
        )

        custom_sections_data.append({
            "title": section_title,
            "content": section_content
        })

st.divider()

if st.button("🚀 Generate PDF Resume", type="primary", use_container_width=True):
    # ... validation logic ...
    with st.spinner("AI is crafting your PDF..."):
        st.session_state.form_data["custom_sections"] = custom_sections_data
        
        pdf_path, error = Generator.generate_pdf(st.session_state.form_data)
        
        if error:
            st.error(f"Generation failed: {error}")
        elif pdf_path and os.path.exists(pdf_path):
            st.success("Resume Generated Successfully!")
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="Click here to Download PDF",
                    data=f,
                    file_name=f"Resume_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )