from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def lilo_lego_ev3_color_p2_decision_tree(R, G, B):
    if B <= 8.0:
        if R <= 28.5:
            if R <= 7.5:
                if G <= 14.5:
                    return Color.BLACK
                else:  # if G > 14.5
                    return Color.GREEN
            else:  # if R > 7.5
                return Color.BROWN
        else:  # if R > 28.5
            if G <= 33.0:
                return Color.RED
            else:  # if G > 33.0
                return Color.YELLOW
    else:  # if B > 8.0
        if R <= 10.0:
            return Color.BLUE
        else:  # if R > 10.0
            if B <= 43.5:
                return None
            else:  # if B > 43.5
                return Color.WHITE
