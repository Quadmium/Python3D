class Transform:
	def __init__(self, x = 0, y = 0, z = 0):
		self.x = x
		self.y = y
		self.z = z

class Mesh:
	def __init__(self, points = []):
		self.points = points

class GameObject:
	def __init__(self, mesh = Mesh(), transform = Transform()):
		self.mesh = mesh
		self.transform = transform

class World:
	def __init__(self, gameObjects = []):
		self.gameObjects = gameObjects