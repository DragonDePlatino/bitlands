import re

grass_data = {
	'MEADOW-GRASS':'GREEN:BLADE',
	'HAIR GRASS':'GREEN:BLADE',
	'BENTGRASS':'GREEN:BLADE',
	'RYEGRASS':'GREEN:BLADE',
	'FESCUE GRASS':'GREEN:BLADE',
	'REEDGRASS':'GREEN:BLADE',
	'KNOTGRASS':'GREEN:BLADE',
	'ZOYSIA':'GREEN:BLADE',
	'DOG\'S TOOTH GRASS':'GREEN:BLADE',
	'DALLISGRASS':'GREEN:BLADE',
	'CARPETGRASS':'GREEN:BLADE',
	'SATINTAIL':'GREEN:BLADE',
	'GRAMA':'GREEN:BLADE',
	'DROPSEED GRASS':'GREEN:BLADE',
	'NEEDLE GRASS':'GREEN:BLADE',
	'BABY TOES SUCCULENT':'GREEN:BLADE',
	'PEBBLE PLANTS':'GREEN:BLADE',
	'BLUE SEDGE':'GREEN:BLADE',
	'FIELD SEDGE':'GREEN:BLADE',
	'PURPLE MOOR GRASS':'GREEN:BLADE',
	'VELVET GRASS':'GREEN:BLADE',
	'MEADOWSWEET':'GREEN:BLADE',
	'RUSH':'GREEN:BLADE',
	'MARSH THISTLE':'GREEN:BLADE',
	'COMMON REED':'GREEN:BLADE',
	'CATTAIL':'GREEN:BLADE',
	'SAWGRASS':'GREEN:BLADE',
	'COTTONGRASS':'GREEN:BLADE',
	'WHITE MOUNTAIN HEATHER':'GREEN:BLADE',
	'MOUNTAIN AVENS':'GREEN:BLADE',
	'CLOUDBERRY':'GREEN:BLADE',
	'WORMY TENDRILS':'PURPLE:ARM',
	'EYEBALL':'GRAY:EYE',
	'BUBBLE BULBS':'TEAL:SHROOM',
	'DOWNY GRASS':'GRAY:BLADE',
	'CAVE MOSS':'TEAL:SHROOM',
	'FLOOR FUNGI':'TEAL:SHROOM',
	'BAMBOO, ARROW':'GREEN:BAMBOO',
	'BAMBOO, GOLDEN':'GREEN:BAMBOO',
	'BAMBOO, HEDGE':'GREEN:BAMBOO'
}

altgrass = {
	'WORMY TENDRILS':'GRASS_ARM2:GRASS_ARM1:GRASS_ARM4:GRASS_ARM3',
	'EYEBALL':'196:196:196:196'
}

regex = re.compile('\[PLANT:(.*)\]')

grasslist = []
with open('objects/plant_grasses.txt', 'r') as file:
	text = file.read()
	grasslist = regex.findall(text)

with open('../objects_patch/plant_grasses.txt', 'w') as file:
	file.write('grass_data = {\n')
	for name in grasslist:
		grass = grass_data[name].split(':')
		file.write('[PLANT:%s]\n' % name)
		file.write('\t[GRASS_COLORS:%s:0:0:%s:0:0:%s:0:0:%s:0:0]\n' % ((grass[0],) * 4))
		file.write('\t[GRASS_TILES:GRASS_%s1:GRASS_%s2:GRASS_%s3:GRASS_%s4]\n' % ((grass[1],) * 4))

		if name in altgrass:
			file.write('\t[ALT_GRASS_TILES:%s]\n' % altgrass[name])




import os, re

'''
	A script to auto-generate Bitlands tree raws.
	Place the objects folder next to this script to generate patches.
'''

