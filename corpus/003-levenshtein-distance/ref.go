// Levenshtein edit distance, Go reference.
// Reads A and B from stdin (one per line), runs a two-row DP.
package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strings"
)

func main() {
	raw, err := io.ReadAll(bufio.NewReader(os.Stdin))
	if err != nil {
		fmt.Fprintln(os.Stderr, "failed to read stdin")
		os.Exit(1)
	}
	lines := strings.SplitN(string(raw), "\n", 3)
	var a, b string
	if len(lines) >= 1 {
		a = lines[0]
	}
	if len(lines) >= 2 {
		b = lines[1]
	}
	if len(a) > 50 || len(b) > 50 {
		fmt.Fprintln(os.Stderr, "each string must be at most 50 characters")
		os.Exit(1)
	}
	m, n := len(a), len(b)
	prev := make([]int, n+1)
	curr := make([]int, n+1)
	for j := 0; j <= n; j++ {
		prev[j] = j
	}
	for i := 0; i < m; i++ {
		curr[0] = i + 1
		for k := 0; k < n; k++ {
			delCost := prev[k+1] + 1
			insCost := curr[k] + 1
			subCost := prev[k]
			if a[i] != b[k] {
				subCost++
			}
			best := delCost
			if insCost < best {
				best = insCost
			}
			if subCost < best {
				best = subCost
			}
			curr[k+1] = best
		}
		prev, curr = curr, prev
	}
	fmt.Print(prev[n], "\n")
}
