import streamlit as st
import numpy as np
import pandas as pd
import rongzi

def phrase():
    st.title("Phrase exploration")

    def load_chengyus() -> pd.DataFrame:
        """Get dataframe of chengyu data"""
        chengyus = pd.read_csv('./assets/chengyu.tsv', sep='\t').set_index('Proverb')
        cols = ['Literal Meaning', 'Figurative Meaning', 'Pinyin']
        chengyus = chengyus[cols]
        return chengyus
    
    def choose_input_method() -> tuple[str, list[str]]:
        """User decides how to get the chinese character components: random or user-input"""
        
        input_methods = ['Random proverb', 'Type a Chinese phrase in yourself']
        
        input_methods_prompt = "Choose a Chinese phrase by one of two methods"
        input_method = st.radio(input_methods_prompt, input_methods)
        st.markdown(f'---\n')
        
        return input_method, input_methods

    def get_phrase() -> str:
        """
            based on the selected input method:
                - populate subsequent sections of the page
                - return the phrase as string p
        """
        
        def refresh_page():
            "refresh page, to get a new random chengyu"
            st.experimental_singleton.clear()
            return None
        
        # get random chengyu
        if input_method == input_methods[0]: 
            p = np.random.choice(chengyus.index)
            label = 'Pick a new proverb.'
            st.button(label, refresh_page())    
        
        # get user-input phrase
        if input_method == input_methods[1]:
            label = 'Enter a name or proverb in Chinese characters,\nmaximum 7 characters:'
            p = st.text_input(label, max_chars=7)
            
        return p

    def show_alternative_paths(df:pd.DataFrame):
        "Display alternative paths as dataframe results"
        st.markdown("#### Alternative paths between each character in the phrase.")
        st.markdown(df.to_markdown(index=False))
        return None
    
    chengyus = load_chengyus()
    input_method, input_methods = choose_input_method()
    p = get_phrase()
    
    # Perform the component path optimization
    rz = rongzi.RongZi()
    df = rz.analyze_sequence(p)
    
    # show phrase
    st.markdown(f"## {p}")

    # show translation of chengyu (if it's a chengyu)
    if input_method == input_methods[0]: 
        chengyu = chengyus.loc[p]
        chengyu = "**"+chengyu.index+"**: " + chengyu
        chengyu = '  \n'.join(chengyu)
        st.markdown(chengyu)        

    # TODO: PUT THIS IN A "DETAILS" DROP-DOWN
    show_alternative_paths(df)

def family_tree():
    st.title("Family-Tree Graph Visualization")
    rz = rongzi.RongZi('好')
    rz.get_vertical_family_tree()
    st.graphviz_chart(rz.vert_tree)

linkback_markdown = """
    ## Back to the [rongzi github page](http://github.com/bhrdj/rongzi).
    ---
    # rongzi app demo
    """

traditional_chars_disclaimer = """
    \n*App currently prioritizes "Traditional" character components as found in Taiwan (ROC). Adding Simplified characters as found in Mainland China (PRC) is currently under construction.*"""


def main():
    st.sidebar.markdown(linkback_markdown)
    page_titles = ["Proverb Exploration","Family-Tree Graph Visualization"]
    page = st.sidebar.radio('', page_titles, index=1)
    st.sidebar.markdown('')
    st.sidebar.markdown(traditional_chars_disclaimer)
    if page == page_titles[0]:
        phrase()
    elif page == page_titles[1]:
        family_tree()

if __name__ == "__main__":
    main()

