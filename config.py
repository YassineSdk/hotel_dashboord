
import streamlit as st
db_config = {
    "host":"localhost",
    "user":"root",
    "password":"2003",
    "database":"hotel_db"
    }

room_types = [
    {"type": "single", "image_url": "https://www.frasersproperty.com/content/dam/frasers-hospitality/english/properties/united-kingdom/south-kensington/park-international-hotel-south-kensington/images/gallery-images/rooms/room-type-main-images/single-room/PIHL_Single%20Room.jpg"},
    {"type": "double", "image_url": "https://www.pearlhotelnyc.com/hs-fs/hubfs/2.jpg?width=992&height=661&name=2.jpg"},
    {"type": "suite", "image_url": "https://www.maurya.com/wp-content/uploads/2017/09/Mithila-Suite-1.jpg"},
]

def reset_guest_form():
    st.session_state["input_name"] = ""
    st.session_state["input_mail"] = ""
    st.session_state["input_phone"] = ""
