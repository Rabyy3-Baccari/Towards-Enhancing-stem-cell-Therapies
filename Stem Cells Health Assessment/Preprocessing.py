import pandas as pd
import os

#Check Readme
csv_folder_path = 'CSV_File_Path'
label_file_path = "Folder_Path"
label_df = pd.read_excel(label_file_path, header=None)
labels = label_df[0].tolist()
# Check if the number of labels matches the number of CSV files
num_files = len([f for f in os.listdir(csv_folder_path) if f.endswith('.csv')])
if len(labels) != num_files:
    raise ValueError("The number of labels does not match the number of CSV files.")

# Process each CSV file
for i, csv_file in enumerate(sorted([f for f in os.listdir(csv_folder_path) if f.endswith('.csv')])):
    file_path = os.path.join(csv_folder_path, csv_file)

    df = pd.read_csv(file_path)

    df['Label'] = labels[i]

    updated_file_path = os.path.join(csv_folder_path, f'updated_{csv_file}')
    df.to_csv(updated_file_path, index=False)