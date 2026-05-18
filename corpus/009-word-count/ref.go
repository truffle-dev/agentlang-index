// Count whitespace-separated tokens in input, Go reference.

package main

import (
	"io"
	"os"
	"strconv"
)

func main() {
	data, err := io.ReadAll(os.Stdin)
	if err != nil {
		os.Exit(1)
	}
	count := 0
	inWord := false
	for _, b := range data {
		isWS := b == 32 || b == 9 || b == 10 || b == 13
		if isWS {
			inWord = false
		} else if !inWord {
			count++
			inWord = true
		}
	}
	os.Stdout.WriteString(strconv.Itoa(count) + "\n")
}
