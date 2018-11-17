#!/usr/bin/env python3

import os, re

# A script to auto-generate Bitlands overrides.

os.makedirs(os.path.dirname('../init/'), exist_ok=True)
file = open('../init/overrides.txt', encoding='latin-1', mode='w')
def header(text):
	file.write('\n================================================================================\n')
	file.write(' %s\n' % text)
	file.write('================================================================================\n\n')

def grid_new():
	grid = []
	for x in range(16):
		grid.append([])
		for y in range(16):
			grid[x].append([])
	return grid

def is_number(s):
	try: 
		int(s)
		return True
	except ValueError:
		return False

def grid_write(grid, tileset, title=''):
	header(title.upper() if title else tileset.upper())
	for y in range(16):
		for x in range(16):
			for t in grid[x][y]:
				tile = t.split(':')
				if len(tile) > 4 and tile[4] in ('I', 'B'):
					# Item or building override
					file.write('[OVERRIDE:%s:%s:%s:%s:%s:%s:%s' % (tile[3], tile[4], tile[0], tile[1], tile[2], tileset, x + y * 16))
					if len(tile) > 5:
						if is_number(tile[5]):
							# Add color
							file.write(':%s:%s' % (int(tile[5]) + 1, int(tile[6]) + 1))

							if len(tile) > 7:
								# Add material
								file.write(':')
								for m in tile[7:]:
									file.write(':%s' % m)
						else:
							# Add material
							file.write('::')
							for m in tile[5:]:
								file.write(':%s' % m)
				else:
					# Tile override
					file.write('[OVERRIDE:%s:T:%s:%s:%s' % (tile[1], tile[0], tileset, x + y * 16))
					if len(tile) > 2:
						if is_number(tile[2]):
							# Add color
							file.write(':%s:%s' % (int(tile[2]) + 1, int(tile[3]) + 1))

							if len(tile) > 4:
								# Add material
								file.write(':')
								for m in tile[4:]:
									file.write(':%s' % m)
						else:
							# Add material
							file.write('::')
							for m in tile[2:]:
								file.write(':%s' % m)
				file.write(']\n')

################################################################################
# TILESETS
################################################################################

header('TILESETS')
tilesets = ('tiles', 'buildings', 'items', 'plants', 'crops', 'workshops')
for i in tilesets:
	file.write('[TILESET:bitlands_%s.bmp:bitlands_%s.bmp:%s]\n' % (i, i, i))

################################################################################
# TILES
################################################################################

tiles = grid_new()

boulders = ('Stone', 'Mineral', 'Lava', 'Feature')
tracks = ('Stone', 'Mineral', 'Constructed', 'Frozen', 'Lava', 'Feature')

walltiles = (	'RD', 'LRD', 'LD', 'LD2', 'RD2',
				'RUD', 'LRUD', 'LUD', 'UD',
				'RU', 'LRU', 'LU', 'LU2', 'RU2',
				'R2U', 'R2D', 'LR', 'L2U', 'L2D', 'Pillar')
walltops = (	201, 	203, 	187, 	183, 
				204, 	206, 	185, 	186)
wallbottoms = (	200, 	202, 	188, 	189, 
				212, 	205, 	190, 	9)
wallswap = {	183:214, 189:211, 212:213, 190:184}

tracktiles =(	'SE:201',	'SEW:203',	'SW:187',	'NS:186',	'S:210',
				'NSE:204',	'NSEW:206',	'NSW:185',	'EW:205',	'N:208',
				'NE:200',	'NEW:202',	'NW:188',	'E:198',	'W:181',)
trackdesig = (	201,	203,	187,	210,
				204,	206,	185,	186,
				200,	202,	188,	208,
				198,	205,	181)
floornames, floortiles = set(), set()

stones = (	'Soil:59', 'Soil:126', 'Soil:247', 'Soil:58', 'Stone:34', 'Stone:246', 'Stone:40',
			'Stone:61','Stone:124', 'Stone:240', 'Stone:171', 'Stone:45', 'Stone:33', 'Stone:63',
			'Stone:19', 'Stone:248', 'Stone:7', 'Stone:9',  'Stone:94', 'Stone:127', 'Stone:16',
			'Stone:250', 'Stone:249', 'Stone:4', 'Feature:35', 'Feature:254', 'Frozen:219', 'Lava:40')
ramps = (	'Soil', 'Stone', 'Mineral', 'Constructed', 'Feature', 'Frozen', 'Lava',
			'GrassLight', 'GrassDark', 'GrassDry', 'GrassDead', 'TreeCap', 'BurningTreeCap', 'TreeDeadCap',
			'MurkyPool', 'RiverRampN', 'RiverRampS', 'RiverRampE', 'RiverRampW', 'RiverRampNE', 'RiverRampNW', 'RiverRampSE', 'RiverRampSW')
stairs = ('UnderworldGate', 'Soil', 'Grass1', 'Grass2', 'Stone', 'Mineral', 'Constructed', 'Feature', 'Frozen', 'Lava')
minable = ('Stone', 'Mineral', 'Frozen', 'Lava', 'Feature')
designation = (30, 95, 43, 60, 62, 88)

