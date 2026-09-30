import pgzrun
from pygame import Rect
import math

# --- CONSTANTES Y CONFIGURACION ---

WIDTH = 800
HEIGHT = 600
TITLE = "Chigüichigüi"

class AnimatedCharacter:
    def __init__(self, x, y, prefix):
        self.prefix = prefix
        self.facing = "" 
        #El actor se inicializa con el primer frame de reposo (idle)
        self.actor = Actor(f"{prefix}_idle_1", (x,y))
        self.is_moving = False
        self.frame_index = 1
        self.animation_timer = 0
        self.animation_delay = 10 #Cambiar la velocidad de la animación

    def update_animation(self):
        """Lógica para alternar cíclicamente entre sprites (1 y 2)."""
        self.animation_timer += 1

        if self.animation_timer >= self.animation_delay:
            self.animation_timer = 0
            self.frame_index += 1

            #Asumimos que tienes 2 frames por animación (ej: run_1 y run_2)
            if self.frame_index > 2:
                self.frame_index = 1

        #Determinar la acción actual para construir el nombre de la imagen
        action = "run" if self.is_moving else "idle"
        self.actor.image = f"{self.prefix}_{action}{self.facing}_{self.frame_index}"

    def draw(self):
        self.actor.draw()

class Player(AnimatedCharacter):
    def __init__(self, x, y):
        super().__init__(x, y, "player")
        self.speed = 5
        self.velocity_y = 0
        self.is_jumping = False
         # Piso temporal para probar la gravedad

    def update(self, keyboard):
        self.is_moving = False

        #Movimiento horizontal
        if keyboard.left:
            self.actor.x -= self.speed
            self.is_moving = True
            self.facing = "_left"
        elif keyboard.right:
            self.actor.x += self.speed
            self.is_moving = True
            self.facing = ""

        #Gravedad (Aplciar fuerza hacia abajo constantemente)
        self.velocity_y += 0.5
        self.actor.y += self.velocity_y

        #Asumimos que esta cayendo a menos que toque una plataforma
        self.is_jumping = True

        # --- Hitbox mas estrecho para los pies ---
        body_hitbox = Rect(self.actor.left + 30, self.actor.top,
                           self.actor.width - 60, self.actor.height)
        
        #Colisión con las plataformas
        for plat in platforms:
            #Si el heroe choca con la plataforma y esta cayendo (velocity_y >0)
            if body_hitbox.colliderect(plat):

                #Caso 1: Cayendo
                if self.velocity_y > 0:
                    if self.actor.bottom <= plat.bottom + 15:
                        self.actor.bottom = plat.top
                        self.velocity_y = 0
                        self.is_jumping = False
                        break #Deja de buscar si ya aterrizó

                #Caso 2: Subiendo
                elif self.velocity_y < 0:
                    self.actor.top = plat.bottom
                    self.velocity_y = 0
                    break

        #Salto
        if keyboard.up and not self.is_jumping:
            self.velocity_y = -12
            self.is_jumping = True

        #Limitar el movimiento para que no salga de la pantalla
        if self.actor.left < 0:
            self.actor.left = 0
        elif self.actor.right > WIDTH:
            self.actor.right = WIDTH


        #Actualiza los sprintes dependiendo de si se movió o no 
        self.update_animation()

