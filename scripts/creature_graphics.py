#!/usr/bin/env python3

import os, re, math

'''
	A script to auto-generate Bitlands graphical files.
	Place the objects folder next to this script to generate bitlands_creatures.txt and bitlands_races.txt
'''

racelist = ('DWARF', 'HUMAN', 'ELF', 'GOBLIN', 'KOBOLD')
proclist = ('DEMON', 'FORGOTTEN_BEAST', 'TITAN')
joblist =  (
	('STANDARD', 'DRUNK', 'ANIMATED', 'GHOST'),
	('CHILD',),
	('BABY',),
	('MINER',),
	('WOODWORKER', 'CARPENTER', 'BOWYER', 'WOODCUTTER'),
	('STONEWORKER', 'ENGRAVER', 'MASON'),
	('RANGER', 'ANIMAL_CARETAKER', 'ANIMAL_TRAINER', 'HUNTER', 'TRAPPER', 'ANIMAL_DISSECTOR'),
	('METALSMITH', 'FURNACE_OPERATOR', 'WEAPONSMITH', 'ARMORER', 'BLACKSMITH', 'METALCRAFTER'),
	('JEWELER', 'GEM_CUTTER', 'GEM_SETTER'),
	('CRAFTSMAN', 'WOODCRAFTER', 'STONECRAFTER', 'BONE_CARVER', 'GLASSMAKER', 'POTTER', 'GLAZER'),
	('LEATHERWORKER', 'WEAVER', 'CLOTHIER', 'WAX_WORKER', 'STRAND_EXTRACTOR', 'PAPERMAKER', 'BOOKBINDER'),
	('FISHERY_WORKER', 'FISHERMAN', 'FISH_DISSECTOR', 'FISH_CLEANER'),
	('FARMER', 'THRESHER', 'TANNER', 'DYER', 'PLANTER', 'BREWER', 'SOAP_MAKER', 'POTASH_MAKER', 'LYE_MAKER', 'WOOD_BURNER', 'PRESSER'),
	('CHEESE_MAKER', 'MILKER', 'COOK', 'MILLER', 'BUTCHER', 'HERBALIST', 'SHEARER', 'SPINNER', 'BEEKEEPER', 'GELDER'),
	('ENGINEER', 'MECHANIC', 'SIEGE_ENGINEER', 'SIEGE_OPERATOR', 'PUMP_OPERATOR'),
	('DOCTOR', 'DIAGNOSER', 'BONE_SETTER', 'SUTURER', 'SURGEON', 'CHIEF_MEDICAL_DWARF'),
	('PERFORMER', 'POET', 'BARD', 'DANCER'),
	('SAGE', 'SCHOLAR', 'PHILOSOPHER', 'MATHEMATICIAN', 'HISTORIAN', 'ASTRONOMER', 'NATURALIST', 'CHEMIST', 'GEOGRAPHER', 'SCRIBE'),
	('HAMMERMAN', 'MASTER_HAMMERMAN'),
	('SPEARMAN', 'MASTER_SPEARMAN'),
	('CROSSBOWMAN', 'MASTER_CROSSBOWMAN'),
	('WRESTLER', 'MASTER_WRESTLER'),
	('AXEMAN', 'MASTER_AXEMAN'),
	('SWORDSMAN', 'MASTER_SWORDSMAN'),
	('MACEMAN', 'MASTER_MACEMAN'),
	('PIKEMAN', 'MASTER_PIKEMAN'),
	('BOWMAN', 'MASTER_BOWMAN'),
	('BLOWGUNMAN', 'MASTER_BLOWGUNMAN'),
	('LASHER', 'MASTER_LASHER'),
	('RECRUIT',),
	('EXPEDITION_LEADER', 'MANAGER', 'BOOKKEEPER', 'BROKER', 'DIPLOMAT', 'OUTPOST_LIASON', 'MERCHANT', 'CLERK', 'ADMINISTRATOR', 'FORCED_ADMINISTRATOR', 'TRADER', 'ARCHITECT', 'ALCHEMIST', 'TAVERN_KEEPER'),
	('CHAMPION', 'MILITIA_CAPTAIN', 'MILITIA_COMMANDER', 'SHERIFF', 'CAPTAIN_OF_THE_GUARD', 'CAPTAIN', 'LIEUTENANT', 'GENERAL', 'RANGER_CAPTAIN'),
	('MAYOR', 'DUKE', 'DUKE_CONSORT', 'DUCHESS', 'DUCHESS_CONSORT', 'COUNT', 'COUNT_CONSORT', 'COUNTESS', 'COUNTESS_CONSORT', 'BARON', 'BARON_CONSORT', 'BARONESS', 'BARONESS_CONSORT'),
	('MONARCH', 'MONARCH_CONSORT', 'KING', 'KING_CONSORT', 'QUEEN', 'QUEEN_CONSORT'),
	('HAMMERER', 'THIEF', 'MASTER_THIEF', 'MONSTER_SLAYER', 'SCOUT', 'SNATCHER', 'MERCENARY', 'CRIMINAL', 'PEDDLER', 'SLAVE', 'PRISONER'),
	('PRIEST', 'HIGH_PRIEST', 'ACOLYTE', 'DRUID', 'PROPHET', 'PILGRIM', 'MONK', 'MESSENGER')
)

