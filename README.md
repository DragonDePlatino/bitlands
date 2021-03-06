### [Forum Thread](http://www.bay12forums.com/smf/index.php?topic=172607.0)

Bitlands is a tileset for the game [Dwarf Fortress](http://bay12games.com/dwarves/) that completely overhauls the graphics while preserving the ASCII aesthetics. This repo contains all of images, raws and configuration files necessary to run the tileset. It also contains the Python scripts used to generate these files and a large collection of graphics that went unused in the final version. Note that you will need a patching program called DFPatch to install these files, which can be found [here](https://github.com/DragonDePlatino/dfpatch/releases/latest).

## Users

If you're just here for the tileset, browse our [releases](https://github.com/DragonDePlatino/bitlands/releases/latest) for the complete package including DFPatch.

## Contributors

If you would like to contribute, please make any proposed changes to the Python scripts rather than the machine-generated files. We would like to keep Bitlands clean and maintainable for future versions instead of hand-editing the final files.

## Build from source

Run the [python scripts](./scripts) after you copy a DwarfFortress `raw/objects` folder into `./scripts`.
The scripts must be started in with `./scripts` as the current working directory.
The output is put in the root of the repository.

To install the tileset, run make and copy [DFPatch](https://github.com/DragonDePlatino/dfpatch) into the repository root.
Copy/move the repository root next to your DwarfFortress installation and run DFPatch.

Example folder layout:

+ DwarfFortress
    + raw
    + data
    + dfhack(.exe)
    + ...
    + bitlands
        + dfpatch(.exe)
        + scripts
        + info.txt
        + defines.txt
        + init
        + init_patch
        + ...
