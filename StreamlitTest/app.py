import ast
import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 5rem;
        padding-bottom: 0rem;
    }}
   
</style>
""",
        unsafe_allow_html=True,
    )


@st.cache
def get_layers(url):
    options = leafmap.get_wms_layers(url)
    return options


def app():
    st.subheader("Add Web Map Service (WMS)")
    
    # st.markdown(
    #     """
    # This app is a demonstration of loading Web Map Service (WMS) layers. Simply enter the URL of the WMS service 
    # in the text box below and press Enter to retrieve the layers. Go to https://apps.nationalmap.gov/services to find 
    # some WMS URLs if needed.
    # """
    # )

    row1_col1, row1_col2 = st.columns([3, 1.3])
    width = 800
    height = 600
    layers = None

    with row1_col2:

        esa_landcover = "https://services.terrascope.be/wms/v2"
        url = st.text_input(
            "Enter a WMS URL:", value="https://services.terrascope.be/wms/v2"
        )
        empty = st.empty()

        if url:
            options = get_layers(url)

            default = None
            if url == esa_landcover:
                default = "WORLDCOVER_2020_MAP"
            layers = empty.multiselect(
                "Select WMS layers to add to the map:", options, default=default
            )
            add_legend = st.checkbox("Add a legend to the map", value=True)
            if default == "WORLDCOVER_2020_MAP":
                legend = str(leafmap.builtin_legends["ESA_WorldCover"])
            else:
                legend = ""
            # if add_legend:
            #     legend_text = st.text_area(
            #         "Enter a legend as a dictionary {label: color}",
            #         value=legend,
            #         height=200,
            #     )

        with row1_col1:
            m = leafmap.Map(center=(36.3, 0), zoom=2)

            if layers is not None:
                for layer in layers:
                    m.add_wms_layer(
                        url, layers=layer, name=layer, attribution=" ", transparent=True
                    )
            if add_legend and legend:
                legend_dict = ast.literal_eval(legend)
                m.add_legend(legend_dict=legend_dict)

            m.to_streamlit(width, height)
            
app()            

