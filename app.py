import asyncio
import json

import pandas as pd
import streamlit as st

from src.database.city_w_id import CITY_W_ID_PATH, save_city_w_id_dict
from src.database.operation import DFPath
from src.main import export_srp_df

st.set_page_config('Scrape 99Acres', '🏠')
msg = st.empty()

if not CITY_W_ID_PATH.exists():
    save_city_w_id_dict()

with open(CITY_W_ID_PATH) as f:
    city_with_id: dict[str, str] = json.load(f)


def delete_previous_data() -> None:
    path = DFPath.srp

    if path.exists():
        path.unlink()


with st.form('scrape_99acres'):
    st.title('Scrape 99Acres.com')

    l, r = st.columns(2)

    from_page = l.number_input('From Page', min_value=1, max_value=100, value=1, format='%d')
    to_page = r.number_input('To Page', min_value=1, max_value=100, value=2, format='%d')
    prop_per_page = st.number_input(
        'Property per page', min_value=30, max_value=1200, value=50, format='%d'
    )

    city_id = st.selectbox(
        'Select City',
        options=city_with_id.keys(),
        format_func=lambda x: city_with_id[x],
    )
    drop_duplicates = st.checkbox('Drop duplicate data points.', value=True)

    form_submitted = st.form_submit_button(use_container_width=True)

if not form_submitted:
    st.subheader('Scrape 99acres.com in one click. Get data of any city listed on the website.')

    if DFPath.srp.exists():
        msg.error('Please delete the previous scrapped data.')
        st.download_button(
            label='Download Previous Scrapped Data',
            data=pd.read_csv(DFPath.srp).to_csv(index=False),
            file_name='real_estate_previous_data.csv',
            mime='.csv',
            on_click=delete_previous_data,
            use_container_width=True,
        )
        st.button('Delete Previous Data', on_click=delete_previous_data, use_container_width=True)

    st.stop()

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
# Scrapping starts
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
page_nums = range(int(from_page), int(to_page))

try:
    if city_id is None:
        raise ValueError('Please select a proper city.')
    if not city_id.isnumeric():
        raise ValueError('Problem with City ID.')
except ValueError as e:
    msg.error(e)
    st.stop()

with st.spinner():
    asyncio.run(export_srp_df(page_nums, int(prop_per_page), int(city_id)))

if st.download_button(
    label='Download Scrapped Data',
    data=pd.read_csv(DFPath.srp).to_csv(index=False),
    file_name=f'real_estate_{city_with_id[city_id]}.csv',
    mime='.csv',
    use_container_width=True,
):
    st.balloons()
