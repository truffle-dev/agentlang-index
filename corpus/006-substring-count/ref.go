// Non-overlapping substring count, Go reference.
// Reads pattern P from line 1 of stdin and text T from line 2.

package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strings"
)

func main() {
	raw, _ := io.ReadAll(bufio.NewReader(os.Stdin))
	parts := strings.SplitN(string(raw), "\n", 3)
	var p, t string
	if len(parts) >= 1 {
		p = parts[0]
	}
	if len(parts) >= 2 {
		t = parts[1]
	}
	count := 0
	if len(p) > 0 {
		m := len(p)
		n := len(t)
		i := 0
		for i+m <= n {
			if t[i:i+m] == p {
				count++
				i += m
			} else {
				i++
			}
		}
	}
	fmt.Printf("%d\n", count)
}
