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
reagent_vols = data["reagent_vols"]
master_mix_vols = data["master_mix_vols"]
samples = data["samples"]

print("RVC Reagent Volumes " + str(reagent_vols))
print("RVC Master Mix Volumes " + str(master_mix_vols))

# Title page
st.title("Reagent Volumes")
st.markdown(
    "All volumes given in uL. The calculator assumes 40X yellow sample buffer is being used."
)

# Create data frames
reagent_vol_df = pd.DataFrame(
        columns=[range(1, samples + 1)],
        index=["Template DNA", "YSB", "Total"],
)

master_mix_vols_df = pd.DataFrame(
    columns = range(1, samples + 1),
    index = ["SYBR Green", "Forward Primer", "Reverse Primer", "Water", "Total"]
)

# Populate data frames
for sample in range(1, samples + 1):
    reagent_vol_df[sample] = reagent_vols[sample]
    master_mix_vols_df[sample] = master_mix_vols[sample]

# Multiply all reagent volumes by 10% to account for pipetting error
reagent_vol_df *= 1.1
master_mix_vols_df *= 1.1

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
