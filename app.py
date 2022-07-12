from utils import *
import streamlit as st

junk_chars = ['"', "'", "</p>", "<jats:p>", "<p>",  '</italic>', '<italic>', '</jats:bold>', '</jats:p>', '<jats:title>', '</jats:title>', '<jats:italic>', "(", ")"]

st.title("The Poetry Machine")

#c1, c2 = st.columns(2)

#with c1:
text_in = st.text_input("Poetry Subject")
#with c2:
    #number_words = st.slider("Poem Length", 1, 80)
go_button = st.button("Compose")



if go_button:
    poem, title = generate_poem(text_in, np.random.randint(4,40))
    for c in junk_chars:
        poem = poem.replace(c, "")
    poem = poem.capitalize()
    poem = poem.strip()
    poem += "."
    title = title.capitalize()
    title_md = f'<p style="font-family:Times New Roman; font-size:2em;">{title}</p>'
    st.markdown(title_md, unsafe_allow_html = True)
    poem_md = poem.replace("\n", "<br />")
    poem_md = f'<p style="font-family:Times New Roman; font-size:12;">{poem_md}</p>'
    st.markdown(poem_md, unsafe_allow_html=True)
    st.download_button("Download Poem", poem, f'{title}.txt')
