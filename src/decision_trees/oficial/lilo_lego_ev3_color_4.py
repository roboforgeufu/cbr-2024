from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def lilo_lego_ev3_color_p4_decision_tree(R, G, B):
    if R <= 35.5:
        if B <= 20.5:
            if G <= 14.0:
                if R <= 15.0:
                    if R <= 1.0:
                        return None
                    else:  # if R > 1.0
                        return Color.BLACK
                else:  # if R > 15.0
                    return Color.BROWN
            else:  # if G > 14.0
                return Color.GREEN
        else:  # if B > 20.5
            return Color.BLUE
    else:  # if R > 35.5
        if G <= 32.0:
            return Color.RED
        else:  # if G > 32.0
            if B <= 45.0:
                return Color.YELLOW
            else:  # if B > 45.0
                return Color.WHITE
