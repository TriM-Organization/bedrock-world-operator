import nbtlib
import time as Time
from dataclasses import dataclass, field


@dataclass
class Abilities:
    attack_mobs: bool = True
    attack_players: bool = True
    build: bool = True
    mine: bool = True
    doors_and_switches: bool = True
    fly_speed: float = 0.05
    flying: bool = False
    instant_build: bool = False
    invulnerable: bool = False
    lightning: bool = False
    mayFly: bool = False
    op: bool = False
    open_containers: bool = True
    permissions_level: int = 0
    player_permissions_level: int = 1
    teleport: bool = False
    walk_speed: float = 0.1
    verticalFly_speed: float = 1.0

    def marshal(self) -> nbtlib.tag.Compound:
        """marshal encode abilities to its NBT represent

        Returns:
            Compound: The NBT represents of abilities
        """
        return nbtlib.tag.Compound(
            {
                "attackmobs": nbtlib.tag.Byte(self.attack_mobs),
                "attackplayers": nbtlib.tag.Byte(self.attack_players),
                "build": nbtlib.tag.Byte(self.build),
                "mine": nbtlib.tag.Byte(self.mine),
                "doorsandswitches": nbtlib.tag.Byte(self.doors_and_switches),
                "flySpeed": nbtlib.tag.Float(self.fly_speed),
                "flying": nbtlib.tag.Byte(self.flying),
                "instabuild": nbtlib.tag.Byte(self.instant_build),
                "invulnerable": nbtlib.tag.Byte(self.invulnerable),
                "lightning": nbtlib.tag.Byte(self.lightning),
                "mayfly": nbtlib.tag.Byte(self.mayFly),
                "op": nbtlib.tag.Byte(self.op),
                "opencontainers": nbtlib.tag.Byte(self.open_containers),
                "permissionsLevel": nbtlib.tag.Int(self.permissions_level),
                "playerPermissionsLevel": nbtlib.tag.Int(self.player_permissions_level),
                "teleport": nbtlib.tag.Byte(self.teleport),
                "walkSpeed": nbtlib.tag.Float(self.walk_speed),
                "verticalFlySpeed": nbtlib.tag.Float(self.verticalFly_speed),
            }
        )

    def unmarshal(self, compound: nbtlib.tag.Compound):
        """unmarshal read data from compound to initialize the field in abilities.

        Args:
            compound (nbtlib.tag.Compound): The given compound.
        """
        self.attack_mobs = bool(compound["attackmobs"])
        self.attack_players = bool(compound["attackplayers"])
        self.build = bool(compound["build"])
        self.mine = bool(compound["mine"])
        self.doors_and_switches = bool(compound["doorsandswitches"])
        self.fly_speed = float(compound["flySpeed"])
        self.flying = bool(compound["flying"])
        self.instant_build = bool(compound["instabuild"])
        self.invulnerable = bool(compound["invulnerable"])
        self.lightning = bool(compound["lightning"])
        self.mayFly = bool(compound["mayfly"])
        self.op = bool(compound["op"])
        self.open_containers = bool(compound["opencontainers"])
        self.permissions_level = int(compound["permissionsLevel"])
        self.player_permissions_level = int(compound["playerPermissionsLevel"])
        self.teleport = bool(compound["teleport"])
        self.walk_speed = float(compound["walkSpeed"])
        self.verticalFly_speed = float(compound["verticalFlySpeed"])


