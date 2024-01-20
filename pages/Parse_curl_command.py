import json

import curler
import streamlit as st

from src.constants import REQUESTS_JSON_PATH

st.set_page_config("Parse curl command", "🎱", "wide", "expanded")

st.header(":green[Parse your cURL command]", divider="green")
st_msg = st.container()

# A button to delete existing requests json file
if REQUESTS_JSON_PATH.exists():
    st.button(
        "**🔥 Delete existing cURL command 🔥**",
        on_click=REQUESTS_JSON_PATH.unlink,
        use_container_width=True,
    )

# Write why should you use curl command
with st.expander("🤔 **Why to use cURL?**"):
    st.markdown(
        """
        1. 🥳 cURL gives you flexibility to bypass the blocking by the website.
        2. 🧩 You can fetch the data which suits you best means you can fetch custom data.
        """
    )

with st.form("curl_command"):
    command = st.text_area(
        "📋 Paste your copied cURL command here",
        height=200,
    )
    submitted = st.form_submit_button(type="primary", use_container_width=True)

if not submitted:
    # Image to show "how to copy curl command?"
    st.columns([0.2, 0.6, 0.2])[1].image(
        "https://curlconverter.com/images/chrome@2x.webp",
        "💭 This is how you can copy curl command from the website.",
        use_column_width=True,
    )
    st.stop()

# If command is not passed.
if command is None:
    st_msg.error("App doesn't get the cURL command", icon="👎")
    st.stop()
    raise
else:
    command = command.replace("\\\n", " ")

# Parse the command and show the error if any occurred
try:
    parsed = curler.parse_curl(command)
except Exception as e:
    st_msg.error(e, icon="🫨")
    st.toast("Some Error Occurred!", icon="🐛")
    st.stop()
    raise

# Expander to see the parsed curl command
with st.expander("😎 See parsed cURL command!"):
    st.write(parsed)

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
# Store all the required data into `requests.json` file
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
with REQUESTS_JSON_PATH.open("w") as f:
    json.dump(
        {
            "url": parsed.url,
            "params": parsed.params,
            "headers": parsed.headers,
            "cookies": parsed.cookies,
        },
        f,
        indent=2,
    )
    st.toast(
        "cURL command stored in the app. Now you can fetch the custom data using this app.",
        icon="📦",
    )
    st.balloons()
