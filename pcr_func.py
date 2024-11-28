def ysb_vol_calc(reaction_vol, no_samples):
    """ 
    This function calculates the volume of yellow sample buffer to add to a given volume of DNA for SYBR Green based qPCR.
    """
    if reaction_vol == 10:
        ysb_vol = no_samples * 0.25
    elif reaction_vol == 20:
        ysb_vol = no_samples * 0.5
    else:
        print("Reaction volume not supported")
        
            

    return dict(ysb_vol = ysb_vol, dna_vol = dna_vol)