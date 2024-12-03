# Import necessary libraries
import pandas as pd
import re 


def temp_per_well(reaction_vol, dna_conc):
    """
    This function calculates the volume of DNA needed per well for a given concentration of DNA.

    Parameters:
    reaction_vol: int, the total volume of the PCR reaction in uL
    dna_conc: float, the concentration of the DNA in ng/uL


    Returns:
    dna_vol: float, the volume of DNA needed per well in uL
    """
    final_conc = 0.5  # Final concentration of DNA in ng/uL

    # Check if the DNA concentration is less than or equal to 0
    if dna_conc <= 0:
        raise ValueError("DNA concentration cannot be less than or equal to 0.")
    # Calculate the volume of DNA needed per well for a given sample
    dna_vol = (final_conc * reaction_vol) / dna_conc

    return int(dna_vol)  # Return the volume of DNA needed per well


def total_dna_vol(dna_concs, reps, primer_pairs, reaction_vol):
    """
    This function calculates the total volume in uL of DNA needed for per sample with a given number of replicates and primer pairs.

    Parameters:
    reps: int, the number of replicates
    primer_pairs: int, the number of primer pairs
    reaction_vol: int, the total volume of the PCR reaction in uL
    dna_concs: list, the concentrations of the DNA samples
    
    Returns:
    total_dna: float, the total volume of DNA needed in uL
    """

    # Calculate the total volume of DNA needed for a given number of replicates and primer pairs
    # Add 10% extra volume for pipetting error
    for conc in dna_concs:
        total_dna = [temp_per_well(reaction_vol, conc) * reps * primer_pairs]
        
    return total_dna  # Return the total volume of DNA needed


def ysb_vol_calc(reaction_vol, reps, primer_pairs):
    """
    This function calculates the volume of 40X yellow sample buffer needed for a total volume of template DNA,
    based on number of replicates and primer pairs.

    Parameters:
    reaction_vol: int, the total volume of the PCR reaction in uL
    reps: int, the number of replicates
    primer_pairs: int, the number of primer pairs

    Returns:
    ysb_vol: float, the volume of 40X yellow sample buffer needed in uL
    """

    if reaction_vol == 10:
        ysb_vol = (reps * primer_pairs) * 0.25
    elif reaction_vol == 20:
        ysb_vol = (reps * primer_pairs) * 0.5
    else:
        raise ValueError("Unsupported reaction volume. Please use 10 or 20 uL.")
    return ysb_vol