# OW tile and color of each sapling
tree_data = {
	'MANGROVE':('BROAD', 'GREEN'),
	'SAGUARO':('CACTI', 'GREEN'),
	'PINE':('PINE', 'GREEN'),
	'CEDAR':('PINE', 'GREEN'),
	'OAK':('BROAD', 'GREEN'),
	'MAHOGANY':('BROAD', 'GREEN'),
	'ACACIA':('BROAD', 'GREEN'),
	'KAPOK':('BROAD', 'GREEN'),
	'MAPLE':('BROAD', 'GREEN'),
	'WILLOW':('BROAD', 'GREEN'),
	'TOWER_CAP':('SHROOM', 'WHITE', 1),
	'BLACK_CAP':('SHROOM', 'SILVER', 1),
	'NETHER_CAP':('SHROOM', 'NAVY', 1),
	'GOBLIN_CAP':('SHROOM', 'RED', 1),
	'FUNGIWOOD':('SHROOM', 'YELLOW', 1),
	'TUNNEL_TUBE':('DEAD', 'PINK', 1),
	'SPORE_TREE':('DEAD', 'TEAL', 1),
	'BLOOD_THORN':('DEAD', 'MAROON', 1),
	'GLUMPRONG':('DEAD', 'PURPLE', 1),
	'FEATHER':('BROAD', 'WHITE'),
	'HIGHWOOD':('BROAD', 'GREEN'),
	'LARCH':('PINE', 'YELLOW'),
	'CHESTNUT':('BROAD', 'MAROON'),
	'ALDER':('BROAD', 'GREEN'),
	'BIRCH':('BROAD', 'WHITE'),
	'ASH':('BROAD', 'GREEN'),
	'CANDLENUT':('BROAD', 'WHITE'),
	'MANGO':('BROAD', 'YELLOW'),
	'RUBBER':('BROAD', 'GREEN'),
	'CACAO':('BROAD', 'MAROON'),
	'PALM':('PALM', 'LIME'),
	'ABACA':('PALM', 'LIME'),
	'BANANA':('PALM', 'YELLOW'),
	'CARAMBOLA':('BROAD', 'YELLOW'),
	'CASHEW':('BROAD', 'RED'),
	'COFFEE':('BROAD', 'RED'),
	'DURIAN':('BROAD', 'OLIVE'),
	'GUAVA':('BROAD', 'LIME'),
	'PAPAYA':('PALM', 'YELLOW'),
	'PARADISE_NUT':('BROAD', 'MAROON'),
	'RAMBUTAN':('BROAD', 'RED'),
	'TEA':('BROAD', 'GREEN'),
	'AVOCADO':('BROAD', 'GREEN'),
	'LIME':('BROAD', 'LIME'),
	'POMELO':('BROAD', 'YELLOW'),
	'CITRON':('BROAD', 'YELLOW'),
	'ORANGE':('BROAD', 'YELOOW'),
	'BITTER_ORANGE':('BROAD', 'YELLOW'),
	'FINGER_LIME':('BROAD', 'RED'),
	'ROUND_LIME':('BROAD', 'LIME'),
	'DESERT_LIME':('BROAD', 'LIME'),
	'KUMQUAT':('BROAD', 'YELLOW'),
	'CUSTARD-APPLE':('BROAD', 'LIME'),
	'DATE_PALM':('PALM', 'YELLOW'),
	'LYCHEE':('BROAD', 'RED'),
	'MACADAMIA':('BROAD', 'OLIVE'),
	'OLIVE':('BROAD', 'LIME'),
	'POMEGRANATE':('BROAD', 'RED'),
	'ALMOND':('BROAD', 'OLIVE'),
	'APPLE':('BROAD', 'RED'),
	'APRICOT':('BROAD', 'YELLOW'),
	'BAYBERRY':('BROAD', 'RED'),
	'CHERRY':('BROAD', 'RED'),
	'GINKGO':('BROAD', 'YELLOW'),
	'HAZEL':('BROAD', 'GREEN'),
	'PEACH':('BROAD', 'RED'),
	'PEAR':('BROAD', 'WHITE'),
	'PECAN':('BROAD', 'YELLOW'),
	'PERSIMMON':('BROAD', 'RED'),
	'PLUM':('BROAD', 'PURPLE'),
	'SAND_PEAR':('BROAD', 'WHITE'),
	'WALNUT':('BROAD', 'OLIVE')
}

