import pygame
import random
import math

pygame.init()

RESX = 360
RESY = 640

screen = pygame.display.set_mode((RESX, RESY))
pygame.display.set_caption('Rock Paper Scissors')
clock = pygame.time.Clock()
FPS = 30

img_rock = pygame.image.load('emoji_rock.png').convert_alpha()
img_paper = pygame.image.load('emoji_paper.png').convert_alpha()
img_scissors = pygame.image.load('emoji_scissors.png').convert_alpha()

sfx_rock = pygame.mixer.Sound('sound_rock.wav')
sfx_paper = pygame.mixer.Sound('sound_paper.wav')
sfx_scissors = pygame.mixer.Sound('sound_scissors.wav')

class Item:
	def __init__(self, xy, radius, velocity, type):
		self.x = xy[0]
		self.y = xy[1]
		self.r = radius
		self.velocity = velocity
		self.type = type

	def draw(self):
		if self.type == 'r':
			icon = img_rock
		elif self.type == 'p':
			icon = img_paper
		elif self.type == 's':
			icon = img_scissors
		
		screen.blit(icon, (self.x, self.y))

	def update(self):
		self.x += self.velocity[0]
		self.y += self.velocity[1]
		if self.x < 0: self.x = 0
		elif self.x > RESX-20: self.x = RESX-20
		if self.y < 0: self.y = 0
		elif self.y > RESY-20: self.y = RESY-20
		self.draw()

# random.seed(3)
def game():
	items = []
	for _ in range(33):
		items.append(Item((random.randint(20, RESX-20), random.randint(20, RESY-20)), 10, (0, 0), 'r'))
		items.append(Item((random.randint(20, RESX-20), random.randint(20, RESY-20)), 10, (0, 0), 'p'))
		items.append(Item((random.randint(20, RESX-20), random.randint(20, RESY-20)), 10, (0, 0), 's'))

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
		screen.fill((255, 255, 255))

		rocks = [item for item in items if item.type =='r']
		papers = [item for item in items if item.type == 'p']
		sciss = [item for item in items if item.type == 's']

		for item in items:
			r = 1
			item.velocity = [random.uniform(-r, r), random.uniform(-r, r)]

			if item.type == 'r':
				prey_distances = {sci: math.sqrt(pow(item.x-sci.x, 2)+pow(item.y-sci.y, 2)) for sci in sciss}
				predator_distances = {paper: math.sqrt(pow(item.x-paper.x, 2)+pow(item.y-paper.y, 2)) for paper in papers}

				for sci in sciss:
					if math.sqrt(pow(item.x-sci.x, 2)+pow(item.y-sci.y, 2)) <= item.r + sci.r:
						sci.type = 'r'
						sfx_rock.play()
						rocks.append(sci)
						sciss.remove(sci)
						break

			elif item.type == 'p':
				prey_distances = {rock: math.sqrt(pow(item.x-rock.x, 2)+pow(item.y-rock.y, 2)) for rock in rocks}
				predator_distances = {sci: math.sqrt(pow(item.x-sci.x, 2)+pow(item.y-sci.y, 2)) for sci in sciss}

				for rock in rocks:
					if math.sqrt(pow(item.x-rock.x, 2)+pow(item.y-rock.y, 2)) <= item.r + rock.r:
						rock.type = 'p'
						sfx_paper.play()
						papers.append(rock)
						rocks.remove(rock)
						break

			elif item.type == 's':
				prey_distances = {paper: math.sqrt(pow(item.x-paper.x, 2)+pow(item.y-paper.y, 2)) for paper in papers}
				predator_distances = {rock: math.sqrt(pow(item.x-rock.x, 2)+pow(item.y-rock.y, 2)) for rock in rocks}

				for paper in papers:
					if math.sqrt(pow(item.x-paper.x, 2)+pow(item.y-paper.y, 2)) <= item.r + paper.r:
						paper.type = 's'
						sfx_scissors.play()
						sciss.append(paper)
						papers.remove(paper)
						break

			try:
				min_distance = min(prey_distances, key=lambda dis: prey_distances[dis])
				dirx = item.x - min_distance.x
				diry = item.y - min_distance.y

				amount = 0.1 if abs(dirx) < 100 and abs(diry) < 100 else 0
				if dirx >= 0 and diry >= 0:
					item.velocity[0] -= random.uniform(0.3, 0.8) + amount
					item.velocity[1] -= random.uniform(0.3, 0.8) + amount
				elif dirx < 0 and diry >= 0:
					item.velocity[0] += random.uniform(0.3, 0.8) + amount
					item.velocity[1] -= random.uniform(0.3, 0.8) + amount
				elif dirx < 0 and diry < 0:
					item.velocity[0] += random.uniform(0.3, 0.8) + amount
					item.velocity[1] += random.uniform(0.3, 0.8) + amount
				elif dirx >= 0 and diry < 0:
					item.velocity[0] -= random.uniform(0.3, 0.8) + amount
					item.velocity[1] += random.uniform(0.3, 0.8) + amount
			except ValueError:
				...

			try:
				min_distance = min(predator_distances, key=lambda dis: predator_distances[dis])
				dirx = item.x - min_distance.x
				diry = item.y - min_distance.y

				amount = 0.1 if abs(dirx) < 100 and abs(diry) < 100 else 0
				if dirx >= 0 and diry >= 0:
					item.velocity[0] += random.uniform(0.1, 0.2) + amount
					item.velocity[1] += random.uniform(0.2, 0.2) + amount
				elif dirx < 0 and diry >= 0:
					item.velocity[0] -= random.uniform(0.1, 0.2) + amount
					item.velocity[1] += random.uniform(0.1, 0.2) + amount
				elif dirx < 0 and diry < 0:
					item.velocity[0] -= random.uniform(0.1, 0.2) + amount
					item.velocity[1] -= random.uniform(0.1, 0.2) + amount
				elif dirx >= 0 and diry < 0:
					item.velocity[0] += random.uniform(0.1, 0.2) + amount
					item.velocity[1] -= random.uniform(0.1, 0.2) + amount
			except ValueError:
				...

			away_x = away_y = 0
			for other in items:
				if other != item and other.type == item.type:
					if math.sqrt(pow(item.x-other.x, 2)+pow(item.y-other.y, 2)) < item.r:
						away_x = other.x - item.x
						away_y = other.y - item.y

			if away_x > 0 and away_y > 0:
				item.velocity[0] -= random.uniform(1, 1)
				item.velocity[1] -= random.uniform(1, 1)
			elif away_x < 0 and away_y > 0:
				item.velocity[0] += random.uniform(1, 1)
				item.velocity[1] -= random.uniform(1, 1)
			elif away_x < 0 and away_y < 0:
				item.velocity[0] += random.uniform(1, 1)
				item.velocity[1] += random.uniform(1, 1)
			elif away_x > 0 and away_y < 0:
				item.velocity[0] -= random.uniform(1, 1)
				item.velocity[1] += random.uniform(1, 1)
			
			item.update()

		pygame.display.update()
		clock.tick(FPS)

game()
pygame.quit()