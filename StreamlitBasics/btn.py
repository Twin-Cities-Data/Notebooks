import streamlit as st

st.code("""
import streamlit as st
btn=st.button('yo')
if st.button('reset'):
    btn=False
btn""",language="python")

btn=st.button('yo')
if st.button('reset'):
    btn=False
btn
