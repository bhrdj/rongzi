import streamlit as st
import numpy as np
import pandas as pd
import rongzi

def cb():
    st.text('hello')

def proverb():
    st.title("Proverb exploration")
    input_methods_prompt = """Choose a Chinese phrase by one of two methods, and view the resulting component-by-component linkages."""
    input_methods = ['Random proverb',
                     'Type a Chinese phrase in yourself']
    
    st.markdown(f'### {input_methods_prompt}')
    input_method = st.radio('', input_methods)
    st.markdown(f'---\n')
    
    labels = ['Enter a name or proverb in Chinese characters,\nmaximum 7 characters:', '']
    chengyus = pd.read_csv('./assets/chengyu.tsv', sep='\t').set_index('Proverb')
    cols = ['Literal Meaning', 'Figurative Meaning', 'Pinyin']
    chengyus = chengyus[cols]
    
    def refresh_page():
        st.experimental_singleton.clear()

    def show_results(p):
        rz = rongzi.RongZi()
        df = rz.analyze_sequence(p)
        st.markdown(f"# {p}")
        st.markdown(df.to_markdown(index=False))
    
    if input_method == input_methods[0]:
        p = np.random.choice(chengyus.index)
        st.button('Pick a new proverb.', refresh_page())
        
    if input_method == input_methods[1]:
        p = st.text_input(label=labels[1], max_chars=7)

    show_results(p)
    if input_method == input_methods[0]:
        st.text('')
        st.text('')
        st.text('')
        chengyu = chengyus.loc[p]
        chengyu = "**"+chengyu.index+"**: " + chengyu
        chengyu = '  \n'.join(chengyu)
        st.markdown(chengyu)
    
    
def graph():
    st.title("graph visualization")
    st.markdown("""
    This is the next step.
    """)

linkback_md = """
## Back to the [rongzi github page](http://github.com/bhrdj/rongzi).
---
# rongzi app demo
"""
traditional_chars_disclaimer = '\n*App currently prioritizes "Traditional" character components as found in Taiwan. Adding Simplified characters as found in Mainland China is currently under construction.*'


def main():
    st.sidebar.markdown(linkback_md)
    page = st.sidebar.radio('',['Proverb exploration','Graph visualization'])
    st.sidebar.markdown('')
    st.sidebar.markdown(traditional_chars_disclaimer)
    if page == 'Proverb exploration':
        proverb()
    elif page == 'Graph visualization':
        graph()

if __name__ == "__main__":
    main()

