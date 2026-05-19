```go
package main

import (
	"bufio"
	"fmt"
	"os"
)

func levenshtein(a, b string) int {
	m := len(a)
	n := len(b)

	if m == 0 {
		return n
	}
	if n == 0 {
		return m
	}

	d := make([][]int, m+1)
	for i := range d {
		d[i] = make([]int, n+1)
	}

	for i := 0; i <= m; i++ {
		d[i][0] = i
	}
	for j := 0; j <= n; j++ {
		d[0][j] = j
	}

	for i := 1; i <= m; i++ {
		for j := 1; j <= n; j++ {
			cost := 0
			if a[i-1] != b[j-1] {
				cost = 1
			}
			d[i][j] = min(d[i-1][j]+1, min(d[i][j-1]+1, d[i-1][j-1]+cost))
		}
	}

	return d[m][n]
}

func min(x, y int) int {
	if x < y {
		return x
	}
	return y
}

func main() {
	reader := bufio.NewReader(os.Stdin)
	a, _ := reader.ReadString('\n')
	b, _ := reader.ReadString('\n')

	a = a[:len(a)-1] // Remove newline
	b = b[:len(b)-1] // Remove newline

	distance := levenshtein(a, b)
	fmt.Println(distance)
}
```