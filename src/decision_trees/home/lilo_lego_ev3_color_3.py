from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def lilo_lego_ev3_color_p3_decision_tree(R, G, B):
    if B <= 11.0:
        if G <= 2.5:
            return None
        else:  # if G > 2.5
            if R <= 20.0:
                if G <= 14.0:
                    if R <= 4.5:
                        return Color.BLACK
                    else:  # if R > 4.5
                        return Color.BROWN
                else:  # if G > 14.0
                    return Color.GREEN
            else:  # if R > 20.0
                return Color.RED
    else:  # if B > 11.0
        if G <= 34.0:
            return Color.BLUE
        else:  # if G > 34.0
            if B <= 47.0:
                return Color.YELLOW
            else:  # if B > 47.0
                return Color.WHITE
