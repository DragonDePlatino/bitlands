import os, re

'''
	A script to auto-generate Bitlands plant raws.
	Place the objects folder next to this script to generate patches.
'''

# Tile and color of each plant
plant_data = {
	'SINGLE-GRAIN_WHEAT':('GRAIN', 'YELLOW'),
	'TWO-GRAIN_WHEAT':('GRAIN', 'YELLOW'),
	'SOFT_WHEAT':('GRAIN', 'OLIVE'),
	'HARD_WHEAT':('GRAIN', 'YELLOW'),
	'SPELT':('GRAIN', 'LIME'),
	'BARLEY':('GRAIN', 'YELLOW'),
	'BUCKWHEAT':('STALK', 'WHITE'),
	'OATS':('GRAIN', 'YELLOW'),
	'ALFALFA':('STALK', 'PURPLE'),
	'RYE':('GRAIN', 'WHITE'),
	'SORGHUM':('GRAIN', 'MAROON'),
	'RICE':('GRASS', 'YELLOW'),
	'MAIZE':('GRAIN', 'YELLOW'),
	'QUINOA':('GRAIN', 'RED'),
	'KANIWA':('GRASS', 'PINK'),
	'BITTER_VETCH':('STALK', 'PURPLE'),
	'PENDANT_AMARANTH':('BRANCH', 'PINK'),
	'BLOOD_AMARANTH':('STALK', 'RED'),
	'PURPLE_AMARANTH':('GRAIN', 'PURPLE'),
	'RED_SPINACH':('STALK', 'RED'),
	'ELEPHANT-HEAD_AMARANTH':('STALK', 'PURPLE'),
	'PEARL_MILLET':('GRAIN', 'YELLOW'),
	'WHITE_MILLET':('GRAIN', 'WHITE'),
	'FINGER_MILLET':('GRAIN', 'MAROON'),
	'FOXTAIL_MILLET':('GRAIN', 'YELLOW'),
	'FONIO':('GRASS', 'OLIVE'),
	'TEFF':('GRAIN', 'RED'),
	'FLAX':('GRAIN', 'BLUE'),
	'JUTE':('REED', 'LIME'),
	'HEMP':('REED', 'LIME'),
	'COTTON':('BRANCH', 'WHITE'),
	'RAMIE':('REED', 'LIME'),
	'KENAF':('REED', 'LIME'),
	'PAPYRUS_SEDGE':('REED', 'LIME'),
	'ARTICHOKE':('STALK', 'PINK'),
	'ASPARAGUS':('STALK', 'LIME'),
	'BAMBARA_GROUNDNUT':('GRASS', 'LIME'),
	'STRING_BEAN':('VINE', 'LIME'),
	'BROAD_BEAN':('GRAIN', 'LIME'),
	'BEET':('BULB', 'PURPLE'),
	'BITTER_MELON':('VINE', 'LIME'),
	'CABBAGE':('LEAFY', 'GREEN'),
	'CAPER':('BUSH', 'GREEN'),
	'WILD_CARROT':('BULB', 'WHITE'),
	'CASSAVA':('TUBER', 'OLIVE'),
	'CELERY':('TUBER', 'LIME'),
	'CHICKPEA':('STALK', 'LIME'),
	'CHICORY':('STALK', 'CYAN'),
	'COWPEA':('BRANCH', 'LIME'),
	'CUCUMBER':('BRANCH', 'GREEN'),
	'EGGPLANT':('BRANCH', 'PURPLE'),
	'GARDEN_CRESS':('GRASS', 'GREEN'),
	'GARLIC':('BULB', 'WHITE'),
	'HORNED_MELON':('MELON', 'YELLOW'),
	'LEEK':('BULB', 'WHITE'),
	'LENTIL':('STALK', 'GREEN'),
	'LETTUCE':('LEAFY', 'LIME'),
	'MUNG_BEAN':('BRANCH', 'NAVY'),
	'MUSKMELON':('MELON', 'WHITE'),
	'ONION':('BULB', 'WHITE'),
	'PARSNIP':('TUBER', 'WHITE'),
	'PEA':('VINE', 'GREEN'),
	'PEANUT':('BULB', 'OLIVE'),
	'PEPPER':('BRANCH', 'RED'),
	'POTATO':('TUBER', 'OLIVE'),
	'RADISH':('BULB', 'MAROON'),
	'RED_BEAN':('VINE', 'MAROON'),
	'RHUBARB':('BULB', 'MAROON'),
	'SOYBEAN':('BRANCH', 'GREEN'),
	'SPINACH':('LEAFY', 'LIME'),
	'SQUASH':('BULB', 'YELLOW'),
	'SWEET_POTATO':('BULB', 'MAROON'),
	'TARO':('LEAFY', 'GREEN'),
	'TOMATO':('BRANCH', 'RED'),
	'TOMATILLO':('BRANCH', 'LIME'),
	'TURNIP':('BULB', 'PINK'),
	'URAD_BEAN':('BRANCH', 'NAVY'),
	'WATERMELON':('MELON', 'GREEN'),
	'WINTER_MELON':('VINE', 'GREEN'),
	'LESSER_YAM':('TUBER', 'OLIVE'),
	'LONG_YAM':('TUBER', 'OLIVE'),
	'PURPLE_YAM':('TUBER', 'PURPLE'),
	'WHITE_YAM':('TUBER', 'WHITE'),
	'PASSION_FRUIT':('VINE', 'PURPLE'),
	'GRAPE':('BUSH', 'BLUE'),
	'CRANBERRY':('BUSH', 'RED'),
	'BILBERRY':('BUSH', 'BLUE'),
	'BLUEBERRY':('BUSH', 'BLUE'),
	'BLACKBERRY':('BUSH', 'NAVY'),
	'RASPBERRY':('BUSH', 'RED'),
	'PINEAPPLE':('MELON', 'OLIVE'),
	'MUSHROOM_HELMET_PLUMP':('SHROOM', 'PURPLE', 1),
	'GRASS_TAIL_PIG':('GRASS', 'SILVER', 1),
	'GRASS_WHEAT_CAVE':('GRAIN', 'SILVER', 1),
	'POD_SWEET':('BRANCH', 'SILVER', 1),
	'BUSH_QUARRY':('BUSH', 'SILVER', 1),
	'ROOT_MUCK':('BULB', 'OLIVE'),
	'TUBER_BLOATED':('BULB', 'OLIVE'),
	'BULB_KOBOLD':('BULB', 'OLIVE'),
	'BERRIES_PRICKLE':('BUSH', 'OLIVE'),
	'BERRIES_STRAW':('BRANCH', 'RED'),
	'GRASS_LONGLAND':('GRASS', 'YELLOW'),
	'HERB_VALLEY':('STALK', 'LIME'),
	'WEED_RAT':('GRASS', 'GREEN'),
	'BERRIES_FISHER':('LEAFY', 'OLIVE'),
	'REED_ROPE':('REED', 'LIME'),
	'MUSHROOM_CUP_DIMPLE':('SHROOM', 'BLUE', 1),
	'WEED_BLADE':('GRASS', 'GREEN'),
	'ROOT_HIDE':('BULB', 'OLIVE'),
	'SLIVER_BARB':('BARB', 'GREEN'),
	'BERRY_SUN':('GRAIN', 'YELLOW'),
	'VINE_WHIP':('VINE', 'CYAN')
}

