import pygame
import os
import datetime
pygame.init()
W, H = 1400, 1050
screen = pygame.display.set_mode((1400, 1050))
clock = pygame.time.Clock()

image = pygame.image.load("mickeyclock.jpg")
second = pygame.image.load("second.png")
hour = pygame.image.load("second.png")
minutes = pygame.image.load("minutes.png")


def rotated(surf, img, angle, orig):

    image_rect = img.get_rect(topleft=(W//2 - orig[0], H//2 - orig[1]))
    offset_center_to_pivot = pygame.math.Vector2(
        (W//2, H//2)) - image_rect.center

    rotated_image = pygame.transform.rotate(img, -angle)
    rotated_offset = offset_center_to_pivot.rotate(angle)

    rotated_image_center = (720 - rotated_offset.x, 535 - rotated_offset.y)

    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)
    return rotated_image, rotated_image_rect


orig_s = [30, 160]
orig_m = [180, 160]
orig_h = [30, 160]
BLUE = (0, 0, 255)
RED = (255, 0, 0)
angle = 0
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill((255, 255, 255))
    screen.blit(image, (0, 0))
    angle_h = datetime.datetime.now().hour/60 * 360
    angle_s = datetime.datetime.now().second/60 * 360
    angle_m = datetime.datetime.now().minute/60 * 360
   # screen.blit(second, (690, 380))
   # screen.blit(minutes, (530, 380))
    angle_sec, rect_sec = rotated(screen, second, angle_s + 48, orig_s)
    angle_min, rect_min = rotated(screen, minutes, angle_m - 56, orig_m)
    angle_hour, rect_hour = rotated(screen, hour, angle_h + 48, orig_h)
    screen.blit(angle_sec, rect_sec)
    screen.blit(angle_min, rect_min)
    screen.blit(angle_hour, rect_hour)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
