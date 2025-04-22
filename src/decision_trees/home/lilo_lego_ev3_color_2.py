from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def lilo_lego_ev3_color_p2_decision_tree(R, G, B):
    if R <= 8.5:
        if B <= 5.5:
            if G <= 9.5:
                if R <= 4.5:
                    return Color.BLACK
                else:  # if R > 4.5
                    return Color.BROWN
            else:  # if G > 9.5
                return Color.GREEN
        else:  # if B > 5.5
            return Color.BLUE
    else:  # if R > 8.5
        if B <= 8.0:
            if G <= 33.0:
                return Color.RED
            else:  # if G > 33.0
                return Color.YELLOW
        else:  # if B > 8.0
            if B <= 42.5:
                return None
            else:  # if B > 42.5
                return Color.WHITE