# List of growths in each plant.
plant_growth = {
	'SINGLE-GRAIN_WHEAT':('LEAVES:YELLOW',),
	'TWO-GRAIN_WHEAT':('LEAVES:YELLOW',),
	'SOFT_WHEAT':('LEAVES:OLIVE',),
	'HARD_WHEAT':('LEAVES:YELLOW',),
	'SPELT':('LEAVES:GREEN',),
	'BARLEY':('LEAVES:YELLOW',),
	'BUCKWHEAT':('LEAVES:GREEN', 'FLOWERS:WHITE'),
	'OATS':('LEAVES:YELLOW',),
	'ALFALFA':('LEAVES:GREEN', 'FLOWERS:PURPLE'),
	'RYE':('LEAVES:WHITE',),
	'SORGHUM':('LEAVES:GREEN', 'FLOWERS:MAROON'),
	'RICE':('LEAVES:GREEN',),
	'MAIZE':('LEAVES:GREEN',),
	'QUINOA':('LEAVES:GREEN', 'FLOWERS:RED'),
	'KANIWA':('LEAVES:GREEN', 'FLOWERS:PINK'),
	'BITTER_VETCH':('LEAVES:GREEN', 'FLOWERS:PINK', 'POD:LIME'),
	'PENDANT_AMARANTH':('LEAVES:GREEN', 'FLOWERS:PINK'),
	'BLOOD_AMARANTH':('LEAVES:GREEN', 'FLOWERS:RED'),
	'PURPLE_AMARANTH':('LEAVES:GREEN', 'FLOWERS:PURPLE'),
	'RED_SPINACH':('LEAVES:GREEN', 'FLOWERS:RED'),
	'ELEPHANT-HEAD_AMARANTH':('LEAVES:GREEN', 'FLOWERS:PURPLE'),
	'PEARL_MILLET':('LEAVES:GREEN',),
	'WHITE_MILLET':('LEAVES:GREEN',),
	'FINGER_MILLET':('LEAVES:GREEN',),
	'FOXTAIL_MILLET':('LEAVES:GREEN',),
	'FONIO':('LEAVES:GREEN',),
	'TEFF':('LEAVES:GREEN',),
	'FLAX':('LEAVES:GREEN', 'FLOWERS:BLUE'),
	'JUTE':('LEAVES:GREEN', 'FLOWERS:YELLOW'),
	'HEMP':('LEAVES:GREEN',),
	'COTTON':('LEAVES:GREEN', 'FLOWERS:WHITE'),
	'RAMIE':('LEAVES:GREEN',),
	'KENAF':('LEAVES:GREEN', 'FLOWERS:PINK'),
	'PAPYRUS_SEDGE':('LEAVES:GREEN', 'FLOWERS:OLIVE'),
	'ARTICHOKE':('LEAVES:GREEN', 'HEART:WHITE', 'FLOWERS:BLUE'),
	'ASPARAGUS':('LEAVES:GREEN', 'FLOWERS:WHITE', 'BERRIES:RED'),
	'BAMBARA_GROUNDNUT':('LEAVES:GREEN', 'FLOWERS:YELLOW', 'BERRIES:OLIVE'),
	'STRING_BEAN':('LEAVES:GREEN', 'FLOWERS:WHITE', 'POD:LIME'),
	'BROAD_BEAN':('LEAVES:GREEN', 'FLOWERS:PINK', 'POD:LIME'),
	'BEET':('LEAVES:GREEN', 'FLOWERS:WHITE'),
	'BITTER_MELON':('LEAVES:GREEN', 'FLOWERS:YELLOW', 'LONG:LIME'),
	'CABBAGE':('LEAVES:GREEN', 'FLOWERS:PINK'),
	'CAPER':('LEAVES:GREEN', 'BUDS:GREEN', 'FLOWERS:WHITE', 'BERRIES:OLIVE'),
	'WILD_CARROT':('LEAVES:GREEN', 'FLOWERS:WHITE'),
	'CASSAVA':('LEAVES:GREEN', 'FLOWERS:WHITE'),
	'CELERY':('LEAVES:GREEN', 'FLOWERS:WHITE'),
	'CHICKPEA':('LEAVES:GREEN', 'FLOWERS:PINK', 'POD:LIME'),
	'CHICORY':('LEAVES:GREEN', 'FLOWERS:BLUE'),
	'COWPEA':('LEAVES:GREEN', 'FLOWERS:YELLOW', 'POD:LIME'),
	'CUCUMBER':('LEAVES:GREEN', 'FLOWERS:YELLOW', 'LONG:LIME'),
	'EGGPLANT':('LEAVES:GREEN', 'FLOWERS:PURPLE', 'LONG:PURPLE'),
	'GARDEN_CRESS':('LEAVES:GREEN', 'FLOWERS:WHITE'),
	'GARLIC':('LEAVES:GREEN', 'FLOWERS:PURPLE', 'BULB:WHITE'),
	'HORNED_MELON':('LEAVES:GREEN', 'FLOWERS:YELLOW', 'LONG:YELLOW'),
	'LEEK':('LEAVES:GREEN', 'FLOWERS:PINK'),
	'LENTIL':('LEAVES:GREEN', 'FLOWERS:BLUE', 'POD:LIME'),
	'LETTUCE':('LEAVES:GREEN', 'FLOWERS:YELLOW'),
	'MUNG_BEAN':('LEAVES:GREEN', 'FLOWERS:YELLOW', 'POD:LIME'),
	'MUSKMELON':('LEAVES:GREEN', 'FLOWERS:YELLOW', 'MELON:OLIVE'),
	'ONION':('LEAVES:GREEN', 'FLOWERS:PINK', 'BULB:WHITE'),
	'PARSNIP':('LEAVES:GREEN', 'FLOWERS:YELLOW'),
	'PEA':('LEAVES:GREEN', 'FLOWERS:BLUE', 'POD:LIME'),
	'PEANUT':('LEAVES:GREEN', 'FLOWERS:YELLOW', 'NUTS:OLIVE'),
	'PEPPER':('LEAVES:GREEN', 'FLOWERS:WHITE', 'PEPPER:RED'),
	'POTATO':('LEAVES:GREEN', 'FLOWERS:WHITE'),
	'RADISH':('LEAVES:GREEN', 'FLOWERS:WHITE'),
	'RED_BEAN':('LEAVES:GREEN', 'FLOWERS:RED', 'POD:RED'),
	'RHUBARB':('LEAVES:GREEN', 'FLOWERS:WHITE'),
	'SOYBEAN':('LEAVES:GREEN', 'FLOWERS:PINK', 'POD:LIME'),
	'SPINACH':('LEAVES:GREEN', 'FLOWERS:WHITE'),
	'SQUASH':('LEAVES:GREEN', 'FLOWERS:YELLOW', 'LONG:YELLOW'),
	'SWEET_POTATO':('LEAVES:GREEN', 'FLOWERS:WHITE'),
	'TARO':('LEAVES:GREEN', 'FLOWERS:YELLOW'),
	'TOMATO':('LEAVES:GREEN', 'FLOWERS:YELLOW', 'ROUND:RED'),
	'TOMATILLO':('LEAVES:GREEN', 'FLOWERS:YELLOW', 'ROUND:RED'),
	'TURNIP':('LEAVES:GREEN', 'FLOWERS:YELLOW'),
	'URAD_BEAN':('LEAVES:GREEN', 'FLOWERS:YELLOW', 'POD:NAVY'),
	'WATERMELON':('LEAVES:GREEN', 'FLOWERS:YELLOW', 'MELON:LIME'),
	'WINTER_MELON':('LEAVES:GREEN', 'FLOWERS:YELLOW', 'LONG:LIME'),
	'LESSER_YAM':('LEAVES:GREEN', 'FLOWERS:WHITE'),
	'LONG_YAM':('LEAVES:GREEN', 'FLOWERS:PURPLE'),
	'PURPLE_YAM':('LEAVES:GREEN', 'FLOWERS:WHITE'),
	'WHITE_YAM':('LEAVES:GREEN', 'FLOWERS:WHITE'),
	'PASSION_FRUIT':('LEAVES:GREEN', 'FLOWERS:BLUE', 'ROUND:PURPLE'),
	'GRAPE':('LEAVES:GREEN', 'FLOWERS:WHITE', 'ETAERIO:PURPLE'),
	'CRANBERRY':('LEAVES:BLUE', 'FLOWERS:RED', 'BERRIES:RED'),
	'BILBERRY':('LEAVES:GREEN', 'FLOWERS:RED', 'BERRIES:BLUE'),
	'BLUEBERRY':('LEAVES:GREEN', 'FLOWERS:WHITE', 'BERRIES:BLUE'),
	'BLACKBERRY':('LEAVES:GREEN', 'FLOWERS:WHITE', 'ETAERIO:NAVY'),
	'RASPBERRY':('LEAVES:GREEN', 'FLOWERS:WHITE', 'ETAERIO:RED'),
	'PINEAPPLE':('LEAVES:GREEN', 'FLOWERS:RED', 'PINEAPPLE:OLIVE'),
	'MUSHROOM_HELMET_PLUMP':(),
	'GRASS_TAIL_PIG':(),
	'GRASS_WHEAT_CAVE':(),
	'POD_SWEET':(),
	'BUSH_QUARRY':('LEAVES:TEAL',),
	'ROOT_MUCK':(),
	'TUBER_BLOATED':(),
	'BULB_KOBOLD':(),
	'BERRIES_PRICKLE':(),
	'BERRIES_STRAW':('ETAERIO:RED',),
	'GRASS_LONGLAND':(),
	'HERB_VALLEY':(),
	'WEED_RAT':(),
	'BERRIES_FISHER':(),
	'REED_ROPE':(),
	'MUSHROOM_CUP_DIMPLE':(),
	'WEED_BLADE':(),
	'ROOT_HIDE':(),
	'SLIVER_BARB':(),
	'BERRY_SUN':(),
	'VINE_WHIP':()
}

