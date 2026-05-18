// Prime count via Sieve of Eratosthenes, Go reference.
// Reads N from stdin, runs a byte-flag sieve, counts unmarked [2, N].
package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	line, _ := reader.ReadString('\n')
	n, err := strconv.Atoi(strings.TrimSpace(line))
	if err != nil || n < 0 {
		fmt.Fprintln(os.Stderr, "N must be a non-negative integer")
		os.Exit(1)
	}
	if n < 2 {
		fmt.Print("0\n")
		return
	}
	composite := make([]byte, n+1)
	for i := 2; i*i <= n; i++ {
		if composite[i] == 0 {
			for j := i * i; j <= n; j += i {
				composite[j] = 1
			}
		}
	}
	count := 0
	for k := 2; k <= n; k++ {
		if composite[k] == 0 {
			count++
		}
	}
	fmt.Print(count, "\n")
}
