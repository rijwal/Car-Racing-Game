import pygame

# #the scale image which allows for the game to change the size of the pngs in  order to fit with the game screen/window size
# def scaleimage(assets, factor):
#     sz = round(assets.get_width() * factor), round(assets.get_height() * factor)
#     return pygame.transform.scale(assets, sz)

# #made a system in order to allow for the car to be placed on the screen and allow to turn and move (i could have easily used the window.blit function but chose to find a method of simplifying the issue and allowing for the car to change angles in order to turn)
# def blit_rotate_center(win, image, top_left, angle): 
#     rotated_image = pygame.transform.rotate(image, angle)
#     new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
#     win.blit(rotated_image, new_rect.topleft)




    