# Raws name of each growth
real_name = {
	'LEAVES':'LEAVES',
	'FLOWERS':'FLOWERS',
	'BUDS':'BUDS',
	'HEART':'HEART',
	'BULB':'BULB',
	'POD':'POD',
	'NUTS':'FRUIT',
	'BERRIES':'FRUIT',
	'ETAERIO':'FRUIT',
	'ROUND':'FRUIT',
	'LONG':'FRUIT',
	'MELON':'FRUIT',
	'PEPPER':'FRUIT',
	'PINEAPPLE':'FRUIT'
}

# Timespan and priority of each growth
grow_time = {
	'LEAVES':'ALL:1',
	'FLOWERS':'60000:119999:2',
	'BUDS':'60000:119999:2',
	'HEART':'0:59999:3',
	'BULB':'ALL:3',
	'POD':'120000:200000:3',
	'FRUIT':'120000:200000:3'
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
for inname in ('plant_crops.txt', 'plant_garden.txt', 'plant_standard.txt'):
	plantlist = []
	with open('objects/' + inname, 'r') as infile:
		intext = infile.read()
		plantlist = regex.findall(intext)

	with open('../objects_patch/' + inname, encoding='utf-8', mode='w') as outfile:
		for name in plantlist:
			if name == "MANGROVE":
				break

			plant = plant_data[name]
			color = 'GREEN' if len(plant) == 2 else 'TEAL'
			outfile.write('[PLANT:%s]\n' % name)
			outfile.write('\t[PICKED_TILE:%d]\n' % t)
			outfile.write('\t[PICKED_COLOR:%s:0:0]\n' % color)
			outfile.write('\t[DEAD_PICKED_TILE:%d]\n' % t)
			outfile.write('\t[DEAD_PICKED_COLOR:%s:0:0]\n' % color)
			outfile.write('\t[SHRUB_TILE:SHRUB_%s]\n' % plant[0])
			outfile.write('\t[SHRUB_COLOR:%s:0:0]\n' % color)
			outfile.write('\t[DEAD_SHRUB_TILE:SHRUB_%s]\n' % plant[0])
			outfile.write('\t[DEAD_SHRUB_COLOR:%s:0:0]\n' % color)

			for growth in plant_growth[name]:
				if not growth:
					continue

				growth = growth.split(':')
				real = real_name[growth[0]]
				priority = str(grow_time[real])
				tile = 0 if real == 'LEAVES' else 'SHRUB_' + plant[0]
				if 'BULB:WHITE' in plant_growth[name]:
					if real == 'FLOWERS':
						priority = '60000:119999:3'
					elif real == 'BULB':
						priority = 'ALL:2'

				outfile.write('\t[GROWTH:%s]\n' % real)
				outfile.write('\t\t[GROWTH_PRINT:%s:GROWTH_%s:%s:0:0:%s]\n' % (tile, growth[0], growth[1], priority)) 
			
			t += 1
			while t in (126, 205, 247):
				t += 1

import os, re

################################################################################
# TREES
################################################################################

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