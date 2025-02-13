from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def stitch_ht_nxt_color_v2_p4_decision_tree(R, G, B, W):
    if G <= 222.0:
        if R <= 180.5:
            if B <= 127.5:
                return None
            else:  # if B > 127.5
                return Color.BLUE
        else:  # if R > 180.5
            if G <= 100.0:
                return Color.RED
            else:  # if G > 100.0
                return Color.BROWN
    else:  # if G > 222.0
        if R <= 161.0:
            return Color.GREEN
        else:  # if R > 161.0
            return Color.WHITE
