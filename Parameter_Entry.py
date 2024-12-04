import streamlit as st
import pcr_func as pcr
import pickle as pkl
import pandas as pd
import streamlit_funcs as sf

# Title page
st.title("SYBR Green qPCR calculator")

# Fetch necessary info from user via sidebar (reaction volume, number of primer pairs, number of samples, number of replicates)
with st.expander("PCR Reaction Information", expanded=True):
    st.write("Enter the following information:")
    st.write("1. Total volume of the PCR reaction in uL")
    reaction_volumes = [10, 20]
    reaction_vol = st.selectbox("Reaction Volume", reaction_volumes)
    st.write("2. Number of primer pairs")
    primer_pairs = st.number_input("Number of Primer Pairs", min_value=1, value=1)
    st.write("3. Number of samples")
    samples = st.number_input("Number of Samples", min_value=1, step=1)
    st.write("4. Number of replicates")
    reps = st.number_input("Number of Replicates", min_value=1, step=1)

# Get gene names for each primer pair
with st.expander("Gene/Primer Pair Information", expanded=True):
    st.write("Enter the gene name for each primer pair:")
    gene_names = []
    for primer_index in range(primer_pairs):
        gene_name = st.text_input(f"Gene name for Primer Pair {primer_index + 1}")
        gene_names.append(gene_name)

# Get DNA concentration for each sample from user
with st.expander("DNA Concentration Information", expanded=True):
    st.write("Enter the DNA concentration for each sample in ng/uL:")
    dna_concs = []
    for sample_index in range(samples):
        conc = st.number_input(f"DNA Concentration for Sample {sample_index + 1}")
        dna_concs.append(conc)

# Check if user wants to include controls
with st.expander("Control Information", expanded=True):
    inc_controls = st.checkbox("Include Controls")

# Calculate plate layout based on user input
if st.button("Calculate Plate Layout"):

    # Hardcoded values for testing
    reaction_vol = 20
    primer_pairs = 3
    samples = 12
    reps = 2
    gene_names = ["RPL13", "YWHAZ", "GAPDH"]
    dna_concs = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
    inc_controls = True

    # Calculate plate layouts
    plate_layout, vol_plate_layout = pcr.ninetysix_plate_planner(
        samples, dna_concs, reaction_vol, gene_names, reps, inc_controls
    )

    # Calculate total DNA volume per sample
    total_dna_vols = pcr.total_dna_vol(dna_concs, reps, primer_pairs, reaction_vol)

    # Calculate YSB volumes per sample
    ysb_vols = pcr.ysb_vol_calc(reaction_vol, reps, primer_pairs)

    # Calculate master mix volumes
    master_mix_vols = pcr.master_mix_vol_calc(
        reaction_vol, gene_names, samples, reps, inc_controls
    )

    # Add st.write statements to display the data
    st.write("Total DNA Volumes: " + str(total_dna_vols))
    st.write("YSB Volumes: " + str(ysb_vols))
    st.write("Master Mix Volumes: " + str(master_mix_vols))
    st.write("reaction_vol: " + str(reaction_vol))
    st.write("primer_pairs: " + str(primer_pairs))
    st.write("samples: " + str(samples))
    st.write("reps: " + str(reps))
    st.write("gene_names: " + str(gene_names))
    st.write("dna_concs: " + str(dna_concs))
    st.write("inc_controls: " + str(inc_controls))
    
    # Pack data into a dictionary
    data = {
        "reaction_vol": reaction_vol,
        "primer_pairs": primer_pairs,
        "samples": samples,
        "reps": reps,
        "gene_names": gene_names,
        "dna_concs": dna_concs,
        "controls": inc_controls,
        "plate_layout": plate_layout,
        "vol_plate_layout": vol_plate_layout,
        "total_dna_vols": total_dna_vols,
        "ysb_vols": ysb_vols,
        "master_mix_vols": master_mix_vols,
    }

    # Print dict
    st.write(data)
    # Save data to a pickle file
    with open("data.pkl", "wb") as f:
        pkl.dump(data, f)

    # Navigate to the plate layout page
    # sf.nav_page("Plate_Layout")
