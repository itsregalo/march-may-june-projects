# build obstacles on the road

import pygame

class Obstacle:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.rect = pygame.Rect(x1, y1, x2-x1, y2-y1)
        self.color = (255, 0, 0)
        self.width = 2

    def draw(self, win):
        pygame.draw.line(win, self.color, (self.x1, self.y1), (self.x2, self.y2), self.width)

    def isCollide(self, car):
        if car.rect.colliderect(self.rect):
            return True
        return False

    def isCollide2(self, car):
        if car.rect.colliderect(self.rect):
            return True
        return False

    def isCollide3(self, car):
        if car.rect.colliderect(self.rect):
            return True
        return False

    def isCollide4(self, car):
        if car.rect.colliderect(self.rect):
            return True
        return False

    def isCollide5(self, car):
        if car.rect.colliderect(self.rect):
            return True
        return False

    def isCollide6(self, car):
        if car.rect.colliderect(self.rect):
            return True
        return False

# the file of shame
def getObstacles():
    obstacles = []

    obstacle1 = Obstacle(0,0,50,50)
    obstacle2 = Obstacle(50,0,100,50)
    obstacle3 = Obstacle(100,0,150,50)
    obstacle4 = Obstacle(150,0,200,50)
    obstacle5 = Obstacle(200,0,250,50)
    obstacle6 = Obstacle(250,0,300,50)
    obstacle7 = Obstacle(300,0,350,50)
    obstacle8 = Obstacle(350,0,400,50)
    obstacle9 = Obstacle(400,0,450,50)
    obstacle10 = Obstacle(450,0,500,50)
    obstacle11 = Obstacle(500,0,550,50)
    obstacle12 = Obstacle(550,0,600,50)
    obstacle13 = Obstacle(600,0,650,50)
    obstacle14 = Obstacle(650,0,700,50)
    obstacle15 = Obstacle(700,0,750,50)
    obstacle16 = Obstacle(750,0,800,50)
    obstacle17 = Obstacle(800,0,850,50)
    obstacle18 = Obstacle(850,0,900,50)
    obstacle19 = Obstacle(900,0,950,50)
    obstacle20 = Obstacle(950,0,1000,50)
    obstacle21 = Obstacle(1000,0,1050,50)
    obstacle22 = Obstacle(1050,0,1100,50)
    obstacle23 = Obstacle(1100,0,1150,50)
    obstacle24 = Obstacle(1150,0,1200,50)
    obstacle25 = Obstacle(1200,0,1250,50)
    obstacle26 = Obstacle(1250,0,1300,50)
    obstacle27 = Obstacle(1300,0,1350,50)
    obstacle28 = Obstacle(1350,0,1400,50)
    obstacle29 = Obstacle(1400,0,1450,50)
    obstacle30 = Obstacle(1450,0,1500,50)

    # append all obstacles to the list
    obstacles.append(obstacle1)
    obstacles.append(obstacle2)
    obstacles.append(obstacle3)
    obstacles.append(obstacle4)
    obstacles.append(obstacle5)
    obstacles.append(obstacle6)
    obstacles.append(obstacle7)
    obstacles.append(obstacle8)
    obstacles.append(obstacle9)
    obstacles.append(obstacle10)
    obstacles.append(obstacle11)
    obstacles.append(obstacle12)
    obstacles.append(obstacle13)
    obstacles.append(obstacle14)
    obstacles.append(obstacle15)
    obstacles.append(obstacle16)
    obstacles.append(obstacle17)
    obstacles.append(obstacle18)
    obstacles.append(obstacle19)
    obstacles.append(obstacle20)
    obstacles.append(obstacle21)
    obstacles.append(obstacle22)
    obstacles.append(obstacle23)
    obstacles.append(obstacle24)
    obstacles.append(obstacle25)
    obstacles.append(obstacle26)
    obstacles.append(obstacle27)
    obstacles.append(obstacle28)
    obstacles.append(obstacle29)
    obstacles.append(obstacle30)

    return obstacles