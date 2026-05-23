# 🎮 PLATFORMER PARALLAX - Jogo 2D com Dragão

NOMES: Gustavo Bender Dietrich e Eduarda da Silva Cardoso

Jogo de plataforma 2D com efeito **parallax scrolling**, física de pulo realista e dragão voador épico! 🐉

![Status](https://img.shields.io/badge/status-concluído-brightgreen)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![OpenGL](https://img.shields.io/badge/OpenGL-2.0-orange)

---

## 📋 Descrição do Projeto

Implementação de um jogo de plataforma 2D usando **OpenGL**, **GLFW** e **Python**, desenvolvido como exercício de **Computação Gráfica** sobre:

✅ **Mapeamento de Texturas** (texture mapping)  
✅ **Transformações em Objetos** (translação, coordenadas)  
✅ **Efeito Parallax Scrolling** (camadas em diferentes velocidades)  
✅ **Física de Pulo** (gravidade e parábola)  
✅ **Projeção Ortográfica** (1 unidade = 1 pixel)

---

## 🎯 Funcionalidades

### 🎮 **Gameplay**
- Personagem controlável com teclado (⬅️➡️⬆️)
- Pulo com física realista (gravidade + parábola)
- Parallax scrolling horizontal (chão se move)
- Dragão voando majestosamente no céu

### 🎨 **Visual**
- Céu com gradiente azul (fixo)
- Chão de pedras com parallax
- Personagem cavaleiro (sprite 80x80)
- Dragão vermelho animado (120x80)

### ⚙️ **Técnico**
- Projeção ortográfica 800x600
- Texturas PNG com transparência
- Sistema de física simplificado
- Loop de jogo em 60 FPS

---

## 🚀 Instalação

### **Requisitos**
- Python 3.8 ou superior
- Sistema operacional: Windows, Linux ou macOS

### **Passo 1: Clone ou baixe o projeto**
```bash
# Se tiver git instalado:
git clone https://github.com/seu-usuario/platformer-parallax.git
cd platformer-parallax

# Ou baixe o ZIP e extraia
```

### **Passo 2: Instale as dependências**
```bash
pip install PyOpenGL PyOpenGL_accelerate glfw Pillow numpy
```

### **Passo 3: Organize os arquivos**
```
projeto/
├── platformer_dragao_LENTO.py    ← Código principal
└── textures/                      ← Pasta de texturas
    ├── ground.png                 (chão de pedras)
    ├── player.png                 (cavaleiro)
    └── dragon.png                 (dragão vermelho)
```

### **Passo 4: Execute o jogo**
```bash
python platformer_dragao_LENTO.py
```

---

## 🎮 Controles

| Tecla | Ação |
|-------|------|
| **⬅️ ESQUERDA** | Move o mundo para a esquerda (personagem "vai" para direita) |
| **➡️ DIREITA** | Move o mundo para a direita (personagem "vai" para esquerda) |
| **⬆️ CIMA** | Pular (com física de gravidade) |
| **ESC** | Sair do jogo |

> **Nota:** O personagem fica fixo horizontalmente no centro. O mundo é que se move (parallax)!

---

## 🛠️ Configurações Ajustáveis

### **Física do Pulo** (linhas 11-13)
```python
GRAVITY = 0.5          # Gravidade (menor = cai mais devagar)
JUMP_STRENGTH = 12.0   # Força do pulo (maior = pula mais alto)
GROUND_LEVEL = 150     # Altura do chão em pixels
```

### **Velocidade do Dragão** (linha ~68)
```python
self.speed = 0.3  # Velocidade horizontal (menor = mais lento)
```

### **Velocidade do Parallax** (linha ~23)
```python
self.speed = 0.5  # Velocidade do scroll (0.0 a 1.0)
```

### **Tamanho da Janela** (linhas 8-9)
```python
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
```

---

## 📐 Conceitos de Computação Gráfica

### **1. Projeção Ortográfica**
```python
glOrtho(0, 800, 0, 600, -1, 1)
```
- 1 unidade do mundo = 1 pixel na tela
- Coordenadas: (0,0) = canto inferior esquerdo

### **2. Mapeamento de Texturas**
```python
glTexCoord2f(0, 0)  # Canto da textura
glVertex2f(x, y)    # Canto do polígono
```
- Mapeia imagem PNG em quads (retângulos)
- Suporta transparência (alpha channel)

### **3. Parallax Scrolling**
- Camadas em diferentes velocidades
- Cria ilusão de profundidade em 2D
- Chão (velocidade 0.5) vs Céu (fixo, velocidade 0.0)

### **4. Física Simplificada**
```python
velocity_y -= GRAVITY        # Aplica gravidade
position_y += velocity_y     # Atualiza posição
```
- Gravidade constante para baixo
- Movimento parabólico no pulo

---

## 📊 Estrutura do Código

```
platformer_dragao_LENTO.py
│
├─ Configurações Globais (linhas 8-13)
│  └─ WINDOW_WIDTH, GRAVITY, JUMP_STRENGTH, etc.
│
├─ Classe GroundLayer (linhas 17-57)
│  └─ Camada do chão com parallax horizontal
│
├─ Classe Dragon (linhas 60-121)
│  └─ Dragão voador com movimento ondulatório
│
├─ Classe Player (linhas 124-208)
│  └─ Personagem com física de pulo
│
├─ Funções de Renderização (linhas 211-245)
│  └─ draw_sky_background(), load_texture_from_file()
│
└─ Loop Principal (linhas 299-361)
   └─ Entrada, física, renderização, swap buffers
```

---

## 🎨 Assets (Texturas)

### **Incluídos no Projeto:**
- `dragon.png` - Dragão vermelho pixel art (120x80)
- `player.png` - Cavaleiro (80x80)

### **Necessários (não incluídos):**
- `ground.png` - Textura de chão tileable

**Onde encontrar texturas gratuitas:**
- [OpenGameArt](https://opengameart.org/)
- [Itch.io Game Assets](https://itch.io/game-assets/free)
- [CraftPix Freebies](https://craftpix.net/freebies/)

---

## 🐛 Solução de Problemas

### **Erro: "No module named 'OpenGL'"**
```bash
pip install PyOpenGL PyOpenGL_accelerate
```

### **Erro: "No module named 'glfw'"**
```bash
pip install glfw
```

### **Janela não abre / Tela preta**
- Verifique se sua placa de vídeo suporta OpenGL 2.0+
- Atualize os drivers gráficos
- Execute como administrador

### **Texturas não aparecem (placeholders coloridos)**
- Verifique se a pasta `textures/` existe
- Confirme os nomes dos arquivos: `ground.png`, `player.png`, `dragon.png`
- Use caminhos relativos (não absolutos)

### **Controles invertidos**
- ✅ Versão atual já corrigida!
- Se usar versão antiga, edite linha ~30: `self.offset_x += ...` (não `-=`)

### **Dragão muito rápido/lento**
- Ajuste `self.speed = 0.3` na classe Dragon
- Valores sugeridos: 0.2 (lento), 0.5 (rápido)

---

## 📚 Referências

### **Documentação**
- [GLFW Documentation](https://www.glfw.org/docs/latest/)
- [PyOpenGL Documentation](http://pyopengl.sourceforge.net/)
- [OpenGL Reference](https://www.khronos.org/registry/OpenGL/)

### **Tutoriais**
- [LearnOpenGL](https://learnopengl.com/)
- [OpenGL Tutorial](http://www.opengl-tutorial.org/)

### **Teoria de Parallax**
- [Parallax Scrolling - Wikipedia](https://en.wikipedia.org/wiki/Parallax_scrolling)
- [Game Programming Patterns](https://gameprogrammingpatterns.com/)

---

## 📝 Créditos

- **Desenvolvido por:** [Seu Nome]
- **Disciplina:** Computação Gráfica
- **Tema:** Mapeamento de Texturas e Transformações
- **Linguagem:** Python 3
- **Bibliotecas:** OpenGL, GLFW, Pillow, NumPy

---

## 📄 Licença

Este projeto é de uso educacional e livre para modificação.

---

## 🎓 Aprendizados

Durante o desenvolvimento deste projeto, foram aplicados:

✅ Conceitos de **sistemas de coordenadas** (mundo vs tela)  
✅ **Mapeamento UV** de texturas em polígonos  
✅ **Física 2D** simplificada (gravidade, velocidade, aceleração)  
✅ **Game loop** básico (entrada → atualização → renderização)  
✅ **Parallax scrolling** para criar sensação de profundidade  
✅ **Alpha blending** para transparência  
✅ **Projeção ortográfica** 2D

---

## 🚀 Possíveis Melhorias Futuras

- [ ] Adicionar animação de caminhada do personagem
- [ ] Implementar colisão com obstáculos
- [ ] Sistema de pontuação
- [ ] Mais camadas de parallax (montanhas, árvores)
- [ ] Efeitos sonoros e música
- [ ] Múltiplos níveis/fases
- [ ] Power-ups e itens colecionáveis
- [ ] Inimigos com IA básica

---

## ❓ Perguntas Frequentes

**P: Posso usar outras texturas?**  
R: Sim! Apenas mantenha os nomes dos arquivos ou ajuste no código (linhas 294-296).

**P: Como adiciono mais camadas de parallax?**  
R: Crie mais instâncias de `ParallaxLayer` com velocidades diferentes.

**P: Funciona em Mac/Linux?**  
R: Sim! Python e OpenGL são multiplataforma. Apenas instale as dependências.

**P: Posso vender um jogo baseado neste código?**  
R: O código é livre, mas verifique licenças das texturas de terceiros.

---

## 📞 Contato

Dúvidas ou sugestões? Entre em contato:
- **Email:** seu.email@exemplo.com
- **GitHub:** [@seu-usuario](https://github.com/seu-usuario)

---

**🎮 Divirta-se jogando e aprendendo!** ✨

*Desenvolvido com ❤️ e muita dedicação para aprender OpenGL*
