import streamlit as st
import numpy as np
import pandas as pd
import rongzi

rz = rongzi.RongZi()

def phrase():
    st.title("Phrase Path Visualization")

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
        if not df.empty:
            st.markdown("#### Alternative paths between each character in the phrase.")
            st.markdown(df.to_markdown(index=False))
        return None
    
    chengyus = load_chengyus()
    input_method, input_methods = choose_input_method()
    p = get_phrase()
    
    # Perform the component path optimization
    phrase_paths = rz.analyze_sequence(p)
    
    # show phrase
    st.markdown(f"## {p}")

    # show translation of chengyu (if it's a chengyu)
    if input_method == input_methods[0]: 
        chengyu = chengyus.loc[p]
        chengyu = "**"+chengyu.index+"**: " + chengyu
        chengyu = '  \n'.join(chengyu)
        st.markdown(chengyu)        

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
        def refresh_page():
            "refresh page, to get a new random character"
            st.experimental_singleton.clear()
            return None
        def remove_silently(l:list, c:str) -> list:
            try:
                return l.remove(c)
            except ValueError:
                return l
        
        # get random component with num_kids > 0 and num_parents >0
        while input_method == input_methods[0]:
            c = np.random.choice(rz.ccd.index)
            # only take a component with both kids and parents
            len_kids, len_parents = len(rz.get_kids(c)), len(remove_silently(rz.get_parents(c), c))  # FIX THIS !!!
            if any([len_kids==0, len_parents==0]) is True:
                continue
            label = 'Pick a new character.'
            st.button(label, refresh_page())
            break
        
        # get user-input phrase
        if input_method == input_methods[1]:
            label = 'Enter a single chinese character or component'
            c = st.text_input(label, max_chars=1)
        return c

    input_method, input_methods = choose_input_method()
    c = get_component()
    # c = '癟'
    
    max_sibs = 10
    too_many_kids = False
    if (c != ''):
        st.markdown(f"## {c}")
        tree_rz = rongzi.RongZi(c)
        excess_kids = tree_rz.get_vertical_family_tree(max_sibs)
        tree_rz.vert_tree.render(format='pdf', directory=directory)
    try:
        st.markdown(f'*Note: Some components in this tree are so common that they are present in more than {max_sibs} larger characters.'\
                    f'So, the descendants of the following list of characters: {excess_kids} were truncated to a maximum of {max_sibs} in this graph.*')
    except:
        pass

def test_graphviz_pdf():
    import streamlit as st
    import matplotlib.pyplot as plt
    from fpdf import FPDF
    import base64
    import numpy as np
    from tempfile import NamedTemporaryFile
    
    from sklearn.datasets import load_iris

    def create_download_link(val, filename):
        b64 = base64.b64encode(val)  # val looks like b'...'
        return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

    df = load_iris(as_frame=True)["data"]

    figs = []

    for col in df.columns:
        fig, ax = plt.subplots()
        ax.plot(df[col])
        st.pyplot(fig)
        figs.append(fig)

    export_as_pdf = st.button("Export Report")

    if export_as_pdf:
        pdf = FPDF()
        for fig in figs:
            pdf.add_page()
            with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                    fig.savefig(tmpfile.name)
                    pdf.image(tmpfile.name, 10, 10, 200, 100)
        html = create_download_link(pdf.output(dest="S").encode("latin-1"), "testfile")
        st.markdown(html, unsafe_allow_html=True)

        
linkback_markdown = """
    ## Back to the [rongzi github page](http://github.com/bhrdj/rongzi).
    ---
    # rongzi app demo
    """
traditional_chars_disclaimer = """
    \n*App currently mixes "Traditional" character components as found in Taiwan (ROC) and "Simplified" components as in Mainland China (PRC). Separation of the two is a feature on the TODO list.*"""

def main():
    st.sidebar.markdown(linkback_markdown)
    page_titles = ["Proverb Exploration","Family-Tree Graph Visualization", "test graphviz pdf download"]
    page = st.sidebar.radio('', page_titles, index=2)
    st.sidebar.markdown('')
    st.sidebar.markdown(traditional_chars_disclaimer)
    if page == page_titles[0]:
        phrase()
    elif page == page_titles[1]:
        family_tree()
    elif page == page_titles[2]:
        test_graphviz_pdf()

if __name__ == "__main__":
    main()

