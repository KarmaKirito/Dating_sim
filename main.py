import pygame, sys
import datetime

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
user_name = ''
messages = [' ']
active_x = 0
message = messages[active_x]
counter = 0
speed = 1
'''pygame.mixer.music.load('Renai Circulation - Sengoku Nadeko.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(1)'''
for button in buttons_menu:
    button.set_alpha(200)


def check_date():
    current_date = datetime.date.today()
    target_date = datetime.date(2023, 6, 28)

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
        text = font.render(line, True, (255, 255, 255))
        screen.blit(text, (75, 520 + i * 30))


class Button:
    def __init__(self, image, text_input, pos, font, base_color, hovering_color):
        self.image, self.text_input = image, text_input
        self.x_cor = pos[0]
        self.y_cor = pos[1]
        self.font, self.base_color, self.hovering_color = font, base_color, hovering_color
        self.text = self.font.render(self.text_input, True, (255, 255, 255))
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_cor, self.y_cor))
        self.text_rect = self.text.get_rect(center=(self.x_cor, self.y_cor))

    def update(self):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkforInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


def change_update(position, list):
    for buttons in list:
        buttons.changeColor(position)
        buttons.update()


def get_font(size):
    return pygame.font.Font('font.ttf', size)


def setting():
    global buttons_menu
    Back = Button(buttons_menu[1], 'Back', (RES[0] / 2, 600), get_font(30), (0, 0, 0), (255, 255, 255))
    while True:
        setting_mouse_pos = pygame.mouse.get_pos()
        screen.fill((100, 100, 100))
        list = [Back]
        change_update(setting_mouse_pos, list)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Back.checkforInput(setting_mouse_pos):
                    Menu()
        pygame.display.update()
        pygame.display.flip()


