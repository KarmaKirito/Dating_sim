import datetime
import pygame
import sys
from Button import Button

pygame.init()
RES = (1024, 740)
screen = pygame.display.set_mode(RES)
pygame.display.set_caption('Dating simulator')
clock = pygame.time.Clock()
FPS = 60
button_img_menu = pygame.image.load('Dating_sim_pic/button_img_menu.png').convert_alpha()
button_img_menu_play = pygame.transform.scale(button_img_menu, (200, 70))
button_img_menu_settings = pygame.transform.scale(button_img_menu, (370, 70))
buttons_menu = [button_img_menu_settings, button_img_menu_play]
play_bg1 = pygame.image.load('Dating_sim_pic/play_bg1.jpg')
squirrel_bg = pygame.image.load('Dating_sim_pic/leading_squirrel2.0.jpg')
paused_squirrel_bg = pygame.image.load('Dating_sim_pic/paused_squirrel.jpg')
paused_squirrel_bg2 = pygame.image.load('Dating_sim_pic/paused_squirrel2.jpg')
running_squirrel = pygame.image.load('Dating_sim_pic/running_squirrel1.jpg')
enchanted_cave = pygame.image.load('Dating_sim_pic/enchanted_cave.jpg')
persistent_squirrel = pygame.image.load('Dating_sim_pic/persistent_squirrel.jpg')
Elara = pygame.image.load('Dating_sim_pic/Elara_2.jpg')
Elara_playing_with_animals = pygame.image.load('Dating_sim_pic/Elara_playing_with_animals.jpg')
Elara_suprised = pygame.image.load('Dating_sim_pic/Elara_suprised.jpg')
Squirrel_point = pygame.image.load('Dating_sim_pic/Point_at_squirrrel.jpg')
Elara_explain = pygame.image.load('Dating_sim_pic/Elara_explain.jpg')
Elara_with_animals = pygame.image.load('Dating_sim_pic/Elara_with_animals.jpg')
Elara_stroke_bunny = pygame.image.load('Dating_sim_pic/Elara_bunny.jpg')
Elara_admired = pygame.image.load('Dating_sim_pic/Elara_admired.jpg')
Elara_ask = pygame.image.load('Dating_sim_pic/Elara_ask.jpg')
Elara_end_chap1 = pygame.image.load('Dating_sim_pic/Elara_embark_adventure.jpg')
Elara_end_chap1_2 = pygame.image.load('Dating_sim_pic/Elara_embark_adventure_2.jpg')
status_bg = pygame.image.load('Dating_sim_pic/status_bg.jpg')
setting_bg = pygame.image.load('Dating_sim_pic/setting_bg.jpg')
music_bg = pygame.image.load('Dating_sim_pic/music_bg.jpg')
Elara_main = pygame.transform.scale(pygame.image.load('Dating_sim_pic/Elara_main.jpg'), (700, 700))
Elara_main = pygame.transform.flip(Elara_main, True, False)
image_mapping = \
    {0: play_bg1, 1: play_bg1, 2: squirrel_bg, 3: paused_squirrel_bg, 4: paused_squirrel_bg2, 5: running_squirrel,
     6: running_squirrel, 7: persistent_squirrel, 8: enchanted_cave, 9: Elara, 10: Elara_playing_with_animals,
     11: Elara_suprised, 12: Elara_suprised, 13: Squirrel_point, 14: Elara_explain, 15: Elara_with_animals,
     16: Elara_stroke_bunny, 17: Elara_admired, 18: Elara_ask, 19: Elara_end_chap1, 20: Elara_end_chap1_2}