def ninetysix_plate_planner(
    sample_no, dna_concs, reaction_vol, genes, reps, inc_controls=True
):
    """
    This function calculates a 96 plate layout for a given number of samples, primer pairs and replicates.

    Parameters:
    sample_no: int, the number of samples
    dna_concs: list, the concentrations of the DNA samples
    reaction_vol: int, the total volume of the PCR reaction in uL
    genes: list, the names of the genes/primer pairs
    reps: int, the number of replicates
    inc_controls: boolean, whether to include controls in the plate layout. Default is True.

    Returns:
    plate_layout: dataframe, a dataframe with the plate layout
    vol_plate_layout: dataframe, a dataframe with the volume of reagents needed per well
    """

    print("Sample_no: ", sample_no)
    print("DNA_concs: ", dna_concs)
    print("Reaction_vol: ", reaction_vol)
    print("Genes: ", genes)
    print("Reps: ", reps)
    print("Inc_controls: ", inc_controls)

    if len(dna_concs) != sample_no:
        raise ValueError(
            "Number of DNA concentrations does not match the number of samples."
        )

    # Define the dataframe with the rows and columns of the 96 well plate
    rows = ["A", "B", "C", "D", "E", "F", "G", "H"]
    columns = list(range(1, 13))
    plate_layout = pd.DataFrame(index=rows, columns=columns)
    vol_plate_layout = pd.DataFrame(index=rows, columns=columns)

    # Calculate the total number of reactions, maximum number of wells and control wells
    total_reactions = sample_no * reps * len(genes)
    max_wells = 96
    # Calc number of control wells, if inc_controls = True.
    # Per gene, one no template control, one positive control, one negative control per gene
    control_wells = len(genes) * 3 if inc_controls else 0
    if total_reactions + control_wells > max_wells:
        raise ValueError(
            "The number of reactions exceeds the number of wells in the plate."
        )

    # Populate plate layout dataframe with sample-primer-repeat number combinations and volume plate layout with volumes
    row_index = 0
    for gene in genes:
        for repeat in range(1, reps + 1):
            for sample in range(1, sample_no + 1):
                # Each repeat of a gene gets its own row
                row = rows[row_index]
                col = columns[sample - 1]  # Each sample gets its own column
                plate_layout.loc[row, col] = f"{gene}_{sample}_{repeat}"

                # Populate volume plate layout with volumes
                dna_vol = temp_per_well(reaction_vol, dna_concs[sample - 1])
                sybr_vol = 10 if reaction_vol == 20 else 5
                primer_vol = 1 if reaction_vol == 20 else 0.5
                water_vol = (
                    int(reaction_vol)
                    - int(dna_vol)
                    - int(sybr_vol)
                    - int((primer_vol) * 2)
                    - ysb_vol_calc(reaction_vol, 1, 1)
                )
                vol_plate_layout.loc[row, col] = (
                    f"{int(dna_vol)} DNA -{int(sybr_vol)} SYBR -{int(primer_vol)} Each Primer -{int(water_vol)} Water"
                )
            row_index += 1

    # Add control wells to the dataframe
    if inc_controls:
        control_row = rows[row_index]
        cont_index = 0

        # Place no template control wells for each gene
        for gene in genes:
            plate_layout.loc[control_row, columns[cont_index]] = f"{gene}_NTC"
            cont_index += 1
        # Place positive control wells for each gene
        for gene in genes:
            plate_layout.loc[control_row, columns[cont_index + 1]] = f"{gene}_PC"
            cont_index += 1
        # Place negative control wells for each gene
        for gene in genes:
            plate_layout.loc[control_row, columns[cont_index + 2]] = f"{gene}_NC"
            cont_index += 1

    # Populate volume plate layout with volumes for control wells
    if inc_controls:

        # Find all wells with NTC and calculate volumes
        ntc_wells = plate_layout[plate_layout.map(lambda x: bool(re.search(r'ntc', str(x), re.IGNORECASE)))].stack().index.tolist()

    if ntc_wells:
        for well in ntc_wells:
            row, col = well
            water_vol = int(reaction_vol) - int(sybr_vol) - int((primer_vol) * 2)
            vol_plate_layout.loc[row, col] = (
                f"{int(sybr_vol)} SYBR -{int(primer_vol)} Each Primer -{int(water_vol)} Water"
            )

    return plate_layout, vol_plate_layout


# Master mix volumes calculator
def master_mix_vols(reaction_vol, genes, samples, reps, inc_controls):
    """
    This function calculates the volumes of master mix components needed for a given number of reactions.

    Parameters:
    reaction_vol: int, the total volume of the PCR reaction in uL
    genes: list, the names of the genes/primer pairs in use
    samples: int, the number of samples
    reps: int, the number of replicates
    inc_controls: boolean, whether to include controls in the plate layout.

    Returns:
    master_mix_vols: List, a list with the volumes of the master mix components
    """

    # Dictionary of master mix components and their volumes in uL
    master_mix_20ul = {
        "SYBR Green": 10,
        "Forward Primer": 1,
        "Reverse Primer": 1,
        "Nuclease-free Water": 6.5,
    }

    master_mix_10ul = {
        "SYBR Green": 5,
        "Forward Primer": 0.5,
        "Reverse Primer": 0.5,
        "Nuclease-free Water": 3.25,
    }

    # Calculate the total number of reactions per gene/primer pair
    total_reactions_per_primer_pair = (samples * reps) * len(genes)

    # Add control reactions if inc_controls is True
    if inc_controls:
        total_reactions_per_primer_pair += 3 * len(
            genes
        )  # 3 control reactions per gene

    # Calculate the volumes of master mix components for each gene/primer_pair
    master_mix_vols = {}
    for gene in genes:
        if reaction_vol == 20:
            master_mix_vols[gene] = {
                k: v * total_reactions_per_primer_pair
                for k, v in master_mix_20ul.items()
            }
        elif reaction_vol == 10:
            master_mix_vols[gene] = {
                k: v * total_reactions_per_primer_pair
                for k, v in master_mix_10ul.items()
            }
        else:
            raise ValueError("Unsupported reaction volume. Please use 10 or 20 uL.")

    return master_mix_vols
