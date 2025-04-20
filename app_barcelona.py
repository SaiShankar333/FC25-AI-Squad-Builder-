
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from data_loader import load_player_data
from formation_engine import select_best_11_and_bench
from PIL import Image
import base64

st.set_page_config(layout="wide")
st.title("FC Barcelona: Best XI Recommender")

formation_options = [
    "4-3-3", "4-4-2", "3-5-2", "4-2-3-1", "5-3-2",
    "3-4-3", "4-1-4-1", "4-5-1", "4-3-1-2", "4-2-2-2"
]

st.sidebar.markdown("### Available Formations")
for f in formation_options:
    st.sidebar.markdown(f"- " + f)

formation = st.sidebar.selectbox("Select Formation", formation_options)

players = load_player_data("Barcelona/barcelona.json")
best_xi, subs = select_best_11_and_bench(players, formation)

# Crest centered at top
crest = Image.open("Barcelona/barcelona_crest.webp")
st.image(crest, width=150, caption="FC Barcelona")

# Player rendering block (including manager style)
def render_player_block(player, team_folder, image_size=100, override_name=None, override_pos=None, override_ovr=None, img_file=None):
    if player is None:
        return "<div style='display:inline-block; width:120px; text-align:center;'>No player</div>"

    name = override_name or player["Name"]
    position = override_pos or (player.get("Position", "") if isinstance(player["Position"], str) else player["Position"][0])
    ovr = override_ovr or player["OVR"]

    image_path = img_file or os.path.join(team_folder, "Potraits", name.replace(" ", "_") + ".webp")

    image_html = ""
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_f:
            img_bytes = img_f.read()
            encoded = base64.b64encode(img_bytes).decode()
            image_html = f"<img src='data:image/webp;base64,{encoded}' width='{image_size}'><br>"

    return (
        f"<div style='display:inline-block; width:120px; text-align:center; margin:10px;'>"
        f"{image_html}"
        f"<strong>{name}</strong><br>"
        f"OVR: {ovr}<br>"
        f"{position}"
        f"</div>"
    )

# Render Starting XI
st.markdown("## Starting XI")
for row in best_xi:
    html_row = "".join([render_player_block(p, "Barcelona") for p in row])
    st.markdown(f"<div style='text-align:center'>{html_row}</div>", unsafe_allow_html=True)

# Render Substitutes
st.markdown("## Substitutes")
html_subs = "".join([render_player_block(p, "Barcelona", image_size=90) for p in subs])
st.markdown(f"<div style='text-align:center'>{html_subs}</div>", unsafe_allow_html=True)

# Add Manager as 8th 'sub'
manager_html = render_player_block(
    player={"Name": "Hans-Dieter Flick", "OVR": "--", "Position": "Manager"},
    team_folder="Barcelona",
    image_size=90,
    override_name="Hans-Dieter Flick",
    override_pos="Manager",
    override_ovr="--",
    img_file="Barcelona/manager.webp"
)
st.markdown(f"<div style='text-align:center'>{manager_html}</div>", unsafe_allow_html=True)