# List of growths in each plant.
tree_growth = {
	'MANGROVE':('LEAVES:GREEN', 'FLOWERS:WHITE', 'ROUND:LIME'),
	'SAGUARO':('FLOWERS:WHITE', 'ROUND:RED'),
	'PINE':('LEAVES:GREEN', 'SEED_CONE:OLIVE', 'POLLEN_CONE:YELLOW'),
	'CEDAR':('LEAVES:GREEN', 'SEED_CONE:OLIVE', 'POLLEN_CONE:YELLOW'),
	'OAK':('LEAVES:AUTUMN', 'DROOP:YELLOW', 'ACORN:MAROON'),
	'MAHOGANY':('LEAVES:GREEN', 'FLOWERS:RED', 'TREEPOD:OLIVE'),
	'ACACIA':('LEAVES:GREEN', 'DROOP:YELLOW', 'POD:OLIVE'),
	'KAPOK':('LEAVES:GREEN', 'FLOWERS:RED', 'TREEPOD:LIME'),
	'MAPLE':('LEAVES:AUTUMN', 'FLOWERS:RED', 'SAMARA:LIME'),
	'WILLOW':('LEAVES:GREEN', 'POLLEN_CATKINS:YELLOW', 'SEED_CATKINS:WHITE', 'ROUND:LIME'),
	'TOWER_CAP':(),
	'BLACK_CAP':(),
	'NETHER_CAP':(),
	'GOBLIN_CAP':(),
	'FUNGIWOOD':(),
	'TUNNEL_TUBE':(),
	'SPORE_TREE':(),
	'BLOOD_THORN':(),
	'GLUMPRONG':(),
	'FEATHER':('FEATHERS:LIME', 'EGGS:LIME'),
	'HIGHWOOD':('LEAVES:GREEN', 'FLOWERS:BLUE'),
	'LARCH':('LEAVES:AUTUMN', 'SEED_CONE:OLIVE', 'POLLEN_CONE:YELLOW'),
	'CHESTNUT':('LEAVES:AUTUMN', 'POLLEN_CATKINS:YELLOW', 'SEED_CATKINS:WHITE', 'ACORN:MAROON'),
	'ALDER':('LEAVES:AUTUMN', 'POLLEN_CATKINS:YELLOW', 'SEED_CATKINS:WHITE', 'CONE:MAROON'),
	'BIRCH':('LEAVES:AUTUMN', 'POLLEN_CATKINS:YELLOW', 'SEED_CATKINS:WHITE'),
	'ASH':('LEAVES:AUTUMN', 'FLOWERS:WHITE', 'BERRIES:RED'),
	'CANDLENUT':('LEAVES:GREEN', 'FLOWERS:WHITE', 'NUTS:WHITE'),
	'MANGO':('LEAVES:GREEN', 'FLOWERS:YELLOW', 'ROUND:YELLOW'),
	'RUBBER':('LEAVES:GREEN',),
	'CACAO':('LEAVES:GREEN', 'FLOWERS:WHITE', 'TREEPOD:MAROON'),
	'PALM':('LEAVES:GREEN', 'FLOWERS:YELLOW', 'BERRIES:NAVY'),
	'ABACA':('LEAVES:GREEN', 'FLOWERS:PINK'),
	'BANANA':('LEAVES:GREEN', 'FLOWERS:PINK', 'LONG:YELLOW'),
	'CARAMBOLA':('LEAVES:GREEN', 'FLOWERS:PINK', 'TREEPOD:YELLOW'),
	'CASHEW':('LEAVES:GREEN', 'FLOWERS:PINK', 'TREEPOD:RED'),
	'COFFEE':('LEAVES:GREEN', 'FLOWERS:WHITE', 'BERRIES:RED'),
	'DURIAN':('LEAVES:GREEN', 'FLOWERS:YELLOW', 'MELON:OLIVE'),
	'GUAVA':('LEAVES:GREEN', 'FLOWERS:YELLOW', 'ROUND:LIME'),
	'PAPAYA':('LEAVES:GREEN', 'FLOWERS:WHITE', 'ROUND:LIME'),
	'PARADISE_NUT':('LEAVES:GREEN', 'FLOWERS:RED', 'TREEPOD:MAROON'),
	'RAMBUTAN':('LEAVES:GREEN', 'FLOWERS:WHITE', 'ROUND:RED'),
	'TEA':('LEAVES:GREEN', 'FLOWERS:PINK', 'BERRIES:RED'),
	'AVOCADO':('LEAVES:GREEN', 'FLOWERS:WHITE', 'ROUND:NAVY'),
	'LIME':('LEAVES:GREEN', 'FLOWERS:WHITE', 'ROUND:LIME'),
	'POMELO':('LEAVES:GREEN', 'FLOWERS:WHITE', 'ROUND:LIME'),
	'CITRON':('LEAVES:GREEN', 'FLOWERS:WHITE', 'ROUND:YELLOW'),
	'ORANGE':('LEAVES:GREEN', 'FLOWERS:YELLOW', 'ROUND:YELLOW'),
	'BITTER_ORANGE':('LEAVES:GREEN', 'FLOWERS:WHITE', 'ROUND:YELLOW'),
	'FINGER_LIME':('LEAVES:GREEN', 'FLOWERS:WHITE', 'LONG:RED'),
	'ROUND_LIME':('LEAVES:GREEN', 'FLOWERS:WHITE', 'ROUND:LIME'),
	'DESERT_LIME':('LEAVES:GREEN', 'FLOWERS:WHITE', 'ROUND:LIME'),
	'KUMQUAT':('LEAVES:GREEN', 'FLOWERS:WHITE', 'ROUND:YELLOW'),
	'CUSTARD-APPLE':('LEAVES:GREEN', 'FLOWERS:WHITE', 'ETAERIO:LIME'),
	'DATE_PALM':('LEAVES:GREEN', 'DROOP:YELLOW', 'BERRIES:MAROON'),
	'LYCHEE':('LEAVES:GREEN', 'FLOWERS:WHITE', 'BERRIES:RED'),
	'MACADAMIA':('LEAVES:GREEN', 'DROOP:WHITE', 'NUTS:WHITE'),
	'OLIVE':('LEAVES:GREEN', 'FLOWERS:WHITE', 'BERRIES:LIME'),
	'POMEGRANATE':('LEAVES:AUTUMN', 'FLOWERS:RED', 'ROUND:MAROON'),
	'ALMOND':('LEAVES:AUTUMN', 'FLOWERS:WHITE', 'NUTS:OLIVE'),
	'APPLE':('LEAVES:AUTUMN', 'FLOWERS:PINK', 'ROUND:RED'),
	'APRICOT':('LEAVES:AUTUMN', 'FLOWERS:WHITE', 'ROUND:YELLOW'),
	'BAYBERRY':('LEAVES:GREEN', 'POLLEN_CATKINS:YELLOW', 'SEED_CATKINS:WHITE', 'BERRIES:RED'),
	'CHERRY':('LEAVES:AUTUMN', 'FLOWERS:PINK', 'BERRIES:RED'),
	'GINKGO':('LEAVES:AUTUMN', 'POLLEN_CATKINS:YELLOW', 'NUTS:WHITE'),
	'HAZEL':('LEAVES:AUTUMN', 'POLLEN_CATKINS:YELLOW', 'NUTS:MAROON'),
	'PEACH':('LEAVES:AUTUMN', 'FLOWERS:PINK', 'ROUND:RED'),
	'PEAR':('LEAVES:AUTUMN', 'FLOWERS:WHITE', 'ROUND:LIME'),
	'PECAN':('LEAVES:AUTUMN', 'POLLEN_CATKINS:LIME', 'NUTS:MAROON'),
	'PERSIMMON':('LEAVES:AUTUMN', 'FLOWERS:WHITE', 'ROUND:RED'),
	'PLUM':('LEAVES:AUTUMN', 'FLOWERS:PINK', 'ROUND:PURPLE'),
	'SAND_PEAR':('LEAVES:AUTUMN', 'FLOWERS:WHITE', 'ROUND:YELLOW'),
	'WALNUT':('LEAVES:AUTUMN', 'POLLEN_CATKINS:LIME', 'FLOWERS:WHITE', 'NUTS:OLIVE')
}

