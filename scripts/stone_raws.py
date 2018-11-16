import os, re

'''
	A script to auto-generate Bitlands tree raws.
	Place the objects folder next to this script to generate patches.
'''

# Foreground, background and type of each inorganic
stone_data = {
	'ONYX':('BLACK:FIRESAFE:OPAL_LOW'),
	'MORION':('BLACK:FIRESAFE:PRISM_LOW'),
	'SCHORL':('BLACK:FIRESAFE:PRISM_LOW'),
	'LACE AGATE':('CYAN:FIRESAFE:OPAL_LOW'),
	'BLUE JADE':('TEAL:FIRESAFE:OPAL_LOW'),
	'LAPIS LAZULI':('NAVY:FIRESAFE:OPAL_LOW'),
	'PRASE':('GREEN:FIRESAFE:OPAL_LOW'),
	'PRASE OPAL':('LIME:FIRESAFE:OPAL_MED'),
	'BLOODSTONE':('MAROON:FIRESAFE:OPAL_LOW'),
	'MOSS AGATE':('TEAL:FIRESAFE:OPAL_LOW'),
	'MOSS OPAL':('YELLOW:FIRESAFE:OPAL_MED'),
	'VARISCITE':('TEAL:FIRESAFE:OPAL_LOW'),
	'CHRYSOPRASE':('TEAL:FIRESAFE:OPAL_LOW'),
	'CHRYSOCOLLA':('TEAL:FIRESAFE:OPAL_LOW'),
	'SARD':('RED:FIRESAFE:OPAL_LOW'),
	'CARNELIAN':('RED:FIRESAFE:OPAL_LOW'),
	'BANDED AGATE':('OLIVE:FIRESAFE:OPAL_LOW'),
	'SARDONYX':('RED:FIRESAFE:OPAL_LOW'),
	'CHERRY OPAL':('RED:FIRESAFE:OPAL_MED'),
	'LAVENDER JADE':('PINK:FIRESAFE:OPAL_LOW'),
	'PINK JADE':('PINK:FIRESAFE:OPAL_LOW'),
	'TUBE AGATE':('OLIVE:FIRESAFE:OPAL_LOW'),
	'FIRE AGATE':('MAROON:FIRESAFE:OPAL_LOW'),
	'PLUME AGATE':('MAROON:FIRESAFE:OPAL_LOW'),
	'BROWN JASPER':('OLIVE:FIRESAFE:OPAL_LOW'),
	'PICTURE JASPER':('OLIVE:FIRESAFE:OPAL_LOW'),
	'SMOKY QUARTZ':('BLACK:FIRESAFE:PRISM_LOW'),
	'WAX OPAL':('OLIVE:FIRESAFE:OPAL_MED'),
	'WOOD OPAL':('OLIVE:FIRESAFE:OPAL_MED'),
	'AMBER OPAL':('OLIVE:FIRESAFE:OPAL_MED'),
	'GOLD OPAL':('YELLOW:FIRESAFE:OPAL_MED'),
	'CITRINE':('YELLOW:FIRESAFE:PRISM_LOW'),
	'YELLOW JASPER':('YELLOW:FIRESAFE:OPAL_LOW'),
	'TIGEREYE':('OLIVE:FIRESAFE:OPAL_LOW'),
	'TIGER IRON':('MAROON:FIRESAFE:OPAL_LOW'),
	'SUNSTONE':('MAROON:FIRESAFE:OPAL_LOW'),
	'RESIN OPAL':('NAVY:FIRESAFE:OPAL_MED'),
	'PYRITE':('GRAY:FIRESAFE:OPAL_LOW'),
	'CLEAR TOURMALINE':('WHITE:FIRESAFE:PRISM_MED'),
	'GRAY CHALCEDONY':('GRAY:FIRESAFE:OPAL_LOW'),
	'DENDRITIC AGATE':('WHITE:FIRESAFE:OPAL_LOW'),
	'SHELL OPAL':('TEAL:FIRESAFE:OPAL_MED'),
	'BONE OPAL':('WHITE:FIRESAFE:OPAL_MED'),
	'WHITE CHALCEDONY':('WHITE:FIRESAFE:OPAL_LOW'),
	'FORTIFICATION AGATE':('MAROON:FIRESAFE:OPAL_LOW'),
	'MILK QUARTZ':('WHITE:FIRESAFE:PRISM_LOW'),
	'MOONSTONE':('CYAN:FIRESAFE:OPAL_LOW'),
	'WHITE JADE':('WHITE:FIRESAFE:OPAL_LOW'),
	'JASPER OPAL':('TEAL:FIRESAFE:OPAL_MED'),
	'PINEAPPLE OPAL':('WHITE:FIRESAFE:OPAL_MED'),
	'ONYX OPAL':('BLACK:FIRESAFE:OPAL_MED'),
	'MILK OPAL':('WHITE:FIRESAFE:OPAL_MED'),
	'PIPE OPAL':('OLIVE:FIRESAFE:OPAL_MED'),
	'AVENTURINE':('GREEN:FIRESAFE:OPAL_LOW'),
	'TURQUOISE':('CYAN:FIRESAFE:OPAL_LOW'),
	'QUARTZ_ROSE':('PINK:FIRESAFE:PRISM_LOW'),
	'CRYSTAL_ROCK':('PURPLE:FIRESAFE:CLUSTER_LOW'),
	'BLACK ZIRCON':('BLACK:FIRESAFE:CLUSTER_HIGH'),
	'BLACK PYROPE':('BLACK:FIRESAFE:CLUSTER_HIGH'),
	'MELANITE':('BLACK:FIRESAFE:CLUSTER_MED'),
	'INDIGO TOURMALINE':('CYAN:FIRESAFE:CLUSTER_RARE'),
	'BLUE GARNET':('BLUE:FIRESAFE:CLUSTER_RARE'),
	'TSAVORITE':('LIME:FIRESAFE:CLUSTER_RARE'),
	'GREEN TOURMALINE':('LIME:FIRESAFE:CLUSTER_HIGH'),
	'DEMANTOID':('LIME:FIRESAFE:CLUSTER_RARE'),
	'GREEN ZIRCON':('LIME:FIRESAFE:CLUSTER_HIGH'),
	'GREEN JADE':('GREEN:FIRESAFE:OPAL_HIGH'),
	'HELIODOR':('YELLOW:FIRESAFE:PRISM_HIGH'),
	'PERIDOT':('LIME:FIRESAFE:PRISM_HIGH'),
	'RED ZIRCON':('RED:FIRESAFE:CLUSTER_HIGH'),
	'RED TOURMALINE':('PINK:FIRESAFE:CLUSTER_MED'),
	'RED PYROPE':('RED:FIRESAFE:CLUSTER_HIGH'),
	'ALMANDINE':('MAROON:FIRESAFE:CLUSTER_HIGH'),
	'RED GROSSULAR':('RED:FIRESAFE:CLUSTER_HIGH'),
	'PINK TOURMALINE':('RED:FIRESAFE:CLUSTER_MED'),
	'RED BERYL':('PURPLE:FIRESAFE:PRISM_HIGH'),
	'FIRE OPAL':('RED:FIRESAFE:OPAL_MED'),
	'RHODOLITE':('PURPLE:FIRESAFE:CLUSTER_HIGH'),
	'SPINEL_PURPLE':('PURPLE:FIRESAFE:CLUSTER_HIGH'),
	'ALEXANDRITE':('PURPLE:FIRESAFE:CLUSTER_HIGH'),
	'TANZANITE':('BLUE:FIRESAFE:PRISM_HIGH'),
	'MORGANITE':('WHITE:FIRESAFE:CLUSTER_HIGH'),
	'VIOLET SPESSARTINE':('PURPLE:FIRESAFE:CLUSTER_HIGH'),
	'PINK GARNET':('PINK:FIRESAFE:CLUSTER_HIGH'),
	'KUNZITE':('PINK:FIRESAFE:PRISM_HIGH'),
	'CINNAMON GROSSULAR':('RED:FIRESAFE:CLUSTER_HIGH'),
	'HONEY YELLOW BERYL':('YELLOW:FIRESAFE:PRISM_HIGH'),
	'JELLY OPAL':('CYAN:FIRESAFE:OPAL_MED'),
	'BROWN ZIRCON':('OLIVE:FIRESAFE:CLUSTER_HIGH'),
	'YELLOW ZIRCON':('YELLOW:FIRESAFE:CLUSTER_HIGH'),
	'GOLDEN BERYL':('YELLOW:FIRESAFE:CLUSTER_HIGH'),
	'YELLOW SPESSARTINE':('YELLOW:FIRESAFE:PRISM_HIGH'),
	'TOPAZ':('CYAN:FIRESAFE:CLUSTER_HIGH'),
	'TOPAZOLITE':('OLIVE:FIRESAFE:CLUSTER_HIGH'),
	'YELLOW GROSSULAR':('YELLOW:FIRESAFE:CLUSTER_HIGH'),
	'RUBICELLE':('RED:FIRESAFE:CLUSTER_HIGH'),
	'CLEAR GARNET':('WHITE:FIRESAFE:PRISM_HIGH'),
	'GOSHENITE':('WHITE:FIRESAFE:PRISM_HIGH'),
	'CAT\'S EYE':('YELLOW:FIRESAFE:OPAL_HIGH'),
	'CLEAR ZIRCON':('YELLOW:FIRESAFE:CLUSTER_RARE'),
	'AMETHYST':('PURPLE:FIRESAFE:CLUSTER_HIGH'),
	'AQUAMARINE':('CYAN:FIRESAFE:PRISM_HIGH'),
	'SPINEL_RED':('RED:FIRESAFE:CLUSTER_HIGH'),
	'CHRYSOBERYL':('YELLOW:FIRESAFE:CLUSTER_HIGH'),
	'OPAL_PFIRE':('RED:FIRESAFE:OPAL_HIGH'),
	'OPAL_REDFLASH':('RED:FIRESAFE:OPAL_HIGH'),
	'OPAL_BLACK':('BLACK:FIRESAFE:OPAL_RARE'),
	'OPAL_WHITE':('WHITE:FIRESAFE:OPAL_HIGH'),
	'OPAL_CRYSTAL':('CYAN:FIRESAFE:OPAL_HIGH'),
	'OPAL_CLARO':('WHITE:FIRESAFE:OPAL_HIGH'),
	'OPAL_LEVIN':('BLACK:FIRESAFE:OPAL_HIGH'),
	'OPAL_HARLEQUIN':('BLUE:FIRESAFE:OPAL_HIGH'),
	'OPAL_PINFIRE':('TEAL:FIRESAFE:OPAL_HIGH'),
	'OPAL_BANDFIRE':('BLUE:FIRESAFE:OPAL_HIGH'),
	'DIAMOND_LY':('YELLOW:FIRESAFE:CLUSTER_RARE'),
	'DIAMOND_FY':('YELLOW:FIRESAFE:CLUSTER_RARE'),
	'EMERALD':('LIME:FIRESAFE:CLUSTER_RARE'),
	'RUBY':('RED:FIRESAFE:CLUSTER_RARE'),
	'SAPPHIRE':('BLUE:FIRESAFE:CLUSTER_RARE'),
	'DIAMOND_CLEAR':('WHITE:FIRESAFE:CLUSTER_RARE'),
	'DIAMOND_RED':('MAROON:FIRESAFE:CLUSTER_RARE'),
	'DIAMOND_GREEN':('LIME:FIRESAFE:CLUSTER_RARE'),
	'DIAMOND_BLUE':('BLUE:FIRESAFE:CLUSTER_RARE'),
	'DIAMOND_YELLOW':('YELLOW:FIRESAFE:CLUSTER_RARE'),
	'DIAMOND_BLACK':('BLACK:FIRESAFE:CLUSTER_RARE'),
	'SAPPHIRE_STAR':('PURPLE:FIRESAFE:OPAL_RARE'),
	'RUBY_STAR':('PINK:FIRESAFE:OPAL_RARE'),
	'SANDSTONE':('OLIVE:MAGMASAFE:SEDIMENTARY'),
	'SILTSTONE':('YELLOW:FIRESAFE:SEDIMENTARY'),
	'MUDSTONE':('GRAY:FIRESAFE:SEDIMENTARY'),
	'SHALE':('BLACK:FIRESAFE:SEDIMENTARY'),
	'CLAYSTONE':('MAROON:FIRESAFE:SEDIMENTARY'),
	'ROCK_SALT':('WHITE:FIRESAFE:SEDIMENTARY'),
	'LIMESTONE':('WHITE:FIRESAFE:FLUX'),
	'CONGLOMERATE':('GRAY:FIRESAFE:SEDIMENTARY'),
	'DOLOMITE':('WHITE:MAGMASAFE:FLUX'),
	'CHERT':('SILVER:MAGMASAFE:SEDIMENTARY'),
	'CHALK':('WHITE:FIRESAFE:FLUX'),
	'GRANITE':('WHITE:FIRESAFE:INTRUSIVE'),
	'DIORITE':('BLACK:FIRESAFE:INTRUSIVE'),
	'GABBRO':('BLACK:MAGMASAFE:INTRUSIVE'),
	'RHYOLITE':('OLIVE:FIRESAFE:EXTRUSIVE'),
	'BASALT':('BLACK:MAGMASAFE:EXTRUSIVE'),
	'ANDESITE':('GRAY:FIRESAFE:EXTRUSIVE'),
	'DACITE':('GRAY:FIRESAFE:EXTRUSIVE'),
	'OBSIDIAN':('BLACK:PURPLE:EXTRUSIVE'),
	'QUARTZITE':('SILVER:MAGMASAFE:METAMORPHIC'),
	'SLATE':('BLACK:FIRESAFE:METAMORPHIC'),
	'PHYLLITE':('GRAY:FIRESAFE:METAMORPHIC'),
	'SCHIST':('OLIVE:FIRESAFE:METAMORPHIC'),
	'GNEISS':('GRAY:FIRESAFE:METAMORPHIC'),
	'MARBLE':('WHITE:FIRESAFE:FLUX'),
	'HEMATITE':('IRON:MAGMASAFE:ORE_MED'),
	'LIMONITE':('IRON:FIRESAFE:ORE_MED'),
	'GARNIERITE':('NICKEL:FIRESAFE:ORE_LOW'),
	'NATIVE_GOLD':('GOLD:FIRESAFE:ORE_HIGH'),
	'NATIVE_SILVER':('WHITE:FIRESAFE:ORE_MED'),
	'NATIVE_COPPER':('COPPER:FIRESAFE:ORE_LOW'),
	'MALACHITE':('COPPER:NOTSAFE:ORE_LOW'),
	'GALENA':('SILVER:MAGMASAFE:ORE_MED'),
	'SPHALERITE':('ZINC:MAGMASAFE:ORE_LOW'),
	'CASSITERITE':('TIN:MAGMASAFE:ORE_LOW'),
	'COAL_BITUMINOUS':('FUEL:FIRESAFE:FUEL'),
	'LIGNITE':('FUEL:FIRESAFE:FUEL'),
	'NATIVE_PLATINUM':('PLATINUM:MAGMASAFE:ORE_HIGH'),
	'CINNABAR':('RED:FIRESAFE:BUILDING'),
	'COBALTITE':('BLUE:FIRESAFE:BUILDING'),
	'TETRAHEDRITE':('GRAY:FIRESAFE:ORE_LOW'),
	'HORN_SILVER':('SILVER:NOTSAFE:ORE_MED'),
	'GYPSUM':('YELLOW:NOTSAFE:PLASTER'),
	'TALC':('WHITE:MAGMASAFE:BUILDING'),
	'JET':('BLACK:FIRESAFE:BUILDING'),
	'PUDDINGSTONE':('OLIVE:FIRESAFE:BUILDING'),
	'PETRIFIED_WOOD':('RED:MAGMASAFE:BUILDING'),
	'GRAPHITE':('BLACK:FIRESAFE:BUILDING'),
	'BRIMSTONE':('YELLOW:NOTSAFE:BUILDING'),
	'KIMBERLITE':('GRAY:FIRESAFE:BUILDING'),
	'BISMUTHINITE':('BISMUTH:FIRESAFE:ORE_LOW'),
	'REALGAR':('RED:NOTSAFE:BUILDING'),
	'ORPIMENT':('YELLOW:NOTSAFE:BUILDING'),
	'STIBNITE':('SILVER:NOTSAFE:BUILDING'),
	'MARCASITE':('OLIVE:NOTSAFE:BUILDING'),
	'SYLVITE':('RED:FIRESAFE:BUILDING'),
	'CRYOLITE':('WHITE:FIRESAFE:BUILDING'),
	'PERICLASE':('GREEN:MAGMASAFE:BUILDING'),
	'ILMENITE':('BLACK:MAGMASAFE:BUILDING'),
	'RUTILE':('YELLOW:MAGMASAFE:BUILDING'),
	'MAGNETITE':('IRON:MAGMASAFE:ORE_MED'),
	'CHROMITE':('BLACK:MAGMASAFE:BUILDING'),
	'PYROLUSITE':('BLACK:NOTSAFE:BUILDING'),
	'PITCHBLENDE':('BLACK:MAGMASAFE:BUILDING'),
	'BAUXITE':('MAROON:MAGMASAFE:BUILDING'),
	'NATIVE_ALUMINUM':('ALUMINIUM:FIRESAFE:ORE_HIGH'),
	'BORAX':('WHITE:FIRESAFE:BUILDING'),
	'OLIVINE':('GREEN:MAGMASAFE:BUILDING'),
	'HORNBLENDE':('BLACK:FIRESAFE:BUILDING'),
	'KAOLINITE':('WHITE:MAGMASAFE:BUILDING'),
	'SERPENTINE':('OLIVE:NOTSAFE:BUILDING'),
	'ORTHOCLASE':('YELLOW:MAGMASAFE:BUILDING'),
	'MICROCLINE':('TEAL:FIRESAFE:BUILDING'),
	'MICA':('OLIVE:MAGMASAFE:BUILDING'),
	'CALCITE':('WHITE:MAGMASAFE:FLUX'),
	'SALTPETER':('YELLOW:NOTSAFE:BUILDING'),
	'ALABASTER':('SILVER:NOTSAFE:PLASTER'),
	'SELENITE':('SILVER:NOTSAFE:PLASTER'),
	'SATINSPAR':('SILVER:NOTSAFE:PLASTER'),
	'ANHYDRITE':('SILVER:MAGMASAFE:BUILDING'),
	'ALUNITE':('OLIVE:MAGMASAFE:BUILDING'),
	'RAW_ADAMANTINE':('ADAMANTINE:MAGMASAFE:ADAMANTINE'),
	'SLADE':('BLACK:NAVY:SLADE'),
	'CLAY':('SILVER:GRAY:CLAY'),
	'SILTY_CLAY':('TEAL:SILVER:CLAY'),
	'SANDY_CLAY':('OLIVE:SILVER:CLAY'),
	'CLAY_LOAM':('MAROON:GRAY:CLAY'),
	'SANDY_CLAY_LOAM':('SILVER:MAROON:SOIL'),
	'SILTY_CLAY_LOAM':('GRAY:MAROON:SOIL'),
	'LOAM':('RED:MAROON:SOIL'),
	'SANDY_LOAM':('OLIVE:MAROON:SOIL'),
	'SILT_LOAM':('TEAL:MAROON:SOIL'),
	'LOAMY_SAND':('MAROON:OLIVE:SOIL'),
	'SILT':('SILVER:OLIVE:SOIL'),
	'SAND_TAN':('SILVER:OLIVE:SAND'),
	'SAND_YELLOW':('YELLOW:OLIVE:SAND'),
	'SAND_WHITE':('WHITE:SILVER:SAND'),
	'SAND_BLACK':('BLACK:NAVY:SAND'),
	'SAND_RED':('RED:MAROON:SAND'),
	'PEAT':('BLACK:MAROON:SOIL'),
	'PELAGIC_CLAY':('SILVER:TEAL:OCEAN'),
	'CALCAREOUS_OOZE':('WHITE:TEAL:OCEAN'),
	'SILICEOUS_OOZE':('CYAN:TEAL:OCEAN'),
	'FIRE_CLAY':('RED:GRAY:CLAY')
}

