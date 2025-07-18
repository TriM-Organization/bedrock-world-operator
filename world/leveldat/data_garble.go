//go:build garble

package leveldat

import (
	"math"
	"time"

	block_general "github.com/TriM-Organization/bedrock-world-operator/block/general"
	"github.com/sandertv/gophertunnel/minecraft/protocol"
)

// Data holds a collection of data that specify a range of Settings of the
// world. These Settings usually alter the way that players interact with the
// world. The data held here is usually saved in a level.dat file of the world.
// Data may be used in LevelDat.Unmarshal to collect the data of the level.dat.
type Data struct {
	BaseGameVersion                string  `nbt:"baseGameVersion"`
	BiomeOverride                  string  `nbt:"BiomeOverride"`
	ConfirmedPlatformLockedContent bool    `nbt:"ConfirmedPlatformLockedContent"`
	CenterMapsToOrigin             bool    `nbt:"CenterMapsToOrigin"`
	CheatsEnabled                  bool    `nbt:"cheatsEnabled"`
	DaylightCycle                  int32   `nbt:"daylightCycle"`
	Difficulty                     int32   `nbt:"Difficulty"`
	EduOffer                       int32   `nbt:"eduOffer"`
	FlatWorldLayers                string  `nbt:"FlatWorldLayers"`
	ForceGameType                  bool    `nbt:"ForceGameType"`
	GameType                       int32   `nbt:"GameType"`
	Generator                      int32   `nbt:"Generator"`
	InventoryVersion               string  `nbt:"InventoryVersion"`
	LANBroadcast                   bool    `nbt:"LANBroadcast"`
	LANBroadcastIntent             bool    `nbt:"LANBroadcastIntent"`
	LastPlayed                     int64   `nbt:"LastPlayed"`
	LevelName                      string  `nbt:"LevelName"`
	LimitedWorldOriginX            int32   `nbt:"LimitedWorldOriginX"`
	LimitedWorldOriginY            int32   `nbt:"LimitedWorldOriginY"`
	LimitedWorldOriginZ            int32   `nbt:"LimitedWorldOriginZ"`
	LimitedWorldDepth              int32   `nbt:"limitedWorldDepth"`
	LimitedWorldWidth              int32   `nbt:"limitedWorldWidth"`
	MinimumCompatibleClientVersion []int32 `nbt:"MinimumCompatibleClientVersion"`
	MultiPlayerGame                bool    `nbt:"MultiplayerGame"`
	MultiPlayerGameIntent          bool    `nbt:"MultiplayerGameIntent"`
	NetherScale                    int32   `nbt:"NetherScale"`
	NetworkVersion                 int32   `nbt:"NetworkVersion"`
	Platform                       int32   `nbt:"Platform"`
	PlatformBroadcastIntent        int32   `nbt:"PlatformBroadcastIntent"`
	RandomSeed                     int64   `nbt:"RandomSeed"`
	ShowTags                       bool    `nbt:"showtags"`
	SingleUseWorld                 bool    `nbt:"isSingleUseWorld"`
	SpawnX                         int32   `nbt:"SpawnX"`
	SpawnY                         int32   `nbt:"SpawnY"`
	SpawnZ                         int32   `nbt:"SpawnZ"`
	SpawnV1Villagers               bool    `nbt:"SpawnV1Villagers"`
	StorageVersion                 int32   `nbt:"StorageVersion"`
	Time                           int64   `nbt:"Time"`
	XBLBroadcast                   bool    `nbt:"XBLBroadcast"`
	XBLBroadcastIntent             int32   `nbt:"XBLBroadcastIntent"`
	XBLBroadcastMode               int32   `nbt:"XBLBroadcastMode"`
	Abilities                      struct {
		AttackMobs             bool    `nbt:"attackmobs"`
		AttackPlayers          bool    `nbt:"attackplayers"`
		Build                  bool    `nbt:"build"`
		Mine                   bool    `nbt:"mine"`
		DoorsAndSwitches       bool    `nbt:"doorsandswitches"`
		FlySpeed               float32 `nbt:"flySpeed"`
		Flying                 bool    `nbt:"flying"`
		InstantBuild           bool    `nbt:"instabuild"`
		Invulnerable           bool    `nbt:"invulnerable"`
		Lightning              bool    `nbt:"lightning"`
		MayFly                 bool    `nbt:"mayfly"`
		OP                     bool    `nbt:"op"`
		OpenContainers         bool    `nbt:"opencontainers"`
		PermissionsLevel       int32   `nbt:"permissionsLevel"`
		PlayerPermissionsLevel int32   `nbt:"playerPermissionsLevel"`
		Teleport               bool    `nbt:"teleport"`
		WalkSpeed              float32 `nbt:"walkSpeed"`
		VerticalFlySpeed       float32 `nbt:"verticalFlySpeed"`
	} `nbt:"abilities"`
	BonusChestEnabled               bool           `nbt:"bonusChestEnabled"`
	BonusChestSpawned               bool           `nbt:"bonusChestSpawned"`
	CommandBlockOutput              bool           `nbt:"commandblockoutput"`
	CommandBlocksEnabled            bool           `nbt:"commandblocksenabled"`
	CommandsEnabled                 bool           `nbt:"commandsEnabled"`
	CurrentTick                     int64          `nbt:"currentTick"`
	DoDayLightCycle                 bool           `nbt:"dodaylightcycle"`
	DoEntityDrops                   bool           `nbt:"doentitydrops"`
	DoFireTick                      bool           `nbt:"dofiretick"`
	DoImmediateRespawn              bool           `nbt:"doimmediaterespawn"`
	DoInsomnia                      bool           `nbt:"doinsomnia"`
	DoMobLoot                       bool           `nbt:"domobloot"`
	DoMobSpawning                   bool           `nbt:"domobspawning"`
	DoTileDrops                     bool           `nbt:"dotiledrops"`
	DoWeatherCycle                  bool           `nbt:"doweathercycle"`
	DrowningDamage                  bool           `nbt:"drowningdamage"`
	EduLevel                        bool           `nbt:"eduLevel"`
	EducationFeaturesEnabled        bool           `nbt:"educationFeaturesEnabled"`
	ExperimentalGamePlay            bool           `nbt:"experimentalgameplay"`
	FallDamage                      bool           `nbt:"falldamage"`
	FireDamage                      bool           `nbt:"firedamage"`
	FunctionCommandLimit            int32          `nbt:"functioncommandlimit"`
	HasBeenLoadedInCreative         bool           `nbt:"hasBeenLoadedInCreative"`
	HasLockedBehaviourPack          bool           `nbt:"hasLockedBehaviorPack"`
	HasLockedResourcePack           bool           `nbt:"hasLockedResourcePack"`
	ImmutableWorld                  bool           `nbt:"immutableWorld"`
	IsCreatedInEditor               bool           `nbt:"isCreatedInEditor"`
	IsExportedFromEditor            bool           `nbt:"isExportedFromEditor"`
	IsFromLockedTemplate            bool           `nbt:"isFromLockedTemplate"`
	IsFromWorldTemplate             bool           `nbt:"isFromWorldTemplate"`
	IsWorldTemplateOptionLocked     bool           `nbt:"isWorldTemplateOptionLocked"`
	KeepInventory                   bool           `nbt:"keepinventory"`
	LastOpenedWithVersion           []int32        `nbt:"lastOpenedWithVersion"`
	LightningLevel                  float32        `nbt:"lightningLevel"`
	LightningTime                   int32          `nbt:"lightningTime"`
	MaxCommandChainLength           int32          `nbt:"maxcommandchainlength"`
	MobGriefing                     bool           `nbt:"mobgriefing"`
	NaturalRegeneration             bool           `nbt:"naturalregeneration"`
	PRID                            string         `nbt:"prid"`
	PVP                             bool           `nbt:"pvp"`
	RainLevel                       float32        `nbt:"rainLevel"`
	RainTime                        int32          `nbt:"rainTime"`
	RandomTickSpeed                 int32          `nbt:"randomtickspeed"`
	RequiresCopiedPackRemovalCheck  bool           `nbt:"requiresCopiedPackRemovalCheck"`
	SendCommandFeedback             bool           `nbt:"sendcommandfeedback"`
	ServerChunkTickRange            int32          `nbt:"serverChunkTickRange"`
	ShowCoordinates                 bool           `nbt:"showcoordinates"`
	ShowDeathMessages               bool           `nbt:"showdeathmessages"`
	SpawnMobs                       bool           `nbt:"spawnMobs"`
	SpawnRadius                     int32          `nbt:"spawnradius"`
	StartWithMapEnabled             bool           `nbt:"startWithMapEnabled"`
	TexturePacksRequired            bool           `nbt:"texturePacksRequired"`
	TNTExplodes                     bool           `nbt:"tntexplodes"`
	UseMSAGamerTagsOnly             bool           `nbt:"useMsaGamertagsOnly"`
	WorldStartCount                 int64          `nbt:"worldStartCount"`
	Experiments                     map[string]any `nbt:"experiments"`
	FreezeDamage                    bool           `nbt:"freezedamage"`
	WorldPolicies                   map[string]any `nbt:"world_policies"`
	WorldVersion                    int32          `nbt:"WorldVersion"`
	RespawnBlocksExplode            bool           `nbt:"respawnblocksexplode"`
	ShowBorderEffect                bool           `nbt:"showbordereffect"`
	PermissionsLevel                int32          `nbt:"permissionsLevel"`
	PlayerPermissionsLevel          int32          `nbt:"playerPermissionsLevel"`
	IsRandomSeedAllowed             bool           `nbt:"isRandomSeedAllowed"`
	DoLimitedCrafting               bool           `nbt:"dolimitedcrafting"`
	EditorWorldType                 int32          `nbt:"editorWorldType"`
	PlayersSleepingPercentage       int32          `nbt:"playerssleepingpercentage"`
	RecipesUnlock                   bool           `nbt:"recipesunlock"`
	NaturalGeneration               bool           `nbt:"naturalgeneration"`
	ProjectilesCanBreakBlocks       bool           `nbt:"projectilescanbreakblocks"`
	ShowRecipeMessages              bool           `nbt:"showrecipemessages"`
	IsHardcore                      bool           `nbt:"IsHardcore"`
	ShowDaysPlayed                  bool           `nbt:"showdaysplayed"`
	TNTExplosionDropDecay           bool           `nbt:"tntexplosiondropdecay"`
	HasUncompleteWorldFileOnDisk    bool           `nbt:"HasUncompleteWorldFileOnDisk"`
	PlayerHasDied                   bool           `nbt:"PlayerHasDied"`
	NeteaseEncryptFlag              bool           `nbt:"neteaseEncryptFlag"`              // Netease
	NeteaseStrongholdSelectedChunks [][]int64      `nbt:"neteaseStrongholdSelectedChunks"` // Netease
}

