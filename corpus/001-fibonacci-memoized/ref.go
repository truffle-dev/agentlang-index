// Fibonacci with memoization, Go reference.
// Reads N from stdin, caches fib(i) in a map[int]uint64.
// uint64 holds fib(N) for N up to 93.
package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func fib(k int, memo map[int]uint64) uint64 {
	if v, ok := memo[k]; ok {
		return v
	}
	v := fib(k-1, memo) + fib(k-2, memo)
	memo[k] = v
	return v
}

func main() {
	reader := bufio.NewReader(os.Stdin)
	line, _ := reader.ReadString('\n')
	n, err := strconv.Atoi(strings.TrimSpace(line))
	if err != nil || n < 0 {
		fmt.Fprintln(os.Stderr, "N must be a non-negative integer")
		os.Exit(1)
	}
	memo := map[int]uint64{0: 0, 1: 1}
	fmt.Print(fib(n, memo), "\n")
}
