def collect_patient_details():
    # Collecting basic patient information
    print("Welcome to the Hospital Patient Registration System.")
    print("Please provide the following details:")

    patient_name = input("Enter patient's full name: ")
    age = int(input("Enter patient's age: "))  # Convert input to integer
    gender = input("Enter patient's gender (Male/Female/Other): ")
    contact_number = input("Enter patient's contact number: ")
    email = input("Enter patient's email address: ")
    
    # Collecting emergency contact details
    emergency_contact_name = input("Enter emergency contact name: ")
    emergency_contact_number = input("Enter emergency contact number: ")
    
    # Collecting medical history
    print("\nPlease provide the following medical history details:")
    allergies = input("Does the patient have any known allergies? (Yes/No): ")
    if allergies.lower() == 'yes':
        allergies_details = input("Please list the allergies: ")
    else:
        allergies_details = "None"
    
    chronic_conditions = input("Does the patient have any chronic conditions? (Yes/No): ")
    if chronic_conditions.lower() == 'yes':
        chronic_conditions_details = input("Please list the chronic conditions: ")
    else:
        chronic_conditions_details = "None"
    
    previous_surgeries = input("Has the patient had any previous surgeries? (Yes/No): ")
    if previous_surgeries.lower() == 'yes':
        surgeries_details = input("Please list the previous surgeries: ")
    else:
        surgeries_details = "None"
    
    # Collecting current symptoms
    print("\nPlease describe the current symptoms:")
    symptoms = input("Enter the patient's current symptoms: ")

    # Collecting additional details
    print("\nPlease provide the following additional details:")
    current_medications = input("Is the patient currently on any medications? (Yes/No): ")
    if current_medications.lower() == 'yes':
        medications_details = input("Please list the current medications: ")
    else:
        medications_details = "None"

    # Display collected information
    print("\nPatient Details Summary:")
    print(f"\nPatient Name: {patient_name}")
    print(f"Age: {age}")
    print(f"Gender: {gender}")
    print(f"Contact Number: {contact_number}")
    print(f"Email Address: {email}")
    
    print(f"\nEmergency Contact:")
    print(f"Name: {emergency_contact_name}")
    print(f"Phone: {emergency_contact_number}")
    
    print(f"\nMedical History:")
    print(f"Allergies: {allergies_details}")
    print(f"Chronic Conditions: {chronic_conditions_details}")
    print(f"Previous Surgeries: {surgeries_details}")
    
    print(f"\nCurrent Symptoms: {symptoms}")
    
    print(f"\nCurrent Medications: {medications_details}")
    
    # Store the details in a dictionary or a database
    patient_details = {
        'Name': patient_name,
        'Age': age,
        'Gender': gender,
        'Contact Number': contact_number,
        'Email': email,
        'Emergency Contact': {
            'Name': emergency_contact_name,
            'Phone': emergency_contact_number
        },
        'Medical History': {
            'Allergies': allergies_details,
            'Chronic Conditions': chronic_conditions_details,
            'Previous Surgeries': surgeries_details
        },
        'Current Symptoms': symptoms,
        'Current Medications': medications_details
    }

    # Simulating storing data (you can save to a database or file in real use cases)
    return patient_details

# Calling the function to collect patient details
patient_data = collect_patient_details()

# Optionally, you can print out the collected data or use it for further processing
print("\nThe collected patient data is stored as follows:")
print(patient_data)
