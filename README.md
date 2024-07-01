# Blueprint materials checker

A script for checking the number of materials needed for a blueprint in Space Engineers.

```json
{
  "blocks": {
    "SmallBlockLargeFlatAtmosphericThrustDShapeZZZ": 1,
    "SmallBlockSmallFlatAtmosphericThrust": 10,
    "SmallBlockArmorSlope2Tip": 6,
    "SmallBlockSmallGenerator": 1,
  },
  "components": {
    "SteelPlate": 175,
    "Construction": 262,
    "LargeTube": 18
  },
  "unknown_blocks": [
    "SmallBlockLargeFlatAtmosphericThrustDShapeZZZ"
  ]
}
```

## Blocks

Blocks are defined in .sbc (xml format) files, multiple blocks can be defined in a single file.

The scraper script will iterate through all of these files and compile a list of all the blocks it finds.

```xml
<Definitions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
             xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    <CubeBlocks>
        <Definition>
            <Id>
                <TypeId>CubeBlock</TypeId>
                <SubtypeId>LargeBlockArmorBlock</SubtypeId>
            </Id>
            <DisplayName>DisplayName_Block_LightArmorBlock</DisplayName>
            <Icon>Textures\GUI\Icons\Cubes\light_armor_cube.dds</Icon>
            <Description>Description_LightArmor</Description>
    ...
```

Blocks are indexed using their TypeId first, then SubtypeId and DisplayName. If a block does not have a SubtypeId defined, then the TypeId will be used instead.

If you have any custom blocks, as long as they are defined in the same format and saved in the same location, then they should just work. Full support for modded and custom blocks is coming soon.

## Configuration

In `config.yaml` specify the location of your Space Engineers cube data directory and the drive it lives on. You can also pick from logging options.

```yaml
se_path: "F:/Steam/steamapps/common/SpaceEngineers/Content"
mods_path: "F:/Steam/steamapps/workshop/content/244850"
logger:
  handlers:
    stream:
      level: INFO
      bubble: false
#    timed_rotating_file:
#      level: INFO
#      bubble: true
#      date_format: "%Y-%m-%d_%H:%M:%S"
```

## Command line

If you like to use the command line:

```commandline
    usage: check_mats.py [-h] -f FILE [-c [CONFIG]] [-mb | --modded-blocks]
    
    Determine the blocks that make up a blueprint
    
    options:
      -h, --help                      show this help message and exit
      -f FILE, --file FILE            a blueprint to check
      -c [CONFIG], --config [CONFIG]  override config.yaml with another, better yaml file
      -mb, --modded-blocks            load modded blocks from mods path
```

Remember you will still need to have set the paths in the config for this to work.

## To do

* Display component materials estimates
* Configurable production pipeline
* Turn this into an engine and add a lovely frontend

## Dependencies

* PyYAML==6.0.1
* Logbook==1.7.0.post0
* pytest==7.4.4
