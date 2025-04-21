package world

import "github.com/df-mc/goleveldb/leveldb"

// Database wrapper a level database,
// and expose some useful functions.
type database struct {
	ldb *leveldb.DB
}

// Has returns true if the DB does contains the given key.
//
// It is safe to modify the contents of the argument after Has returns.
func (db *database) Has(key []byte) (has bool, err error) {
	return db.ldb.Has(key, nil)
}

// Get gets the value for the given key. It returns ErrNotFound if the
// DB does not contains the key.
//
// The returned slice is its own copy, it is safe to modify the contents
// of the returned slice.
// It is safe to modify the contents of the argument after Get returns.
func (db *database) Get(key []byte) (value []byte, err error) {
	return db.ldb.Get(key, nil)
}

// Put sets the value for the given key. It overwrites any previous value
// for that key; a DB is not a multi-map. Write merge also applies for Put, see
// Write.
//
// It is safe to modify the contents of the arguments after Put returns but not
// before.
func (db *database) Put(key []byte, value []byte) error {
	return db.ldb.Put(key, value, nil)
}

// Delete deletes the value for the given key. Delete will not returns error if
// key doesn't exist. Write merge also applies for Delete, see Write.
//
// It is safe to modify the contents of the arguments after Delete returns but
// not before.
func (db *database) Delete(key []byte) error {
	return db.ldb.Delete(key, nil)
}

// Close closes the DB. This will also releases any outstanding snapshot,
// abort any in-flight compaction and discard open transaction.
//
// It is not safe to close a DB until all outstanding iterators are released.
// It is valid to call Close multiple times. Other methods should not be
// called after the DB has been closed.
func (db *database) Close() error {
	return db.ldb.Close()
}