class Enemy(AnimatedCharacter):
    def __init__(self, x, y, min_val, max_val, name_enemy, is_vertical=False, speed=2, pause_duration=0):
        super().__init__(x, y, name_enemy)
        self.min_val = min_val
        self.max_val = max_val
        self.speed = speed
        self.direction = 1 # 1 es drecha, -1 es izquierda
        self.is_vertical = is_vertical

        #Variables para controlar el reposo en los bordes
        self.pause_duration = pause_duration
        self.pause_timer = 0
        self.is_resting = False
        self.is_moving = (self.speed > 0)

    def update(self):

        #Caso A: El enemigo está descansando en el borde
        if self.is_resting:
            self.is_moving = False
            self.pause_timer -= 1

            #Cuando termina su descanso, decide hacia donde debe voltear
            if self.pause_timer <= 0:
                self.is_resting = False

                #Siempre se aleja del borde que acaba de tocar
                if self.is_vertical:
                    self.direction = -1 if self.actor.y >= self.max_val else 1
                else:
                    self.direction = -1 if self.actor.x >= self.max_val else 1

                self.facing = "_left" if self.direction == -1 else ""
        
        #Caso B: El enemigo esta patrullando
        else:
            self.is_moving = True

            if self.is_vertical:
                #Logica vuelo vertical
                self.actor.y += self.speed * self.direction

                #El centro "y" para evitar que se trabe el dibujo por ser alto
                if self.actor.y >= self.max_val:
                    self.actor.y = self.max_val
                    self.is_resting = True
                    self.pause_timer = self.pause_duration
                elif self.actor.y <= self.min_val:
                    self.actor.y = self.min_val
                    self.is_resting = True
                    self.pause_timer = self.pause_duration

            else:
                #Logica de patrullaje horizontal
                self.actor.x += self.speed * self.direction

                #Usamos el centro "x" para evitar que se trabe por el ancho del dibujo
                if self.actor.x >= self.max_val:
                    self.actor.x = self.max_val
                    self.is_resting = True
                    self.pause_timer = self.pause_duration
                elif self.actor.x <= self.min_val:
                    self.actor.x = self.min_val
                    self.is_resting = True
                    self.pause_timer = self.pause_duration

        self.update_animation()

class Reward:
    def __init__(self, x, y):
        self.actor = Actor("swag_1", (x, y))
        self.base_y = y
        self.float_timer = 0
        self.frame_timer = 0
        self.frame = 1

    def update(self):
        self.float_timer += 0.1
        self.actor.y = self.base_y + math.sin(self.float_timer) * 5

        self.frame_timer += 1
        if self.frame_timer >= 15:
            self.frame_timer = 0
            self.frame = 2 if self.frame == 1 else 1
            self.actor.image = f"swag_{self.frame}"

    def draw(self):
        self.actor.draw()

# --- ESTADOS DEL JUEGO ---

STATE_MENU = "Menú"
STATE_PLAY = "Play"
STATE_GAMEOVER = "Gameover"

game_state = STATE_MENU
music_enabled = True
music.play("bg_music")

# --- PLATAFORMAS ---
#Rect(x, y, ancho, alto)
platforms = [
    Rect((0,550), (WIDTH, 40)),
    Rect((340,380), (160, 40)),
    Rect((30, 280), (200, 40)),
    Rect((260, 140), (80, 20)),
    Rect((450, 140), (80, 20)),
    Rect((600, 180), (170, 40))
]

# --- BOTONES DEL MENU --- 
# Rect (x, y, width, height)

btn_start = Actor("btn_play_normal", (700, 200), (200, 50))
btn_audio = Actor("btn_audio_on", (700, 300), (200, 50))
btn_exit = Actor("btn_exit_normal", (700, 400), (200, 50))

#-- OBJETOS DEL JUEGO--

hero = Player(50, 550)
enemy_1 = Enemy(400, 300, min_val=340, max_val=500, name_enemy = "pelican", pause_duration = 180)
enemy_2 = Enemy(720, 140, min_val=630, max_val=760, name_enemy = "caiman", pause_duration=180)
enemy_3 = Enemy(400, 50, min_val=50, max_val=250, name_enemy = "pelican", is_vertical=True)

#Moneda
reward = Reward(720,110)

#Variable para saber el resultado al final del juego
player_won = False

