import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# 1. Load the massive NASA file
print("Loading NASA OSD-120 data matrix...")
df = pd.read_csv("GLDS-120_rna_seq_differential_expression_rRNArm_GLbulkRNAseq.csv", low_memory=False)

# 2. Inspect the dimensions (How many genes and columns are we dealing with)
print(f"Dataset Shape: {df.shape}")

# 3. Print just the top 5 rows and column names to see how NASA labeled everything
print("\n--- Column Metadata Preview ---")
print(df.head())

# 4. Extract all 598 column names into a clean Python list
all_columns = list(df.columns)

# 5. Look for columns containing statistical markers
#stat_columns = [col for col in all_columns if "Log2" in col or "pvalue" in col or "Pvalue" in col]

#print(f"\nFound {len(stat_columns)} statistical columns.")
#print("First 15 target statistical column headers:")
#print(stat_columns[:15])

# 6. Target the exact experimental contrast columns
#target_columns = [col for col in all_columns if "Col-0 & Space Flight & Dark Treatment" in col]

#print("\n--- Isolated Project Targets ---")
#for index, name in enumerate(target_columns):
    #print(f"Index {index}: {name}")

# ====================================================================
# PHASE I PROJECT CALCULATIONS: VARIABLE INITIALIZATION
# ====================================================================

# Save the exact text strings of the target columns into clean variables
LFC_COL = 'Log2fc_(Col-0 & Ground Control & Dark Treatment)v(Col-0 & Space Flight & Dark Treatment)'
PVAL_COL = 'P.value_(Col-0 & Ground Control & Dark Treatment)v(Col-0 & Space Flight & Dark Treatment)'

# 7. Print the first 5 rows of the chosen columns alongside the TAIR column to verify access
# Pass a list of our target column variables straight into .head()
print("\n--- Verifying Target Column Access ---")
print(df[['TAIR', LFC_COL, PVAL_COL]].head())

# ====================================================================
# PHASE I PRODUCTION FILTERS: Cytoplasm HSP70
# ====================================================================

# TASK: Create a boolean mask to isolate the row for the HSP70 gene (AT3G12580)

# CODE HERE:
hsp70_row = df[df['TAIR'] == 'AT3G12580']

# Print the result to check its real-world spaceflight behavior
#print("\n--- HSP70 Target Gene Profile ---")
#print(hsp70_row[['TAIR', LFC_COL, PVAL_COL]])

# ====================================================================
# Phase I PRODUCTION FILTERS: Rough ER HSP70
# ====================================================================

# CODE HERE:
hsp70_ER = df[df['TAIR'] == 'AT5G42020']

# CODE HERE:
#print("\n--- HSP70 Target Gene (ER) ---")
#print(hsp70_ER[['TAIR', LFC_COL, PVAL_COL]])

# ====================================================================
# Phase I PRODUCTION FILTERS: Rough Mitochondria HSP70
# ====================================================================

# CODE HERE:

hsp70_Mito = df[df['TAIR'] == 'AT5G09590']


# CODE HERE:
#print("\n--- HSP70 Target Gene (Mitochondria) ---")
#print(hsp70_Mito[['TAIR', LFC_COL, PVAL_COL]])

# ====================================================================
# PHASE I PRODUCTION: MASTER MATRIX CONCATENATION
# ====================================================================

# TASK: Use pd.concat() to fuse the three individual row slices into one table
# Elements to combine: hsp70_row, hsp70_ER, and hsp70_Mito

# CODE HERE:
hsp_panel_df = pd.concat([hsp70_row, hsp70_ER, hsp70_Mito], axis=0)

# Print master panel summary to verify the complete structural fusion
print("\n=== MASTER COMPARTMENTAL HSP PANEL ===")
print(hsp_panel_df[['TAIR', LFC_COL, PVAL_COL]])

# ====================================================================
# PHASE I PRODUCTION: MATHEMATICAL TRANSFORM TO PERCENTAGE CHANGE
# ====================================================================

# TASK: Calculate the raw percentage change from the logarithmic base-2 column

# CODE HERE:
hsp_panel_df['Calculated_Percentage_Change'] = (np.power(2, hsp_panel_df[LFC_COL]) - 1) * 100

# Print the expanded matrix layout to verify our non-logarithmic calculations
print("\n=== FINAL TRANSCRIPTOMIC DEFENSE ANALYSIS PANEL ===")
print(hsp_panel_df[['TAIR', LFC_COL, PVAL_COL, 'Calculated_Percentage_Change']])

# ====================================================================
# PHASE I PRODUCTION: DATA VISUALIZATION (MATPLOTLIB)
# ====================================================================

print("\nGenerating Phase I Master Analysis Chart...")

# 1. Define the names of the 3 cellular compartments for the X-axis
compartments = ['Cytoplasm', 'Rough ER', 'Mitochondria']

# 2. Extract the calculated percentage numbers as a clean Python list
percentages = hsp_panel_df['Calculated_Percentage_Change'].tolist()

# 3. Create a blank figure canvas layout that is 8 inches wide and 6 inches high
plt.figure(figsize=(8, 6))

# 4. Draw the vertical pillars using our compartments as X and percentages as Y
plt.bar(compartments, percentages, color='slategray', edgecolor='black', width=0.5)

# 5. Stamp a distinct horizontal line right at 0% to highlight the downward drop
plt.axhline(0, color='black', linewidth=1.2, linestyle='--')

#6. Apply clear axis labels and a descriptive title
plt.ylabel('Transcriptional Modification  (% Change vs Earth)', fontsize=12, fontweight='bold')
plt.xlabel('Cellular Organelle Compartment', fontsize=12, fontweight='bold')
plt.title('Transcriptomic Blunting of Root HSP70 Network\nUnder Spaceflight Conditions (OSD-120)', fontsize=13, fontweight='bold', pad=15)

# 7. Set strict y-axis viewing grid limits to wrap our negative percentages neatly
plt.ylim(-60, 20)

# 8. Save a high-resolution 300 DPI image file directly to our folder
plt.savefig('hsp_blunting_analysis.png', dpi=300, bbox_inches='tight')
print("SUCCESS: Master chart saved as 'hsp_blunting_analysis.png' inside your folder!")
