import streamlit as st
from core.smanager import StateManager

p0 = st.Page("pages/home.py", title="Home", icon=":material/home:")
p1 = st.Page("pages/p1.py", title="Personal Information", icon=":material/person:")
p2 = st.Page("pages/p2.py", title="Education Details", icon=":material/school:")
p3 = st.Page("pages/p3.py", title="Work Experience", icon=":material/work:")
p4 = st.Page("pages/p4.py", title="Projects", icon=":material/rocket:")
p5 = st.Page("pages/p5.py", title="Finalize & Download", icon=":material/download:")

pg = st.navigation([p0, p1, p2, p3, p4, p5])
StateManager.initialize()
pg.run()