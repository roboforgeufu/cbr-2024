from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def lilo_lego_ev3_color_p3_decision_tree(R, G, B):
    if R <= 19.5:
        if B <= 12.0:
            if G <= 18.0:
                return Color.BLACK
            else:  # if G > 18.0
                return Color.GREEN
        else:  # if B > 12.0
            if R <= 7.5:
                return Color.BLUE
            else:  # if R > 7.5
                return None
    else:  # if R > 19.5
        if G <= 37.0:
            if R <= 38.5:
                return Color.BROWN
            else:  # if R > 38.5
                return Color.RED
        else:  # if G > 37.0
            if B <= 37.5:
                return Color.YELLOW
            else:  # if B > 37.5
                return Color.WHITE
