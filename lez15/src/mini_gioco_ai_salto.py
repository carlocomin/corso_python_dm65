import pygame
import torch
import torch.nn as nn
import torch.nn.functional as F
import random
import matplotlib.pyplot as plt

# --- Parametri gioco ---
LARGHEZZA, ALTEZZA = 600, 300
FPS = 60
GRAVITÀ = 1
SALTO_FORZA = -15
OSTACOLO_VEL = 5

# --- Rete neurale del bot ---
class BotNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(3, 6)
        self.fc2 = nn.Linear(6, 1)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = torch.sigmoid(self.fc2(x))
        return x

# --- Visualizzazione training ---
def visualizza_training(losses):
    plt.plot(losses)
    plt.title("Andamento della perdita (loss)")
    plt.xlabel("Epoca")
    plt.ylabel("Loss")
    plt.grid(True)
    plt.show()

# --- Inizializza pygame ---
pygame.init()
schermo = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# --- Classe ostacolo ---
class Ostacolo:
    def __init__(self):
        self.w = 30
        self.h = random.randint(40, 80)
        self.x = LARGHEZZA
        self.y = ALTEZZA - self.h

    def muovi(self):
        self.x -= OSTACOLO_VEL

    def disegna(self):
        pygame.draw.rect(schermo, (255,0,0), (self.x, self.y, self.w, self.h))

    def collide(self, bot):
        return (
            self.x < bot.x + bot.w and
            self.x + self.w > bot.x and
            self.y < bot.y + bot.h
        )

# --- Stato del giocatore ---
class Giocatore:
    def __init__(self):
        self.x = 50
        self.y = ALTEZZA - 50
        self.w = 30
        self.h = 50
        self.vel = 0
        self.terra = self.y

    def aggiorna(self):
        self.vel += GRAVITÀ
        self.y += self.vel
        if self.y > self.terra:
            self.y = self.terra
            self.vel = 0

    def salta(self):
        if self.y == self.terra:
            self.vel = SALTO_FORZA
            return True
        return False

    def disegna(self):
        pygame.draw.rect(schermo, (0, 255, 0), (self.x, self.y, self.w, self.h))

# --- Inizializza entità ---
bot = Giocatore()
ostacoli = []
modello = BotNet()

# --- Dati di addestramento (esempio supervised fittizio) ---
X_train = torch.tensor([
    [200, 50, OSTACOLO_VEL],
    [120, 60, OSTACOLO_VEL],
    [80, 70, OSTACOLO_VEL],
    [50, 75, OSTACOLO_VEL],
    [30, 70, OSTACOLO_VEL]
], dtype=torch.float32)
Y_train = torch.tensor([[0],[0],[1],[1],[1]], dtype=torch.float32)

# --- Addestramento con visualizzazione ---
loss_fn = nn.BCELoss()
optimizer = torch.optim.Adam(modello.parameters(), lr=0.05)
losses = []

for epoca in range(200):
    pred = modello(X_train)
    loss = loss_fn(pred, Y_train)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    losses.append(loss.item())

visualizza_training(losses)

# --- Loop principale ---
frame = 0
running = True
messaggio = ""

while running:
    clock.tick(FPS)
    frame += 1
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False

    # Generazione ostacolo
    if frame % 100 == 0:
        ostacoli.append(Ostacolo())

    # Logica AI
    if ostacoli:
        primo = ostacoli[0]
        dist = primo.x - bot.x
        if dist < 0: dist = 0
        input_ai = torch.tensor([[dist, primo.h, OSTACOLO_VEL]], dtype=torch.float32)
        output = modello(input_ai)
        if output.item() > 0.5:
            success = bot.salta()
            if success:
                messaggio = "➡️ Salto effettuato"
        else:
            messaggio = ""

    # Update
    bot.aggiorna()
    for o in ostacoli:
        o.muovi()
    ostacoli = [o for o in ostacoli if o.x + o.w > 0]

    # Collisione
    for o in ostacoli:
        if o.collide(bot):
            messaggio = "💥 Collisione!"
            break

    # Disegno
    schermo.fill((30, 30, 30))
    bot.disegna()
    for o in ostacoli:
        o.disegna()

    schermo.blit(font.render("Mini-Progetto AI con PyTorch", True, (255,255,255)), (10, 10))
    if messaggio:
        schermo.blit(font.render(messaggio, True, (255, 255, 0)), (10, 40))

    pygame.display.flip()

pygame.quit()