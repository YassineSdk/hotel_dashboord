import streamlit as st 
from config import room_types
import mysql.connector
from config import db_config
import re 
from guest import add_guest
from database import execute_query
from booking import get_avaible_room 
from booking import book_room 
from booking import get_avaible_metrics
from config import db_config
import pandas as pd 
import datetime as dt
import plotly.express as px
from config import reset_guest_form

#Data sources

conn = mysql.connector.connect(**db_config)

booking = pd.read_sql("SELECT * FROM bookings", con=conn)
guest = pd.read_sql("SELECT * FROM guests", con=conn)
query = """select b.id , b.guest_id , g.email ,r.type , b.check_in , b.check_out
        from bookings b
        join guests g on b.guest_id = g.id 
        join rooms r on b.room_id = r.id 
        order by b.check_in desc
    """
full_data= execute_query(query,fetch=True)
full_data = pd.DataFrame(full_data)

guest['active'] = guest['id'].apply(lambda x : "active" if x in booking['guest_id'].tolist() else "not active" )
rooms = pd.read_sql("select * from rooms", con=conn)
av_room =   get_avaible_metrics() 


st.set_page_config(layout='wide',page_title='Hotel managment',page_icon=":hotel:")
guest_id = None
tab1, tab2, tab3, tab4,tab5 = st.tabs(["🏠 Main", "👤 Guest Info", "🛏️ Booking", "📋 All Bookings","guests 👤"])
with tab1:
    st.subheader('performance dashbord')
    cols = st.columns(4)
    with cols[0]:
        st.container(border=True).metric('nombre des guests',guest['email'].count())
    with cols[1]:
        st.container(border=True).metric('nombre des reservation',booking['id'].count())
    with cols[2]:
        st.container(border=True).metric('nombre des rooms avaible for the next 2 days ',f'{av_room}/{rooms["number"].count()}')
    colss = st.columns(2)
    with colss[0]:
        data_1 = guest['active'].value_counts().reset_index()
        fig = px.pie(data_frame=data_1,
                    names='active',
                    values='count'
                    ,hole=0.4,
                    title="guest booking activity")
        with st.container(border=True) :              
            st.plotly_chart(fig,use_container_width=True)   
    with colss[1]:
        data_2 = full_data['type'].value_counts().reset_index().sort_values(by='count',ascending=True) 
        fig_1 = px.bar(data_frame=data_2,
                        x='type',
                        y='count',
                        title='booking by room type')
        fig_1.update_layout(yaxis=dict(showgrid=False))
        with st.container(border=True) :             
            st.plotly_chart(fig_1)                            


with tab2 :
    st.subheader('Step 1 : please enter the guest data')    
    st.divider()
    col_1 , col_2 = st.columns(2)
    with col_1 :
        name = st.text_input('full Name',max_chars=30,key="input_name")
        email = st.text_input('email address',max_chars=40,key="input_mail") 
        phone = st.text_input('phone number',max_chars=10,key="input_phone")
        button_SG = st.button(label="Save guest")
        clear = st.button(label='clear',on_click=reset_guest_form)
    with col_2 :
        st.image("https://img.freepik.com/vecteurs-libre/illustration-du-concept-reservation-hotel_114360-27117.jpg?ga=GA1.1.2098360286.1750543959&semt=ais_items_boosted&w=740", use_container_width="auto",width=400) 
    
    if button_SG:
        valid = True

        if not re.match(r"^\S+@\S+\.\S+$", str(email.strip())):
            st.error("❌ Invalid email address format.")
            valid = False

        if len(name.strip()) <= 5:
            st.error("❌ Name must be at least 5 characters long.")
            valid = False

        if not phone.isdigit() and len(phone.strip()) > 10:
            st.error("❌ Phone number must be at least 10 digits and numeric.")
            valid = False

        if valid:
            success, guest_id, msg = add_guest(name, email, phone)
            st.toast(msg)
            if success:
                st.success(f"✅ {msg} ID: {guest_id}")
                st.session_state['guest_id'] = guest_id
                st.session_state['booking_tab_active'] = True
                st.toast("➡️ Now go to the '🛏️ Booking' tab to continue.")
            else:
                if guest_id:
                    st.info(f"ℹ️ {msg} Proceeding with booking for guest ID: {guest_id}")
                    st.session_state['guest_id'] = guest_id
                    st.session_state['booking_tab_active'] = True
                    st.toast("➡️ Now go to the '🛏️ Booking' tab to continue.")
        else:
            st.write(f"❌ please fill in the data correctly")


    # Only show this if a guest was just added or found, not on every rerun
    if st.session_state.get('guest_id', None) and st.session_state.get('booking_tab_active', False):
        st.success("Guest is ready to book!")

with tab3:
    if st.session_state.get('booking_tab_active', False) and 'guest_id' in st.session_state:
        st.header("booking form")
        st.divider()
        result = execute_query("SELECT name FROM guests WHERE id = %s", (st.session_state['guest_id'],), fetch=True)
        name = result[0]['name'] 
        st.write(f"hi user {name}")
        col_1, col_2 = st.columns(2)
        with col_1:
            check_in = st.date_input("Check-in Date ")  
            check_out = st.date_input("Check-out Date")
            room_type = st.selectbox(label="select a room", options=['single', 'double', 'suite']) 
            button_book = st.button('book room')
            if button_book:
                if not room_type:
                    st.error("Please select a room type.")
                elif check_out <= check_in:
                    st.error('please check your check-in and check-out dates')
                else:
                    room_id = get_avaible_room(room_type, check_in, check_out)
                    if room_id:
                        book_room(st.session_state['guest_id'], room_id, check_in, check_out)
                        st.success('room is booked suceessfully !')
                    else:
                        st.warning('room is not avaibles')    
        with col_2:
            st.image("https://img.freepik.com/vecteurs-libre/illustration-concept-chasseur_114360-13511.jpg?uid=R94731443&ga=GA1.1.530378877.1745685662&semt=ais_hybrid&w=740", use_container_width="auto",width=480)    

with tab4 : 
    st.subheader('bookings')
    st.divider()
    st.data_editor(full_data)

with tab5 :
    st.subheader('guests')
    st.divider()
    guest = pd.read_sql("SELECT * FROM guests", con=conn)
    full_data['active'] = full_data['id'].apply(lambda x : "active" if x in booking['guest_id'].tolist() else "not active" )
    guest['status'] = guest['id'].apply(lambda x : "active" if x in booking['guest_id'].tolist() else "not active" )
    count_freq = full_data['guest_id'].value_counts().reset_index()
    count_freq.columns = ['id','reservation_count']
    guest = pd.merge(guest,count_freq, on='id',how='left')
    st.data_editor(guest)







