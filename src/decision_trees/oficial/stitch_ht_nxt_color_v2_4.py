from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def stitch_ht_nxt_color_v2_p4_decision_tree(R, G, B, W):
    if R <= 206.0:
        if G <= 219.0:
            if R <= 39.5:
                return None
            else:  # if R > 39.5
                return Color.BLUE
        else:  # if G > 219.0
            return Color.GREEN
    else:  # if R > 206.0
        if G <= 96.5:
            return Color.RED
        else:  # if G > 96.5
            if G <= 182.0:
                return Color.BROWN
            else:  # if G > 182.0
                return Color.WHITE
