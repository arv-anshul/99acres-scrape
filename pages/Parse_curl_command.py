import json

import curler
import streamlit as st

from src.components.fetch import REQUESTS_PATH

st.set_page_config("Parse curl command", "🎱", "wide", "expanded")

st.header(":green[Parse your cURL command]", divider="green")
st_msg = st.container()

# A button to delete existing requests json file
if REQUESTS_PATH.exists():
    st.button(
        "**🔥 Delete existing cURL command 🔥**",
        on_click=REQUESTS_PATH.unlink,
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

example_curl_command = r"""curl 'https://www.99acres.com/api-aggregator/discovery/srp/search?property_type=1%2C4%2C3%2C2&class=O&area_unit=1&platform=DESKTOP&moduleName=GRAILS_SRP&workflow=GRAILS_SRP&page_size=25&page=1&city=8&preference=S&res_com=R&seoUrlType=DEFAULT&recomGroupType=VSP&pageName=SRP&groupByConfigurations=true&lazy=true' \
  -H 'authority: www.99acres.com' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'cache-control: no-cache' \
  -H 'dnt: 1' \
  -H 'pragma: no-cache' \
  -H 'referer: https://www.99acres.com/search/property/buy/gurgaon?city=8&preference=S&area_unit=1&res_com=R' \
  -H 'sec-ch-ua: "Chromium";v="117", "Not;A=Brand";v="8"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36' \
  --compressed"""

with st.form("curl_command"):
    command = st.text_area(
        "📋 Paste your copied cURL command here",
        value=example_curl_command,
        height=450,
        key="COMMAND",
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
with REQUESTS_PATH.open("w") as f:
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
