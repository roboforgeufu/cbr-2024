from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def lilo_lego_ev3_color_p4_decision_tree(R, G, B):
    if B <= 26.0:
        if R <= 35.5:
            if B <= 10.5:
                if G <= 14.0:
                    if R <= 14.5:
                        return Color.BLACK
                    else:  # if R > 14.5
                        return Color.BROWN
                else:  # if G > 14.0
                    return Color.GREEN
            else:  # if B > 10.5
                return None
        else:  # if R > 35.5
            if G <= 32.0:
                return Color.RED
            else:  # if G > 32.0
                return Color.YELLOW
    else:  # if B > 26.0
        if G <= 20.0:
            return Color.BLUE
        else:  # if G > 20.0
            return Color.WHITE
