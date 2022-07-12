from utils import *
import streamlit as st

junk_chars = ['"', "'", "</p>", "<jats:p>", "<p>",  '</italic>', '<italic>', '</jats:bold>']

st.title("The Poetry Machine")

#c1, c2 = st.columns(2)

#with c1:
text_in = st.text_input("Poetry Subject")
#with c2:
    #number_words = st.slider("Poem Length", 1, 80)
go_button = st.button("Compose")



if go_button:
    poem, title = generate_poem(text_in, np.random.randint(4,60))
    for c in junk_chars:
        poem = poem.replace(c, "")

    poem = poem.capitalize()
    poem = poem.strip()
    poem += "."
    title = title.capitalize()
    st.header(title)
    st.text(poem)
    st.download_button("Download Poem", poem, f'{title}.txt')