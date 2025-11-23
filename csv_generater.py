import pandas as pd
from random import choice, randint, uniform
from datetime import datetime, timedelta

# Sample data
first_names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Ethan']
last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones']
genders = ['F', 'M']
diagnoses = ['Flu', 'Diabetes', 'Hypertension', 'Allergy', 'Cold']
treatments = ['Medication A', 'Therapy B', 'Surgery C', 'Checkup', 'Vaccination']

records = []

# Generate 50 random records
for i in range(1, 51):
    birth_date = datetime(1950,1,1) + timedelta(days=randint(0, 25000))
    visit_date = datetime(2025,1,1) + timedelta(days=randint(0, 365))
    cost = round(uniform(50, 1000), 2)
    
    record = {
        'patient_id': i,
        'first_name': choice(first_names),
        'last_name': choice(last_names),
        'birth_date': birth_date.strftime('%Y-%m-%d'),
        'gender': choice(genders),
        'diagnosis': choice(diagnoses),
        'visit_date': visit_date.strftime('%Y-%m-%d'),
        'treatment': choice(treatments),
        'cost': cost
    }
    records.append(record)

# Create DataFrame
df = pd.DataFrame(records)

# Save as CSV
df.to_csv('medical_records.csv', index=False)

print("CSV file 'medical_records.csv' generated successfully!")
