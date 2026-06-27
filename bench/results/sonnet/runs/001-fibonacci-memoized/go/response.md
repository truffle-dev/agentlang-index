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

	memo := make([]int64, n+1)
	for i := range memo {
		memo[i] = -1
	}

	var fib func(int) int64
	fib = func(k int) int64 {
		if k == 0 {
			return 0
		}
		if k == 1 {
			return 1
		}
		if memo[k] != -1 {
			return memo[k]
		}
		memo[k] = fib(k-1) + fib(k-2)
		return memo[k]
	}

	fmt.Fprintf(writer, "%d\n", fib(n))
}
```