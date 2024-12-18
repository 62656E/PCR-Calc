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
master_mix_vols_df = data["master_mix_vols"]
ysb_vols = data["ysb_vols"]
samples = data["samples"]
total_dna_vols = data["total_dna_vols"]


# Title page
st.title("Reagent Volumes")
st.markdown(
    "All volumes given in uL. The calculator assumes 40X yellow sample buffer is being used."
)

# Create data frames
ysb_vols_df = pd.DataFrame(
    data=[ysb_vols, total_dna_vols],
    columns=range(1, samples + 1),
    index=["YSB Volumes (uL)", "Total DNA (uL)"],
)

# Add total column to ysb_vols_df
ysb_vols_df["Total"] = ysb_vols_df.sum(axis=1)

# Multiply all reagent volumes by 10% to account for pipetting error
ysb_vols_df *= 1.1
master_mix_vols_df *= 1.1

# Display both dataframes
st.write("YSB and Sample DNA Volumes")
st.write(ysb_vols_df)
st.write("Master Mix Volumes")
st.write(master_mix_vols_df)

# Add download links for reagent volumes

ysb_temp_buffer = BytesIO()
ysb_vols_df.to_csv(ysb_temp_buffer, index=False)
ysb_temp_buffer.seek(0)

master_buffer = BytesIO()
master_mix_vols_df.to_csv(master_buffer, index=False)
master_buffer.seek(0)

st.download_button(
    label="Download Plate Layout",
    data=ysb_temp_buffer,
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
