# Import necessary libraries
import pandas as pd

def temp_per_well(reaction_vol, dna_conc, final_conc = 0.5):
    """
    This function calculates the volume of DNA needed per well for a given concentration of DNA.
    
    Parameters:
    reaction_vol: int, the total volume of the PCR reaction in uL
    dna_conc: float, the concentration of the DNA in ng/uL
    final_conc: float, the final concentration of DNA in the PCR reaction in ng/uL. Default value is 0.5.
    
    Returns:
    dna_vol: float, the volume of DNA needed per well in uL
    """
    
    # Check if the DNA concentration is less than or equal to 0
    if dna_conc <= 0:
        raise ValueError("DNA concentration cannot be less than or equal to 0.")
    else: # Calculate the volume of DNA needed per well for a given sample
        dna_vol = (final_conc * reaction_vol) / dna_conc
    return dna_vol # Return the volume of DNA needed per well

def total_dna_vol(dna_vol, reps, primer_pairs):
    """
    This function calculates the total volume in uL of DNA needed for per sample with a given number of replicates and primer pairs.
    
    Parameters:
    dna_vol: float, the volume of DNA needed per well in uL
    reps: int, the number of replicates
    primer_pairs: int, the number of primer pairs
    
    Returns:
    total_dna: float, the total volume of DNA needed in uL
    """
    
    # Calculate the total volume of DNA needed for a given number of replicates and primer pairs
    total_dna = (dna_vol * reps * primer_pairs) * 1.1 # Add 10% extra volume for pipetting error
    return total_dna # Return the total volume of DNA needed 
    
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
    return ysb_vol

def ninetysix_plate_planner(sample_no, dna_concs, reaction_vol, genes, reps, inc_controls = True):
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
    
    # Define the dataframe with the rows and columns of the 96 well plate
    rows = ["A","B","C","D","E","F","G","H"]
    columns = list(range(1,13))
    plate_layout = pd.DataFrame(index = rows, columns = columns)
    vol_plate_layout = pd.DataFrame(index = rows, columns = columns)
    
    # Calculate the total number of reactions, maximum number of wells and control wells
    total_reactions = sample_no * reps * len(genes)
    max_wells = 96 
    # Calc number of control wells, if inc_controls = True. 
    # Per gene, one no template control, one positive control, one negative control per gene
    control_wells = len(genes) * 3 if inc_controls else 0
    if total_reactions + control_wells > max_wells:
        raise ValueError("The number of reactions exceeds the number of wells in the plate.")
    
# Populate dataframe with sample-primer-repeat number combinations
    well_index = 0
    for gene in genes:  
        for sample in range(1,sample_no + 1):
            for repeat in range(1,reps + 1):
                row = rows[well_index // 12]
                col = columns[well_index % 12]
                plate_layout.loc[row,col] = f"{gene}_{sample}_{repeat}"
                well_index += 1

# Add control wells to the dataframe
    cont_index = 0
    if inc_controls:
        for gene in genes:
            row = "H"
            col = columns[cont_index] 
            plate_layout.loc[row,col] = f"NTC_{gene}"
            cont_index += 1
        for gene in genes:
            row = "H"
            col = columns[cont_index] 
            plate_layout.loc[row,col] = f"PC_{gene}"
            cont_index += 1
        for gene in genes:
            row = "H"
            col = columns[cont_index] 
            plate_layout.loc[row,col] = f"NC_{gene}"
            cont_index += 1
            
    # Add volume of reagents needed per well to the vol_plate_layout dataframe
    well_index = 0
    for sample in range(1,sample_no + 1):
        row = rows[well_index // 12]
        col = columns[well_index % 12]
        dna_vol = temp_per_well(reaction_vol, dna_concs[sample]) + 0.5 if reaction_vol == 20 else + 0.25
        sybr_vol = 10 if reaction_vol == 20 else 5
        primer_vol = 1 if reaction_vol == 20 else 0.5
        water_vol = reaction_vol - dna_vol - sybr_vol - primer_vol
        vol_plate_layout.loc[row,col] = f"{dna_vol} uL DNA, {sybr_vol} uL SYBR, {primer_vol} uL primers, {water_vol} uL water"
    



            

            

    