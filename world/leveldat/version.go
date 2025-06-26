package leveldat

import (
	"strconv"
	"strings"

	block_general "github.com/TriM-Organization/bedrock-world-operator/block/general"
	"github.com/sandertv/gophertunnel/minecraft/protocol"
)

// Version is the current version stored in level.dat files.
const Version = 10

// minimumCompatibleClientVersion is the minimum compatible client version,
// required by the latest Minecraft data provider.
var minimumCompatibleClientVersion []int32

// init initializes the minimum compatible client version.
func init() {
	var fullVersion []string

	if block_general.UseNeteaseBlockStates {
		fullVersion = append(strings.Split("1.21.0", "."), "0", "0")
	} else {
		fullVersion = append(strings.Split(protocol.CurrentVersion, "."), "0", "0")
	}

	for _, v := range fullVersion {
		i, _ := strconv.Atoi(v)
		minimumCompatibleClientVersion = append(minimumCompatibleClientVersion, int32(i))
	}
}
