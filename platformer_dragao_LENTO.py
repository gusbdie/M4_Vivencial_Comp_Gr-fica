import glfw
from OpenGL.GL import *
from PIL import Image
import numpy as np
import os
import random
from datetime import datetime

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

GRAVITY = 0.5
JUMP_STRENGTH = 12.0
GROUND_LEVEL = 150


class GroundLayer:
    
    def __init__(self, texture_id, height=150):
        self.texture_id = texture_id
        self.height = height
        self.offset_x = 0.0
        self.speed = 0.5
    
    def update_offset(self, player_dx):
        self.offset_x += player_dx * self.speed
    
    def draw(self):
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glEnable(GL_TEXTURE_2D)
        
        tx = (self.offset_x / WINDOW_WIDTH) % 1.0
        
        glBegin(GL_QUADS)
        glTexCoord2f(tx, 1.0)
        glVertex2f(0, 0)
        
        glTexCoord2f(tx + 2.0, 1.0)
        glVertex2f(WINDOW_WIDTH, 0)
        
        glTexCoord2f(tx + 2.0, 0.0)
        glVertex2f(WINDOW_WIDTH, self.height)
        
        glTexCoord2f(tx, 0.0)
        glVertex2f(0, self.height)
        glEnd()
        
        glDisable(GL_TEXTURE_2D)


class Dragon:
    
    def __init__(self, texture_id, width, height):
        self.texture_id = texture_id
        self.width = width
        self.height = height
        
        self.x = -width
        self.y = WINDOW_HEIGHT - 150
        
        self.speed = 0.3
        
        self.wave_offset = 0
        self.wave_speed = 0.02
        self.wave_amplitude = 20
    
    def update(self):
        self.x += self.speed
        
        self.wave_offset += self.wave_speed
        y_offset = np.sin(self.wave_offset) * self.wave_amplitude
        
        if self.x > WINDOW_WIDTH:
            self.x = -self.width
            self.y = WINDOW_HEIGHT - random.randint(120, 200)
        
        return y_offset
    
    def draw(self, y_offset):
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        actual_y = self.y + y_offset
        
        glBegin(GL_QUADS)
        glTexCoord2f(0, 1)
        glVertex2f(self.x, actual_y)
        
        glTexCoord2f(1, 1)
        glVertex2f(self.x + self.width, actual_y)
        
        glTexCoord2f(1, 0)
        glVertex2f(self.x + self.width, actual_y + self.height)
        
        glTexCoord2f(0, 0)
        glVertex2f(self.x, actual_y + self.height)
        glEnd()
        
        glDisable(GL_BLEND)
        glDisable(GL_TEXTURE_2D)


class Player:
    
    def __init__(self, texture_id, width, height):
        self.texture_id = texture_id
        self.width = width
        self.height = height
        
        self.x = (WINDOW_WIDTH - width) // 2
        
        self.y = GROUND_LEVEL
        
        self.velocity_y = 0.0
        self.is_jumping = False
        self.on_ground = True
        
        self.move_speed = 3.0
    
    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_STRENGTH
            self.is_jumping = True
            self.on_ground = False
    
    def update(self):
        self.velocity_y -= GRAVITY
        
        self.y += self.velocity_y
        
        if self.y <= GROUND_LEVEL:
            self.y = GROUND_LEVEL
            self.velocity_y = 0
            self.is_jumping = False
            self.on_ground = True
    
    def get_horizontal_movement(self, dx):
        return dx * self.move_speed
    
    def draw(self):
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        glBegin(GL_QUADS)
        glTexCoord2f(0, 1)
        glVertex2f(self.x, self.y)
        
        glTexCoord2f(1, 1)
        glVertex2f(self.x + self.width, self.y)
        
        glTexCoord2f(1, 0)
        glVertex2f(self.x + self.width, self.y + self.height)
        
        glTexCoord2f(0, 0)
        glVertex2f(self.x, self.y + self.height)
        glEnd()
        
        glDisable(GL_BLEND)
        glDisable(GL_TEXTURE_2D)