def track(name):
	if name not in floornames:
		floornames.add(name)
		for t in range(len(trackdesig)):
			x = 12 + t % 4
			y = 8 + t // 4
			tiles[x][y].append('%s:%s' % (name, trackdesig[t]))

def floor(name, pos, varied, uniform=0, smooth=False):
	x = pos[0]
	y = pos[1]

	for v in varied:
		floortiles.add(v)
	if uniform:
		floortiles.add(uniform)

	prefix = ['Light', 'Dark', 'Dry', 'Dead'] if 'Grass' in name else ['']
	postfix = '' if 'Pebbles' in name else 'Floor'
	for i in range(4):
		for p in prefix:
			fullname = name + p + postfix + str(i + 1)
			tiles[x + i][y].append('%s:%s' % (fullname, varied[i]))

			if uniform and uniform != varied[i]:
				tiles[x + i][y].append('%s:%s' % (fullname, uniform))
			if smooth:
				tiles[4][0].append('%s:43' % fullname)
			track(fullname)

	if smooth:
		fullname = name + 'FloorSmooth'
		tiles[5][0].append('%s:43' % fullname)
		track(fullname)

def wall(name, pos, mat=''):
	postfix = 'Wall' if name == 'Constructed' else 'WallSmooth'
	for tile in walltiles:
		realfix = '' if tile == 'Pillar' else postfix
		for t in range(len(walltops)):
			x = 0 + t % 4
			y = 8 + t // 4
			tiles[x][y].append('%s%s%s:%s%s' % (name, realfix, tile, walltops[t], mat))

			if walltops[t] in wallswap:
				tiles[x][y].append('%s%s%s:%s%s' % (name, realfix, tile, wallswap[walltops[t]], mat))

		for b in range(len(wallbottoms)):
			x = pos[0] + b % 4
			y = pos[1] + b // 4
			tiles[x][y].append('%s%s%s:%s%s' % (name, realfix, tile, wallbottoms[b], mat))

			if wallbottoms[b] in wallswap:
				tiles[x][y].append('%s%s%s:%s%s' % (name, realfix, tile, wallswap[wallbottoms[b]], mat))

tiles[0][0] = ['OpenSpace:178']
tiles[1][0] = ['OpenSpace:249', 'OpenSpace:250']
tiles[2][0] = ['Chasm:35']

for t in ('', 'Dead'):
	for i in range(1, 5):
		tiles[3][0].append('Tree%sCapFloor%s:249' % (t, i))
		tiles[3][0].append('Tree%sCapFloor%s:46' % (t, i))

tiles[5][0] = ['ConstructedFloor:43']
tiles[6][0] = ['BrookTop:236']
tiles[7][0] = ['Driftwood:240']
tiles[8][0] = ['SemiMoltenRock:176']
tiles[9][0] = ['EeriePit:42']
tiles[10][0] = ['Fire:39', 'BurningTreeCapFloor:46']
tiles[11][0] = ['Fire:44', 'BurningTreeTwigs:59']
tiles[12][0] = ['Fire:46', 'BurningTreeBranches:172']
tiles[13][0] = ['Fire:96', 'BurningTreeTrunk:19', 'BurningTreeCapWall:19']
tiles[14][0] = ['Campfire:15']

tiles[0][1] = ['FurrowedSoil:126']
tiles[1][1] = ['FurrowedSoil:247']
tiles[2][1] = ['FurrowedSoil:205']
tiles[3][1] = ['Ashes1:242']
tiles[4][1] = ['Ashes2:243']
tiles[5][1] = ['Ashes3:126']
tiles[6][1] = ['ANY_ROAD:RoadDirt::126:B']
tiles[7][1] = ['ANY_ROAD:RoadDirt::247:B']
tiles[8][1] = ['ANY_ROAD:RoadPaved::43:B']
tiles[9][1] = ['ANY_ROAD:RoadPaved::247:B']

for s in range(len(stones)):
	x = s % 16
	y = 2 + s // 16

	stone = stones[s].split(':')
	prefix = ('Stone', 'Mineral') if stone[0] == 'Stone' else (stone[0],)
	for p in prefix:
		tiles[x][y].append('%sWall:%s' % (p, stone[1]))

for w in range(len(minable)):
	for i in range(3):
		tiles[12 + i][3].append('%sWallWorn%s:%s' % (minable[w], i + 1, 176 + i))

for b in boulders:
	tiles[15][3].append('%sBoulder:236' % b)

floor('Soil', [0, 4], [39, 44, 96, 46], 46)
floor('Soil', [0, 5], [247, 247, 126, 126], 247) # Sand
floor('SoilWet', [0, 6], [39, 44, 96, 46], 46)
floor('SoilWet', [0, 6], [247, 247, 126, 126], 247) # Sand
floor('Frozen', [0, 7], [178, 178, 178, 178], 46, True)

floor('Stone', [4, 4], [39, 44, 96, 44], 46, True)
floor('Mineral', [4, 4], [39, 44, 96, 44], 46, True)
floor('StonePebbles', [4, 5], [39, 44, 96, 46], 46)
floor('MineralPebbles', [4, 5], [39, 44, 96, 46], 46)
floor('LavaPebbles', [4, 5], [39, 44, 96, 46], 46)
floor('FeaturePebbles', [4, 5], [39, 44, 96, 46], 46)
floor('Feature', [4, 6], [39, 44, 96, 44], 46, True)
floor('Lava', [4, 7], [39, 44, 96, 44], 46, True)

