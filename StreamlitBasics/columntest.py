import streamlit as st
st.code("""
import streamlit as st
left, middle, right = st.columns(3, border=True)

left.markdown("Lorem ipsum " * 10)
middle.markdown("Lorem ipsum " * 5)
right.markdown("Lorem ipsum ")

btml, btmr = st.columns(2, border=True)

with btml:
    st.markdown("lorry lipdum"*9)
with btmr:
    st.markdown("mo text"*10)
""")
left, middle, right = st.columns(3, border=True)

left.markdown("Lorem ipsum " * 10)
middle.markdown("Lorem ipsum " * 5)
right.markdown("Lorem ipsum ")

btml, btmr = st.columns(2, border=True)

with btml:
    st.markdown("lorry lipdum"*9)
with btmr:
    st.markdown("mo text"*10)
    
