import asyncio
import json
from warnings import filterwarnings

import pandas as pd
import streamlit as st
from streamlit.elements.lib.mutable_status_container import StatusContainer

from src import fetch
from src.constants import CITY_W_ID_PATH, SRP_CSV_PATH
from src.logger import get_logger
from src.utils import SRP_DATA_COLUMNS

filterwarnings("ignore", category=pd.errors.DtypeWarning)

st.set_page_config("Fetch Properties Data", "🏠", "wide")
st_msg = st.container()
logger = get_logger(__name__)

st.header(":red[🏠 Fetch Real Estate Properties Data from] :blue[99acres.com]")

with CITY_W_ID_PATH.open() as f:
    CITY_W_ID: dict[str, str] = json.load(f)


with st.form("fetch_data_from_99acres"):
    l, r = st.columns(2)
    from_page = l.number_input("📄 From Page", min_value=1, value=1, format="%d")
    to_page = r.number_input("📄 To Page", min_value=1, value=2, format="%d")

    prop_per_page = st.number_input(
        "🏠 Properties per Page",
        min_value=25,
        max_value=100,
        value=50,
        format="%d",
        help="No. of properties per page! (Max. 50)",
    )

    city_id = st.selectbox(
        "🌇 **Select City**",
        options=CITY_W_ID.keys(),
        format_func=lambda x: CITY_W_ID[x],
        help="These cities are listed on 99acres.com",
    )

    want_whole_data = st.checkbox(
        "📦 Fetch Whole Data!",
        value=False,
        help="You will get all the fetched data without filtering.",
    )

    form_submitted = st.form_submit_button(
        "**Fetch Properties Data**", use_container_width=True, type="primary"
    )

if not form_submitted:
    if SRP_CSV_PATH.exists():
        st.download_button(
            label="🏡 :green[**Download Previous Scrapped Data**] 🏡",
            data=SRP_CSV_PATH.read_text(),
            file_name="real_estate_previous_data.csv",
            mime=".csv",
            on_click=SRP_CSV_PATH.unlink,
            use_container_width=True,
        )
        st.button(
            ":red[**Delete Previous Data**]",
            on_click=SRP_CSV_PATH.unlink,
            use_container_width=True,
        )
    st.stop()

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
# Scrapping starts
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
page_nums = range(int(from_page), int(to_page))

if city_id is None:
    st_msg.exception(ValueError("Please select a proper city."))
    st.stop()
    raise

if not city_id.isnumeric():
    st_msg.exception(ValueError("Problem with City ID."))
    st.stop()

if from_page > to_page:
    st_msg.exception(
        ValueError("📄 'From Page' field must be lesser than 'To Page' field.")
    )
    st.stop()


async def fetch_raw_data():
    responses = await fetch.fetch_all_responses(
        list(page_nums), int(prop_per_page), city_id=int(city_id), status=status
    )
    data = [j for i in responses for j in i["properties"] if "PROP_ID" in j]
    logger.info(f"Shape of data after gathering SRP: {len(data)}")
    return pd.DataFrame(data)


async def clean_raw_data(df: pd.DataFrame) -> pd.DataFrame:
    if "DESCRIPTION" in df.columns:
        df["DESCRIPTION"] = df["DESCRIPTION"].str.replace("\n", " ")
    return df


async def merge_existing_data(df: pd.DataFrame) -> pd.DataFrame:
    if SRP_CSV_PATH.exists():
        old_df = pd.read_csv(SRP_CSV_PATH)
        status.write(f"🗂️ :orange[Shape of stored data:] **{old_df.shape}**")
        df = pd.concat([old_df, df])

    if _ := df.duplicated("PROP_ID").sum():
        status.write(f"🔥 :red[Dropping **{_}** duplicated data.]")

    logger.warning("Drop %s rows.", df.duplicated(["PROP_ID"]).sum())
    df = df.drop_duplicates(["PROP_ID"], keep="last")
    return df


async def store_df(status: StatusContainer):
    df = await fetch_raw_data()
    status.write("😎 :orange[Data has been scrapped!]")
    status.write(f"🧩 :green[Shape of scrapped data:] **{df.shape}**")

    df = await clean_raw_data(df)
    status.write("🧹 :orange[Data cleaning done!]")

    if not want_whole_data:
        status.write("🗑️ :gray[Filtered the data to keep only required columns.]")
        df = df[list(set(df.columns) & set(SRP_DATA_COLUMNS))]
        status.write(f"🧩 :green[Shape after filtering:] **{df.shape}**")
    else:
        status.write("❌ :red[Filtering on fetched data not applied.]")

    df = await merge_existing_data(df)
    status.write(f"🥳 :violet[We have total scrapped data shape:] **{df.shape}**")

    status.write(f'🌐 :blue[Storing the data at] "{SRP_CSV_PATH}"')
    df.to_csv(SRP_CSV_PATH, index=False)


with st.status("🎉 Scrapping process starts!", expanded=True) as status:
    asyncio.run(store_df(status))
    status.update(
        label=f"🥳 **We scrapped :red[{CITY_W_ID[city_id]}] city properties data.**",
        expanded=True,
        state="complete",
    )


if st.download_button(
    label="Download Scrapped Data",
    data=SRP_CSV_PATH.read_text(),
    file_name=f"real_estate_{CITY_W_ID[city_id]}.csv",
    mime=".csv",
    type="primary",
    use_container_width=True,
):
    st.balloons()
