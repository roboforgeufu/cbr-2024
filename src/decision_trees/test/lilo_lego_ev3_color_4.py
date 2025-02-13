from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def lilo_lego_ev3_color_p4_decision_tree(R, G, B):
    if G <= 8.5:
        if R <= 31.5:
            if R <= 9.0:
                if B <= 1.5:
                    return None
                else:  # if B > 1.5
                    return Color.BLACK
            else:  # if R > 9.0
                return Color.BROWN
        else:  # if R > 31.5
            return Color.RED
    else:  # if G > 8.5
        if G <= 15.0:
            return Color.BLUE
        else:  # if G > 15.0
            if G <= 26.0:
                return Color.GREEN
            else:  # if G > 26.0
                if B <= 22.5:
                    return Color.YELLOW
                else:  # if B > 22.5
                    return Color.WHITE
