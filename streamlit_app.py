import streamlit as st
import numpy as np
import pandas as pd
import rongzi
import graphviz
from fpdf import FPDF
import base64
from tempfile import NamedTemporaryFile

rz = rongzi.RongZi()

def phrase():
    st.title("Phrase Path Visualization")
    st.markdown('Like "six degrees of separation," for Chinese Characters.')
    st.markdown('---')
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
    
    def show_path_graph(phrase, pp:pd.DataFrame):
        if pp.empty:
            return None
        dot = rz.get_paths_graph(pp)
        st.graphviz_chart(dot)
        # export_graphviz_pdf(phrase, dot)
        
    def show_alternative_paths(pp:pd.DataFrame):
        "Display alternative paths as dataframe results"
        if pp.empty:
            return None
        st.markdown('---')
        st.markdown("#### Alternative paths between each character in the phrase.")
        st.markdown(pp.to_markdown(index=False))
        return None
    
    def show_chengyu_info():
        # show translation of chengyu (if it's a chengyu)
        if input_method == input_methods[0]: 
            chengyu = chengyus.loc[p]
            chengyu = "**"+chengyu.index+"**: " + chengyu
            chengyu = '  \n'.join(chengyu)
            st.markdown(chengyu)        
    
    chengyus = load_chengyus()
    input_method, input_methods = choose_input_method()
    p = get_phrase()
    
    phrase_paths = rz.analyze_sequence(p) # Optimize component path
    st.markdown(f"## {p}") # show phrase
    show_path_graph(p, phrase_paths) 
    show_chengyu_info() # only if user selected "random proverb"
    
    # TODO: PUT THIS IN A "DETAILS" DROP-DOWN
    show_alternative_paths(phrase_paths)

def family_tree():
    st.title("Single-Character Family-Tree Graph Visualization")
    
    def choose_input_method() -> tuple[str, list[str]]:
        """User decides how to get a single chinese character: random or user-input"""
        input_methods = ['Random character', 'Type a Chinese character in yourself']
        input_methods_prompt = "Choose a single Chinese character (or component) by one of two methods"
        input_method = st.radio(input_methods_prompt, input_methods)
        
        st.markdown(f'---\n')
        
        return input_method, input_methods
    
    def get_component() -> str:
        """
            based on the selected input method:
                - populate subsequent sections of the page
                - return the component as string c
        """
        def get_random_component(): 
            def refresh_page():
                "refresh page, to get a new random character"
                st.experimental_singleton.clear()
                return None
            def remove_silently(l:list, c:str) -> list:
                try:
                    return l.remove(c)
                except ValueError:
                    return l            
            
            c = ''
            # get random component with num_kids > 0 and num_parents >0
            while input_method == input_methods[0]:
                
                c = np.random.choice(rz.ccd.index)
                # only take a component with both kids and parents
                len_kids = len(rz.get_kids(c))
                len_parents = len(remove_silently(rz.get_parents(c), c))
                if any([len_kids==0, len_parents==0]) is True:
                    continue
                
                label = 'Pick a new character.'
                st.button(label, refresh_page())
                break
                
            return c
        
        c = get_random_component()
        
        if input_method == input_methods[1]:
            label = 'Enter a single chinese character or component'
            c = st.text_input(label, max_chars=1)
        
        return c

    input_method, input_methods = choose_input_method()
    c = get_component()
        
    max_sibs = 50
    excess_kids = False
    if (c != ''):
        st.markdown(f"## {c}")
        tree_rz = rongzi.RongZi(c)
        excess_kids = tree_rz.get_vertical_family_tree(max_sibs)
        # export_graphviz_pdf(f"family_tree_{c}", tree_rz.vert_tree)
        st.graphviz_chart(tree_rz.vert_tree)
    
    if excess_kids:
        st.markdown(f'*Note: Some components in this tree are so common that they are present in more than {max_sibs} larger characters. '\
                    f'So, the children of the following list of characters: {excess_kids} were truncated to a maximum of {max_sibs} in this graph.*')
    
def export_graphviz_pdf(filename:str, dot):
    # REMOVED THIS FUNCTION BECAUSE IT WASN'T WORKING YET ON STREAMLIT CLOUD
    #    (IT WAS WORKING ON STREAMLIT HOSTED ON MY AWS EC2 INSTANCE, 
    #     BUT LOCALLY-HOSTED STREAMLIT ONLY NATIVELY OFFERS HTTP, NOT HTTPS.)
    # THE ISSUE MAY HAVE HAD SOMETHING TO DO WITH GRAPHVIZ ITSELF NEEDING TO BE
    #    INSTALLED ON THE SERVER ITSELF, NOT JUST THE PYTHON GRAPHVIZ LIBRARY,
    #    FOR THE PDF EXPORT TO WORK RIGHT.
    # def _create_download_link(val, filename):
    #     b64 = base64.b64encode(val)  # val looks like b'...'
    #     return_str = f'''<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download pdf</a>  
    #     <i>(Pdf format may be easier to resize and view.)</i>'''
    #     return return_str

    # pdf = FPDF()
    # pdf.add_page()
    # with NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
    #     bytes_file = graphviz.pipe('dot', 'pdf', bytes(dot.source, 'utf-8'))
    #     html = _create_download_link(bytes_file, filename)
    #     st.markdown(html, unsafe_allow_html=True)
    pass

linkback_markdown = """
    #### links to:
    - My portfolio: [portfolio.bhrdwj.net](https://portfolio.bhrdwj.net)
    - This app's github: [github.com/bhrdj/rongzi](https://github.com/bhrdj/rongzi)
    ---
    # rongzi app demo
    """
todo_markdown = """
    TODO list:
    - App currently mixes "Traditional" character components as found in Taiwan (ROC) and "Simplified" components as in Mainland China (PRC). Alternative options for managing this aspect should be available.
    - Many components have very low use-frequency, and are nonetheless treated equivalently as more common characters. Prioritizing high-frequency characters and components when optimizing phrase-paths should be implemented.
    - For the Chinese-language-learner use-case, adding in example sentences using the proverbs would be helpful.
    """

def main():
    st.sidebar.markdown(linkback_markdown)
    page_titles = ["Proverb Exploration","Family-Tree Graph Visualization"]
    page = st.sidebar.radio('', page_titles, index=0)
    st.sidebar.markdown('')
    st.sidebar.markdown(traditional_chars_disclaimer)
    if page == page_titles[0]:
        phrase()
    elif page == page_titles[1]:
        family_tree()

if __name__ == "__main__":
    main()