@dataclass
class LevelDat:
    """
    LevelDat holds a collection of data that
    specify a range of Settings of the world.

    These Settings usually alter the way that
    players interact with the world.

    The data held here is usually saved in a
    level.dat file of the world.
    """

    base_game_version: str = "*"
    biome_override: str = ""
    confirmed_platform_locked_content: bool = False
    center_maps_to_origin: bool = False
    cheats_enabled: bool = False
    daylight_cycle: int = 0
    difficulty: int = 2
    edu_offer: int = 0
    flat_world_layers: str = ""
    force_game_type: bool = False
    game_type: int = 1
    generator: int = 2
    inventory_version: str = "1.20.50"
    LANB_roadcast: bool = True
    LANB_roadcast_intent: bool = True
    last_played: int = 0
    level_name: str = "World"
    limited_world_origin_x: int = 0
    limited_world_origin_y: int = 32767
    limited_world_origin_z: int = 0
    limited_world_depth: int = 16
    limited_world_width: int = 16
    minimum_compatible_client_version: tuple[int, int, int, int, int] = (
        1,
        20,
        50,
        0,
        0,
    )
    multi_player_game: bool = True
    multi_player_game_intent: bool = True
    nether_scale: int = 8
    network_version: int = 630
    platform: int = 2
    platform_broadcast_intent: int = 3
    random_seed: int = field(default_factory=lambda: int(Time.time()))
    show_tags: bool = True
    single_use_world: bool = False
    spawn_x: int = 0
    spawn_y: int = 32767
    spawn_z: int = 0
    spawn_v1_villagers: bool = False
    storage_version: int = 9
    time: int = 0
    XBL_broadcast: bool = False
    XBL_broadcast_intent: int = 3
    XBL_broadcast_mode: int = 0
    abilities: Abilities = field(default_factory=lambda: Abilities())
    bonus_chest_enabled: bool = False
    bonus_chest_spawned: bool = False
    command_block_output: bool = True
    command_blocks_enabled: bool = True
    commands_enabled: bool = True
    current_tick: int = 0
    do_day_light_cycle: bool = True
    do_entity_drops: bool = True
    do_fire_tick: bool = True
    do_immediate_respawn: bool = False
    do_insomnia: bool = True
    do_mob_loot: bool = True
    do_mob_spawning: bool = True
    do_tile_drops: bool = True
    do_weather_cycle: bool = True
    drowning_damage: bool = True
    edu_level: bool = False
    education_features_enabled: bool = False
    experimental_game_play: bool = False
    fall_damage: bool = True
    fire_damage: bool = True
    function_command_limit: int = 10000
    has_been_loaded_in_creative: bool = True
    has_locked_behaviour_pack: bool = False
    has_locked_resource_pack: bool = False
    immutable_world: bool = False
    is_created_in_editor: bool = False
    is_exported_from_editor: bool = False
    is_from_locked_template: bool = False
    is_from_world_template: bool = False
    is_world_template_option_locked: bool = False
    keep_inventory: bool = False
    last_opened_with_version: tuple[int, int, int, int, int] = (1, 20, 50, 0, 0)
    lightning_level: float = 1.0
    lightning_time: int = 0
    max_command_chain_length: int = 65535
    mob_griefing: bool = True
    natural_regeneration: bool = True
    prid: str = ""
    pvp: bool = True
    rain_level: float = 1.0
    rain_time: int = 0
    random_tick_speed: int = 1
    requires_copied_pack_removal_check: bool = False
    send_command_feedback: bool = True
    server_chunk_tick_range: int = 6
    show_coordinates: bool = False
    show_death_messages: bool = True
    spawn_mobs: bool = True
    spawn_radius: int = 5
    start_with_map_enabled: bool = False
    texture_packs_required: bool = False
    tnt_explodes: bool = True
    use_msa_gamer_tags_only: bool = False
    world_start_count: int = 0
    experiments: nbtlib.tag.Compound = field(
        default_factory=lambda: nbtlib.tag.Compound()
    )
    freeze_damage: bool = True
    world_policies: nbtlib.tag.Compound = field(
        default_factory=lambda: nbtlib.tag.Compound()
    )
    world_version: int = 1
    respawn_blocks_explode: bool = True
    show_border_effect: bool = True
    permissions_level: int = 0
    player_permissions_level: int = 0
    is_random_seed_allowed: bool = False
    do_limited_crafting: bool = False
    editor_world_type: int = 0
    players_sleeping_percentage: int = 0
    recipes_unlock: bool = False
    natural_generation: bool = False
    projectiles_can_break_blocks: bool = False
    show_recipe_messages: bool = False
    is_hardcore: bool = False
    show_days_played: bool = False
    tnt_explosion_drop_decay: bool = False
    has_uncomplete_world_file_on_disk: bool = False
    player_has_died: bool = False

    def marshal(self) -> nbtlib.tag.Compound:
        """marshal encode level dat to its NBT represent

        Returns:
            Compound: The NBT represent of level dat
        """
        return nbtlib.tag.Compound(
            {
                "baseGameVersion": nbtlib.tag.String(self.base_game_version),
                "BiomeOverride": nbtlib.tag.String(self.biome_override),
                "ConfirmedPlatformLockedContent": nbtlib.tag.Byte(
                    self.confirmed_platform_locked_content
                ),
                "CenterMapsToOrigin": nbtlib.tag.Byte(self.center_maps_to_origin),
                "cheatsEnabled": nbtlib.tag.Byte(self.cheats_enabled),
                "daylightCycle": nbtlib.tag.Int(self.daylight_cycle),
                "Difficulty": nbtlib.tag.Int(self.difficulty),
                "eduOffer": nbtlib.tag.Int(self.edu_offer),
                "FlatWorldLayers": nbtlib.tag.String(self.flat_world_layers),
                "ForceGameType": nbtlib.tag.Byte(self.force_game_type),
                "GameType": nbtlib.tag.Int(self.game_type),
                "Generator": nbtlib.tag.Int(self.generator),
                "InventoryVersion": nbtlib.tag.String(self.inventory_version),
                "LANBroadcast": nbtlib.tag.Byte(self.LANB_roadcast),
                "LANBroadcastIntent": nbtlib.tag.Byte(self.LANB_roadcast_intent),
                "LastPlayed": nbtlib.tag.Long(self.last_played),
                "LevelName": nbtlib.tag.String(self.level_name),
                "LimitedWorldOriginX": nbtlib.tag.Int(self.limited_world_origin_x),
                "LimitedWorldOriginY": nbtlib.tag.Int(self.limited_world_origin_y),
                "LimitedWorldOriginZ": nbtlib.tag.Int(self.limited_world_origin_z),
                "limitedWorldDepth": nbtlib.tag.Int(self.limited_world_depth),
                "limitedWorldWidth": nbtlib.tag.Int(self.limited_world_width),
                "MinimumCompatibleClientVersion": nbtlib.tag.List(
                    [
                        nbtlib.tag.Int(self.minimum_compatible_client_version[0]),
                        nbtlib.tag.Int(self.minimum_compatible_client_version[1]),
                        nbtlib.tag.Int(self.minimum_compatible_client_version[2]),
                        nbtlib.tag.Int(self.minimum_compatible_client_version[3]),
                        nbtlib.tag.Int(self.minimum_compatible_client_version[4]),
                    ]
                ),
                "MultiplayerGame": nbtlib.tag.Byte(self.multi_player_game),
                "MultiplayerGameIntent": nbtlib.tag.Byte(self.multi_player_game_intent),
                "NetherScale": nbtlib.tag.Int(self.nether_scale),
                "NetworkVersion": nbtlib.tag.Int(self.network_version),
                "Platform": nbtlib.tag.Int(self.platform),
                "PlatformBroadcastIntent": nbtlib.tag.Int(
                    self.platform_broadcast_intent
                ),
                "RandomSeed": nbtlib.tag.Long(self.random_seed),
                "showtags": nbtlib.tag.Byte(self.show_tags),
                "isSingleUseWorld": nbtlib.tag.Byte(self.single_use_world),
                "SpawnX": nbtlib.tag.Int(self.spawn_x),
                "SpawnY": nbtlib.tag.Int(self.spawn_y),
                "SpawnZ": nbtlib.tag.Int(self.spawn_z),
                "SpawnV1Villagers": nbtlib.tag.Byte(self.spawn_v1_villagers),
                "StorageVersion": nbtlib.tag.Int(self.storage_version),
                "Time": nbtlib.tag.Long(self.time),
                "XBLBroadcast": nbtlib.tag.Byte(self.XBL_broadcast),
                "XBLBroadcastIntent": nbtlib.tag.Int(self.XBL_broadcast_intent),
                "XBLBroadcastMode": nbtlib.tag.Int(self.XBL_broadcast_mode),
                "abilities": self.abilities.marshal(),
                "bonusChestEnabled": nbtlib.tag.Byte(self.bonus_chest_enabled),
                "bonusChestSpawned": nbtlib.tag.Byte(self.bonus_chest_spawned),
                "commandblockoutput": nbtlib.tag.Byte(self.command_block_output),
                "commandblocksenabled": nbtlib.tag.Byte(self.command_blocks_enabled),
                "commandsEnabled": nbtlib.tag.Byte(self.commands_enabled),
                "currentTick": nbtlib.tag.Long(self.current_tick),
                "dodaylightcycle": nbtlib.tag.Byte(self.do_day_light_cycle),
                "doentitydrops": nbtlib.tag.Byte(self.do_entity_drops),
                "dofiretick": nbtlib.tag.Byte(self.do_fire_tick),
                "doimmediaterespawn": nbtlib.tag.Byte(self.do_immediate_respawn),
                "doinsomnia": nbtlib.tag.Byte(self.do_insomnia),
                "domobloot": nbtlib.tag.Byte(self.do_mob_loot),
                "domobspawning": nbtlib.tag.Byte(self.do_mob_spawning),
                "dotiledrops": nbtlib.tag.Byte(self.do_tile_drops),
                "doweathercycle": nbtlib.tag.Byte(self.do_weather_cycle),
                "drowningdamage": nbtlib.tag.Byte(self.drowning_damage),
                "eduLevel": nbtlib.tag.Byte(self.edu_level),
                "educationFeaturesEnabled": nbtlib.tag.Byte(
                    self.education_features_enabled
                ),
                "experimentalgameplay": nbtlib.tag.Byte(self.experimental_game_play),
                "falldamage": nbtlib.tag.Byte(self.fall_damage),
                "firedamage": nbtlib.tag.Byte(self.fire_damage),
                "functioncommandlimit": nbtlib.tag.Int(self.function_command_limit),
                "hasBeenLoadedInCreative": nbtlib.tag.Byte(
                    self.has_been_loaded_in_creative
                ),
                "hasLockedBehaviorPack": nbtlib.tag.Byte(
                    self.has_locked_behaviour_pack
                ),
                "hasLockedResourcePack": nbtlib.tag.Byte(self.has_locked_resource_pack),
                "immutableWorld": nbtlib.tag.Byte(self.immutable_world),
                "isCreatedInEditor": nbtlib.tag.Byte(self.is_created_in_editor),
                "isExportedFromEditor": nbtlib.tag.Byte(self.is_exported_from_editor),
                "isFromLockedTemplate": nbtlib.tag.Byte(self.is_from_locked_template),
                "isFromWorldTemplate": nbtlib.tag.Byte(self.is_from_world_template),
                "isWorldTemplateOptionLocked": nbtlib.tag.Byte(
                    self.is_world_template_option_locked
                ),
                "keepinventory": nbtlib.tag.Byte(self.keep_inventory),
                "lastOpenedWithVersion": nbtlib.tag.List(
                    [
                        nbtlib.tag.Int(self.last_opened_with_version[0]),
                        nbtlib.tag.Int(self.last_opened_with_version[1]),
                        nbtlib.tag.Int(self.last_opened_with_version[2]),
                        nbtlib.tag.Int(self.last_opened_with_version[3]),
                        nbtlib.tag.Int(self.last_opened_with_version[4]),
                    ]
                ),
                "lightningLevel": nbtlib.tag.Float(self.lightning_level),
                "lightningTime": nbtlib.tag.Int(self.lightning_time),
                "maxcommandchainlength": nbtlib.tag.Int(self.max_command_chain_length),
                "mobgriefing": nbtlib.tag.Byte(self.mob_griefing),
                "naturalregeneration": nbtlib.tag.Byte(self.natural_regeneration),
                "prid": nbtlib.tag.String(self.prid),
                "pvp": nbtlib.tag.Byte(self.pvp),
                "rainLevel": nbtlib.tag.Float(self.rain_level),
                "rainTime": nbtlib.tag.Int(self.rain_time),
                "randomtickspeed": nbtlib.tag.Int(self.random_tick_speed),
                "requiresCopiedPackRemovalCheck": nbtlib.tag.Byte(
                    self.requires_copied_pack_removal_check
                ),
                "sendcommandfeedback": nbtlib.tag.Byte(self.send_command_feedback),
                "serverChunkTickRange": nbtlib.tag.Int(self.server_chunk_tick_range),
                "showcoordinates": nbtlib.tag.Byte(self.show_coordinates),
                "showdeathmessages": nbtlib.tag.Byte(self.show_death_messages),
                "spawnMobs": nbtlib.tag.Byte(self.spawn_mobs),
                "spawnradius": nbtlib.tag.Int(self.spawn_radius),
                "startWithMapEnabled": nbtlib.tag.Byte(self.start_with_map_enabled),
                "texturePacksRequired": nbtlib.tag.Byte(self.texture_packs_required),
                "tntexplodes": nbtlib.tag.Byte(self.tnt_explodes),
                "useMsaGamertagsOnly": nbtlib.tag.Byte(self.use_msa_gamer_tags_only),
                "worldStartCount": nbtlib.tag.Long(self.world_start_count),
                "experiments": self.experiments,
                "freezedamage": nbtlib.tag.Byte(self.freeze_damage),
                "world_policies": self.world_policies,
                "WorldVersion": nbtlib.tag.Int(self.world_version),
                "respawnblocksexplode": nbtlib.tag.Byte(self.respawn_blocks_explode),
                "showbordereffect": nbtlib.tag.Byte(self.show_border_effect),
                "permissionsLevel": nbtlib.tag.Int(self.permissions_level),
                "playerPermissionsLevel": nbtlib.tag.Int(self.player_permissions_level),
                "isRandomSeedAllowed": nbtlib.tag.Byte(self.is_random_seed_allowed),
                "dolimitedcrafting": nbtlib.tag.Byte(self.do_limited_crafting),
                "editorWorldType": nbtlib.tag.Int(self.editor_world_type),
                "playerssleepingpercentage": nbtlib.tag.Int(
                    self.players_sleeping_percentage
                ),
                "recipesunlock": nbtlib.tag.Byte(self.recipes_unlock),
                "naturalgeneration": nbtlib.tag.Byte(self.natural_generation),
                "projectilescanbreakblocks": nbtlib.tag.Byte(
                    self.projectiles_can_break_blocks
                ),
                "showrecipemessages": nbtlib.tag.Byte(self.show_recipe_messages),
                "IsHardcore": nbtlib.tag.Byte(self.is_hardcore),
                "showdaysplayed": nbtlib.tag.Byte(self.show_days_played),
                "tntexplosiondropdecay": nbtlib.tag.Byte(self.tnt_explosion_drop_decay),
                "HasUncompleteWorldFileOnDisk": nbtlib.tag.Byte(
                    self.has_uncomplete_world_file_on_disk
                ),
                "PlayerHasDied": nbtlib.tag.Byte(self.player_has_died),
            }
        )

    def unmarshal(self, compound: nbtlib.tag.Compound):
        """unmarshal read data from compound to initialize the field in level dat.

        Args:
            compound (nbtlib.tag.Compound): The given compound.
        """
        self.base_game_version = str(compound["baseGameVersion"])
        self.biome_override = str(compound["BiomeOverride"])
        self.confirmed_platform_locked_content = bool(
            compound["ConfirmedPlatformLockedContent"]
        )
        self.center_maps_to_origin = bool(compound["CenterMapsToOrigin"])
        self.cheats_enabled = bool(compound["cheatsEnabled"])
        self.daylight_cycle = int(compound["daylightCycle"])
        self.difficulty = int(compound["Difficulty"])
        self.edu_offer = int(compound["eduOffer"])
        self.flat_world_layers = str(compound["FlatWorldLayers"])
        self.force_game_type = bool(compound["ForceGameType"])
        self.game_type = int(compound["GameType"])
        self.generator = int(compound["Generator"])
        self.inventory_version = str(compound["InventoryVersion"])
        self.LANB_roadcast = bool(compound["LANBroadcast"])
        self.LANB_roadcast_intent = bool(compound["LANBroadcastIntent"])
        self.last_played = int(compound["LastPlayed"])
        self.level_name = str(compound["LevelName"])
        self.limited_world_origin_x = int(compound["LimitedWorldOriginX"])
        self.limited_world_origin_y = int(compound["LimitedWorldOriginY"])
        self.limited_world_origin_z = int(compound["LimitedWorldOriginZ"])
        self.limited_world_depth = int(compound["limitedWorldDepth"])
        self.limited_world_width = int(compound["limitedWorldWidth"])
        self.minimum_compatible_client_version = (
            int(compound["MinimumCompatibleClientVersion"][0]),
            int(compound["MinimumCompatibleClientVersion"][1]),
            int(compound["MinimumCompatibleClientVersion"][2]),
            int(compound["MinimumCompatibleClientVersion"][3]),
            int(compound["MinimumCompatibleClientVersion"][4]),
        )
        self.multi_player_game = bool(compound["MultiplayerGame"])
        self.multi_player_game_intent = bool(compound["MultiplayerGameIntent"])
        self.nether_scale = int(compound["NetherScale"])
        self.network_version = int(compound["NetworkVersion"])
        self.platform = int(compound["Platform"])
        self.platform_broadcast_intent = int(compound["PlatformBroadcastIntent"])
        self.random_seed = int(compound["RandomSeed"])
        self.show_tags = bool(compound["showtags"])
        self.single_use_world = bool(compound["isSingleUseWorld"])
        self.spawn_x = int(compound["SpawnX"])
        self.spawn_y = int(compound["SpawnY"])
        self.spawn_z = int(compound["SpawnZ"])
        self.spawn_v1_villagers = bool(compound["SpawnV1Villagers"])
        self.storage_version = int(compound["StorageVersion"])
        self.time = int(compound["Time"])
        self.XBL_broadcast = bool(compound["XBLBroadcast"])
        self.XBL_broadcast_intent = int(compound["XBLBroadcastIntent"])
        self.XBL_broadcast_mode = int(compound["XBLBroadcastMode"])
        self.abilities.unmarshal(compound["abilities"])
        self.bonus_chest_enabled = bool(compound["bonusChestEnabled"])
        self.bonus_chest_spawned = bool(compound["bonusChestSpawned"])
        self.command_block_output = bool(compound["commandblockoutput"])
        self.command_blocks_enabled = bool(compound["commandblocksenabled"])
        self.commands_enabled = bool(compound["commandsEnabled"])
        self.current_tick = int(compound["currentTick"])
        self.do_day_light_cycle = bool(compound["dodaylightcycle"])
        self.do_entity_drops = bool(compound["doentitydrops"])
        self.do_fire_tick = bool(compound["dofiretick"])
        self.do_immediate_respawn = bool(compound["doimmediaterespawn"])
        self.do_insomnia = bool(compound["doinsomnia"])
        self.do_mob_loot = bool(compound["domobloot"])
        self.do_mob_spawning = bool(compound["domobspawning"])
        self.do_tile_drops = bool(compound["dotiledrops"])
        self.do_weather_cycle = bool(compound["doweathercycle"])
        self.drowning_damage = bool(compound["drowningdamage"])
        self.edu_level = bool(compound["eduLevel"])
        self.education_features_enabled = bool(compound["educationFeaturesEnabled"])
        self.experimental_game_play = bool(compound["experimentalgameplay"])
        self.fall_damage = bool(compound["falldamage"])
        self.fire_damage = bool(compound["firedamage"])
        self.function_command_limit = int(compound["functioncommandlimit"])
        self.has_been_loaded_in_creative = bool(compound["hasBeenLoadedInCreative"])
        self.has_locked_behaviour_pack = bool(compound["hasLockedBehaviorPack"])
        self.has_locked_resource_pack = bool(compound["hasLockedResourcePack"])
        self.immutable_world = bool(compound["immutableWorld"])
        self.is_created_in_editor = bool(compound["isCreatedInEditor"])
        self.is_exported_from_editor = bool(compound["isExportedFromEditor"])
        self.is_from_locked_template = bool(compound["isFromLockedTemplate"])
        self.is_from_world_template = bool(compound["isFromWorldTemplate"])
        self.is_world_template_option_locked = bool(
            compound["isWorldTemplateOptionLocked"]
        )
        self.keep_inventory = bool(compound["keepinventory"])
        self.last_opened_with_version = (
            int(compound["lastOpenedWithVersion"][0]),
            int(compound["lastOpenedWithVersion"][1]),
            int(compound["lastOpenedWithVersion"][2]),
            int(compound["lastOpenedWithVersion"][3]),
            int(compound["lastOpenedWithVersion"][4]),
        )
        self.lightning_level = float(compound["lightningLevel"])
        self.lightning_time = int(compound["lightningTime"])
        self.max_command_chain_length = int(compound["maxcommandchainlength"])
        self.mob_griefing = bool(compound["mobgriefing"])
        self.natural_regeneration = bool(compound["naturalregeneration"])
        self.prid = str(compound["prid"])
        self.pvp = bool(compound["pvp"])
        self.rain_level = float(compound["rainLevel"])
        self.rain_time = int(compound["rainTime"])
        self.random_tick_speed = int(compound["randomtickspeed"])
        self.requires_copied_pack_removal_check = bool(
            compound["requiresCopiedPackRemovalCheck"]
        )
        self.send_command_feedback = bool(compound["sendcommandfeedback"])
        self.server_chunk_tick_range = int(compound["serverChunkTickRange"])
        self.show_coordinates = bool(compound["showcoordinates"])
        self.show_death_messages = bool(compound["showdeathmessages"])
        self.spawn_mobs = bool(compound["spawnMobs"])
        self.spawn_radius = int(compound["spawnradius"])
        self.start_with_map_enabled = bool(compound["startWithMapEnabled"])
        self.texture_packs_required = bool(compound["texturePacksRequired"])
        self.tnt_explodes = bool(compound["tntexplodes"])
        self.use_msa_gamer_tags_only = bool(compound["useMsaGamertagsOnly"])
        self.world_start_count = int(compound["worldStartCount"])
        self.experiments = compound["experiments"]
        self.freeze_damage = bool(compound["freezedamage"])
        self.world_policies = compound["world_policies"]
        self.world_version = int(compound["WorldVersion"])
        self.respawn_blocks_explode = bool(compound["respawnblocksexplode"])
        self.show_border_effect = bool(compound["showbordereffect"])
        self.permissions_level = int(compound["permissionsLevel"])
        self.player_permissions_level = int(compound["playerPermissionsLevel"])
        self.is_random_seed_allowed = bool(compound["isRandomSeedAllowed"])
        self.do_limited_crafting = bool(compound["dolimitedcrafting"])
        self.editor_world_type = int(compound["editorWorldType"])
        self.players_sleeping_percentage = int(compound["playerssleepingpercentage"])
        self.recipes_unlock = bool(compound["recipesunlock"])
        self.natural_generation = bool(compound["naturalgeneration"])
        self.projectiles_can_break_blocks = bool(compound["projectilescanbreakblocks"])
        self.show_recipe_messages = bool(compound["showrecipemessages"])
        self.is_hardcore = bool(compound["IsHardcore"])
        self.show_days_played = bool(compound["showdaysplayed"])
        self.tnt_explosion_drop_decay = bool(compound["tntexplosiondropdecay"])
        self.has_uncomplete_world_file_on_disk = bool(
            compound["HasUncompleteWorldFileOnDisk"]
        )
        self.player_has_died = bool(compound["PlayerHasDied"])