def play():
    global buttons_menu, messages, active_x, speed, counter, message, user_name
    font = get_font(20)
    done = False
    paused = False
    game_quit = Button(None, 'Quit', (525, 340), get_font(30), (252, 122, 86), (252, 186, 86))
    speech_frame = pygame.transform.scale(buttons_menu[0], (924, 200))
    speech_frame = Button(speech_frame, '', (RES[0] / 2, 600), font, (247, 236, 136), (247, 236, 136))
    speech_frame_border = pygame.Surface((940, 216), pygame.SRCALPHA)
    speech_frame_border.fill((255, 255, 255))
    speech_frame_border_rect = speech_frame_border.get_rect(center=(RES[0] / 2, 600))
    arrow_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
    arrow_dir = 1
    arrow_speed = 1
    arrow_pos_x = 875
    transition_time = 120  # Number of frames for the transition
    transition_counter = 0
    playing_bg1 = play_bg1
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
            screen.blit(speech_frame_border, speech_frame_border_rect)
            change_update(play_mouse_pos, list1)
            if counter < speed * len(message):
                counter += 1
            elif counter >= speed * len(message):
                done = True
            words = messages[active_x][0:counter // speed].split(' ')
            make_lines_for_message(words, font)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if speech_frame.checkforInput(play_mouse_pos):
                        if done and active_x < len(messages) - 1:
                            active_x += 1
                            transition_counter = transition_time
                            if active_x == 2:
                                playing_bg1 = squirrel_bg
                            elif active_x == 3:
                                playing_bg1 = paused_squirrel_bg
                            elif active_x == 4:
                                playing_bg1 = paused_squirrel_bg2
                            elif active_x == 5 or active_x == 6:
                                playing_bg1 = running_squirrel
                            elif active_x == 7:
                                playing_bg1 = persistent_squirrel
                            elif active_x == 8:
                                playing_bg1 = enchanted_cave
                            elif active_x == 9:
                                playing_bg1 = Elara
                            elif active_x == 10:
                                playing_bg1 = Elara_playing_with_animals
                            elif active_x == 11 or active_x == 12:
                                playing_bg1 = Elara_suprised
                            elif active_x == 13:
                                playing_bg1 = Squirrel_point
                            elif active_x == 14:
                                playing_bg1 = Elara_explain
                            else:
                                playing_bg1 = play_bg1
                            done = False
                            message = messages[active_x]
                            counter = 0
                        else:
                            counter = speed * len(message)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = not paused
                    if event.key == pygame.K_RETURN:
                        if done and active_x < len(messages) - 1:
                            active_x += 1
                            transition_counter = transition_time
                            if active_x == 2:
                                playing_bg1 = squirrel_bg
                            elif active_x == 3:
                                playing_bg1 = paused_squirrel_bg
                            elif active_x == 4:
                                playing_bg1 = paused_squirrel_bg2
                            elif active_x == 5 or active_x == 6:
                                playing_bg1 = running_squirrel
                            elif active_x == 7:
                                playing_bg1 = persistent_squirrel
                            elif active_x == 8:
                                playing_bg1 = enchanted_cave
                            else:
                                playing_bg1 = play_bg1
                            done = False
                            message = messages[active_x]
                            counter = 0
                        else:
                            counter = speed * len(message)
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
    global buttons_menu, user_name
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
    global user_name, messages, message
    surface_width = 300
    input_rect_alt = Button(None, '          ', (RES[0] / 2, 300), get_font(30), (0, 0, 0), (0, 0, 0))
    list = [input_rect_alt]
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

        change_update(mouse_pos, list)
        clock.tick(FPS)
        pygame.display.flip()
        pygame.display.update()

        if not active and len(user_name) > 0:
            messages = ['{}: Lost in the forest Ah, where am I? This forest seems endless. I hope I can find my way '
                        'out soon.'.format(user_name),
                        'Suddenly, a lively squirrel appears, chattering and scampering around.',
                        '{}: Hey there, little guy. You seem to know your way around here. Mind showing me the way '
                        'out of this forest?'.format(user_name),
                        'Squirrel pauses, looks back at MC, and then starts dashing deeper into the forest.',
                        '{}: Huh? Wait up! Maybe that squirrel knows something. I should follow it and see where it '
                        'leads me.'.format(user_name),
                        '{} follows the squirrel, maneuvering through the dense foliage and underbrush.'.format(
                            user_name),
                        "{}: This squirrel is quite persistent. It must be taking me somewhere important.".format(
                            user_name),
                        "The squirrel leads MC to a hidden grove within the forest, where sunlight filters through "
                        "the canopy, illuminating a beautiful meadow.",
                        "{}: Wow, I never expected to find such a serene place in this forest. It's breathtaking.".format(
                            user_name),
                        "Suddenly, {} notices Elara playfully chasing after woodland creatures in the meadow.".format(
                            user_name),
                        "{}: Is that... Elara? She seems to be having a blast with those animals. Her laughter is "
                        "infectious.".format(user_name),
                        "{}'s curiosity gets the better of them, and they step forward, accidentally "
                        "catching Elara's attention.".format(user_name),
                        "Elara: (Surprised and slightly off balance) Oh! Well, hello there! "
                        "You caught me off guard. I didn't expect to see anyone else here.",
                        "{}: Hi! Sorry for interrupting your playful chase. I was actually following this squirrel, "
                        "and it led me to this magical meadow.".format(user_name),
                        "Elara: (Grinning mischievously) Ah, that little rascal! They seem to have a knack for guiding "
                        "lost wanderers. I'm glad it brought you here.",
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

            message = messages[active_x]
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
                     "Gather around the bedroom: Set up a cozy space where we can sit together"
                     "with enough room for the photo album and art supplies.",
                     "Reflect on memories: Take turns sharing stories and memories associated with each photo you've "
                     "collected. Discuss the emotions and experiences tied to those moments, fostering a sense of "
                     "connection and nostalgia.",
                     "Can't believe I gonna say this but, remember to take pictures!!",
                     "If you can't remember all of the steps above, I've hand written that out, open my diary and "
                     "take the paper that's currently in it out. The steps are in there. Good luck!",
                     "Note: For mah big brother, STARDEW VALLEY!!!! I just realized it's an isometric game O_o",
                     "Last note: If Daddy can't attend this, mommy do it =))"]
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
