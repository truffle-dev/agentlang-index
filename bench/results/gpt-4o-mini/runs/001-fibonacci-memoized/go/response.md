```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func fib(n int, memo map[int]int) int {
	if n <= 1 {
		return n
	}
	if val, exists := memo[n]; exists {
		return val
	}
	memo[n] = fib(n-1, memo) + fib(n-2, memo)
	return memo[n]
}

func main() {
	reader := bufio.NewReader(os.Stdin)
	writer := bufio.NewWriter(os.Stdout)

	input, _ := reader.ReadString('\n')
	n, _ := strconv.Atoi(input[:len(input)-1])

	memo := make(map[int]int)
	result := fib(n, memo)

	fmt.Fprintln(writer, result)
	writer.Flush()
}
```