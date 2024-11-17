from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def sandy_lego_ev3_color_p4_decision_tree(R, G, B):
    if R <= 24.0:
        if B <= 2.0:
            if R <= 9.5:
                if G <= 9.0:
                    return Color.BLACK
                else:  # if G > 9.0
                    return Color.GREEN
            else:  # if R > 9.5
                return Color.BROWN
        else:  # if B > 2.0
            if R <= 5.0:
                return Color.BLUE
            else:  # if R > 5.0
                return None
    else:  # if R > 24.0
        if B <= 13.0:
            if G <= 17.5:
                return Color.RED
            else:  # if G > 17.5
                return Color.YELLOW
        else:  # if B > 13.0
            return Color.WHITE
