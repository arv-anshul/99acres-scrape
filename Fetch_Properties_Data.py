import asyncio
import json
from pathlib import Path

import pandas as pd
import streamlit as st
from streamlit.elements.lib.mutable_status_container import StatusContainer

from src import utils
from src.components import convert, fetch
from src.database.city_w_id import CITY_W_ID_PATH, save_city_w_id_dict
from src.logger import get_logger
from src.utils import SRP_DATA_COLUMNS, DFPath

st.set_page_config('Scrape 99Acres', '🏠')
st_msg = st.container()
logger = get_logger(__name__)

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

    want_whole_data = st.checkbox(
        '📦 Fetch whole data!',
        value=False,
        help='You will get all the fetched data without filtering.',
    )

    form_submitted = st.form_submit_button(use_container_width=True)

if not form_submitted:
    st.subheader('Scrape 99acres.com in one click. Get data of any city listed on the website.')

    if DFPath.SRP.exists():
        st_msg.error('Please delete the previous scrapped data.')
        st.download_button(
            label='Download Previous Scrapped Data',
            data=DFPath.SRP.read_text(),
            file_name='real_estate_previous_data.csv',
            mime='.csv',
            on_click=delete_previous_data,
            args=(DFPath.SRP,),
            type='primary',
            use_container_width=True,
        )
        st.button(
            'Delete Previous Data',
            on_click=delete_previous_data,
            args=(DFPath.SRP,),
            use_container_width=True,
        )

    st.stop()

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
# Scrapping starts
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
page_nums = range(int(from_page), int(to_page))

if city_id is None:
    st.exception(ValueError('Please select a proper city.'))
    st.stop()
    raise

if not city_id.isnumeric():
    st.exception(ValueError('Problem with City ID.'))
    st.stop()


async def fetch_raw_data():
    responses = await fetch.fetch_all_responses(
        list(page_nums), int(prop_per_page), city_id=int(city_id)
    )
    data = await convert.filter_batch_response(responses)
    return pd.DataFrame(data['srp'])


async def merge_existing_data(df: pd.DataFrame) -> pd.DataFrame:
    if DFPath.SRP.exists():
        old_df = pd.read_csv(DFPath.SRP)
        status.write(f'🗂️ :orange[Shape of stored data:] **{old_df.shape}**')
        df = pd.concat([old_df, df])

    df = await utils.drop_duplicates(df)
    return df


async def store_df(status: StatusContainer):
    df = await fetch_raw_data()

    status.write('😎 :orange[Data has been scrapped!]')
    status.write(f'🧩 :green[Shape of scrapped data:] **{df.shape}**')

    if not want_whole_data:
        status.write('🗑️ Filter the data and keep only required columns.')
        df = df[list(set(df.columns) & set(SRP_DATA_COLUMNS))]
        status.write(f'🧩 :green[Shape after filtering:] **{df.shape}**')
    else:
        status.write('❌ :red[Filtering on fetched data not applied.]')

    df = await merge_existing_data(df)
    status.write(f'🥳 :violet[We have total scrapped data shape:] **{df.shape}**')

    status.write(f'🌐 :blue[Storing the data at] "{DFPath.SRP}"')
    df.to_csv(DFPath.SRP, index=False)


with st.status('🎉 Scrapping process starts!', expanded=True) as status:
    asyncio.run(store_df(status))
    status.update(
        label=f'🥳 **We scrapped :red[{city_with_id[city_id]}] city properties data.**',
        expanded=True,
        state='complete',
    )


if st.download_button(
    label='Download Scrapped Data',
    data=DFPath.SRP.read_text(),
    file_name=f'real_estate_{city_with_id[city_id]}.csv',
    mime='.csv',
    type='primary',
    use_container_width=True,
):
    st.balloons()
