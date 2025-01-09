#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install rdkit pandas')
import pandas as pd
from rdkit import Chem
from rdkit.ML.Descriptors import MoleculeDescriptors
from rdkit.Chem import Descriptors
import warnings
warnings.filterwarnings('ignore')

# Load the CSV file containing SMILES
file_path = 'Human Oral Bioavailability - Copy - Copy.xlsx' 
data = pd.read_excel(file_path)

# Initialize the descriptor calculator with all RDKit descriptors
descriptor_names = [desc[0] for desc in Descriptors.descList]
calculator = MoleculeDescriptors.MolecularDescriptorCalculator(descriptor_names)

# Function to calculate descriptors for a given SMILES string
def calculate_descriptors(smiles):
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            return calculator.CalcDescriptors(mol)
        else:
            return [None] * len(descriptor_names)  # Return None if invalid SMILES
    except Exception as e:
        print(f"Error calculating descriptors for {smiles}: {e}")
        return [None] * len(descriptor_names)

# Apply the descriptor calculation to each SMILES in the CSV
data['Descriptors'] = data['SMILES'].apply(calculate_descriptors)

# Split the descriptors into separate columns
descriptor_df = pd.DataFrame(data['Descriptors'].tolist(), columns=descriptor_names)
result = pd.concat([data.drop(columns=['Descriptors']), descriptor_df], axis=1)

# Save the resulting dataframe to a new CSV file
output_file = 'hob_out.csv' 
result.to_csv(output_file, index=True)

print(f"Descriptors calculated and saved to {output_file}")


# In[ ]:




