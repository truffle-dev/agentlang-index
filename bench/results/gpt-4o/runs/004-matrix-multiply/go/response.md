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

	// Read the size of the matrices
	line, _ := reader.ReadString('\n')
	N, _ := strconv.Atoi(strings.TrimSpace(line))

	// Read matrix A
	A := make([][]int, N)
	for i := 0; i < N; i++ {
		line, _ := reader.ReadString('\n')
		parts := strings.Fields(line)
		A[i] = make([]int, N)
		for j := 0; j < N; j++ {
			A[i][j], _ = strconv.Atoi(parts[j])
		}
	}

	// Read matrix B
	B := make([][]int, N)
	for i := 0; i < N; i++ {
		line, _ := reader.ReadString('\n')
		parts := strings.Fields(line)
		B[i] = make([]int, N)
		for j := 0; j < N; j++ {
			B[i][j], _ = strconv.Atoi(parts[j])
		}
	}

	// Compute matrix C = A * B
	C := make([][]int, N)
	for i := 0; i < N; i++ {
		C[i] = make([]int, N)
		for j := 0; j < N; j++ {
			sum := 0
			for k := 0; k < N; k++ {
				sum += A[i][k] * B[k][j]
			}
			C[i][j] = sum
		}
	}

	// Output matrix C
	for i := 0; i < N; i++ {
		for j := 0; j < N; j++ {
			if j > 0 {
				writer.WriteString(" ")
			}
			writer.WriteString(strconv.Itoa(C[i][j]))
		}
		writer.WriteString("\n")
	}
}
```