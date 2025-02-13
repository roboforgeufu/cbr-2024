from pybricks.parameters import Color


# Arquivo gerado automaticamente
def sandy_lego_ev3_color_p4_decision_tree(R, G, B):
    if R <= 11.0:
        if G <= 1.0:
            return None
        else:  # if G > 1.0
            if B <= 1.0:
                if G <= 6.5:
                    if G <= 4.5:
                        return Color.BROWN
                    else:  # if G > 4.5
                        return Color.BLACK
                else:  # if G > 6.5
                    return Color.GREEN
            else:  # if B > 1.0
                return Color.BLUE
    else:  # if R > 11.0
        if B <= 4.5:
            if G <= 16.0:
                return Color.RED
            else:  # if G > 16.0
                return Color.YELLOW
        else:  # if B > 4.5
            return Color.WHITE
