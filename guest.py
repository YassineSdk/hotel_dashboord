from database import get_connection, execute_query

def guest_exist(email):
    result = execute_query(
        "SELECT id FROM guests WHERE email = %s",
        (email,),
        fetch=True
    )
    return result[0] if result else None

def add_guest(name, email, phone):
    try:
        existing_guest = guest_exist(email)
        if existing_guest:
            return False, existing_guest['id'], "Guest already exists."

        insert_query = "INSERT INTO guests (name, email, phone) VALUES (%s, %s, %s)"
        new_id = execute_query(insert_query, (name, email, phone), return_lastrowid=True)
        
        return True, new_id, "Guest added successfully!"
    except Exception as e:
        return False, None, f"Error while adding guest: {str(e)}"






