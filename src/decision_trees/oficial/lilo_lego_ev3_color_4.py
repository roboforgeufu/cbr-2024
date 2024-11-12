from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def lilo_lego_ev3_color_p4_decision_tree(R, G, B):
    if G <= 1.5:
        return None
    else:  # if G > 1.5
        if B <= 16.5:
            if R <= 12.0:
                if B <= 3.5:
                    return Color.BLACK
                else:  # if B > 3.5
                    return Color.GREEN
            else:  # if R > 12.0
                if G <= 22.5:
                    if R <= 30.5:
                        return Color.BROWN
                    else:  # if R > 30.5
                        return Color.RED
                else:  # if G > 22.5
                    return Color.YELLOW
        else:  # if B > 16.5
            if B <= 47.5:
                return Color.BLUE
            else:  # if B > 47.5
                return Color.WHITE