pygame.mixer.music.load('Sunflowers.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0)
black = (0, 0, 0)
white = (255, 255, 255)
light_cyan = (140, 245, 245)
light_orange = (250, 197, 82)
user_name = ''
messages_beginning = [' ']
messages_ask_ruins = [' ']
messages_ask_waterfall = [' ']
messages_stay_silent = [' ']
messages_ask_Elara_feelings = [' ']
messages_share_story = [' ']
chose_optionsA1 = [False, False]
chose_optionsA2 = [False, False, False]
all_message = [messages_beginning, messages_ask_waterfall, messages_ask_ruins, messages_stay_silent,
               messages_ask_Elara_feelings, messages_share_story]
current_message = messages_beginning
love_scale = 0
active_x = 19
counter = 0
speed = 2
fixer1 = 0
fixer2 = 500
chap1_end, chap2_end, has_chosenA1, has_chosenA2 = False, False, False, False
blit_Elara, blit_optionsA2 = False, False
for button in buttons_menu:
    button.set_alpha(200)


def check_date():
    current_date = datetime.date.today()
    target_date = datetime.date(2023, 7, 3)

    if current_date == target_date:
        return True
    else:
        return False


def create_button_bg(x_coor, y_coor, width, height, color):
    normal_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    border_surface = pygame.Surface((width + 8, height + 8), pygame.SRCALPHA)
    alpha_value = 125

    normal_surface.fill((*color[:3], alpha_value))
    border_surface.fill((255, 255, 255, alpha_value))

    normal_rect = normal_surface.get_rect(center=(x_coor, y_coor))
    border_rect = border_surface.get_rect(center=(x_coor, y_coor))

    screen.blit(border_surface, border_rect)
    screen.blit(normal_surface, normal_rect)


def make_lines_for_message(words, font):
    lines = []
    current_line = ''
    for word in words:
        test_line = current_line + word + ' '
        if font.size(test_line)[0] <= 900:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + ' '
    lines.append(current_line)

    # Draw the lines of text
    for i, line in enumerate(lines):
        text = font.render(line, True, white)
        screen.blit(text, (75, 520 + i * 30))


def lovometer(scale, x, y):
    ratio = scale/600
    love_scaling = pygame.Rect(x, y, 600*ratio, 40)
    love_border = pygame.Rect(x-5, y-5, 610, 50)
    pygame.draw.rect(screen, (240, 213, 236), love_border, width=5)
    pygame.draw.rect(screen, (250, 107, 231), love_scaling)

# Combine the changeColor and the update function into one and make it possible to do multiple buttons at once


def change_update(position, list):
    for buttons in list:
        buttons.changeColor(position)
        buttons.update(screen)


def get_font(size):
    return pygame.font.Font('font.ttf', size)


def Music():
    global buttons_menu, chap1_end
    Back = Button(buttons_menu[1], 'Back', (RES[0] / 2, 700), get_font(30), black, white)
    font = get_font(30)
    font2 = get_font(40)
    volume_up_button = Button(None, '+', (480, 625), font, white, black)
    volume_down_button = Button(None, '-', (520 + 40, 625), font, white, black)
    MUSIC_1_X = 100
    MUSIC_1 = Button(image=None, text_input='Renai circulation', font=font2, pos=(540, MUSIC_1_X), base_color='Gold',
                     hovering_color=white)
    MUSIC_2 = Button(image=None, text_input='ChinaX', font=font2, pos=(520, MUSIC_1_X + 150), base_color='Gold',
                     hovering_color=white)
    MUSIC_3 = Button(image=None, text_input='base', font=font2, pos=(520, MUSIC_1_X + 300), base_color='Gold',
                     hovering_color=white)
    MUSIC_STOP = Button(image=None, text_input='Mute', font=font2, pos=(520, MUSIC_1_X + 450), base_color='Gold',
                        hovering_color=white)
    button_bg_color = (247, 191, 121)
    while True:
        setting_mouse_pos = pygame.mouse.get_pos()
        screen.blit(music_bg, (0, -100))
        list_button = [Back, MUSIC_1, MUSIC_2, MUSIC_3, MUSIC_STOP, volume_down_button, volume_up_button]
        music_button = [MUSIC_1, MUSIC_2, MUSIC_3]
        create_button_bg(520, 100, 750, 75, button_bg_color)
        create_button_bg(520, 250, 300, 75, button_bg_color)
        create_button_bg(520, 400, 300, 75, button_bg_color)
        create_button_bg(520, 550, 300, 75, button_bg_color)
        change_update(setting_mouse_pos, list_button)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Back.checkforInput(setting_mouse_pos):
                    setting()
                for buttons in music_button:
                    if buttons.checkforInput(setting_mouse_pos):
                        pygame.mixer.music.stop()
                        if buttons is MUSIC_1:
                            pygame.mixer.music.load('Renai Circulation - Sengoku Nadeko.mp3')
                        elif buttons is MUSIC_2:
                            pygame.mixer.music.load('ANIME_GAME_PICS/ChinaX-Nightcore.mp3')
                        elif buttons is MUSIC_3:
                            pygame.mixer.music.load('Otjanbird-Pt.-II.mp3')
                        pygame.mixer.music.play(-1)
                    current_volume = pygame.mixer.music.get_volume()
                    if current_volume <= 0.9:
                        pygame.mixer.music.set_volume(current_volume + 0.1)
                    else:
                        pygame.mixer.music.set_volume(1.0)
                if volume_down_button.checkforInput(setting_mouse_pos):
                    current_volume = pygame.mixer.music.get_volume()
                    if current_volume >= 0.1:
                        pygame.mixer.music.set_volume(current_volume - 0.1)
                    else:
                        pygame.mixer.music.set_volume(0)
                if MUSIC_STOP.checkforInput(setting_mouse_pos):
                    pygame.mixer.music.set_volume(0)
        pygame.display.update()
        pygame.display.flip()


def Status():
    global chap1_end
    font = get_font(20)
    back_button = Button(buttons_menu[1], 'Back', (RES[0] / 2, RES[1]*0.945), get_font(30), (0, 0, 0), (255, 255, 255))
    unfinished_color = (0, 0, 255)
    finished_color = (0, 255, 0)
    list_button = [back_button]
    color = unfinished_color
    while True:
        screen.fill((100, 100, 100))
        screen.blit(status_bg, (0, 0))
        status_mouse_pos = pygame.mouse.get_pos()
        chap_1 = font.render('Chapter 1', True, color)
        chap_2 = font.render('Chapter 2', True, unfinished_color)
        if chap1_end:
            color = finished_color
        create_button_bg(525, 125, 300, 100, (255, 0, 0))
        create_button_bg(525, 325, 300, 100, (255, 0, 0))
        screen.blit(chap_1, (435, 115))
        screen.blit(chap_2, (435, 315))
        lovometer(love_scale, RES[0]/2 - 300, 500)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkforInput(status_mouse_pos):
                    setting()
        change_update(status_mouse_pos, list_button)
        pygame.display.flip()
        pygame.display.update()


def setting():
    font = get_font(45)
    back_button = Button(buttons_menu[1], 'Back', (RES[0] / 2, RES[1]*0.945), get_font(30), (0, 0, 0), (255, 255, 255))
    Music_button = Button(None, 'Music', (RES[0] / 2, RES[1]*0.155), font, (0, 0, 0), (255, 255, 255))
    Chaps_button = Button(None, 'Chapters', (RES[0] / 2, RES[1]*0.425), font, (0, 0, 0), (255, 255, 255))
    list_button = [Music_button, Chaps_button, back_button]
    while True:
        screen.fill((100, 100, 100))
        screen.blit(setting_bg, (0, 0))
        setting_mouse_pos = pygame.mouse.get_pos()
        create_button_bg(RES[0]/2, RES[1]*0.155, 450, 100, light_cyan)
        create_button_bg(RES[0]/2, RES[1]*0.425, 500, 100, light_cyan)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Music_button.checkforInput(setting_mouse_pos):
                    Music()
                if Chaps_button.checkforInput(setting_mouse_pos):
                    Status()
                if back_button.checkforInput(setting_mouse_pos):
                    Menu()
        change_update(setting_mouse_pos, list_button)
        pygame.display.flip()
        pygame.display.update()


def play():
    global buttons_menu, active_x, speed, counter, chap1_end, chap2_end, has_chosenA1, fixer1, \
        current_message, all_message, chose_optionsA1, blit_Elara, blit_optionsA2, has_chosenA2, fixer2, love_scale
    font = get_font(20)
    done = False
    paused = False
    game_quit = Button(None, 'Quit', (RES[0]/2, RES[1]*0.46), get_font(30), (252, 122, 86), (252, 186, 86))
    speech_frame = pygame.transform.scale(buttons_menu[0], (RES[0]-100, 200))
    sf_x, sf_y = RES[0] / 2, RES[1] * 0.81
    speech_frame = Button(speech_frame, '', (sf_x, sf_y), font, (247, 236, 136), (247, 236, 136))
    speech_frame_border = pygame.Surface((RES[0] - 84, 216), pygame.SRCALPHA)
    speech_frame_border.fill((255, 255, 255))
    speech_frame_border_rect = speech_frame_border.get_rect(center=(RES[0] / 2, 600))
    optionA1a = Button(None, 'Explore the enchanted waterfall', (375 + fixer1, 350 + fixer1), font, black, white)
    optionA1b = Button(None, 'Ask about ruins', (225 + fixer1, 450 + fixer1), font, black, white)
    optionA2a = Button(None, "....", (250 + fixer2, 250 + fixer2), font, black, white)
    optionA2b = Button(None, "Ask about Elara's feelings", (375 + fixer2, 350 + fixer2), font, black, white)
    optionA2c = Button(None, "Share a story", (250 + fixer2, 450 + fixer2), font, black, white)
    list_button1 = [optionA1a, optionA1b]
    list_button2 = [optionA2a, optionA2b, optionA2c]
    arrow_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
    arrow_dir = 1
    arrow_speed = 1
    arrow_pos_x = 875
    transition_time = 120  # Number of frames for the transition
    transition_counter = 0
    if not has_chosenA1:
        current_message = messages_beginning
    elif chose_optionsA1[0]:
        current_message = messages_ask_waterfall
    elif chose_optionsA1[1]:
        current_message = messages_ask_ruins
    if not has_chosenA1:
        playing_bg1 = image_mapping.get(active_x)
    else:
        playing_bg1 = play_bg1
    message = current_message[active_x]
    while True:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_quit.checkforInput(mouse_pos):
                    paused = not paused
                    Menu()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
        pause_button = get_font(30).render('Paused', True, (191, 117, 180))
        list = [game_quit]
        if paused:
            change_update(mouse_pos, list)
            screen.blit(pause_button, (425, 275))
        pygame.display.update()
        pygame.display.flip()
        while not paused:
            clock.tick(60)
            play_mouse_pos = pygame.mouse.get_pos()
            if transition_counter > 0:
                alpha_value = 255 * (transition_counter / transition_time)
                transition_counter -= 1
            else:
                alpha_value = 0
            playing_bg1.set_alpha(255 - alpha_value)
            screen.blit(playing_bg1, (0, -100))
            list1 = [speech_frame]
            speech_frame_border.set_alpha(175)
            if blit_Elara:
                screen.blit(Elara_main, (RES[0] - Elara_main.get_width(), 60))
            screen.blit(speech_frame_border, speech_frame_border_rect)
            change_update(play_mouse_pos, list1)
            if counter < speed * len(message):
                counter += 1
            elif counter >= speed * len(message):
                done = True
            words = current_message[active_x][0:counter // speed].split(' ')
            make_lines_for_message(words, font)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for buttons in list_button1:
                        if buttons.checkforInput(play_mouse_pos):
                            active_x = 0
                            counter = 0
                            has_chosenA1 = True
                            if buttons is optionA1a:
                                chose_optionsA1[0] = True
                                message = messages_ask_waterfall[active_x]
                                love_scale += 10
                                current_message = messages_ask_waterfall
                            if buttons is optionA1b:
                                chose_optionsA1[1] = True
                                message = messages_ask_ruins[active_x]
                                love_scale += 5
                                current_message = messages_ask_ruins
                            done = False
                            print(love_scale)
                    for buttons in list_button2:
                        if buttons.checkforInput(play_mouse_pos) and has_chosenA1:
                            active_x = 0
                            counter = 0
                            has_chosenA2 = True
                            if buttons is optionA2a:
                                chose_optionsA2[0] = True
                                message = messages_stay_silent[active_x]
                                current_message = messages_stay_silent
                            if buttons is optionA2b:
                                chose_optionsA2[1] = True
                                message = messages_ask_Elara_feelings[active_x]
                                love_scale += 5
                                current_message = messages_ask_Elara_feelings
                            if buttons is optionA2c:
                                chose_optionsA2[2] = True
                                message = messages_share_story[active_x]
                                love_scale += 100
                                current_message = messages_share_story
                            done = False
                            print(love_scale)
                    if speech_frame.checkforInput(play_mouse_pos):
                        if done and active_x < len(current_message) - 1:
                            active_x += 1
                            transition_counter = transition_time
                            if not has_chosenA1:
                                playing_bg1 = image_mapping.get(active_x, play_bg1)
                                if active_x == 20:
                                    chap1_end = True
                            else:
                                playing_bg1 = play_bg1
                            if chose_optionsA1[0] or chose_optionsA1[1]:
                                blit_Elara = True
                                if not has_chosenA2:
                                    chose_optionsA2[1] = False
                                    has_chosenA2 = False
                                if active_x == len(current_message) - 1:
                                    blit_optionsA2 = True
                            done = False
                            message = current_message[active_x]
                            counter = 0
                        else:
                            counter = speed * len(message)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = not paused
            if has_chosenA1:
                fixer2 = 0
            if blit_optionsA2:
                fixer1 = 500
                optionA1a = Button(None, 'Explore the enchanted waterfall', (375+fixer1, 350+fixer1), font, black, white)
                optionA1b = Button(None, 'Ask about ruins', (225+fixer1, 450+fixer1), font, black, white)
                list_button1 = [optionA1a, optionA1b]
                change_update(play_mouse_pos, list_button1)
            if chap1_end and done and not has_chosenA1:
                create_button_bg(375, 350, 655, 60, light_orange)
                create_button_bg(250, 450, 400, 60, light_orange)
                change_update(play_mouse_pos, list_button1)
            if blit_optionsA2 and done and not has_chosenA2:
                create_button_bg(375, 350, 655, 60, light_orange)
                create_button_bg(250, 450, 400, 60, light_orange)
                create_button_bg(250, 250, 400, 60, light_orange)
                optionA2a = Button(None, "....", (250 + fixer2, 250 + fixer2), font, black, white)
                optionA2b = Button(None, "Ask about Elara's feelings", (375 + fixer2, 350 + fixer2), font, black, white)
                optionA2c = Button(None, "Share a story", (250 + fixer2, 450 + fixer2), font, black, white)
                list_button2 = [optionA2a, optionA2b, optionA2c]
                change_update(play_mouse_pos, list_button2)
                print('updated')
            arrow_rect = arrow_surface.get_rect(center=(arrow_pos_x, 650))
            if done:
                pygame.draw.polygon(arrow_surface, (100, 100, 100), [(0, 0), (0, 50), (50, 25)])
                screen.blit(arrow_surface, arrow_rect)
                arrow_pos_x += arrow_speed * arrow_dir
                if arrow_pos_x <= 850 or arrow_pos_x >= 900:
                    arrow_dir *= -1
            pygame.display.flip()
            pygame.display.update()


def Menu():
    global buttons_menu
    font = get_font(45)
    Settings = Button(None, 'Settings', (RES[0] / 2, 600), font, (255, 255, 255),
                      (245, 137, 221))
    Play = Button(None, 'Play', (RES[0] / 2, 300), font, (255, 255, 255), (245, 137, 221))
    menu_bg = pygame.image.load('Dating_sim_pic/menu_bg.jpg').convert_alpha()
    while True:
        clock.tick(60)  # Limit the frame rate to 60 FPS
        screen.blit(menu_bg, (0, -200))
        Menu_mouse_pos = pygame.mouse.get_pos()
        button_list = [Settings, Play]
        create_button_bg(Settings.x_cor, Settings.y_cor, 375, 75, (247, 191, 121))
        create_button_bg(Play.x_cor, Play.y_cor, 300, 75, (247, 191, 121))
        change_update(Menu_mouse_pos, button_list)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if Settings.checkforInput(Menu_mouse_pos):
                    setting()
                if Play.checkforInput(Menu_mouse_pos):
                    play()
        pygame.display.update()


def get_name():
    global user_name, messages_ask_ruins, messages_ask_waterfall, messages_beginning, messages_stay_silent, \
        messages_ask_Elara_feelings, messages_share_story
    surface_width = 300
    input_rect_alt = Button(None, '          ', (RES[0] / 2, 300), get_font(30), (0, 0, 0), (0, 0, 0))
    list_button = [input_rect_alt]
    active = False
    font = get_font(30)
    name_bg = pygame.image.load('Dating_sim_pic/name_bg.jpg').convert_alpha()
    input_surface = pygame.Surface((surface_width, 75), pygame.SRCALPHA)
    input_rect = input_surface.get_rect(center=(input_rect_alt.x_cor, input_rect_alt.y_cor))
    arrow_surface = pygame.Surface((40, 20), pygame.SRCALPHA)
    arrow_pos_y = input_rect.y + 80  # Initial y position of the arrow
    arrow_speed = 0.5  # Speed of the arrow's movement
    arrow_direction = 1  # Direction of the arrow's movement (1 for up, -1 for down)
    arrow_text = get_font(30).render('Your name', True, (252, 157, 3))

    while True:
        mouse_pos = pygame.mouse.get_pos()
        border_surface = pygame.Surface((surface_width + 8, 83), pygame.SRCALPHA)
        input_surface = pygame.Surface((surface_width, 75), pygame.SRCALPHA)
        border_surface.fill((255, 255, 255, 150))
        input_surface.fill((145, 64, 198, 150))
        border_rect = border_surface.get_rect(center=(input_rect_alt.x_cor, input_rect_alt.y_cor))
        input_rect = input_surface.get_rect(center=(input_rect_alt.x_cor, input_rect_alt.y_cor))
        screen.fill((100, 100, 100))
        screen.blit(name_bg, (0, -100))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_BACKSPACE:
                    user_name = user_name[:-1]
                elif event.key == pygame.K_RETURN:
                    active = False  # Deactivate input if Enter key is pressed
                elif event.key != pygame.K_BACKSPACE:
                    user_name += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect_alt.checkforInput(mouse_pos):
                    active = True
                else:
                    active = False  # Deactivate input if clicked outside input box area

        screen.blit(border_surface, border_rect)
        screen.blit(input_surface, input_rect)
        text_surface = font.render(user_name, True, (255, 255, 255))
        screen.blit(text_surface, (input_rect.x + 15, input_rect.y + 15))
        surface_width = max(text_surface.get_width() + 20, 300)
        arrow_pos_y += arrow_speed * arrow_direction  # Update the arrow's y position
        if arrow_pos_y <= input_rect.y + 80 or arrow_pos_y >= input_rect.y + 100:
            arrow_direction *= -1  # Reverse the direction when reaching the upper or lower limit
        pygame.draw.polygon(arrow_surface, (255, 255, 255), [(0, 20), (20, 0), (40, 20)])  # Draw the arrow shape
        arrow_rect = arrow_surface.get_rect(midtop=(input_rect.x + input_rect.width / 2, arrow_pos_y))
        screen.blit(arrow_surface, arrow_rect)
        screen.blit(arrow_text, (arrow_rect.x - 110, arrow_rect.y + 50))
        change_update(mouse_pos, list_button)
        clock.tick(FPS)
        pygame.display.flip()
        pygame.display.update()
        if not active and len(user_name) > 0:
            messages_beginning = [
                '{}: Lost in the forest Ah, where am I? This forest seems endless. I hope I can find my way out soon.'.format(
                    user_name),
                'Suddenly, a lively squirrel appears, chattering and scampering around.',
                '{}: Hey there, little guy. You seem to know your way around here. Mind showing me the way '
                'out of this forest?'.format(user_name),
                'Squirrel pauses, looks back at {}, and then starts dashing deeper into the forest.'.format(user_name),
                '{}: Huh? Wait up! Maybe that squirrel knows something. I should follow it and see where it '
                'leads me.'.format(user_name),
                '{} follows the squirrel, maneuvering through the dense foliage and underbrush.'.format(user_name),
                "{}: This squirrel is quite persistent. It must be taking me somewhere important.".format(user_name),
                "The squirrel leads {} to a hidden grove within the forest, where sunlight filters through "
                "the canopy, illuminating a beautiful meadow.".format(user_name),
                "{}: Wow, I never expected to find such a serene place in this forest. It's breathtaking.".format(user_name),
                "Suddenly, {} notices Elara playfully chasing after woodland creatures in the meadow.".format(user_name),
                "{}: Is that... Elara? She seems to be having a blast with those animals. Her laughter is "
                "infectious.".format(user_name),
                "{}'s curiosity gets the better of them, and they step forward, accidentally "
                "catching Elara's attention.".format(user_name),
                "Elara: (Surprised and slightly off balance) Oh! Well, hello there! "
                "You caught me off guard. I didn't expect to see anyone else here.",
                "{}: Hi! Sorry for interrupting your playful chase, I was actually following this squirrel,"
                "and it led me to this magical meadow. My name is {}, you are Elara right?".format(user_name, user_name),
                "Your name has been whispered among the forest's whispers. I heard tales of your bond with "
                "animals and the wonders you bring to this realm.",
                "Elara: (Grinning mischievously) Ah, yes I'm Elara, (turns to look at the squirrel) that "
                "little rascal! They seem to have a knack for guiding lost wanderers. I'm glad it brought you "
                "here.",
                "{}: It's incredible to witness your interaction with these creatures. You have a special "
                "bond with them, don't you?".format(user_name),
                "Elara: (Gently stroking a nearby rabbit) Yes, I do. I can communicate with animals and "
                "understand their needs. It's one of the many wonders of this magical realm.",
                "{}: That's amazing! I've always admired people who can connect with nature. I'm fascinated "
                "by this enchanting world.".format(user_name),
                "Elara: Well, since you've stumbled upon this meadow, how about I become your guide? I can "
                "help you navigate through this realm and uncover its secrets.",
                "{}: That sounds incredible! I'd be honored to have you as my guide, Elara. Let's embark on "
                "this adventure together.".format(user_name)]
            messages_ask_ruins = [
                "{}: (Curious) This forest seems like it's filled with mysteries. I can't help but wonder, are there "
                "any ancient ruins hidden within its depths?".format(user_name),
                "Elara: Ah, the ancient ruins... They hold a great mystery and history within these enchanted woods. ",
                "Elara: Many adventurers have tried to uncover their secrets, but few have succeeded.",
                "Elara: Legend has it that deep within the ruins lies a hidden artifact of immense power. It is said "
                "to grant unimaginable abilities to those who possess it.",
                "Elara: However, accessing the ruins is not an easy task. The path is treacherous and filled with "
                "dangerous obstacles.",
                "Elara: Only the brave and determined can hope to find their way through.",
                "Elara: If you truly seek the secrets of the ruins, we can embark on a perilous journey together.",
                "Elara: But be warned, the challenges we'll face are not to be taken lightly.",
                "{}: (Contemplating) The ruins sound intriguing, but I must be cautious. I need more "
                "information before deciding.".format(user_name),
                "Elara: (Nods) Understandable. Take your time to weigh your options. Should you choose to venture "
                "into the ruins, know that I'll be by your side, guiding and protecting you."
            ]
            messages_ask_waterfall = [
                "{}: The waterfall here sounds captivating. I'm drawn to its beauty and the promise of serenity. "
                "But before we embark on this journey, may I ask you a question?".format(user_name),
                "Elara: Yes? (looks with curiosity)",
                "{}: Are there any dangers we should be aware of when exploring the waterfall? I want to ensure our "
                "safety during this adventure.".format(user_name),
                "Elara: (Thoughtful) Ah, a wise question indeed. While the waterfall is a place of enchantment and "
                "tranquility, there are natural elements we should consider.",
                "Elara:  The terrain around the waterfall can be slippery, so we must exercise caution. The currents "
                "can be strong, especially after heavy rainfall.",
                "Elara: It's important to stay vigilant and be mindful of our surroundings.",
                "Elara: Additionally, the waterfall attracts various wildlife, including some that may be "
                "territorial. We should respect their habitat and maintain a safe distance.",
                "Elara: But fear not, I have extensive knowledge of the area, and together we can navigate the "
                "waterfall with care and appreciation for its beauty.",
                "{}: (Grateful) I appreciate your guidance and concern for our safety. With your expertise, "
                "I feel confident in exploring the waterfall.".format(user_name),
                "Elara: If you wish to explore the waterfall, I'll gladly accompany you. Together, "
                "we can immerse ourselves in its enchanting presence and uncover its secrets."
            ]
            messages_stay_silent = [
                "{}: ...".format(user_name),
                "Elara: (Understanding) It's alright if you don't have an answer right now. Sometimes, actions speak "
                "louder than words.",
                "Elara: Let's continue our journey to the waterfall and let the magic of this forest unfold around us."
            ]
            messages_ask_Elara_feelings = [
                "{}: Well, Elara, your kindness and warmth have caught my attention. It feels as though there's a "
                "deeper reason behind it. Can you share what you're feeling?".format(user_name),
                "Elara: (Laughs softly) I appreciate your curiosity. The truth is, this enchanted forest has a way of "
                "bringing people together, revealing hidden connections and shared destinies.",
                "Elara: It's as if fate has intertwined our paths for a greater purpose.",
                "Elara: I sense a genuine spirit within you, someone who appreciates the wonders of nature and holds "
                "a deep curiosity for the unknown.",
                "Elara: It's that spark that has inspired me to be open and guide you through this realm",
                "{}: (Moved) Your words touch my heart. I believe our meeting in this magical place is no "
                "coincidence. Now, let's begin!".format(user_name)
            ]
            messages_share_story = [
                "{}: Elara, before we continue, I want to express my sincere gratitude for your "
                "kindness and guidance thus far.".format(user_name),
                "{}:Your presence and the way you connect with nature have already made "
                "a profound impact on me.".format(user_name),
                "Elara: (Curious) Thank you, {}. I'm glad to have had a positive influence on you. Is there something "
                "specific you'd like to share or discuss?".format(user_name),
                "{}: (Reflective) Actually, there's a personal story I'd like to share. In my childhood, "
                "I often found solace and joy in the beauty of nature.".format(user_name),
                "{}:There was a small creek near my home where I would spend hours exploring, captivated by the "
                "flowing water and the gentle sounds of the forest.".format(user_name),
                "{}: But as time went on, life became busier, and I lost touch with that connection.".format(user_name),
                "{}: Being here with you, in this enchanting forest, brings back those cherished memories and "
                "rekindles a sense of wonder within me.".format(user_name),
                "Elara: (Listening attentively) Nature has a remarkable way of touching our souls and reminding us of "
                "the magic that exists in the world.",
                "Elara: It's heartening to hear your story and witness the reawakening of that connection.",
                "{}: Your presence and the way you interact with nature have reminded me of the beauty and serenity "
                "that lies within this realm.".format(user_name),
                "{}: I am grateful to have crossed paths with you and to be embarking on this adventure "
                "together.".format(user_name),
                "Elara: (Smiling) The feeling is mutual. Our shared appreciation for nature brings us closer, "
                "and I believe it's no coincidence that our paths have converged.",
                "Elara: Together, we can continue to explore, learn, and uncover the mysteries of this enchanted "
                "forest.",
                "{}: (Filled with anticipation) I couldn't agree more, Elara. Thanks for your kindness, by the way, "
                "should we go now?".format(user_name),
                "Elara: (Excited) Absolutely, {}. The forest is waiting, ready to reveal its secrets.".format(user_name),
                "Elara: Let's delve deeper into its wonders and forge an unforgettable connection with this magical "
                "realm. Our adventure begins now"
            ]

            Menu()


def hpbd_event():
    font = get_font(20)
    happy_birthday_bg = pygame.image.load('Dating_sim_pic/happy_birthday_event.jpg')
    speech_frame = pygame.transform.scale(buttons_menu[0], (924, 200))
    speech_frame = Button(speech_frame, '', (RES[0] / 2, 600), font, (247, 236, 136), (247, 236, 136))
    speech_frame_border = pygame.Surface((940, 216), pygame.SRCALPHA)
    speech_frame_border_rect = speech_frame_border.get_rect(center=(RES[0] / 2, 600))
    speech_frame_border.set_alpha(125)
    hpbd_messages = ['Hello! do you know what date is it???', "Exactly! Today is my BIRTHDAY!!!",
                     "So for this special occasion, I got a mission for us as a family.",
                     "Let's create a memorable photo album together that reflects our journey and reminds us of the "
                     "love and joy we share.",
                     "Follow the steps below to complete the mission and strengthen our bond!",
                     "Gather around the bedroom: Set up a cozy space where we can sit together "
                     "with enough room for the photo albums.",
                     "Reflect on memories: Take turns sharing stories and memories associated with each photo you've "
                     "collected.",
                     "Discuss the emotions and experiences tied to those moments.",
                     "If you can't remember all of the steps above, I've hand written that out, open my diary and "
                     "take the paper that's currently in it out. The steps are in there. Good luck!",
                     "Note1: For mah big brother, STARDEW VALLEY!!!! I just realized it's an isometric game O_o",
                     "Note2: If Daddy can't attend this, mommy do it =))",
                     "Last note (for the day daddy see this): What do you think the thing I struggled the most while "
                     "making this game is? And why?",
                     "Hint: It was thought to be obvious, but I only realized how hard it is when I tried to do it."]
    Continue_game = Button(None, 'Head to the game', (RES[0] / 2, RES[1] / 2), get_font(45), (0, 0, 0), (194, 245, 86))
    arrow_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
    arrow_dir = 1
    arrow_speed = 1
    arrow_pos_x = 875
    hpbd_count = 0
    hpbd_active_message = 0
    hpbd_speed = 3
    hpbd_done = False
    hpbd_message = hpbd_messages[hpbd_active_message]
    while True:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        speech_frame_border.fill((225, 225, 225))
        speech_frame_border.set_alpha(125)
        list1 = [speech_frame]
        list2 = [Continue_game]
        screen.blit(happy_birthday_bg, (0, -200))
        screen.blit(speech_frame_border, speech_frame_border_rect)
        change_update(mouse_pos, list1)
        hpbd_words = hpbd_message[0:hpbd_count // hpbd_speed].split(' ')
        make_lines_for_message(hpbd_words, font)
        if hpbd_count <= hpbd_speed * len(hpbd_message):
            hpbd_count += 1
        elif hpbd_count >= hpbd_speed * len(hpbd_message):
            hpbd_done = True
        if hpbd_active_message == len(hpbd_messages) - 1 and hpbd_done:
            change_update(mouse_pos, list2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if speech_frame.checkforInput(mouse_pos):
                    if hpbd_done and hpbd_active_message < len(hpbd_messages) - 1:
                        hpbd_active_message += 1
                        hpbd_message = hpbd_messages[hpbd_active_message]
                        hpbd_count = 0
                        hpbd_done = False
                    else:
                        hpbd_count = hpbd_speed * len(hpbd_message)
                if Continue_game.checkforInput(mouse_pos):
                    get_name()
        arrow_rect = arrow_surface.get_rect(center=(arrow_pos_x, 650))
        if hpbd_done:
            pygame.draw.polygon(arrow_surface, (100, 100, 100), [(0, 0), (0, 50), (50, 25)])
            screen.blit(arrow_surface, arrow_rect)
            arrow_pos_x += arrow_speed * arrow_dir
            if arrow_pos_x <= 850 or arrow_pos_x >= 900:
                arrow_dir *= -1
        pygame.display.flip()
        pygame.display.update()


if check_date():
    hpbd_event()
else:
    get_name()
