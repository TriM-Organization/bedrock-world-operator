package leveldat

import "strings"

// LowerMapKeyName make all the key in src to its lower represents.
// Of course, this changes will also made on all the sub-maps of src.
func LowerMapKeyName(src map[string]any) (dst map[string]any) {
	dst = make(map[string]any)
	for key, value := range src {
		subMap, ok := value.(map[string]any)
		if ok {
			dst[strings.ToLower(key)] = LowerMapKeyName(subMap)
			continue
		}
		dst[strings.ToLower(key)] = value
	}
	return
}