// FillDefault fills out d with all the default level.dat values.
func (d *Data) FillDefault() {
	d.Abilities.AttackMobs = true
	d.Abilities.AttackPlayers = true
	d.Abilities.Build = true
	d.Abilities.DoorsAndSwitches = true
	d.Abilities.FlySpeed = 0.05
	d.Abilities.Mine = true
	d.Abilities.OpenContainers = true
	d.Abilities.PlayerPermissionsLevel = 1
	d.Abilities.WalkSpeed = 0.1
	d.Abilities.VerticalFlySpeed = 1.0
	d.BaseGameVersion = "*"
	d.CommandBlockOutput = true
	d.CommandBlocksEnabled = true
	d.CommandsEnabled = true
	d.Difficulty = 2
	d.DoDayLightCycle = true
	d.DoEntityDrops = true
	d.DoFireTick = true
	d.DoInsomnia = true
	d.DoMobLoot = true
	d.DoMobSpawning = true
	d.DoTileDrops = true
	d.DoWeatherCycle = true
	d.DrowningDamage = true
	d.FallDamage = true
	d.FireDamage = true
	d.FreezeDamage = true
	d.FunctionCommandLimit = 10000
	d.GameType = 1
	d.Generator = 2
	d.HasBeenLoadedInCreative = true

	if block_general.UseNeteaseBlockStates {
		d.InventoryVersion = "1.21.0"
	} else {
		d.InventoryVersion = protocol.CurrentVersion
	}

	d.LANBroadcast = true
	d.LANBroadcastIntent = true
	d.LastOpenedWithVersion = minimumCompatibleClientVersion
	d.LevelName = "World"
	d.LightningLevel = 1.0
	d.LimitedWorldDepth = 16
	d.LimitedWorldOriginY = math.MaxInt16
	d.LimitedWorldWidth = 16
	d.MaxCommandChainLength = math.MaxUint16
	d.MinimumCompatibleClientVersion = minimumCompatibleClientVersion
	d.MobGriefing = true
	d.MultiPlayerGame = true
	d.MultiPlayerGameIntent = true
	d.NaturalRegeneration = true
	d.NetherScale = 8

	if block_general.UseNeteaseBlockStates {
		d.NetworkVersion = 630
	} else {
		d.NetworkVersion = protocol.CurrentProtocol
	}

	d.PVP = true
	d.Platform = 2
	d.PlatformBroadcastIntent = 3
	d.RainLevel = 1.0
	d.RandomSeed = time.Now().Unix()
	d.RandomTickSpeed = 1
	d.RespawnBlocksExplode = true
	d.SendCommandFeedback = true
	d.ServerChunkTickRange = 6
	d.ShowBorderEffect = true
	d.ShowDeathMessages = true
	d.ShowTags = true
	d.SpawnMobs = true
	d.SpawnRadius = 5
	d.SpawnY = math.MaxInt16
	d.StorageVersion = 9
	d.TNTExplodes = true
	d.WorldVersion = 1
	d.XBLBroadcastIntent = 3
}
