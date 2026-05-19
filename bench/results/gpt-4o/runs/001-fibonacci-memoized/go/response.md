```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	writer := bufio.NewWriter(os.Stdout)
	defer writer.Flush()

	input, _ := reader.ReadString('\n')
	input = input[:len(input)-1] // Remove the newline character
	n, err := strconv.Atoi(input)
	if err != nil {
		fmt.Fprintln(writer, "error")
		return
	}

	memo := make(map[int]int64)
	result := fib(n, memo)
	fmt.Fprintln(writer, result)
}

func fib(n int, memo map[int]int64) int64 {
	if n <= 1 {
		return int64(n)
	}
	if val, exists := memo[n]; exists {
		return val
	}
	memo[n] = fib(n-1, memo) + fib(n-2, memo)
	return memo[n]
}
```