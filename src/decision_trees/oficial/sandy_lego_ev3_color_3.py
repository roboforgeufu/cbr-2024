from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def sandy_lego_ev3_color_p3_decision_tree(R, G, B):
    if R <= 1.0:
        return None
    else:  # if R > 1.0
        if G <= 8.5:
            if R <= 7.5:
                if B <= 5.0:
                    return Color.BLACK
                else:  # if B > 5.0
                    return Color.BLUE
            else:  # if R > 7.5
                if R <= 22.0:
                    return Color.BROWN
                else:  # if R > 22.0
                    return Color.RED
        else:  # if G > 8.5
            if B <= 22.0:
                if G <= 22.0:
                    return Color.GREEN
                else:  # if G > 22.0
                    return Color.YELLOW
            else:  # if B > 22.0
                return Color.WHITE
