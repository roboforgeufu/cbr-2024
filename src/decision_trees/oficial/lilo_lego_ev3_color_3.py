from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def lilo_lego_ev3_color_p3_decision_tree(R, G, B):
    if B <= 20.5:
        if G <= 2.5:
            return None
        else:  # if G > 2.5
            if R <= 17.0:
                if B <= 3.0:
                    return Color.BLACK
                else:  # if B > 3.0
                    return Color.GREEN
            else:  # if R > 17.0
                if G <= 43.0:
                    if R <= 38.5:
                        return Color.BROWN
                    else:  # if R > 38.5
                        return Color.RED
                else:  # if G > 43.0
                    return Color.YELLOW
    else:  # if B > 20.5
        if B <= 58.0:
            return Color.BLUE
        else:  # if B > 58.0
            return Color.WHITE
