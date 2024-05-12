# Blueprint materials checker

A script for checking the number of materials needed for a blueprint in Space Engineers.

```json
{
  "blocks": {
    "SmallBlockLargeFlatAtmosphericThrustDShape": 2,
    "SmallBlockSmallFlatAtmosphericThrust": 10,
    "SmallBlockArmorSlope2Tip": 6,
    "SmallBlockSmallGenerator": 1,
    "SmallBlockGyro": 1,
    "SmallBlockBatteryBlock": 2,
    "SmallBlockRadioAntenna": 1,
    "SmallBlockCockpit": 1,
    "ConnectorMedium": 1,
    "SmallBlockArmorBlock": 2,
    "SmallControlPanel": 1,
    "SmallBlockSmallAtmosphericThrustSciFi": 4,
    "HalfSlopeArmorBlock": 8,
    "SmallBlockArmorCorner2Tip": 4,
    "SmallBlockArmorHalfCorner": 2,
    "HalfArmorBlock": 2
  }
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
se_path: "/Steam/steamapps/common/SpaceEngineers/Content/Data/CubeBlocks"
drive: "F:"
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
usage: check_mats.py [-h] [-c [CONFIG]]

Determine the blocks that make up a blueprint

options:
  -h, --help                        show this help message and exit
  -c [CONFIG], --config [CONFIG]    override config.yaml with another, better yaml file
```

Remember you will still need to have set the paths in the config for this to work.

## To do

* Custom/modded block support
* Required components output

## Dependencies

* PyYAML==6.0.1
* Logbook==1.7.0.post0
