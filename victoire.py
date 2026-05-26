import pygame
import cv2

def video(cheminv, chemina, ecran):
    cap = cv2.VideoCapture(cheminv)
    clock = pygame.time.Clock()
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        fps = 30
    pygame.mixer.music.load(chemina)
    pygame.mixer.music.play()
    largeur, hauteur = ecran.get_size()
    running = True
    while running and cap.isOpened():
        r, f = cap.read()
        if not r:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN]:
                    running = False
        f = cv2.resize(f, (largeur, hauteur))
        f = cv2.cvtColor(f, cv2.COLOR_BGR2RGB)
        fsur = pygame.image.frombuffer(f.tobytes(), (largeur, hauteur), "RGB")
        ecran.blit(fsur, (0,0))
        pygame.display.flip()
        clock.tick(fps)
    pygame.mixer.music.stop()
    cap.release()