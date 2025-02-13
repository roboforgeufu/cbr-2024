from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def junior_lego_ev3_color_p2_decision_tree(R, G, B):
    if R <= 1.0:
        return None
    else:  # if R > 1.0
        if R <= 7.0:
            return Color.GREEN
        else:  # if R > 7.0
            if B <= 21.5:
                if R <= 15.0:
                    return Color.BROWN
                else:  # if R > 15.0
                    return Color.RED
            else:  # if B > 21.5
                if R <= 20.0:
                    return Color.BLUE
                else:  # if R > 20.0
                    return Color.WHITE