floor('Grass', [8, 4], [39, 44, 46, 96], 46)
floor('Grass', [8, 5], [5, 5, 5, 5]) # Flowers
floor('Grass', [8, 6], [124, 186, 244, 245]) # Bamboo
floor('Grass', [8, 7], [94, 166, 167, 252]) # Underground

floor('Grass', [12, 4], [169, 170, 242, 243]) # Tendrils
floor('Grass', [12, 5], [9, 79, 111, 248]) # Bubble 1
floor('Grass', [12, 6], [196, 196, 196, 196]) # Bubble 2

wall('Stone', [4, 8])
wall('Mineral', [4, 8])
wall('Constructed', [4, 8], ':IS_STONE')

wall('Constructed', [8, 8], ':WOOD')

wall('Frozen', [0, 10])
wall('Feature', [0, 10])

wall('Lava', [4, 10])

# Must always be at bottom
wall('Constructed', [0, 10])

tiles[ 8][10] = ['FrozenFortification:206', 'FeatureFortification:206']
tiles[ 9][10] = ['StoneFortification:206', 'MineralFortification:206', 'ConstructedFortification:206', 'ConstructedFortification:206:WOOD']
tiles[10][10] = ['ConstructedFortification:206:IS_GEM']
tiles[10][11] = ['LavaFortification:206']

for s in stairs:
	tiles[ 8][11].append('%sStairU:60' % s)
	tiles[ 9][11].append('%sStairD:62' % s)
	tiles[10][11].append('%sStairUD:88' % s)

for r in ramps:
	name = r if 'Ramp' in r else r + 'Ramp'
	tiles[8][14].append('%s:30' % name)
tiles[12][14] = ['RampTop:31']

for t in range(len(tracktiles)):
	x = t % 5
	y = 12 + t // 5

	track = tracktiles[t].split(':')
	for name in tracks:
		tiles[x][y].append('%sFloorTrack%s:%s' % (name, track[0], track[1]))

		if len(track[0]) > 1:
			tiles[x + 5][y].append('%sRampTrack%s:30' % (name, track[0]))
			tiles[x + 9][y].append('%sRampTrack%s:31' % (name, track[0]))

for d in range(len(designation)):
	for m in minable:
		x = d
		y = 15
		tiles[x][y].append('%sWall:%s' % (m, designation[d]))

tiles[6][15] = ['TreeTrunkPillar:47']

grid_write(tiles, tilesets[0])

################################################################################
# BUILDINGS
################################################################################

builds = grid_new()

bridges = (	'201',	'187',	'43',		'210',
			'200',	'188',	'111:206',	'186',
			'198',	'205',	'181',		'208')
windmills =(92,		186, 	47,
			205,	79,		196,
			0,		179)
siege =(220, 221, 222, 223, 210, 181, 198, 208,
		30,  16,  17,  31,  47,  92,  8,   177,
		209, 174, 175, 186, 205, 207, 179, 196)
buildlist = (
	'ACTIVITY_ZONE::240',
	'ANY_BARRACKS::88',
	'ANY_HOSPITAL::88',
	'ANY_HOSPITAL_STORAGE::88',
	'ANY_MACHINE::88',
	'ANY_NOBLE_ROOM::88',
	'ARCHERY_TARGET:ArcheryTarget:88',
	'AXLE_HORIZONTAL::205',
	'AXLE_HORIZONTAL::196',
	'AXLE_HORIZONTAL::186',
	'AXLE_HORIZONTAL::179',
	'AXLE_VERTICAL::9',
	'AXLE_VERTICAL::111',
	'BARS_FLOOR:BarsFloor:240',
	'BARS_VERTICAL:BarsVertical:19',
	'CHAIN:Chain:21',
	'GEAR_ASSEMBLY:GearAssembly:15',
	'GEAR_ASSEMBLY:GearAssembly:42',
	'GRATE_FLOOR:GrateFloor:35',
	'GRATE_WALL:GrateWall:215',
	'HATCH:Hatch:155',
	'NEST:Nest:172',
	'NEST_BOX:NestBox:8',
	'ROLLERS:Rollers:209',
	'ROLLERS:Rollers:182',
	'ROLLERS:Rollers:207',
	'ROLLERS:Rollers:199',
	'SCREW_PUMP:ScrewPump:246',
	'SCREW_PUMP:ScrewPump:37',
	'STOCKPILE:Stockpile:61',
	'SUPPORT:Support:73',
	'TRAP:Trap:149:0',
	'TRAP:Trap:162:0',
	'TRAP:Trap:94:1',
	'TRAP:Trap:94:2',
	'TRAP:Trap:94:3',
	'TRAP:Trap:94:4',
	'WAGON:Wagon:178',
	'WATER_WHEEL:WaterWheel:186',
	'WATER_WHEEL:WaterWheel:196',
	'WATER_WHEEL:WaterWheel:205',
	'WATER_WHEEL:WaterWheel:179',
	'WEAPON_UPRIGHT::179',
	'WELL:Well:9',
	'WORKSHOP_CUSTOM:Workshop:207:SCREW_PRESS',
	'WORKSHOP_MILLSTONE:Workshop:111')

