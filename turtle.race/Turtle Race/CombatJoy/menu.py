import pygame
import config

pygame.init()

font = pygame.font.Font('assets/PressStart2P.ttf', 45)
font_smaller = pygame.font.Font('assets/PressStart2P.ttf', 15)

size = (900, 650)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Turtle Race")

# Image of the stages
stage1_pic = pygame.image.load("assets/city_map.png")
stage1_pic = pygame.transform.scale(stage1_pic, (180, 130))
stage1_pic_rect = stage1_pic.get_rect()
stage1_pic_rect.center = (225, 300)

stage1_text = font_smaller.render("Stage 1 - City", True, config.white)
stage1_text_rect = stage1_text.get_rect()
stage1_text_rect.center = (225, 380)

stage2_pic = pygame.image.load("assets/vegetation_map.png")
stage2_pic = pygame.transform.scale(stage2_pic, (180, 130))
stage2_pic_rect = stage2_pic.get_rect()
stage2_pic_rect.center = (675, 300)

stage2_text = font_smaller.render("Stage 2 - Field", True, config.white)
stage2_text_rect = stage2_text.get_rect()
stage2_text_rect.center = (675, 380)

# Message for the player to choose a stage
message_text = font.render("Choose a Stage:", True, config.white)
message_text_rect = message_text.get_rect()
message_text_rect.center = (450, 175)

# stage decision
stage = 1
select_text = font.render(("Stage: " + str(stage)), True, config.white)
select_text_rect = select_text.get_rect()
select_text_rect.center = (450, 500)

while config.stage_select < 0:
    screen.fill(config.black)
    screen.blit(stage1_pic, stage1_pic_rect)
    screen.blit(stage1_text, stage1_text_rect)
    screen.blit(stage2_pic, stage2_pic_rect)
    screen.blit(stage2_text, stage2_text_rect)
    screen.blit(message_text, message_text_rect)
    screen.blit(select_text, select_text_rect)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            config.stage_select = 10

        # configuring game keys
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP or event.key == pygame.K_RIGHT:
                if stage == 2:
                    stage = 1
                else:
                    stage += 1
            if event.key == pygame.K_DOWN or event.key == pygame.K_LEFT:
                if stage == 1:
                    stage = 2
                else:
                    stage -= 1
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                config.stage_select = stage - 1

        select_text = font.render(("Stage: " + str(stage)), True, config.white)

        pygame.display.update()

pygame.quit()

exec(open("game.py").read())
