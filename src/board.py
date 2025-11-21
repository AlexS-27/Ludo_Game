from src.cell import RED, GREEN, BLUE, YELLOW

#Create the different cell with colors
def color_ludo(grid):
    #Red zone
    for r in range(0,6):
        for c in range(0,6):
            grid[r][c].color = RED
            grid[r][c].border_width = 0
    #Blue zone
    for r in range(0,6):
        for c in range(9,15):
            grid[r][c].color = BLUE
            grid[r][c].border_width = 0
    #Yellow zone
    for r in range(9,15):
        for c in range(9,15):
            grid[r][c].color = YELLOW
            grid[r][c].border_width = 0
    #Green zone
    for r in range(9,15):
        for c in range(0,6):
            grid[r][c].color = GREEN
            grid[r][c].border_width = 0
    #Red safe zone
    for r in range(1,6):
        c = 7
        grid[r][c].color = RED
    #Yellow safe zone
    for r in range(9,14):
        c=7
        grid[r][c].color = YELLOW
    #Green safe zone
    for c in range(1,6):
        r= 7
        grid[r][c].color = GREEN
    #Blue safe zone
    for c in range(9,14):
        r= 7
        grid[r][c].color = BLUE
    #Red entry
    for r in range(1,2):
        c=6
        grid[r][c].color = RED
    #Yellow entry
    for r in range(13,14):
        c=8
        grid[r][c].color = YELLOW
    #Green entry
    for c in range(1,2):
        r=8
        grid[r][c].color = GREEN
    #Blue entry
    for c in range(13,14):
        r= 6
        grid[r][c].color = BLUE