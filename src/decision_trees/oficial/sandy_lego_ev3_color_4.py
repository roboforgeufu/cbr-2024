from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def sandy_lego_ev3_color_p4_decision_tree(R, G, B):
    if G <= 1.5:
        return None
    else:  # if G > 1.5
        if R <= 9.5:
            if G <= 9.5:
                if B <= 2.5:
                    return Color.BLACK
                else:  # if B > 2.5
                    return Color.BLUE
            else:  # if G > 9.5
                return Color.GREEN
        else:  # if R > 9.5
            if G <= 19.5:
                if R <= 24.0:
                    return Color.BROWN
                else:  # if R > 24.0
                    return Color.RED
            else:  # if G > 19.5
                if B <= 12.0:
                    return Color.YELLOW
                else:  # if B > 12.0
                    return Color.WHITE
