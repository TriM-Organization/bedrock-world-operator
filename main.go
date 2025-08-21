package main

import (
    "fmt"
    "github.com/TriM-Organization/bedrock-world-operator/world"
)

func main() {
    bw, err := world.Open("./world2", nil)
    if err != nil {
        panic(err)
    }
    defer bw.Close()
    fmt.Println(bw)
}