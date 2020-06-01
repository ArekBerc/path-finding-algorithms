import sys
import a_star
import pygame as pg

def edit_path(tuples):
    new_tuples=[]
    for x,y in tuples:
        new_tuples.append((y,x))
    return new_tuples[1:(len(new_tuples) - 1)]

def coloring(a,rectangles,colorr):
    for index, (rect, color) in enumerate(rectangles):
        for x, y in a:
            if index == (y * 36) + x:
                rectangles[index] = (rect, colorr)
                print(rectangles[index])
def coloring2(rectangles,colorr):
    for index, (rect, color) in enumerate(rectangles):
        rectangles[index] = (rect, colorr)



def main():
    screen = pg.display.set_mode((950, 630))
    clock = pg.time.Clock()
    # define some values
    height = 30
    width = 36
    size = 20
    color = (255, 255, 255)
    new_color = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    rectangles = []
    for y in range(height):
        for x in range(width):
            rect = pg.Rect(x * (size + 1), y * (size + 1), size, size)
            # The grid will be a list of (rect, color) tuples.
            rectangles.append((rect, color))
    font = pg.font.Font('freesansbold.ttf', 32)
    text = font.render('GO!', True, new_color, )
    textRect = text.get_rect()
    textRect.center = (850, 585)
    pointsCreated = False
    find = False
    done = False
    obstacles = []
    start = None
    finish = None
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

        mouse_pos = pg.mouse.get_pos()
        if pg.mouse.get_pressed()[0] and 0 < mouse_pos[0] < 755:
            for index, (rect, color) in enumerate(rectangles):
                if rect.collidepoint(mouse_pos):
                    # define start point
                    if start is None and finish is None:
                        rectangles[index] = (rect, red)
                        start = index
                    # define end point
                    elif start is not None and finish is None:
                        if rectangles[index] != (rect, red):
                            rectangles[index] = (rect, blue)
                            pointsCreated = True
                            finish = index
                    # define obstacles
                    elif rectangles[index] != (rect, red) and rectangles[index] != (rect, blue) and rectangles[
                        index] != (rect, new_color):
                        rectangles[index] = (rect, new_color)
                        obstacles.append(index)
        # if green button pressed
        elif pg.mouse.get_pressed()[0] and 800 < mouse_pos[0] < 900 and 550 < mouse_pos[
            1] < 613 and pointsCreated is True and find is False:
            path = a_star.main(start, finish, obstacles)
            if path == None:
                continue
            else:
                path = edit_path(path)
                coloring(path,rectangles,(0,255,0))
                find = True

        # if red button pressed
        elif pg.mouse.get_pressed()[0] and 800 < mouse_pos[0] < 900 and 470 < mouse_pos[1] < 533:
            coloring2(rectangles,(255,255,255))
            finish = None
            start = None
            obstacles = []
            pointsCreated = False
            find = False
        screen.fill((30, 30, 30))
        pg.draw.rect(screen, (100, 100, 100), (755, 0, 245, 630))
        pg.draw.rect(screen, green, (800, 550, 100, 63))
        pg.draw.rect(screen, red, (800, 470, 100, 63))
        screen.blit(text, textRect)


        for rect, color in rectangles:
            pg.draw.rect(screen, color, rect)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
    sys.exit()


