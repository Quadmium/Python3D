import pyglet
import ctypes  # An included library with Python install.
import inspect
from pyglet.window import key

'''
def isprop(v):
	return isinstance(v, property)

ctypes.windll.user32.MessageBoxW(0, '\n'.join([name for (
	name, value) in inspect.getmembers(pyglet.text.Label, isprop)]), "Your title", 1)
'''

window = pyglet.window.Window()

label = pyglet.text.Label('Hello, world', font_name='Times New Roman', font_size=36,
						  x=window.width // 2, y=window.height // 2, anchor_x='center', anchor_y='center')


@window.event
def on_draw():
	window.clear()
	label.draw()


@window.event
def on_key_press(symbol, modifiers):
	if symbol == key.A:
		label.text = "A"
	elif symbol == key.B:
		label.text = "B"

pyglet.app.run()