def draw_sky_background():
    glDisable(GL_TEXTURE_2D)
    
    glBegin(GL_QUADS)
    glColor3f(0.4, 0.6, 0.9)
    glVertex2f(0, WINDOW_HEIGHT)
    glVertex2f(WINDOW_WIDTH, WINDOW_HEIGHT)
    
    glColor3f(0.6, 0.8, 1.0)
    glVertex2f(WINDOW_WIDTH, GROUND_LEVEL)
    glVertex2f(0, GROUND_LEVEL)
    glEnd()
    
    glColor3f(1.0, 1.0, 1.0)


def load_texture_from_file(filepath, placeholder_color=(128, 128, 128, 255)):
    if not os.path.exists(filepath):
        print(f"    Arquivo não encontrado: {filepath}")
        print(f"   Criando textura placeholder...")
        
        width, height = 256, 256
        data = np.zeros((height, width, 4), dtype=np.uint8)
        data[:, :, 0] = placeholder_color[0]
        data[:, :, 1] = placeholder_color[1]
        data[:, :, 2] = placeholder_color[2]
        data[:, :, 3] = placeholder_color[3]
        
        for i in range(0, height, 40):
            lighter = [min(255, c + 40) for c in placeholder_color[:3]]
            data[i:i+20, :, 0] = lighter[0]
            data[i:i+20, :, 1] = lighter[1]
            data[i:i+20, :, 2] = lighter[2]
        
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, 
                     GL_RGBA, GL_UNSIGNED_BYTE, data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        
        return texture_id
    
    try:
        img = Image.open(filepath)
        img_data = img.convert("RGBA")
        width, height = img.size
        data = np.array(list(img_data.getdata()), np.uint8)
        
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, 
                     GL_RGBA, GL_UNSIGNED_BYTE, data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        
        print(f"Textura carregada: {filepath} ({width}x{height})")
        return texture_id
    except Exception as e:
        print(f"Erro ao carregar {filepath}: {e}")
        return load_texture_from_file("", placeholder_color)


def init_opengl():
    glClearColor(0.53, 0.81, 0.92, 1.0)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

def main():
    if not glfw.init():
        print("Erro ao inicializar GLFW")
        return
    
    window = glfw.create_window(
        WINDOW_WIDTH, WINDOW_HEIGHT,
        "Platformer Parallax ",
        None, None
    )
    
    if not window:
        glfw.terminate()
        print("Erro ao criar janela")
        return
    
    glfw.make_context_current(window)
    init_opengl()
    
    print("=" * 60)
    print("CARREGANDO TEXTURAS...")
    print("=" * 60)
    
    ground_tex = load_texture_from_file("textures/ground.png", (139, 90, 43, 255))
    player_tex = load_texture_from_file("textures/player.png", (255, 100, 100, 255))
    dragon_tex = load_texture_from_file("textures/dragon.png", (200, 60, 60, 255))
    
    print("=" * 60)
    print("")
    print("🎮 CONTROLES:")
    print("  ⬅️  ESQUERDA - Move para esquerda")
    print("  ➡️  DIREITA  - Move para direita")
    print("  ⬆️  CIMA     - PULAR")
    print("  ESC         - Sair")
    print("")
    print("✨ CARACTERÍSTICAS:")
    print("  🐉 Dragão voando majestosamente no céu")
    print("  🦘 Pulo realista com física de gravidade")
    print("  🌊 Parallax scrolling horizontal")
    print("=" * 60)
    
    ground = GroundLayer(ground_tex, height=GROUND_LEVEL)
    player = Player(player_tex, 80, 80)
    dragon = Dragon(dragon_tex, 120, 80)
    
    print("▶️  Jogo iniciado! Divirta-se! 🎮")
    last = datetime.now()
    now = datetime.now()
    while not glfw.window_should_close(window):

        now = datetime.now()
        if (now - last).total_seconds() < 1/60:
            continue
        last = now


        glClear(GL_COLOR_BUFFER_BIT)
        
        dx = 0
        jump_pressed = False
        
        if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
            dx = -1
        if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
            dx = 1
        if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
            jump_pressed = True
        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(window, True)
        
        if jump_pressed:
            player.jump()
        
        player.update()
        
        dragon_y_offset = dragon.update()
        
        move_dx = player.get_horizontal_movement(dx)
        ground.update_offset(move_dx)
        
        draw_sky_background()
        
        dragon.draw(dragon_y_offset)
        
        ground.draw()
        
        player.draw()
        
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glfw.terminate()
    print("Fim de Jogo")


if __name__ == "__main__":
    main()