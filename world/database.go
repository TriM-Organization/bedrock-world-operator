package world

import (
	"fmt"
	"os"
	"path/filepath"
	"time"

	"github.com/YingLunTown-DreamLand/bedrock-world-operator/world/leveldat"
	"github.com/df-mc/goleveldb/leveldb"
)

// BedrockWorld implements a world provider for the Minecraft world format, which
// is based on a leveldb database.
type BedrockWorld struct {
	conf Config
	ldb  *leveldb.DB
	dir  string
	ldat *leveldat.Data
}

// Open creates a new provider reading and writing from/to files under the path
// passed using default options. If a world is present at the path, Open will
// parse its data and initialise the world with it. If the data cannot be
// parsed, an error is returned.
func Open(dir string) (*BedrockWorld, error) {
	var conf Config
	return conf.Open(dir)
}

// Close closes the provider, saving any file that might need to be saved, such as the level.dat.
func (db *BedrockWorld) Close() error {
	db.ldat.LastPlayed = time.Now().Unix()

	var ldat leveldat.LevelDat
	if err := ldat.Marshal(*db.ldat); err != nil {
		return fmt.Errorf("close: %w", err)
	}
	if err := ldat.WriteFile(filepath.Join(db.dir, "level.dat")); err != nil {
		return fmt.Errorf("close: %w", err)
	}
	if err := os.WriteFile(filepath.Join(db.dir, "levelname.txt"), []byte(db.ldat.LevelName), 0644); err != nil {
		return fmt.Errorf("close: write levelname.txt: %w", err)
	}
	return db.ldb.Close()
}
