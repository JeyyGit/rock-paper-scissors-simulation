import asyncio
import math
import random
import time

import pygame

pygame.init()

RESX = 1366
RESY = 768

screen = pygame.display.set_mode((RESX, RESY))
pygame.display.set_caption('Rock Paper Scissors')
clock = pygame.time.Clock()
FPS = 30

font = pygame.font.SysFont(None, 30)
text_reset = font.render('Click to reset', False, 'black')

img_rock = pygame.image.load('emoji_rock.png').convert_alpha()
img_paper = pygame.image.load('emoji_paper.png').convert_alpha()
img_scissors = pygame.image.load('emoji_scissors.png').convert_alpha()

img_rock = pygame.transform.scale(img_rock, (40, 40))
img_paper = pygame.transform.scale(img_paper, (40, 40))
img_scissors = pygame.transform.scale(img_scissors, (40, 40))

sfx_rock = pygame.mixer.Sound('sound_rock.wav')
sfx_paper = pygame.mixer.Sound('sound_paper.wav')
sfx_scissors = pygame.mixer.Sound('sound_scissors.wav')

class Item:
	def __init__(self, xy, radius, velocity, type_):
		self.x = xy[0]
		self.y = xy[1]
		self.r = radius
		self.velocity = velocity
		self.type = type_
		self.icon = None
		self.rect = None
		self.set_icon()
		self.rect = self.icon.get_rect()
		self.rect.update(self.x, self.y, 40, 40)

	def set_icon(self):
		if self.type == 'r':
			self.icon = img_rock
		elif self.type == 'p':
			self.icon = img_paper
		elif self.type == 's':
			self.icon = img_scissors

	def draw(self):
		self.set_icon()
		screen.blit(self.icon, self.rect)

	def update(self):
		self.x += self.velocity[0]
		self.y += self.velocity[1]

		if self.x < 0: self.x = 0
		elif self.x > RESX-40: self.x = RESX-40
		if self.y < 0: self.y = 0
		elif self.y > RESY-60: self.y = RESY-60

		self.rect.update(self.x, self.y, 40, 40)
		self.draw()


def init():
	random.seed(time.time())

	items = []
	for _ in range(50):
		items.append(Item((random.randint(0, RESX-40), random.randint(0, RESY-60)), 10, (0, 0), 'r'))
		items.append(Item((random.randint(0, RESX-40), random.randint(0, RESY-60)), 10, (0, 0), 'p'))
		items.append(Item((random.randint(0, RESX-40), random.randint(0, RESY-60)), 10, (0, 0), 's'))

	return items


