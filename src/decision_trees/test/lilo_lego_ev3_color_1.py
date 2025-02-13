from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def lilo_lego_ev3_color_p1_decision_tree(R, G, B):
    if R <= 2.0:
        return None
    else:  # if R > 2.0
        if R <= 10.5:
            if B <= 11.5:
                if G <= 14.5:
                    return Color.BLACK
                else:  # if G > 14.5
                    return Color.GREEN
            else:  # if B > 11.5
                return Color.BLUE
        else:  # if R > 10.5
            if R <= 24.5:
                return Color.BROWN
            else:  # if R > 24.5
                if G <= 21.5:
                    return Color.RED
                else:  # if G > 21.5
                    if B <= 18.0:
                        return Color.YELLOW
                    else:  # if B > 18.0
                        return Color.WHITE
