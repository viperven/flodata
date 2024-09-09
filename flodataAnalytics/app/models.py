from app import mysql
import random
import string

def get_all_parcels():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Parcel")
    parcels = cursor.fetchall()
    cursor.close()
    return parcels

def add_parcel(parcel_data):
    cursor = mysql.connection.cursor()
    query = """
    INSERT INTO Parcel (tracking_number, sender_id, receiver_name, receiver_address, status, weight, bulk_task_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, parcel_data)
    mysql.connection.commit()
    cursor.close()

def get_user_by_email(email):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM User WHERE email = %s"
    cursor.execute(query, [email])
    user = cursor.fetchone()
    cursor.close()
    return user

def add_user(user_data):
    cursor = mysql.connection.cursor()
    query = """
    INSERT INTO User (name, email, password_hash, role)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, user_data)
    mysql.connection.commit()
    cursor.close()

def get_bulk_processing_tasks():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM BulkProcessingTask")
    tasks = cursor.fetchall()
    cursor.close()
    return tasks

def add_bulk_processing_task(task_data):
    cursor = mysql.connection.cursor()
    query = """
    INSERT INTO BulkProcessingTask (batch_id, created_at, status, total_parcels)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, task_data)
    mysql.connection.commit()
    cursor.close()

def get_parcel_status_logs(parcel_id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM ParcelStatusLog WHERE parcel_id = %s"
    cursor.execute(query, [parcel_id])
    logs = cursor.fetchall()
    cursor.close()
    return logs

def add_parcel_status_log(log_data):
    cursor = mysql.connection.cursor()
    query = """
    INSERT INTO ParcelStatusLog (parcel_id, status, timestamp, comment)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, log_data)
    mysql.connection.commit()
    cursor.close()

def generate_tracking_number(length=10):
    """Generate a random tracking number."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def add_parcel_with_tracking(parcel_data):
    """Add a parcel with a generated tracking number."""
    tracking_number = generate_tracking_number()
    cursor = mysql.connection.cursor()
    query = """
    INSERT INTO Parcel (tracking_number, sender_id, receiver_name, receiver_address, status, weight, bulk_task_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    parcel_data_with_tracking = (tracking_number, *parcel_data)
    cursor.execute(query, parcel_data_with_tracking)
    mysql.connection.commit()
    cursor.close()
    return tracking_number

def get_user_by_id(user_id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM User WHERE user_id = %s"
    cursor.execute(query, [user_id])
    user = cursor.fetchone()
    cursor.close()
    return user

def generate_tracking_number(length=10):
    """Generate a random tracking number."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def add_bulk_processing_task_and_get_id(task_data):
    cursor = mysql.connection.cursor()
    query = """
    INSERT INTO BulkProcessingTask (batch_id, created_at, status, total_parcels)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, task_data)
    mysql.connection.commit()

    # Get the last inserted ID (bulk task ID)
    bulk_task_id = cursor.lastrowid
    cursor.close()
    return bulk_task_id
