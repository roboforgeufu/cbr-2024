from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def lilo_lego_ev3_color_p1_decision_tree(R, G, B):
    if R <= 31.0:
        if B <= 8.0:
            if R <= 16.0:
                if G <= 12.5:
                    return Color.BLACK
                else:  # if G > 12.5
                    return Color.GREEN
            else:  # if R > 16.0
                return Color.BROWN
        else:  # if B > 8.0
            if R <= 9.0:
                return Color.BLUE
            else:  # if R > 9.0
                return None
    else:  # if R > 31.0
        if B <= 24.0:
            if G <= 42.5:
                return Color.RED
            else:  # if G > 42.5
                return Color.YELLOW
        else:  # if B > 24.0
            return Color.WHITE
