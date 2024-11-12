from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def junior_lego_ev3_color_p2_decision_tree(R, G, B):
    if R <= 0.5:
        return None
    else:  # if R > 0.5
        if B <= 20.0:
            if G <= 11.5:
                if R <= 15.5:
                    return Color.BROWN
                else:  # if R > 15.5
                    return Color.RED
            else:  # if G > 11.5
                return Color.GREEN
        else:  # if B > 20.0
            if R <= 22.5:
                return Color.BLUE
            else:  # if R > 22.5
                return Color.WHITE
