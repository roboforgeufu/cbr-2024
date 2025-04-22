from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def lilo_lego_ev3_color_p3_decision_tree(R, G, B):
    if B <= 18.5:
        if G <= 1.0:
            return None
        else:  # if G > 1.0
            if R <= 17.0:
                if G <= 14.0:
                    return Color.BLACK
                else:  # if G > 14.0
                    return Color.GREEN
            else:  # if R > 17.0
                if G <= 38.5:
                    if R <= 38.5:
                        return Color.BROWN
                    else:  # if R > 38.5
                        return Color.RED
                else:  # if G > 38.5
                    return Color.YELLOW
    else:  # if B > 18.5
        if R <= 22.5:
            return Color.BLUE
        else:  # if R > 22.5
            return Color.WHITE