# Raws name of each growth
real_name = {
	'LEAVES':'LEAVES',
	'FLOWERS':'FLOWERS',
	'DROOP':'FLOWERS',
	'CONE':'CONE',
	'POLLEN_CONE':'POLLEN_CONE',
	'SEED_CONE':'SEED_CONE',
	'POLLEN_CATKINS':'POLLEN_CATKINS',
	'SEED_CATKINS':'SEED_CATKINS',
	'ACORN':'NUTS',
	'POD':'POD',
	'SAMARA':'FRUIT',
	'NUTS':'FRUIT',
	'BERRIES':'FRUIT',
	'ETAERIO':'FRUIT',
	'ROUND':'FRUIT',
	'LONG':'FRUIT',
	'MELON':'FRUIT',
	'TREEPOD':'FRUIT',
	'FEATHERS':'FEATHERS',
	'EGGS':'EGGS'
}

# Timespan and priority of each growth
grow_time = {
	'LEAVES':'ALL:1',
	'FLOWERS':'60000:119999:2',
	'CONE':'NONE',
	'POLLEN_CONE':'NONE',
	'SEED_CONE':'NONE',
	'POLLEN_CATKINS':'30000:99999:3',
	'SEED_CATKINS':'30000:99999:2',
	'NUTS':'NONE',
	'POD':'120000:200000:3',
	'FRUIT':'120000:200000:3',
	'FEATHERS':'ALL:1',
	'EGGS':'120000:200000:3'
}

