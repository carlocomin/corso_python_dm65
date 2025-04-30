import pygame
import heapq
import random
import sys

# Costanti
LARGHEZZA, ALTEZZA = 600, 450
righe, colonne = 20, 30
TILE = LARGHEZZA // colonne

# Colori
BIANCO = (255,255,255)
NERO = (0,0,0)
VERDE = (0,255,0)
ROSSO = (255,0,0)
GRIGIO = (50,50,50)
AZZURRO = (100,180,255)
VIOLA = (170,0,255)
GIALLO = (255,255,0)
TESTO = (230, 230, 230)

# Nodo
class Nodo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = float('inf')
        self.h = 0
        self.f = float('inf')
        self.padre = None
        self.ostacolo = False

    def __lt__(self, altro):
        return self.f < altro.f

def heuristica(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)

def vicini(griglia, nodo):
    dirs = [(0,1),(1,0),(0,-1),(-1,0)]
    risultato = []
    for dx, dy in dirs:
        nx, ny = nodo.x + dx, nodo.y + dy
        if 0 <= nx < colonne and 0 <= ny < righe:
            vicino = griglia[ny][nx]
            if not vicino.ostacolo:
                risultato.append(vicino)
    return risultato

def disegna_griglia(schermo, griglia, start, goal, open_set, closed_set, percorso):
    for riga in griglia:
        for nodo in riga:
            x, y = nodo.x * TILE, nodo.y * TILE
            if nodo in percorso:
                colore = GIALLO
            elif nodo == start:
                colore = VERDE
            elif nodo == goal:
                colore = ROSSO
            elif nodo in open_set:
                colore = VIOLA
            elif nodo in closed_set:
                colore = AZZURRO
            elif nodo.ostacolo:
                colore = NERO
            else:
                colore = BIANCO
            pygame.draw.rect(schermo, colore, (x, y, TILE-1, TILE-1))

def ricostruisci_percorso(nodo):
    percorso = []
    while nodo.padre:
        percorso.append(nodo)
        nodo = nodo.padre
    return percorso[::-1]

def disegna_legenda(schermo, font):
    legenda = [
        ("Start", VERDE),
        ("Goal", ROSSO),
        ("Ostacolo", NERO),
        ("Visitato", AZZURRO),
        ("Frontiera", VIOLA),
        ("Percorso", GIALLO)
    ]
    base_y = ALTEZZA - 45
    for i, (etichetta, colore) in enumerate(legenda):
        x = 10 + i * 100
        pygame.draw.rect(schermo, colore, (x, base_y, 20, 20))
        testo = font.render(etichetta, True, TESTO)
        schermo.blit(testo, (x + 25, base_y))

# Inizializzazione
pygame.init()
schermo = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption("Mini-Progetto A* Robot")
font = pygame.font.SysFont(None, 20)

griglia = [[Nodo(x, y) for x in range(colonne)] for y in range(righe)]
start = griglia[0][0]
goal = griglia[righe-1][colonne-1]

# Aggiunta ostacoli casuali
for riga in griglia:
    for nodo in riga:
        if nodo not in (start, goal) and random.random() < 0.2:
            nodo.ostacolo = True

def reset_griglia():
    for riga in griglia:
        for nodo in riga:
            nodo.g = float('inf')
            nodo.h = 0
            nodo.f = float('inf')
            nodo.padre = None

running = True
while running:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False
        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            if y < ALTEZZA - 50:
                gx, gy = x // TILE, y // TILE
                if griglia[gy][gx] not in (start, goal):
                    griglia[gy][gx].ostacolo = not griglia[gy][gx].ostacolo
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
            griglia = [[Nodo(x, y) for x in range(colonne)] for y in range(righe)]
            start = griglia[0][0]
            goal = griglia[righe-1][colonne-1]
            for riga in griglia:
                for nodo in riga:
                    if nodo not in (start, goal) and random.random() < 0.2:
                        nodo.ostacolo = True

    reset_griglia()
    open_set = []
    closed_set = set()
    start.g = 0
    start.h = heuristica(start, goal)
    start.f = start.h
    heapq.heappush(open_set, start)

    trovato = False
    while open_set:
        nodo_corrente = heapq.heappop(open_set)
        if nodo_corrente == goal:
            trovato = True
            break
        closed_set.add(nodo_corrente)
        for vicino in vicini(griglia, nodo_corrente):
            nuovo_g = nodo_corrente.g + 1
            if nuovo_g < vicino.g:
                vicino.g = nuovo_g
                vicino.h = heuristica(vicino, goal)
                vicino.f = vicino.g + vicino.h
                vicino.padre = nodo_corrente
                if vicino not in open_set:
                    heapq.heappush(open_set, vicino)

        percorso = ricostruisci_percorso(nodo_corrente)
        schermo.fill(GRIGIO)
        disegna_griglia(schermo, griglia, start, goal, open_set, closed_set, percorso)
        disegna_legenda(schermo, font)
        pygame.display.update()
        pygame.time.delay(20)

pygame.quit()
sys.exit()