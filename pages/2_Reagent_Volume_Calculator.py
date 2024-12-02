import pickle as pkl
import pcr_func as pcr
import streamlit as st
from io import BytesIO
import base64
import pandas as pd

# Load data from pickle file
with open("data.pkl", "rb") as f:
    data = pkl.load(f)

# Unpack data
reaction_vol = data["reaction_vol"]
primer_pairs = data["primer_pairs"]
samples = data["samples"]
reps = data["reps"]
gene_names = data["gene_names"]
dna_concs = data["dna_concs"]
inc_controls = data["controls"]

# Print data to check it has been loaded correctly
print(reaction_vol)
print(primer_pairs)
print(samples)
print(reps)
print(gene_names)
print(dna_concs)
print(inc_controls)

# Title page
st.title("Reagent Volumes")
st.markdown(
    "All volumes given in uL. The calculator assumes 40X yellow sample buffer is being used."
)

# Calculate total DNA volume needed per sample
total_dna_vols = {}
for sample in range(samples):
    total_dna_vols[sample] = pcr.total_dna_vol(pcr.temp_per_well(reaction_vol, dna_concs[sample]), reps, primer_pairs)

# Calculate 40X yellow sample buffer volume needed per sample
ysb_vols = {}
for sample in range(samples):
    ysb_vols[sample] = pcr.ysb_vol_calc(reaction_vol, reps, primer_pairs)

# Create dataframe for reagent volumes
reagent_vols = pd.DataFrame(
    {
        "Sample": range(samples),
        "Total DNA Volume (uL)": [total_dna_vols[sample] for sample in range(samples)],
        "40X YSB Volume (uL)": [ysb_vols[sample] for sample in range(samples)],
    }
)

# Calculate total volume of master mix, and its constituents, needed for all reactions
master_mix_vols = pcr.master_mix_vols(reaction_vol, gene_names, samples, reps, inc_controls)

# Create dataframe for master mix volumes
master_mix_vols = pd.DataFrame(columns=gene_names, index = ["SYBR Green", "Forward Primer", "Reverse Primer", "Water"])

# Populate dataframe with master mix volumes
for gene in gene_names:
    master_mix_vols.loc["SYBR Green", gene] = master_mix_vols[gene]["SYBR Green"]
    master_mix_vols.loc["Forward Primer", gene] = master_mix_vols[gene]["Forward Primer"]
    master_mix_vols.loc["Reverse Primer", gene] = master_mix_vols[gene]["Reverse Primer"]
    master_mix_vols.loc["Water", gene] = master_mix_vols[gene]["Water"]
    
# Multiply all reagent volumes by 10% to account for pipetting error
reagent_vols *= 1.1
master_mix_vols *= 1.1

# Display both dataframes
st.write("Reagent Volumes")
st.write(reagent_vols)
st.write("Master Mix Volumes")
st.write(master_mix_vols)

# Add download links for reagent volumes

reagent_buffer = BytesIO()
reagent_vols.to_csv(reagent_buffer, index=False)
reagent_buffer.seek(0)

master_buffer = BytesIO()
master_mix_vols.to_csv(master_buffer, index=False)
master_buffer.seek(0)

st.download_button(
    label="Download Plate Layout",
    data=reagent_buffer,
    file_name="Template_YSB_Volumes.csv",
    mime="text/csv",
)

st.download_button(
    label="Download Volume Layout",
    data=master_buffer,
    file_name="Master_Mix_Volumes.csv",
    mime="text/csv",
)

# Add reset button
if st.button("Reset"):
    st.experimental_rerun()









