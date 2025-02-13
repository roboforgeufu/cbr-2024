from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def lilo_lego_ev3_color_p4_decision_tree(R, G, B):
    if B <= 12.0:
        if G <= 1.0:
            return None
        else:  # if G > 1.0
            if R <= 24.0:
                if G <= 9.5:
                    if R <= 5.5:
                        return Color.BLACK
                    else:  # if R > 5.5
                        return Color.BROWN
                else:  # if G > 9.5
                    return Color.GREEN
            else:  # if R > 24.0
                return Color.RED
    else:  # if B > 12.0
        if B <= 49.0:
            if G <= 28.0:
                return Color.BLUE
            else:  # if G > 28.0
                return Color.YELLOW
        else:  # if B > 49.0
            return Color.WHITE
