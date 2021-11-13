import pygame
import random
import math
import time

pygame.init()

display = pygame.display.set_mode((600, 600))
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
		self.xy = xy
		self.radius = radius
		self.velocity = velocity
		self.type = type

	def draw(self):
		x, y = map(int, self.xy)
		if self.type == 'r':
			img = img_rock
		elif self.type == 'p':
			img = img_paper
		elif self.type == 's':
			img = img_scissors
		
		display.blit(img, (x, y))

	def update(self):
		self.xy[0] += self.velocity[0]
		self.xy[1] += self.velocity[1]
		self.draw()

def game():
	random.seed(0)
	items = []
	for _ in range(30):
		items.append(Item([random.randint(50, 550), random.randint(50, 550)], 10, [0, 0], 'r'))
		items.append(Item([random.randint(50, 550), random.randint(50, 550)], 10, [0, 0], 'p'))
		items.append(Item([random.randint(50, 550), random.randint(50, 550)], 10, [0, 0], 's'))

	time.sleep(10)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return

		display.fill((255, 255, 255))

		rocks = [item for item in items if item.type == 'r']
		papers = [item for item in items if item.type == 'p']
		sciss = [item for item in items if item.type == 's']
		# print(len(rocks), len(papers), len(sciss))

		for item in items:
			item.velocity = [random.randint(-1, 1), random.randint(-1, 1)]

			walk = False
			if item.type == 'r':
				for sci in sciss:
					if math.sqrt(pow(item.xy[0]-sci.xy[0], 2) + pow(item.xy[1]-sci.xy[1], 2)) <= item.radius + sci.radius:
						sci.type = 'r'
						sfx_rock.play()
						break
				
				sciss = [item for item in items if item.type == 's']
				dir_x = 0
				dir_y = 0
				for sci in sciss:
					walk = True
					dir_x += item.xy[0] - sci.xy[0]
					dir_y += item.xy[1] - sci.xy[1]

			elif item.type == 'p':
				for rock in rocks:
					if math.sqrt(pow(item.xy[0]-rock.xy[0], 2) + pow(item.xy[1]-rock.xy[1], 2)) <= item.radius + rock.radius:
						rock.type = 'p'
						sfx_paper.play()
						break

				rocks = [item for item in items if item.type == 'r']
				dir_x = 0
				dir_y = 0
				for rock in rocks:
					walk = True
					dir_x =  item.xy[0] - rock.xy[0]
					dir_y =  item.xy[1] - rock.xy[1]

			elif item.type == 's':
				for paper in papers:
					if math.sqrt(pow(item.xy[0]-paper.xy[0], 2) + pow(item.xy[1]-paper.xy[1], 2)) <= item.radius + paper.radius:
						paper.type = 's'
						sfx_scissors.play()
						break

				sciss = [item for item in items if item.type == 's']
				dir_x = 0
				dir_y = 0
				for paper in papers:
					walk = True
					dir_x =  item.xy[0] - paper.xy[0]
					dir_y =  item.xy[1] - paper.xy[1]
			
			if walk:
				walk = random.choice([True, False, True])
			if walk:
				if dir_x >= 0 and dir_y >= 0:
					item.velocity[0] -= 1
					item.velocity[1] -= 1
				elif dir_x < 0 and dir_y >= 0:
					item.velocity[0] += 1
					item.velocity[1] -= 1
				elif dir_x < 0 and dir_y < 0:
					item.velocity[0] += 1
					item.velocity[1] += 1
				elif dir_x >= 0 and dir_y < 0:
					item.velocity[0] -= 1
					item.velocity[1] += 1
			
			item.update()

		pygame.display.update()
		clock.tick(FPS)

game()
pygame.quit()