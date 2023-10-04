import asyncio
import json
from pathlib import Path

import pandas as pd
import streamlit as st
from pydantic import ValidationError

from src.components import convert, fetch
from src.database import operation
from src.database.city_w_id import CITY_W_ID_PATH, save_city_w_id_dict
from src.database.operation import DFPath
from src.main import export_srp_df
from src.utils import ERRORED_DATA_PATH

st.set_page_config('Scrape 99Acres', '🏠')
msg = st.empty()

if not CITY_W_ID_PATH.exists():
    save_city_w_id_dict()

with open(CITY_W_ID_PATH) as f:
    city_with_id: dict[str, str] = json.load(f)


def delete_previous_data(path: Path) -> None:
    if path.exists():
        path.unlink()


with st.form('scrape_99acres'):
    st.title('Scrape 99Acres.com')

    l, r = st.columns(2)

    from_page = l.number_input('From Page', min_value=1, value=1, format='%d')
    to_page = r.number_input('To Page', min_value=1, value=2, format='%d')
    prop_per_page = st.number_input(
        'Property per page', min_value=25, max_value=100, value=50, format='%d'
    )

    city_id = st.selectbox(
        'Select City',
        options=city_with_id.keys(),
        format_func=lambda x: city_with_id[x],
    )
    drop_duplicates = st.checkbox('Drop duplicate data points.', value=True)
    want_raw_data = st.checkbox(
        '**Give me raw data!**',
        value=True,
        help="If checked then doesn't throw errors.",
    )

    form_submitted = st.form_submit_button(use_container_width=True)

if not form_submitted:
    st.subheader('Scrape 99acres.com in one click. Get data of any city listed on the website.')

    if DFPath.srp.exists():
        msg.error('Please delete the previous scrapped data.')
        st.download_button(
            label='Download Previous Scrapped Data',
            data=DFPath.srp.read_text(),
            file_name='real_estate_previous_data.csv',
            mime='.csv',
            on_click=delete_previous_data,
            args=(DFPath.srp,),
            type='primary',
            use_container_width=True,
        )
        st.button(
            'Delete Previous Data',
            on_click=delete_previous_data,
            args=(DFPath.srp,),
            use_container_width=True,
        )

    # Errored JSON data to download
    if ERRORED_DATA_PATH.exists():
        st.download_button(
            '**Download Validation Errored Data**',
            data=ERRORED_DATA_PATH.read_text(),
            file_name=ERRORED_DATA_PATH.name,
            mime=ERRORED_DATA_PATH.suffix,
            on_click=delete_previous_data,
            args=(ERRORED_DATA_PATH,),
            type='primary',
            use_container_width=True,
        )

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


async def fetch_raw_data():
    responses = await fetch.fetch_all_responses(
        list(page_nums),
        int(prop_per_page),
        city_id=int(city_id),  # type: ignore
    )
    data = await convert.filter_batch_response(responses)
    return await operation.drop_duplicates(pd.DataFrame(data['srp']))


with st.spinner():
    if want_raw_data:
        df = asyncio.run(fetch_raw_data())
        df.to_csv(DFPath.srp, index=False)
    else:
        try:
            asyncio.run(
                export_srp_df(
                    page_nums,
                    int(prop_per_page),
                    int(city_id),  # type: ignore
                )
            )
        except ValidationError as e:
            msg.info(
                "You city's data contains some validation error. "
                "You have to work with this data.",
                icon='🥹',
            )

            # Errored JSON data to download
            if ERRORED_DATA_PATH.exists():
                st.download_button(
                    '**Download Validation Errored Data**',
                    data=ERRORED_DATA_PATH.read_text(),
                    file_name=ERRORED_DATA_PATH.name,
                    mime=ERRORED_DATA_PATH.suffix,
                    on_click=delete_previous_data,
                    args=(ERRORED_DATA_PATH,),
                    type='primary',
                    use_container_width=True,
                )

            st.exception(e)
            st.stop()

if st.download_button(
    label='Download Scrapped Data',
    data=DFPath.srp.read_text(),
    file_name=f'real_estate_{city_with_id[city_id]}.csv',  # type: ignore
    mime='.csv',
    type='primary',
    use_container_width=True,
):
    st.balloons()
