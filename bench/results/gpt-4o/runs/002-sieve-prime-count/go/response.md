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

	// Read input
	line, _ := reader.ReadString('\n')
	N, _ := strconv.Atoi(line[:len(line)-1])

	// Handle edge cases
	if N < 2 {
		fmt.Fprintln(writer, 0)
		return
	}

	// Sieve of Eratosthenes
	isPrime := make([]bool, N+1)
	for i := 2; i <= N; i++ {
		isPrime[i] = true
	}

	for p := 2; p*p <= N; p++ {
		if isPrime[p] {
			for multiple := p * p; multiple <= N; multiple += p {
				isPrime[multiple] = false
			}
		}
	}

	// Count primes
	count := 0
	for i := 2; i <= N; i++ {
		if isPrime[i] {
			count++
		}
	}

	// Output the result
	fmt.Fprintln(writer, count)
}
```