def ysb_vol_calc(reaction_vol, no_samples):
    """ 
    This function calculates the volume of yellow sample buffer to add to a given volume of DNA for SYBR Green based qPCR.
    """
    if reaction_vol == 10:
        ysb_vol = no_samples * 0.25
    elif reaction_vol == 20:
        ysb_vol = no_samples * 0.5
    return ysb_vol

def dna_vol_calc(reaction_vol, no_samples, dna_conc):
    """
    This function calculates the volume of DNA to add to a given volume of yellow sample buffer for SYBR Green based qPCR.
    """


            

    