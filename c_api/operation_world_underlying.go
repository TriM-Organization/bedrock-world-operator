package main

import "C"
import "fmt"

//export DB_Has
func DB_Has(id C.int, key *C.char) C.int {
	w := openedWorld.LoadObject(int(id))
	if w == nil {
		return -1
	}
	has, _ := (*w).Has(asGoBytes(key))
	return asCbool(has)
}

//export DB_Get
func DB_Get(id C.int, key *C.char) *C.char {
	w := openedWorld.LoadObject(int(id))
	if w == nil {
		return asCbytes(nil)
	}
	value, _ := (*w).Get(asGoBytes(key))
	return asCbytes(value)
}

//export DB_Put
func DB_Put(id C.int, key *C.char, value *C.char) *C.char {
	w := openedWorld.LoadObject(int(id))
	if w == nil {
		return C.CString("DB_Put: World not found")
	}

	err := (*w).Put(asGoBytes(key), asGoBytes(value))
	if err != nil {
		return C.CString(fmt.Sprintf("DB_Put: %v", err))
	}

	return C.CString("")
}

//export DB_Delete
func DB_Delete(id C.int, key *C.char) *C.char {
	w := openedWorld.LoadObject(int(id))
	if w == nil {
		return C.CString("DB_Delete: World not found")
	}

	err := (*w).Delete(asGoBytes(key))
	if err != nil {
		return C.CString(fmt.Sprintf("DB_Delete: %v", err))
	}

	return C.CString("")
}
