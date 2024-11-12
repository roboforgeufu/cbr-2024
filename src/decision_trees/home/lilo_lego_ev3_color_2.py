from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def lilo_lego_ev3_color_p2_decision_tree(R, G, B):
    if G <= 3.5:
        return None
    else:  # if G > 3.5
        if R <= 21.5:
            if B <= 10.0:
                if G <= 15.5:
                    if R <= 5.5:
                        return Color.BLACK
                    else:  # if R > 5.5
                        return Color.BROWN
                else:  # if G > 15.5
                    return Color.GREEN
            else:  # if B > 10.0
                return Color.BLUE
        else:  # if R > 21.5
            if B <= 6.0:
                return Color.RED
            else:  # if B > 6.0
                if B <= 31.5:
                    return Color.YELLOW
                else:  # if B > 31.5
                    return Color.WHITE
