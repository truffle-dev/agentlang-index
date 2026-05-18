// Run-length encode the input, Go reference.

package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
)

func main() {
	data, err := io.ReadAll(os.Stdin)
	if err != nil {
		os.Exit(1)
	}
	if len(data) == 0 {
		return
	}
	w := bufio.NewWriter(os.Stdout)
	defer w.Flush()
	curByte := data[0]
	curCount := 1
	for i := 1; i < len(data); i++ {
		b := data[i]
		if b == curByte {
			curCount++
		} else {
			fmt.Fprintf(w, "%d %d\n", curCount, curByte)
			curByte = b
			curCount = 1
		}
	}
	fmt.Fprintf(w, "%d %d\n", curCount, curByte)
}
