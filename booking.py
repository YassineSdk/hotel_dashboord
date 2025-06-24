from database import execute_query
import streamlit as st
from database import  execute_query
import pandas as pd
import datetime as dt

def get_avaible_room(room_type,check_in,check_out):
    query = """
    select id from rooms where type = %s and id not in ( 
    select room_id from bookings
    where not (check_out <= %s OR check_in >= %s))
    limit 1;
    """
    result = execute_query(query,(room_type, check_in, check_out),fetch=True)
    if result:
        return result[0]['id']
    return None


def book_room(guest_id, room_id, check_in, check_out):
    query = """
        INSERT INTO bookings (guest_id, room_id, check_in, check_out, status)
        VALUES (%s, %s, %s, %s, %s)
    """
    params = (guest_id, room_id, check_in, check_out, 'confirmed')
    execute_query(query, params)


from database import  execute_query
import pandas as pd
import datetime 
def get_avaible_metrics() :
    query = """
    select number , type  from rooms where  id not in ( 
    select room_id from bookings
    where not (check_out <= %s OR check_in >= %s));
    """

    result = execute_query(query,(datetime.date.today(), pd.to_datetime("2025-06-23") + dt.timedelta(days=2)),fetch=True)
    data = pd.DataFrame(result)
    nom_rooms = data['number'].count()
    return int(nom_rooms)