async def game():
	items = init()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			elif event.type == pygame.MOUSEBUTTONDOWN:
				items = init()

		screen.fill((255, 255, 255))
		screen.blit(text_reset, (10, 10))

		rocks = [item for item in items if item.type =='r']
		papers = [item for item in items if item.type == 'p']
		sciss = [item for item in items if item.type == 's']

		len_rocks = round(len(rocks)/len(items) * RESX)
		len_papers = round(len(papers)/len(items) * RESX)
		len_sciss = round(len(sciss)/len(items) * RESX)

		pygame.draw.rect(screen, 'red', [0, RESY-40, len_rocks, RESY])
		pygame.draw.rect(screen, 'green', [len_rocks, RESY-40, len_papers, RESY])
		pygame.draw.rect(screen, 'blue', [len_rocks+len_papers, RESY-40, RESX, RESY])

		if rocks:
			screen.blit(img_rock, [len_rocks/2-20, RESY-40])
		if papers:
			screen.blit(img_paper, [len_rocks+len_papers-len_papers/2-20, RESY-40])
		if sciss:
			screen.blit(img_scissors, [len_rocks+len_papers+len_sciss-len_sciss/2-20, RESY-40])

		for item in items:
			r = 1.2
			item.velocity = [random.uniform(-r, r), random.uniform(-r, r)]

			if item.type == 'r':
				prey_distances = {sci: math.sqrt(pow(item.x-sci.x, 2)+pow(item.y-sci.y, 2)) for sci in sciss}
				predator_distances = {paper: math.sqrt(pow(item.x-paper.x, 2)+pow(item.y-paper.y, 2)) for paper in papers}

				for sci in sciss:
					if item.rect.colliderect(sci.rect):
						sci.type = 'r'
						sfx_rock.play()
						rocks.append(sci)
						sciss.remove(sci)
						break

			elif item.type == 'p':
				prey_distances = {rock: math.sqrt(pow(item.x-rock.x, 2)+pow(item.y-rock.y, 2)) for rock in rocks}
				predator_distances = {sci: math.sqrt(pow(item.x-sci.x, 2)+pow(item.y-sci.y, 2)) for sci in sciss}

				for rock in rocks:
					if item.rect.colliderect(rock.rect):
						rock.type = 'p'
						sfx_paper.play()
						papers.append(rock)
						rocks.remove(rock)
						break

			elif item.type == 's':
				prey_distances = {paper: math.sqrt(pow(item.x-paper.x, 2)+pow(item.y-paper.y, 2)) for paper in papers}
				predator_distances = {rock: math.sqrt(pow(item.x-rock.x, 2)+pow(item.y-rock.y, 2)) for rock in rocks}

				for paper in papers:
					if item.rect.colliderect(paper.rect):
						paper.type = 's'
						sfx_scissors.play()
						sciss.append(paper)
						papers.remove(paper)
						break

			# walk to preys
			try:
				min_distance = min(prey_distances, key=lambda dis: prey_distances[dis])
				dirx = item.x - min_distance.x
				diry = item.y - min_distance.y

				walk_min, walk_max = 1.0, 1.2
				amount = 0.1 if abs(dirx) < 100 and abs(diry) < 100 else 0
				if dirx >= 0 and diry >= 0:
					item.velocity[0] -= random.uniform(walk_min, walk_max) + amount
					item.velocity[1] -= random.uniform(walk_min, walk_max) + amount
				elif dirx < 0 and diry >= 0:
					item.velocity[0] += random.uniform(walk_min, walk_max) + amount
					item.velocity[1] -= random.uniform(walk_min, walk_max) + amount
				elif dirx < 0 and diry < 0:
					item.velocity[0] += random.uniform(walk_min, walk_max) + amount
					item.velocity[1] += random.uniform(walk_min, walk_max) + amount
				elif dirx >= 0 and diry < 0:
					item.velocity[0] -= random.uniform(walk_min, walk_max) + amount
					item.velocity[1] += random.uniform(walk_min, walk_max) + amount
			except ValueError:
				...

			# walk away from predators
			try:
				min_distance = min(predator_distances, key=lambda dis: predator_distances[dis])
				dirx = item.x - min_distance.x
				diry = item.y - min_distance.y

				walk_min, walk_max = 0.4, 0.6
				amount = 0.1 if abs(dirx) < 100 and abs(diry) < 100 else 0
				if dirx >= 0 and diry >= 0:
					item.velocity[0] += random.uniform(walk_min, walk_max) + amount
					item.velocity[1] += random.uniform(walk_min, walk_max) + amount
				elif dirx < 0 and diry >= 0:
					item.velocity[0] -= random.uniform(walk_min, walk_max) + amount
					item.velocity[1] += random.uniform(walk_min, walk_max) + amount
				elif dirx < 0 and diry < 0:
					item.velocity[0] -= random.uniform(walk_min, walk_max) + amount
					item.velocity[1] -= random.uniform(walk_min, walk_max) + amount
				elif dirx >= 0 and diry < 0:
					item.velocity[0] += random.uniform(walk_min, walk_max) + amount
					item.velocity[1] -= random.uniform(walk_min, walk_max) + amount
			except ValueError:
				...

			# gives distance to same species
			away_x = away_y = 0
			for other in items:
				if other != item and other.type == item.type:
					if item.rect.collidepoint(other.rect.center):
						away_x = other.rect.centerx - item.rect.centerx
						away_y = other.rect.centery - item.rect.centery

			walk_min, walk_max = 1, 1.2
			if away_x > 0 and away_y > 0:
				item.velocity[0] -= random.uniform(walk_min, walk_max)
				item.velocity[1] -= random.uniform(walk_min, walk_max)
			elif away_x < 0 and away_y > 0:
				item.velocity[0] += random.uniform(walk_min, walk_max)
				item.velocity[1] -= random.uniform(walk_min, walk_max)
			elif away_x < 0 and away_y < 0:
				item.velocity[0] += random.uniform(walk_min, walk_max)
				item.velocity[1] += random.uniform(walk_min, walk_max)
			elif away_x > 0 and away_y < 0:
				item.velocity[0] -= random.uniform(walk_min, walk_max)
				item.velocity[1] += random.uniform(walk_min, walk_max)
			
			item.update()

		if not rocks and not papers:
			win = font.render('Scissors WIN!!', False, 'red')
			screen.blit(win, (RESX/2-win.get_rect().centerx, RESY/2-win.get_rect().centery))
		elif not rocks and not sciss:
			win = font.render('Paper WIN!!', False, 'red')
			screen.blit(win, (RESX/2-win.get_rect().centerx, RESY/2-win.get_rect().centery))
		elif not papers and not sciss:
			win = font.render('Rock WIN!!', False, 'red')
			screen.blit(win, (RESX/2-win.get_rect().centerx, RESY/2-win.get_rect().centery))

		pygame.display.update()
		clock.tick(FPS)

		await asyncio.sleep(0.00001)

asyncio.run(game())
pygame.quit()
