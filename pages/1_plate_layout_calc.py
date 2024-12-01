import streamlit as st
import pcr_func as pcr
from io import BytesIO
import base64
import pickle as pkl

# Load data from pickle file
with open ("data.pkl", "rb") as f:
    data = pkl.load(f)
    
# Unpack data
reaction_vol = data["reaction_vol"]
primer_pairs = data["primer_pairs"]
samples = data["samples"]
reps = data["reps"]
gene_names = data["gene_names"]
dna_concs = data["dna_concs"]
inc_controls = data["controls"]

# Title page
st.title("SYBR Green qPCR layout calculator")
st.markdown(
    "All volumes given in uL. The calculator assumes 40X yellow sample buffer is being used."
)

# Calculate plate layout based on user input
if st.sidebar.button("Calculate Plate Layout"):
    plate_layout, vol_plate_layout = pcr.ninetysix_plate_planner(
        samples, dna_concs, reaction_vol, gene_names, reps, controls
    )

    # Display plate_layout and vol_plate_layout in a table
    st.header("Volume Plate Layout:")
    st.markdown("Format of below cells is gene/primer pair name-sample number-repeat.")
    st.dataframe(plate_layout)
    # Display the volume layout for each well in the 96-well plate
    st.header("Volume Plate Layout:")
    st.markdown("Volume of reagents needed per well in uL.")
    st.dataframe(vol_plate_layout)

    # Save the plate layout and volume layout as CSV files

    layout_buffer = BytesIO()
    plate_layout.to_csv(layout_buffer, index=False)
    layout_buffer.seek(0)

    volume_buffer = BytesIO()
    vol_plate_layout.to_csv(volume_buffer, index=False)
    volume_buffer.seek(0)

st.download_button(
    label="Download Plate Layout",
    data=layout_buffer,
    file_name="plate_layout.csv",
    mime="text/csv",
)

st.download_button(
    label="Download Volume Layout",
    data=volume_buffer,
    file_name="volume_layout.csv",
    mime="text/csv",
)

# Add reset button
if st.sidebar.button("Reset"):
    st.experimental_rerun()
