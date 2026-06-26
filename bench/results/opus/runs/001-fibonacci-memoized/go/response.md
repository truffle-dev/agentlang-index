```go
package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	writer := bufio.NewWriter(os.Stdout)
	defer writer.Flush()

	var n int
	fmt.Fscan(reader, &n)

	memo := make(map[int]int64)
	memo[0] = 0
	memo[1] = 1

	var fib func(int) int64
	fib = func(k int) int64 {
		if v, ok := memo[k]; ok {
			return v
		}
		memo[k] = fib(k-1) + fib(k-2)
		return memo[k]
	}

	fmt.Fprintf(writer, "%d\n", fib(n))
}
```