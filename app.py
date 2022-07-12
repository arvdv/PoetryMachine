from utils import *
import streamlit as st


st.title("The Poetry Machine")

c1, c2 = st.columns(2)

with c1:
    text_in = st.text_input("Poetry Subject")
with c2:
    number_words = st.slider("Poem Length", 1, 80)
    go_button = st.button("Compose")


if go_button:
    st.write(generate_poem(text_in, number_words))