#if foreround color is black, make basic color navy
#if both colors are the same, swap foreground color between silver/gray

# Real color of each rock type
real_color = {
	'BLACK':'BLACK',
	'NAVY':'NAVY',
	'GREEN':'GREEN',
	'TEAL':'TEAL',
	'MAROON':'MAROON',
	'PURPLE':'PURPLE',
	'OLIVE':'OLIVE',
	'SILVER':'SILVER',
	'GRAY':'GRAY',
	'BLUE':'BLUE',
	'LIME':'LIME',
	'CYAN':'CYAN',
	'RED':'RED',
	'PINK':'PINK',
	'YELLOW':'YELLOW',
	'WHITE':'WHITE',

	'NOTSAFE':'WHITE',
	'FIRESAFE':'SILVER',
	'MAGMASAFE':'GRAY',

	'FUEL':'BLACK',
	'IRON':'MAROON',
	'TIN':'BLACK',
	'LEAD':'GRAY',
	'ZINC':'SILVER',
	'NICKEL':'TEAL',
	'BISMUTH':'BLUE',
	'COPPER':'TEAL',
	'GOLD':'YELLOW',
	'ALUMINIUM':'WHITE',
	'PLATINUM':'WHITE',
	'ADAMANTINE':'CYAN'
}

regex = re.compile('\[INORGANIC:(.+)\]')
os.makedirs(os.path.dirname('../objects_patch/'), exist_ok=True)
for inname in ('inorganic_stone_gem.txt', 'inorganic_stone_layer.txt', 'inorganic_stone_mineral.txt', 'inorganic_stone_soil.txt'):
	stonelist = []
	with open('objects/' + inname, 'r') as infile:
		intext = infile.read()
		stonelist = regex.findall(intext)

	with open('../objects_patch/' + inname, encoding='utf-8', mode='w') as outfile:
		for name in stonelist:

			stone = stone_data[name].split(':')
			fg = real_color[stone[0]]
			bg = real_color[stone[1]]
			color = 'NAVY' if fg == 'BLACK' else fg
			tile = stone[2]
			outfile.write('[INORGANIC:%s]\n' % name)
			outfile.write('\t[TILE_COLOR:%s:%s:0]\n' % (fg, bg))
			outfile.write('\t[DISPLAY_COLOR:%s:%s:0]\n' % (fg, bg))
			outfile.write('\t[BUILD_COLOR:GRAY:0:0]\n')
			outfile.write('\t[BASIC_COLOR:%s:0]\n' % color)
			outfile.write('\t[TILE:ROCKTILE_%s]\n' % (tile))
			outfile.write('\t[ITEM_SYMBOL:ROCKITEM_%s]\n' % (tile))