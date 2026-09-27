import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import sys

import numpy as np
import pygame

import states


def get_next_state(state, update=True):
    new_state = np.zeros(state.shape, dtype=np.int8)

    for i, row in enumerate(state):
        for j, cell in enumerate(row):
            neighbor_count = 0

            for idx_1, idx_2 in [(i+1, j+1), (i-1, j+1), (i+1, j-1), (i, j+1), (i+1, j), (i-1, j-1), (i-1, j), (i, j-1)]:
                if 0 <= idx_1 < state.shape[0] and 0 <= idx_2 < state.shape[1]:
                    if state[idx_1, idx_2]:
                        neighbor_count += 1

            if not update:
                if cell:
                    new_state[i, j] = neighbor_count if neighbor_count else 1
                continue

            if not cell and neighbor_count == 3:
                new_state[i, j] = neighbor_count
            elif cell and (2 > neighbor_count or neighbor_count > 3):
                new_state[i, j] = 0
            elif cell:
                new_state[i, j] = neighbor_count
    return new_state


def main():
    color = {
        #1 : (19, 170, 25), # dark green
        1 : (255, 0, 0), # red
        2 : (216, 35, 141), # pink
        3 : (115, 50, 225), # purple
        4 : (250, 110, 3), # orange
        5 : (83, 6, 209), # other purple
        6 : (42, 209, 6), # bright green
        7 : (21, 232, 219), # cyan
        8 : (250, 83, 114), # other pink
    }
    
    
    #W, H = (1350,)*2
    W, H = (850,)*2
    #MATRIX_SHAPE = (199, 150)
    MATRIX_SHAPE = 100
    FPS = 12
    
    pygame.init()
    pygame.display.set_caption('game of life\tgen: 0')
    
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((W, H))
    
    # Initial state.
    state = states.diagonals(MATRIX_SHAPE)
    #state = states.random(MATRIX_SHAPE)
    #state = states.empty(MATRIX_SHAPE)
    
    state = get_next_state(state, False)
    
    # Start.
    gen = 1
    getting_state = False
    stop_time = True
    erase_cells = False
    running = True
    while running:
        clock.tick(60 if getting_state and stop_time else FPS)
        screen.fill(0)
    
        # Event handler.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
    
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                stop_time = not stop_time
    
    
            if event.type == pygame.MOUSEBUTTONDOWN:
    
                if event.button == pygame.BUTTON_LEFT:
                    erase_cells = False
                elif event.button == pygame.BUTTON_RIGHT:
                    erase_cells = True
                else:
                    continue
    
                getting_state = not getting_state
                state = get_next_state(state, False)
    
        if getting_state:
            mpos = pygame.mouse.get_pos()
            idx = int(mpos[1]//(H/state.shape[0])), int(mpos[0]//(W/state.shape[1]))
            state[idx[0], idx[1]] = 0 if erase_cells else 1
            state = get_next_state(state, False)
    
    
        # Draw current generation.
        for i, row in enumerate(state):
            for j, cell in enumerate(row):
                if not cell:
                    continue
    
                pygame.draw.circle(screen, color[cell], [(j+.5)*W/state.shape[1], (i+.5)*H/state.shape[0]], max(1, W/state.shape[0]/2), 0)
                #pygame.draw.rect(screen, color[cell], [j*W/state.shape[1], i*H/state.shape[0], max(1, W/state.shape[0]), max(1, W/state.shape[0])], 0)
    
        pygame.display.flip()
    
        if stop_time:
            continue
        state = get_next_state(state)
        state = get_next_state(state, False)
        gen += 1
        pygame.display.set_caption(f'game of life\tgen: {gen}')
    
    
    pygame.quit()
    sys.exit()
    

if __name__ == '__main__':
    main()

