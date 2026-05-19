```go
package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	in := bufio.NewReader(os.Stdin)
	out := bufio.NewWriter(os.Stdout)
	defer out.Flush()

	var N int
	if _, err := fmt.Fscan(in, &N); err != nil {
		fmt.Fprintln(out, 0)
		return
	}

	if N < 2 {
		fmt.Fprintln(out, 0)
		return
	}

	isPrime := make([]bool, N+1)
	for i := 2; i <= N; i++ {
		isPrime[i] = true
	}

	for p := 2; p*p <= N; p++ {
		if isPrime[p] {
			for m := p * p; m <= N; m += p {
				isPrime[m] = false
			}
		}
	}

	count := 0
	for i := 2; i <= N; i++ {
		if isPrime[i] {
			count++
		}
	}

	fmt.Fprintln(out, count)
}
```