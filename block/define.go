package block

var (
	// AirRuntimeID is the runtime ID of an air block.
	AirRuntimeID uint32
	// RuntimeIDToState must hold a function to convert a runtime ID to a name and its state properties.
	RuntimeIDToState func(runtimeID uint32) (name string, properties map[string]any, found bool)
	// StateToRuntimeID must hold a function to convert a name and its state properties to a runtime ID.
	StateToRuntimeID func(name string, properties map[string]any) (runtimeID uint32, found bool)
)
