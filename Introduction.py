import httpx
import streamlit as st

st.set_page_config('README.md', '🗒️', 'wide')


@st.cache_resource
def fetch_intro() -> str:
    url = (
        'https://raw.githubusercontent.com/wiki/arv-anshul/99acres-scrape'
        '/How-I-Approach-to-Create-this-App-using-Streamlit-and-Curler%3F.md'
    )
    with httpx.Client() as client:
        data = client.get(url)
        return data.text


st.header(
    ':red[🥳 How I Approach to Create this App using Streamlit and Curler?]',
    divider='red',
)
st.markdown(fetch_intro())
