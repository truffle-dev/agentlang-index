// Per-byte frequency table, Go reference.

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
	var counts [256]uint32
	for _, b := range data {
		counts[b]++
	}
	w := bufio.NewWriter(os.Stdout)
	defer w.Flush()
	for b := 0; b < 256; b++ {
		if counts[b] > 0 {
			fmt.Fprintf(w, "%d %d\n", b, counts[b])
		}
	}
}
