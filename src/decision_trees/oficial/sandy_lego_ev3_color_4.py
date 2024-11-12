from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def sandy_lego_ev3_color_p4_decision_tree(R, G, B):
    if R <= 1.5:
        return None
    else:  # if R > 1.5
        if G <= 27.5:
            if R <= 10.5:
                if B <= 4.0:
                    if G <= 8.5:
                        return Color.BLACK
                    else:  # if G > 8.5
                        return Color.GREEN
                else:  # if B > 4.0
                    return Color.BLUE
            else:  # if R > 10.5
                if R <= 24.5:
                    return Color.BROWN
                else:  # if R > 24.5
                    return Color.RED
        else:  # if G > 27.5
            if B <= 15.0:
                return Color.YELLOW
            else:  # if B > 15.0
                return Color.WHITE
