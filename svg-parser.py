import xml.etree.ElementTree as ET

tree = ET.parse('sign-in2.svg')
root = tree.getroot()
translate = []
annotations = []
g_attributes = {}
defs = {}
trans_child = []

def getSubChild(child):
	global trans_child
	for subchild in child:
		elm = {}
		attribute = subchild.attrib
		tag = subchild.tag.split('}')[1]
		if tag == 'g' and 'transform' in attribute.keys():
			transform = attribute['transform']
			if transform.startswith('translate'):
				trans_child.append(subchild)
				length = len(transform) - 1
				transform = transform[10:length]
				transform = transform.split(',')
				translate.append(float(transform[0]))
				translate.append(float(transform[1]))

		if tag == 'rect' or tag == 'text' or tag == 'tspan':
			if translate and 'x' in attribute.keys():
				if len(translate) > 2:
					translation = [0] * 2
					for i in range(len(translate)):
						if i % 2 == 0:
							translation[0] += translate[i]
						else:
							translation[1] += translate[i]
				else:
					translation = translate[:]

				attribute['x'] = float(attribute['x']) + translation[0]
				attribute['y'] = float(attribute['y']) + translation[1]
			if tag == 'tspan':
				g_attributes.clear()
				attribute['text'] = subchild.text
			# print tag, attribute, translate, '\n'
			attribute['type'] = tag
			if g_attributes:
				attribute.update(g_attributes)
			annotations.append(attribute)

		if tag == 'g':
			g_attributes.clear()
			for i in attribute.keys():
				if i == 'id' or i == 'transform':
					continue
				else:
					g_attributes[i] = attribute[i]

		if tag == 'use':
			for i in attribute.keys():
				if 'href' in i:
					id = attribute[i]
					del attribute[i]
					break
			id = id.replace('#', '')
			defs_list = defs.copy()
			defs_list[id]['id'] = attribute['id']
			if translate and 'x' in defs_list[id].keys():
				if len(translate) > 2:
					translation = [0] * 2
					for i in range(len(translate)):
						if i % 2 == 0:
							translation[0] += translate[i]
						else:
							translation[1] += translate[i]
				else:
					translation = translate[:]

				defs_list[id]['x'] = float(defs_list[id]['x']) + translation[0]
				defs_list[id]['y'] = float(defs_list[id]['y']) + translation[1]
			annotations.append(defs_list[id])

		if tag == 'path':
			path_data = {}
			path = attribute['d'].split(' ')
			paths = []
			for i in path:
				if i == 'z' or i == 'Z':
					continue
				point = i.split(',')
				if not point[0].replace('.', '').isdigit():
					point[0] = point[0][1:]
				point[0] = float(point[0])
				point[1] = float(point[1])
				paths.extend(point)
			x_array = []
			y_array = []
			for j in range(len(paths)):
				if j % 2 == 0:
					x_array.append(paths[j])
				else:
					y_array.append(paths[j])
			x_max = max(x_array)
			y_max = max(y_array)
			x_min = min(x_array)
			y_min = min(y_array)
			x = x_min
			y = y_min
			if translate:
				if len(translate) > 2:
					translation = [0] * 2
					for i in range(len(translate)):
						if i % 2 == 0:
							translation[0] += translate[i]
						else:
							translation[1] += translate[i]
				else:
					translation = translate[:]
				y = y_min + translation[1]
				x = x_min + translation[0]
			height = y_max - y_min
			width = x_max - x_min
			del attribute['d']
			path_data.update(attribute)
			path_data.update(g_attributes)
			path_data['height'] = height
			path_data['width'] = width
			path_data['x'] = x
			path_data['y'] = y
			annotations.append(path_data)

		getSubChild(subchild)
		if translate and subchild == trans_child[len(trans_child) - 1]:
			translate.pop()
			translate.pop()
			trans_child.pop()
	return annotations

def getDefs(root):
	for child in root:
		tag = child.tag.split('}')[1]
		if tag == 'rect':
			attribute = child.attrib
			if 'id' in attribute.keys():
				id = attribute['id']
				del attribute['id']
				attribute['type'] = 'rect'
				defs[id] = attribute

def getChild(root):
	for child in root:
		tag = child.tag.split('}')[1]
		if len(child) > 0 and tag == 'defs':
			getDefs(child)

		elif len(child) > 0 and tag != 'title' and tag != 'desc' and tag != 'defs':
			getSubChild(child)


getChild(root)
# for i in annotations:
# 	print i
