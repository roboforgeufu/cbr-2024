from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def lilo_lego_ev3_color_p1_decision_tree(R, G, B):
    if G <= 3.0:
        return None
    else:  # if G > 3.0
        if G <= 17.0:
            if R <= 12.5:
                if B <= 8.5:
                    return Color.BLACK
                else:  # if B > 8.5
                    return Color.BLUE
            else:  # if R > 12.5
                if R <= 31.5:
                    return Color.BROWN
                else:  # if R > 31.5
                    return Color.RED
        else:  # if G > 17.0
            if B <= 23.0:
                if G <= 33.5:
                    return Color.GREEN
                else:  # if G > 33.5
                    return Color.YELLOW
            else:  # if B > 23.0
                return Color.WHITE
