from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def lilo_lego_ev3_color_p1_decision_tree(R, G, B):
    if R <= 14.0:
        if B <= 7.0:
            if G <= 11.5:
                if R <= 1.5:
                    return None
                else:  # if R > 1.5
                    if R <= 5.5:
                        return Color.BLACK
                    else:  # if R > 5.5
                        return Color.BROWN
            else:  # if G > 11.5
                return Color.GREEN
        else:  # if B > 7.0
            return Color.BLUE
    else:  # if R > 14.0
        if G <= 15.5:
            return Color.RED
        else:  # if G > 15.5
            if B <= 20.0:
                return Color.YELLOW
            else:  # if B > 20.0
                return Color.WHITE
