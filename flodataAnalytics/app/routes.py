# app/routes.py

from flask import jsonify, request,session
from werkzeug.utils import secure_filename
import pandas as pd  # You need to install pandas for reading Excel/CSV files
import os
import uuid
from app import app
from .models import get_all_parcels, add_parcel,get_user_by_id, add_bulk_processing_task,add_parcel_with_tracking,generate_tracking_number,add_bulk_processing_task_and_get_id



@app.route('/parcels', methods=['GET'])
def get_parcels():
    parcels = get_all_parcels()
    return jsonify(parcels)

@app.route('/add-parcel', methods=['POST'])
def create_parcel():
    try:
        # Get JSON data from the request body
        data = request.get_json()

        # Extract the required fields from the request body
        tracking_number = data.get('tracking_number')
        sender_id = data.get('sender_id')
        receiver_name = data.get('receiver_name')
        receiver_address = data.get('receiver_address')
        status = data.get('status')
        weight = data.get('weight')
        bulk_task_id = data.get('bulk_task_id')  # Optional field

        # Validate if required fields are present
        if not all([tracking_number, sender_id, receiver_name, receiver_address, status, weight]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Add parcel data
        parcel_data = (tracking_number, sender_id, receiver_name, receiver_address, status, weight, bulk_task_id)
        add_parcel(parcel_data)

        return jsonify({'message': 'Parcel added successfully'}), 201
    except Exception as e:
        print
        return jsonify({'error': str(e)}), 500


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/make_delivery', methods=['POST'])
def make_delivery():
    if 'file' in request.files and request.files['file']:
        # Handle bulk file upload
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            # Read the Excel file using pandas
            df = pd.read_excel(filepath)

            # Generate a unique batch ID for bulk processing
            batch_id = str(uuid.uuid4())
            created_at = pd.Timestamp.now()

            # Insert bulk processing task and get the task ID
            total_parcels = len(df)
            bulk_task_id = add_bulk_processing_task_and_get_id((batch_id, created_at, 'pending', total_parcels))

            successful_inserts = 0

            # Process each row in the DataFrame
            for index, row in df.iterrows():
                sender_id = row.get('Sender ID')
                receiver_name = row.get('Receiver Name')
                receiver_address = row.get('Receiver Address')
                weight = row.get('Weight (kg)')
                status = row.get('Status')

                # Ensure all necessary fields are available
                if not all([sender_id, receiver_name, receiver_address, weight, status]):
                    continue  # Skip rows with missing fields

                try:
                    # Generate a tracking number and insert the parcel data
                    parcel_data = (sender_id, receiver_name, receiver_address, status, weight, bulk_task_id)
                    add_parcel_with_tracking(parcel_data)
                    successful_inserts += 1
                except Exception as e:
                    print(f"Error inserting row {index}: {e}")

            if successful_inserts == total_parcels:
                return jsonify({'success': True, 'message': f"All {successful_inserts} parcels were added successfully", 'bulk_task_id': bulk_task_id}), 201
            else:
                return jsonify({'warning': f"Only {successful_inserts} out of {total_parcels} parcels were added successfully", 'bulk_task_id': bulk_task_id}), 207

        else:
            return jsonify({'error': 'Invalid file format'}), 400

    else:
        # Handle single parcel delivery
        sender_id = request.form.get('sender_id')
        receiver_name = request.form.get('receiver_name')
        receiver_address = request.form.get('receiver_address')
        weight = request.form.get('weight')
        status = request.form.get('status')

        # Ensure all necessary fields are available
        if not all([sender_id, receiver_name, receiver_address, weight, status]):
            return jsonify({'error': 'Please provide all required fields'}), 400

        try:
            # Generate a tracking number and insert the parcel data
            parcel_data = (sender_id, receiver_name, receiver_address, status, weight, None)  # No bulk_task_id for single
            tracking_number = add_parcel_with_tracking(parcel_data)

            return jsonify({'success': True, 'message': 'Parcel added successfully', 'tracking_number': tracking_number}), 201

        except Exception as e:
            print(f"Error inserting single parcel: {e}")
            return jsonify({'error': 'Failed to add parcel'}), 500

 


@app.route('/get-user-details', methods=['GET'])
def get_user_details():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401

    # Fetch user by user_id instead of email
    user = get_user_by_id(user_id)  # Add this function in models.py
    if user:
        return jsonify({'success': True, 'user_id': user['user_id'], 'email': user['email']}), 200
    else:
        return jsonify({'error': 'User not found'}), 404