t = 0
for b in buildlist:
	build = b.split(':')
	subtype = build[3] if len(build) == 4 else ''
	builds[t % 16][t // 16].append('%s:%s:%s:%s:B' % (build[0], build[1], subtype, build[2]))
	t += 1

for i in sorted(floortiles):
	if i == 179:
		continue
	builds[t % 16][t // 16].append('WEAPON_UPRIGHT:Weapon::%s:B' % i)

for b in range(len(bridges)):
	x = b % 4
	y = 3 + b // 4
	for bridge in bridges[b].split(':'):
		builds[x][y].append('BRIDGE:::%s:B' % bridge)

for w in range(len(windmills)):
	x = 4 + w % 3
	y = 3 + w // 3
	builds[x][y].append('WINDMILL:::%d:B' % windmills[w])

for s in range(len(siege)):
	x = 7 + s % 8
	y = 3 + s // 8
	builds[x][y].append(':SiegeEngine::%d:B' % siege[s])

grid_write(builds, tilesets[1])

################################################################################
# ITEMS
################################################################################

items = grid_new()
itemlist = (
	'AMMO:47',
	'AMMO:92',
	'AMMO:179',
	'AMMO:196',
	'AMULET:12',
	'ANIMALTRAP:127',
	'ANVIL:229',
	'ARMOR:ITEM_ARMOR_BREASTPLATE:ITEM_ARMOR_MAIL_SHIRT:ITEM_ARMOR_LEATHER:ITEM_ARMOR_COAT:ITEM_ARMOR_SHIRT:ITEM_ARMOR_CLOAK:ITEM_ARMOR_TUNIC:ITEM_ARMOR_TOGA:ITEM_ARMOR_CAPE:ITEM_ARMOR_VEST:ITEM_ARMOR_DRESS:ITEM_ARMOR_ROBE',
	'ARMORSTAND:14',
	'BACKPACK:146',
	'BALLISTAARROWHEAD:17',
	'BALLISTAPARTS:220',
	'BAR:240',
	'BARREL:246',
	'BED:233',
	'BIN:88',
	'BLOCKS:254',
	'BOOK:8',
	'BOULDER:9',
	'BOULDER:7',
	'BOULDER:61',
	'BOULDER:28',
	'BOULDER:227',
	'BOULDER:43',
	'BOULDER:42',
	'BOULDER:243',
	'BOULDER:254',
	'BOX:11',
	'BOX:146',
	'BRACELET:148',
	'BUCKET:150',
	'CABINET:227',
	'CAGE:19',
	'CATAPULTPARTS:220',
	'CHAIN:21',
	'CHAIR:210',
	'CHEESE:37',
	'CLOTH:167',
	'COFFIN:48',
	'COIN:36',
	# 'CORPSE:38:66:67:69:70:71:72:74:75:76:77:78:80:81:82:83:84:85:89:97:98:99:100:101:102:103:104:105:106:107:108:109:110:112:113:114:115:116:117:118:119:120:121:122:142:164',
	# 'CORPSEPIECE:253',
	'CROWN:230',
	'CRUTCH:194',
	'DOOR:15',
	'DOOR:79',
	'DOOR:186',
	'DOOR:197',
	'DOOR:240',
	'EARRING:235',
	'EGG:248',
	'FIGURINE:143',
	# 'FISH:224',
	# 'FISH_RAW:224',
	'FLASK:IS_GLASS',
	'FLASK:LEATHER',
	'FLASK:WOOD',
	'FLOODGATE:42',
	'FLOODGATE:88',
	'FLOODGATE:215',
	'FOOD:ITEM_FOOD_BISCUITS:ITEM_FOOD_STEW:ITEM_FOOD_ROAST',
	'GEM:4',
	'GLOB:247',
	'GLOVES:ITEM_GLOVES_GAUNTLETS:ITEM_GLOVES_GLOVES:ITEM_GLOVES_MITTENS',
	'GOBLET:IS_METAL',
	'GOBLET:IS_STONE',
	'GOBLET:WOOD',
	'GRATE:35',
	'HATCH_COVER:155',
	'HELM:ITEM_HELM_HELM:ITEM_HELM_CAP:ITEM_HELM_HOOD:ITEM_HELM_TURBAN:ITEM_HELM_MASK:ITEM_HELM_VEIL_HEAD:ITEM_HELM_VEIL_FACE:ITEM_HELM_SCARF_HEAD',
	# 'INSTRUMENT:168:168:168:168:168',
	'MEAT:BRAIN',
	'MEAT:EYE',
	'MEAT:GIZZARD',
	'MEAT:GUT',
	'MEAT:HEART',
	'MEAT:KIDNEY',
	'MEAT:LIVER',
	'MEAT:LUNG',
	'MEAT:MUSCLE',
	'MEAT:PANCREAS',
	'MEAT:SPLEEN',
	'MEAT:STOMACH',
	'MILLSTONE:9',
	'ORTHOPEDIC_CAST:159',
	'PANTS:ITEM_PANTS_PANTS:ITEM_PANTS_GREAVES:ITEM_PANTS_LEGGINGS:ITEM_PANTS_LOINCLOTH:ITEM_PANTS_THONG:ITEM_PANTS_SKIRT:ITEM_PANTS_SKIRT_SHORT:ITEM_PANTS_SKIRT_LONG:ITEM_PANTS_BRAIES',
	'PIPE_SECTION:124',
	'PLANT_GROWTH:6:6:6:6',
	'PLANT_GROWTH:5:5:5:5',
	'PLANT_GROWTH:237:237:237:237',
	'PLANT_GROWTH:3:3:3:3',
	'PLANT_GROWTH:229:229:229:229',
	'PLANT_GROWTH:170:170:170:170',
	'PLANT_GROWTH:167:167:167:167',
	'PLANT_GROWTH:166:166:166:166',
	'PLANT_GROWTH:236:236:236:236',
	'PLANT_GROWTH:7:7:7:7',
	'PLANT_GROWTH:169:169:169:169',
	'PLANT_GROWTH:9:9:9:9',
	'PLANT_GROWTH:44:44:44:44',
	'PLANT_GROWTH:224:224:224:224',
	'PLANT_GROWTH:35:35:35:35',
	'PLANT_GROWTH:126:126:126:126',
	'PLANT_GROWTH:162:162:162:162',
	'PLANT_GROWTH:42:42:42:42',
	'PLANT_GROWTH:238:238:238:238',
	'PLANT_GROWTH:147:147:147:147',
	'PLANT_GROWTH:60:60:60:60',
	'PLANT_GROWTH:233:233:233:233',
	'PLANT_GROWTH:168:168:168:168',
	'PLANT_GROWTH:111:111:111:111',
	'QUERN:9',
	'QUIVER:146',
	'REMAINS:253',
	'RING:148',
	'ROUGH:15',
	# 'ROUGH:248',
	# 'ROUGH:7',
	# 'ROUGH:94',
	# 'ROUGH:127',
	# 'ROUGH:249',
	# 'ROUGH:4',
	'SCEPTER:45',
	'SEEDS:250',
	'SHEET:245',
	'SHIELD:ITEM_SHIELD_SHIELD:ITEM_SHIELD_BUCKLER',
	'SHOES:ITEM_SHOES_SHOES:ITEM_SHOES_BOOTS:ITEM_SHOES_BOOTS_LOW:ITEM_SHOES_SANDAL:ITEM_SHOES_CHAUSSE:ITEM_SHOES_SOCKS',
	# 'SIEGEAMMO:179',
	# 'SIEGEAMMO:196'
	'SKIN_TANNED:225',
	'SLAB:239',
	'SMALLGEM:4',
	'SPLINT:159',
	'STATUE:234',
	'TABLE:209',
	'THREAD:237',
	# 'TOOL:147:13:248:248:47:47:47:47:47:47:8:229:232:22:236:173:254:153:158:246:246:236:240:240:92:92:139:227',
	'TOOL:ITEM_TOOL_CAULDRON:ITEM_TOOL_LADLE:ITEM_TOOL_BOWL:ITEM_TOOL_MORTAR:ITEM_TOOL_PESTLE:ITEM_TOOL_KNIFE_CARVING:ITEM_TOOL_KNIFE_BONING:ITEM_TOOL_KNIFE_SLICING:ITEM_TOOL_KNIFE_MEAT_CLEAVER:ITEM_TOOL_FORK_CARVING:ITEM_TOOL_NEST_BOX:ITEM_TOOL_JUG:ITEM_TOOL_LARGE_POT:ITEM_TOOL_HIVE:ITEM_TOOL_HONEYCOMB:ITEM_TOOL_POUCH:ITEM_TOOL_MINECART:ITEM_TOOL_WHEELBARROW:ITEM_TOOL_STEPLADDER:ITEM_TOOL_SCROLL_ROLLERS:ITEM_TOOL_BOOK_BINDING:ITEM_TOOL_SCROLL:ITEM_TOOL_QUIRE:ITEM_TOOL_BOOKCASE:ITEM_TOOL_HELVE:ITEM_TOOL_STONE_AXE:ITEM_TOOL_PEDESTAL:ITEM_TOOL_DISPLAY_CASE',
	'TOTEM:135',
	'TOY:ITEM_TOY_PUZZLEBOX:ITEM_TOY_BOAT:ITEM_TOY_HAMMER:ITEM_TOY_AXE:ITEM_TOY_MINIFORGE',
	'TRACTION_BENCH:232',
	'TRAPCOMP:ITEM_TRAPCOMP_GIANTAXEBLADE:ITEM_TRAPCOMP_ENORMOUSCORKSCREW:ITEM_TRAPCOMP_SPIKEDBALL:ITEM_TRAPCOMP_LARGESERRATEDDISC:ITEM_TRAPCOMP_MENACINGSPIKE',
	'TRAPPARTS:128',
	'WEAPON:ITEM_WEAPON_WHIP:ITEM_WEAPON_AXE_BATTLE:ITEM_WEAPON_HAMMER_WAR:ITEM_WEAPON_SWORD_SHORT:ITEM_WEAPON_SPEAR:ITEM_WEAPON_MACE:ITEM_WEAPON_CROSSBOW:ITEM_WEAPON_PICK:ITEM_WEAPON_BOW:ITEM_WEAPON_BLOWGUN:ITEM_WEAPON_PIKE:ITEM_WEAPON_HALBERD:ITEM_WEAPON_SWORD_2H:ITEM_WEAPON_SWORD_LONG:ITEM_WEAPON_MAUL:ITEM_WEAPON_AXE_GREAT:ITEM_WEAPON_DAGGER_LARGE:ITEM_WEAPON_SCOURGE:ITEM_WEAPON_FLAIL:ITEM_WEAPON_MORNINGSTAR:ITEM_WEAPON_SCIMITAR:ITEM_WEAPON_AXE_TRAINING:ITEM_WEAPON_SWORD_SHORT_TRAINING:ITEM_WEAPON_SPEAR_TRAINING',
	'WEAPONRACK:251',
	'WOOD:22')
itemtile = {
	'ARMOR':91,
	'FOOD':37,
	'FLASK':173,
	'GLOVES':91,
	'GOBLET':20,
	'HELM':91,
	'PANTS':91,
	'SHIELD':91,
	'SHOES':91,
	'TOY':145,
	'TRAPCOMP':228,
	'WEAPON':47}
tooltile = {
	'ITEM_TOOL_CAULDRON':147,
	'ITEM_TOOL_LADLE':13,
	'ITEM_TOOL_BOWL':248,
	'ITEM_TOOL_MORTAR':248,
	'ITEM_TOOL_PESTLE':47,
	'ITEM_TOOL_KNIFE_CARVING':47,
	'ITEM_TOOL_KNIFE_BONING':47,
	'ITEM_TOOL_KNIFE_SLICING':47,
	'ITEM_TOOL_KNIFE_MEAT_CLEAVER':47,
	'ITEM_TOOL_FORK_CARVING':47,
	'ITEM_TOOL_NEST_BOX':8,
	'ITEM_TOOL_JUG':229,
	'ITEM_TOOL_LARGE_POT':232,
	'ITEM_TOOL_HIVE':22,
	'ITEM_TOOL_HONEYCOMB':236,
	'ITEM_TOOL_POUCH':173,
	'ITEM_TOOL_MINECART':254,
	'ITEM_TOOL_WHEELBARROW':153,
	'ITEM_TOOL_STEPLADDER':158,
	'ITEM_TOOL_SCROLL_ROLLERS':246,
	'ITEM_TOOL_BOOK_BINDING':246,
	'ITEM_TOOL_SCROLL':236,
	'ITEM_TOOL_QUIRE':240,
	'ITEM_TOOL_BOOKCASE':240,
	'ITEM_TOOL_HELVE':92,
	'ITEM_TOOL_STONE_AXE':92,
	'ITEM_TOOL_PEDESTAL':139,
	'ITEM_TOOL_DISPLAY_CASE':227}
buildlist = {
	'ANIMALTRAP:127':'TRAP:AnimalTrap',
	'ARMORSTAND:14':'ARMOR_STAND:Armorstand',
	'BED:233':'BED:Bed',
	'BOX:11':'BOX:Box',
	'BOX:146':'BOX:Box',
	'CABINET:227':'CABINET:Cabinet',
	'CAGE:19':'CAGE:Cage',
	'CHAIR:210':'CHAIR:Chair',
	'COFFIN:48':'COFFIN:Coffin',
	'DOOR:15':'DOOR:Door',
	'DOOR:79':'DOOR:Door',
	'DOOR:186':'DOOR:Door',
	'DOOR:197':'DOOR:Door',
	'DOOR:240':'DOOR:Door',
	'FLOODGATE:42':'FLOODGATE:Floodgate',
	'FLOODGATE:88':'FLOODGATE:Floodgate',
	'FLOODGATE:215':'FLOODGATE:Floodgate',
	'MILLSTONE:9':'WORKSHOP_MILLSTONE:Workshop',
	'QUERN:9':'WORKSHOP_QUERN:Workshop',
	'SLAB:239':'SLAB:Slab',
	'STATUE:234':'STATUE:Statue',
	'TABLE:209':'TABLE:Table',
	'TOOL:ITEM_TOOL_HIVE':'HIVE:Hive',
	'TOOL:ITEM_TOOL_BOOKCASE':'BOOKCASE:Bookcase',
	'TOOL:ITEM_TOOL_PEDESTAL':'DISPLAY_CASE:DisplayFurniture',
	'TOOL:ITEM_TOOL_DISPLAY_CASE':'DISPLAY_CASE:DisplayFurniture',
	'TRACTION_BENCH:232':'TRACTION_BENCH:TractionBench',
	'WEAPONRACK:251':'WEAPON_RACK:Weaponrack'}
nomove = ('CORPSE', 'PLANT_GROWTH')

# Get list of creatures for all meat items
creatures = []
regex = re.compile('\[CREATURE:(.*)\]')
for inname in (i for i in os.listdir('objects') if 'creature' in i):
	with open('objects/' + inname, 'r', encoding='latin-1') as infile:
		intext = infile.read()
		creatures += regex.findall(intext)

t = 0
for i in itemlist:
	item = i.split(':')
	subnum = len(item) - 1

	for s in range(subnum):
		if(item[0] == 'MEAT'):
			for c in creatures:
				items[t % 16][t // 16].append('MEAT:MEAT::224:I::CREATURE_MAT:%s:%s' % (c, item[1]))
				items[t % 16][t // 16].append('ANY_REFUSE:MEAT::224:I::CREATURE_MAT:%s:%s' % (c, item[1]))

				# Meat encased in ice walls, pillars and obsidian
				items[t % 16][t // 16].append("ANY_ENCASED:MEAT::219:I:3:11:CREATURE_MAT:%s:%s" % (c, item[1]))
				items[t % 16][t // 16].append("ANY_ENCASED:MEAT::199:I:3:11:CREATURE_MAT:%s:%s" % (c, item[1]))
				items[t % 16][t // 16].append("ANY_ENCASED:MEAT::40:I:0:5:CREATURE_MAT:%s:%s" % (c, item[1]))
		else:
			sub, tile, mat = item[s + 1], item[s + 1], ''

			if not is_number(sub):
				# Item has list of subtypes, not list of tiles
				if (item[0] == 'TOOL'):
					tile = tooltile[sub]
				else:
					tile = itemtile[item[0]]
			elif subnum > 1:
				# Item has list of tiles
				sub = s
			else:
				# Item only has one tile
				sub = ''


			if item[0] in ('FLASK', 'GOBLET'):
				mat = ':' + sub
				sub = ''

			items[t % 16][t // 16].append("%s:%s:%s:%s:I%s" % (item[0], item[0], sub, tile, mat))

			# Check if item is also a building
			b = '%s:%s' % (item[0], sub if sub else item[s + 1])
			if b in buildlist:
				items[t % 16][t // 16].append("%s::%s:B%s" % (buildlist[b], tile, mat))

			# Items encased in ice walls, pillars and obsidian
			items[t % 16][t // 16].append("ANY_ENCASED:%s:%s:219:I:3:11%s" % (item[0], sub, mat))
			items[t % 16][t // 16].append("ANY_ENCASED:%s:%s:199:I:3:11%s" % (item[0], sub, mat))
			items[t % 16][t // 16].append("ANY_ENCASED:%s:%s:40:I:0:5%s" % (item[0], sub, mat))

		if item[0] not in nomove and s < subnum - 1:
			t += 1
	t += 1

items[t % 16][t // 16].append("ANY_WEBS:::15:I")
t += 1
items[t % 16][t // 16].append("WINDOW:WINDOW::177:I:IS_GLASS")
items[t % 16][t // 16].append("WINDOW_ANY:WindowGlass::177:B")
t += 1
items[t % 16][t // 16].append("WINDOW:WINDOW::177:I:IS_GEM")
items[t % 16][t // 16].append("WINDOW_ANY:WindowGem::177:B")
# t += 1
# items[t % 16][t // 16].append("ANY_DEAD_DWARF:CORPSE::1:I")

grid_write(items, tilesets[2])

################################################################################
# PLANTS
################################################################################

plants = grid_new()
trunks = (	('NW:201',),
			('N:205', 'SEW:203'),
			('NE:187',),
			('NS:186', 'BranchW:182', 'BranchE:199'),
			('W:186', 'NSE:204'),
			('NSEW:206',),
			('E:186', 'NSW:185'),
			('EW:205', 'BranchN:207', 'BranchS:209'),
			('SW:200',),
			('S:205', 'NEW:202'),
			('SE:188',),
			(),
			('Interior:10',),
			('Pillar:79',),
			('Sloping:127',))
branches = ('NW:217',	'SEW:194',	'NE:192',	'NS:179',
			'NSE:195',	'NSEW:197',	'NSW:180',	'EW:196',
			'SW:191',	'NEW:193',	'SE:218')
caps = (	'NW:201',	'N:205',		'NE:187',
			'W:186',	'Pillar:79',	'E:186',
			'SW:200',	'S:205',		'SE:188')
shrubs = (174, 215, 20, 157, 152, 21, 5, 6, 229, 235, 147, 231, 15)
growths = (6, 5, 237, 3, 229, 170, 167, 166, 236, 7, 169, 9, 44, 224, 35, 126, 162, 42, 238, 147, 60, 233, 168, 111, 172)
trunkgrowths = (58, 7, 169)
trunktiles = ('Interior', 'Pillar', 'Sloping')
treenum = 72

def trunk(pos, mat=''):
	for i in range(len(trunks)):
		x = pos[0] + i % 4
		y = pos[1] + i // 4
		for p in ('', 'Dead'):
			for t in trunks[i]:
				plants[x][y].append('Tree%sTrunk%s%s' % (p, t, mat))

def branch(pos, mat=''):
	for i in range(len(branches)):
		x = pos[0] + i % 4
		y = pos[1] + i // 4
		for p in ('', 'Dead'):
			plants[x][y].append('Tree%sBranch%s%s' % (p, branches[i], mat))

plants[0][5] = ['FARM_PLOT:FarmPlot::126:B']
plants[1][5] = ['FARM_PLOT:FarmPlot::247:B']
plants[2][5] = ['FARM_PLOT:FarmPlot::205:B']

for i in range(len(shrubs)):
	for p in ('', 'Dead'):
		plants[3 + i][5].append('Shrub%s:%s' % (p, shrubs[i]))

for g in range(len(growths)):
	x = g % 16
	y = 6 + g // 16

	for j in ('Branches', 'BranchesSmooth', 'DeadBranches', 'DeadBranchesSmooth'):
		plants[x][y].append('Tree%s:%s' % (j, growths[g]))
	plants[x][y].append('TreeTrunkInterior:%s' % growths[g])
	plants[x][y].append('TreeTrunkPillar:%s' % growths[g])

	twig = 59 if growths[g] == 172 else growths[g]
	plants[x][y + 2].append('TreeTwigs:%s' % twig)
	plants[x][y + 2].append('TreeTrunkSloping:%s' % twig)

plants[4][13] = ['TreeTwigs:59', 'TreeDeadTwigs:59']
plants[5][13] = ['TreeRoots:172', 'TreeDeadRoots:172']
plants[6][13] = ['TreeRootSloping:127', 'TreeDeadRootSloping:127']

trunk([0, 10])
branch([4, 10])
branch([8, 10], ':WOOD:PLANT:SAGUARO')

for c in range(len(caps)):
	x = 8 + c % 3
	y = 10 + c // 3
	cap = caps[c].split(':')
	prefix = '' if cap[0] == 'Pillar' else 'Wall'
	plants[x][y].append('TreeCap%s%s:%s' % (prefix, cap[0], cap[1]))

grid_write(plants, tilesets[3])

################################################################################
# CROPS
################################################################################

crops = grid_new()
plantnum = 112

for t in range(plantnum):
	i = t + plantnum
	crops[t % 16][t // 16].append('FARM_PLOT:FarmPlot::%s:B' % t)
	crops[i % 16][i // 16].append('PLANT:PLANT::%s:I' % t)

grid_write(crops, tilesets[4])

################################################################################
# WORKSHOPS
################################################################################

workshops = grid_new()

works = {
	'FURNACE_GLASS_ANY:Furnace:':'7:61:93:111',
	# 'FURNACE_GLASS_MAGMA':'7:61:93:111',
	'FURNACE_KILN_ANY:Furnace:':'7:61:93:111',
	# 'FURNACE_KILN_MAGMA':'7:61:93:111',
	'FURNACE_SMELTER_ANY:Furnace:':'7:61:93:111',
	'FURNACE_SMELTER_MAGMA:Furnace:':'7:61:93:111',
	'FURNACE_WOOD:Furnace:':'7:61:93:111',
	'TRADE_DEPOT:TradeDepot:':'47:79:92:219',
	'WORKSHOP_ASHERY:Workshop:':'45:47:88:92:177:246:247',
	'WORKSHOP_BOWYER:Workshop:':'40:45:47:92:93:176:238',
	'WORKSHOP_BUTCHER:Workshop:':'45:47:92:178:236:247',
	'WORKSHOP_CARPENTER:Workshop:':'34:45:47:61:92:93:176',
	'WORKSHOP_CLOTHIER:Workshop:':'45:47:91:92:93:176:237',
	'WORKSHOP_CRAFTSDWARF:Workshop:':'45:47:92:93:176',
	'WORKSHOP_CUSTOM:Workshop:SOAP_MAKER':'8:45:47:61:150',
	'WORKSHOP_DYER:Workshop:':'7:45:47:92:150',
	'WORKSHOP_FARMER:Workshop:':'45:47:65:79:92:210:237:240',
	'WORKSHOP_FISHERY:Workshop:':'35:45:47:92:178:224',
	'WORKSHOP_FORGE_ANY:Workshop:':'7:31:45:47:92:229:240',
	'WORKSHOP_JEWELER:Workshop:':'42:45:47:91:123:176',
	'WORKSHOP_KENNEL:Workshop:':'35:45:47:92:235',
	'WORKSHOP_KITCHEN:Workshop:':'40:45:47:59:78:92:176:236:246',
	'WORKSHOP_LEATHER:Workshop:':'45:47:92:176:177',
	'WORKSHOP_LOOM:Workshop:':'35:45:47:92:167:180:195:237',
	'WORKSHOP_MAGMA_FORGE:Workshop:':'8:45:47:92:196:229',
	'WORKSHOP_MASON:Workshop:':'46:47:59:91:92:111:176',
	'WORKSHOP_MECHANIC:Workshop:':'45:47:91:92:93:94:127:128:176',
	'WORKSHOP_SIEGE:Workshop:':'45:47:92:111:126:176',
	'WORKSHOP_STILL:Workshop:':'45:47:92:111:126:184:205:246',
	'WORKSHOP_TANNER:Workshop:':'8:45:47:92:176',
}

for work, wt in works.items():
	tiles = wt.split(':')
	for t in tiles:
		t = int(t)
		workshops[t % 16][t // 16].append('%s:%s:B' % (work, t))
		

grid_write(workshops, 'workshops')
file.close()