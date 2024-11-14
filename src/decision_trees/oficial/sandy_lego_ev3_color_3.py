from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def sandy_lego_ev3_color_p3_decision_tree(R, G, B):
    if R <= 0.5:
        return None
    else:  # if R > 0.5
        if B <= 7.0:
            if R <= 6.5:
                if G <= 5.5:
                    return Color.BLACK
                else:  # if G > 5.5
                    return Color.GREEN
            else:  # if R > 6.5
                if B <= 0.5:
                    if R <= 18.5:
                        return Color.BROWN
                    else:  # if R > 18.5
                        return Color.RED
                else:  # if B > 0.5
                    return Color.YELLOW
        else:  # if B > 7.0
            if B <= 17.5:
                return Color.BLUE
            else:  # if B > 17.5
                return Color.WHITE