def draw():
    """Función principal de renderizado de Pygame Zero."""
    screen.clear()

    if game_state == STATE_MENU:
        screen.clear()
        screen.blit("fondo_menu", (0,0))
        screen.draw.text("TACTICAL CAPI", center=(600,100), fontsize=60, color=(240, 160, 95), shadow=(2,2))
        #Botones
        btn_start.draw()
        btn_audio.draw()
        btn_exit.draw()

    elif game_state == STATE_PLAY:
        screen.clear()
        screen.blit("fondo_juego", (0,0))

        for plat in platforms:
            if plat.y == 550:
                pass
            else:
                for x in range (plat.x, plat.right, 40):
                    screen.blit("wood", (x,plat.y))

        reward.draw()
        hero.draw()
        enemy_1.draw()
        enemy_2.draw()
        enemy_3.draw()

    elif game_state == STATE_GAMEOVER:
        screen.clear()
        if player_won:
            screen.draw.text("YOU WIN!!!", center=(400,300), fontsize=80, color="yellow")
        else:
            screen.draw.text("GAME OVER", center=(400,300), fontsize=80, color="red")

        screen.draw.text("Press Enter to return to Menu", center=(400,400), fontsize=30, color="white")


def update():
    global game_state, player_won

    if game_state == STATE_PLAY:
        hero.update(keyboard)
        enemy_1.update()
        enemy_2.update()
        enemy_3.update()
        reward.update()

        #--Colisión: Perder (Con Hitboxes ajustados) ---
        #1. Rectangulo mas pequeño para el héroe
        hero_hitbox = Rect(hero.actor.left + 20, hero.actor.top + 20,
                           hero.actor.width - 40, hero.actor.height - 20)

        enemy_1_hitbox = Rect(enemy_1.actor.left + 20, enemy_1.actor.top + 20,
                         enemy_1.actor.width - 40, enemy_1.actor.height - 20)

        enemy_2_hitbox = Rect(enemy_2.actor.left + 20, enemy_2.actor.top + 20,
                              enemy_2.actor.width - 40, enemy_2.actor.height -20)

        enemy_3_hitbox = Rect(enemy_3.actor.left + 20, enemy_3.actor.top + 20,
                                      enemy_3.actor.width - 40, enemy_3.actor.height -20)

        if(hero_hitbox.colliderect(enemy_1_hitbox) or
           hero_hitbox.colliderect(enemy_2_hitbox) or
           hero_hitbox.colliderect(enemy_3_hitbox)):

            player_won = False
            game_state = STATE_GAMEOVER
            if music_enabled:
                sounds.lose.play() 

        #Colisión: GANAR (Si el héroe toca la recompensa)
        if reward.actor.colliderect(hero_hitbox):
            player_won = True
            game_state = STATE_GAMEOVER
            if music_enabled:
                sounds.coin.play()


def on_mouse_down(pos):
    """Detecta los clics del usuario para interactuar con el menú"""
    global game_state, music_enabled

    if game_state == STATE_MENU:
        if btn_start.collidepoint(pos):
            game_state = STATE_PLAY 
            
        elif btn_audio.collidepoint(pos):
            music_enabled = not music_enabled

            if music_enabled:
                btn_audio.image = "btn_audio_on"
                music.play("bg_music")
            else:
                btn_audio.image = "btn_audio_off"
                music.stop()

        elif btn_exit.collidepoint(pos):
            exit()

def on_mouse_move(pos):
    if game_state == STATE_MENU:
        if btn_start.collidepoint(pos):
            btn_start.image = "btn_play_hover"
        else:
            btn_start.image = "btn_play_normal"

        if btn_exit.collidepoint(pos):
            btn_exit.image = "btn_exit_hover"
        else:
            btn_exit.image = "btn_exit_normal"


def on_key_down(key):
    global game_state
    if game_state == STATE_GAMEOVER and key == keys.RETURN:
        hero.actor.pos = (50,400)
        hero.velocity_y = 0

        if music_enabled:
            music.play("bg_music")
        else:
            music.stop()
            
        game_state = STATE_MENU

pgzrun.go()