def draw_grid(surface, grid):
    for row in grid:
        for cell in row:
            cell.draw(surface)
