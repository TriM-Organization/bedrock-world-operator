package world

import (
	"fmt"
	"os"
	"path/filepath"
	"time"

	"github.com/TriM-Organization/bedrock-world-operator/block"
	"github.com/TriM-Organization/bedrock-world-operator/world/leveldat"
)

// BedrockWorld implements a world provider for the Minecraft world format, which
// is based on a leveldb database.
type BedrockWorld struct {
	LevelDB
	databaseConfig      Config
	worldMainDir        string
	leveldatData        *leveldat.Data
	blockRuntimeIDTable *block.BlockRuntimeIDTable
}

// Open creates a new provider reading and writing from/to files under the path
// passed using default options. If a world is present at the path, Open will
// parse its data and initialise the world with it. If the data cannot be
// parsed, an error is returned.
//
// key is used to encrypt the payload of the leveldb key. The encrypt way
// is AES+ECB+PKCS7Padding. Given a key that is nil or 0 length will disable
// encrypt.
//
// table is the block runtime ID table that convert block between itself
// and its runtime ID description. You can use [block.NewBlockRuntimeIDTable]
// to create a new block runtime ID table if not have one.
//
// Note that the length of given key must be 16, otherwise return an error.
func Open(dir string, key []byte, table *block.BlockRuntimeIDTable) (*BedrockWorld, error) {
	var conf Config
	return conf.Open(dir, key, table)
}

// BlockRuntimeIDTable returns its internal block runtime ID table.
func (db *BedrockWorld) BlockRuntimeIDTable() *block.BlockRuntimeIDTable {
	return db.blockRuntimeIDTable
}

// LevelDat return the level dat of this world.
func (db *BedrockWorld) LevelDat() *leveldat.Data {
	return db.leveldatData
}

// UpdateLevelDat update level dat immediately.
func (db *BedrockWorld) UpdateLevelDat() error {
	var ldat leveldat.LevelDat
	if err := ldat.Marshal(*db.leveldatData); err != nil {
		return fmt.Errorf("close: %w", err)
	}
	if err := ldat.WriteFile(filepath.Join(db.worldMainDir, "level.dat")); err != nil {
		return fmt.Errorf("close: %w", err)
	}
	if err := os.WriteFile(filepath.Join(db.worldMainDir, "levelname.txt"), []byte(db.leveldatData.LevelName), 0644); err != nil {
		return fmt.Errorf("close: write levelname.txt: %w", err)
	}
	return nil
}

// CloseWorld closes the provider, saving any file that might need to be saved, such as the level.dat.
func (db *BedrockWorld) CloseWorld() error {
	db.leveldatData.LastPlayed = time.Now().Unix()
	if err := db.UpdateLevelDat(); err != nil {
		return err
	}
	return db.Close()
}