files = [i for i in os.listdir('objects') if 'creature' in i]
creaturelist = []
regex = re.compile('\[CREATURE:(.*)\]')

for inname in files:
	with open('objects/' + inname, encoding='latin-1', mode='r') as infile:
		intext = infile.read()
		creaturelist.extend(regex.findall(intext))

with open('../graphics/graphics_creatures.txt', encoding='latin-1', mode='w') as outfile:
	sheet_width = 42
	tilenum = len(creaturelist)
	outfile.write('graphics_creatures')
	outfile.write('\n\n[OBJECT:GRAPHICS]')
	outfile.write('\n\n[TILE_PAGE:CREATURES]')
	outfile.write('\n\t[FILE:creatures.bmp]')
	outfile.write('\n\t[TILE_DIM:12:18]')
	outfile.write('\n\t[PAGE_DIM:%d:%d]' % (min(sheet_width, tilenum), math.ceil(tilenum / sheet_width)))
	outfile.write('\n\n[CREATURE_GRAPHICS:CREATURES]')

	p = 0
	for name in creaturelist:
		if p and not p % sheet_width:
			outfile.write('\n')

		outfile.write('\n\t[CREATURE_GRAPHICS:%s]' % name)
		outfile.write('\n\t\t[DEFAULT:CREATURES:%d:%d:ADD_COLOR:DEFAULT]' % (p % sheet_width, p // sheet_width))
		p += 1

	for name in proclist:
		for i in range(500):
			outfile.write('\n\t[CREATURE_GRAPHICS:%s_%d' % (name, i))
			outfile.write('\n\t\t[DEFAULT:CREATURES:%d:%d:ADD_COLOR:DEFAULT]' % (p % sheet_width, p // sheet_width))
		p += 1

with open('../graphics/graphics_races.txt', encoding='latin-1', mode='w') as outfile:
	sheet_width = len(joblist)
	tilenum = len(racelist) * len(joblist)
	outfile.write('graphics_races')
	outfile.write('\n\n[OBJECT:GRAPHICS]')
	outfile.write('\n\n[TILE_PAGE:RACES]')
	outfile.write('\n\t[FILE:races.bmp]')
	outfile.write('\n\t[TILE_DIM:12:18]')
	outfile.write('\n\t[PAGE_DIM:%d:%d]' % (min(sheet_width, tilenum), math.ceil(tilenum / sheet_width)))
	outfile.write('\n\n[CREATURE_GRAPHICS:RACES]')

	p = 0
	for name in racelist:
		outfile.write('\n\t[CREATURE_GRAPHICS:%s]' % name)
		for sublist in joblist:
			for job in sublist:
				outfile.write('\n\t\t[%s:RACES:%d:%d:ADD_COLOR:DEFAULT]' % (job, p % sheet_width, p // sheet_width))
			p += 1