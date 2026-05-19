```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	writer := bufio.NewWriter(os.Stdout)
	defer writer.Flush()

	// Read the size of the matrix
	nStr, _ := reader.ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(nStr))

	// Initialize matrices A and B
	A := make([][]int, n)
	B := make([][]int, n)

	// Read matrix A
	for i := 0; i < n; i++ {
		line, _ := reader.ReadString('\n')
		entries := strings.Fields(line)
		A[i] = make([]int, n)
		for j := 0; j < n; j++ {
			A[i][j], _ = strconv.Atoi(entries[j])
		}
	}

	// Read matrix B
	for i := 0; i < n; i++ {
		line, _ := reader.ReadString('\n')
		entries := strings.Fields(line)
		B[i] = make([]int, n)
		for j := 0; j < n; j++ {
			B[i][j], _ = strconv.Atoi(entries[j])
		}
	}

	// Initialize matrix C for the result
	C := make([][]int, n)
	for i := 0; i < n; i++ {
		C[i] = make([]int, n)
		for j := 0; j < n; j++ {
			for k := 0; k < n; k++ {
				C[i][j] += A[i][k] * B[k][j]
			}
		}
	}

	// Write the result matrix C to stdout
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			if j > 0 {
				writer.WriteString(" ")
			}
			writer.WriteString(strconv.Itoa(C[i][j]))
		}
		writer.WriteString("\n")
	}
}
```