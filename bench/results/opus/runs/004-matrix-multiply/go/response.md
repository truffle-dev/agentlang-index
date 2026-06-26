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

	a := make([][]int, n)
	b := make([][]int, n)
	for i := 0; i < n; i++ {
		a[i] = make([]int, n)
		for j := 0; j < n; j++ {
			fmt.Fscan(reader, &a[i][j])
		}
	}
	for i := 0; i < n; i++ {
		b[i] = make([]int, n)
		for j := 0; j < n; j++ {
			fmt.Fscan(reader, &b[i][j])
		}
	}

	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			sum := 0
			for k := 0; k < n; k++ {
				sum += a[i][k] * b[k][j]
			}
			if j > 0 {
				fmt.Fprint(writer, " ")
			}
			fmt.Fprint(writer, sum)
		}
		fmt.Fprintln(writer)
	}
}
```