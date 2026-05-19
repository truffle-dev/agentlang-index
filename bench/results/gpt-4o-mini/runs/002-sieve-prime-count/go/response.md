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

	input, _ := reader.ReadString('\n')
	N, _ := strconv.Atoi(input[:len(input)-1])

	if N < 2 {
		writer.WriteString("0\n")
		writer.Flush()
		return
	}

	isPrime := make([]bool, N+1)
	for i := 2; i <= N; i++ {
		isPrime[i] = true
	}

	for p := 2; p*p <= N; p++ {
		if isPrime[p] {
			for i := p * p; i <= N; i += p {
				isPrime[i] = false
			}
		}
	}

	count := 0
	for i := 2; i <= N; i++ {
		if isPrime[i] {
			count++
		}
	}

	writer.WriteString(fmt.Sprintf("%d\n", count))
	writer.Flush()
}
```