# Dark variety of each color
dark_color = {
	'NAVY':'NAVY',
	'GREEN':'GREEN',
	'TEAL':'TEAL',
	'MAROON':'MAROON',
	'PURPLE':'PURPLE',
	'OLIVE':'OLIVE',
	'SILVER':'SILVER',
	'GRAY':'BLACK',
	'BLUE':'NAVY',
	'LIME':'GREEN',
	'CYAN':'TEAL',
	'RED':'MAROON',
	'PINK':'PURPLE',
	'YELLOW':'OLIVE',
	'WHITE':'SILVER'
}

t = 0
regex = re.compile('\[PLANT:(.+)\]')
os.makedirs(os.path.dirname('../objects_patch/'), exist_ok=True)
for inname in ('plant_standard.txt', 'plant_new_trees.txt'):
	plantlist = []
	with open('objects/' + inname, 'r') as infile:
		intext = infile.read()
		plantlist = regex.findall(intext)

	writemode = 'a' if inname == 'plant_standard.txt' else 'w'
	with open('../objects_patch/' + inname, encoding='utf-8', mode=writemode) as outfile:
		for name in plantlist:
			if not t and name != 'MANGROVE':
				continue
			
			tree = tree_data[name]
			color = 'GREEN' if len(tree) == 2 else 'TEAL'
			dead = 'DEAD' if tree[0] == 'BROAD' else tree[0]
			outfile.write('[PLANT:%s]\n' % name)

			outfile.write('\t[TREE_TILE:TREE_%s]\n' % tree[0])
			outfile.write('\t[TREE_COLOR:%s:0:0]\n' % color)
			outfile.write('\t[DEAD_TREE_TILE:TREE_%s]\n' % dead)
			outfile.write('\t[DEAD_TREE_COLOR:%s:0:0]\n' % color)

			outfile.write('\t[SAPLING_TILE:TREE_%s]\n' % tree[0])
			outfile.write('\t[SAPLING_COLOR:%s:0:0]\n' % color)
			outfile.write('\t[DEAD_SAPLING_TILE:TREE_%s]\n' % dead)
			outfile.write('\t[DEAD_SAPLING_COLOR:%s:0:0]\n' % color)

			for growth in tree_growth[name]:
				if not growth:
					continue

				growth = growth.split(':')
				real = real_name[growth[0]]
				priority = str(grow_time[real])
				tile = 'GROWTH_' + growth[0]
				outfile.write('\t[GROWTH:%s]\n' % real)
				if growth[1] == 'AUTUMN':
					outfile.write('\t\t[GROWTH_PRINT:%s:GROWTH_%s:2:0:0:0:209999:1]\n' % (tile, growth[0]))
					outfile.write('\t\t[GROWTH_PRINT:%s:GROWTH_%s:6:0:1:210000:239999:1]\n' % (tile, growth[0]))
					outfile.write('\t\t[GROWTH_PRINT:%s:GROWTH_%s:4:0:1:240000:269999:1]\n' % (tile, growth[0]))
					outfile.write('\t\t[GROWTH_PRINT:%s:GROWTH_%s:4:0:0:270000:300000:1]\n' % (tile, growth[0]))
				else:
					color = '%s:0:%s' % (dark_color[growth[1]], 0 if dark_color[growth[1]] == growth[1] else 1)
					outfile.write('\t\t[GROWTH_PRINT:%s:GROWTH_%s:%s:%s]\n' % (tile, growth[0], color, priority)) 

			t += 1