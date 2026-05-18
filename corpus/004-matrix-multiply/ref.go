// Square integer matrix multiply, Go reference.
// Reads N, then N rows of A, then N rows of B, prints C = A * B.
package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)

func main() {
	raw, err := io.ReadAll(bufio.NewReader(os.Stdin))
	if err != nil {
		fmt.Fprintln(os.Stderr, "failed to read stdin")
		os.Exit(1)
	}
	tokens := strings.Fields(string(raw))
	pos := 0
	if len(tokens) == 0 {
		fmt.Fprintln(os.Stderr, "missing input")
		os.Exit(1)
	}
	n, err := strconv.Atoi(tokens[pos])
	if err != nil || n < 1 || n > 5 {
		fmt.Fprintln(os.Stderr, "N must be in [1, 5]")
		os.Exit(1)
	}
	pos++
	a := make([][]int, n)
	b := make([][]int, n)
	for i := 0; i < n; i++ {
		a[i] = make([]int, n)
		for j := 0; j < n; j++ {
			a[i][j], err = strconv.Atoi(tokens[pos])
			if err != nil {
				fmt.Fprintln(os.Stderr, "failed to read A")
				os.Exit(1)
			}
			pos++
		}
	}
	for i := 0; i < n; i++ {
		b[i] = make([]int, n)
		for j := 0; j < n; j++ {
			b[i][j], err = strconv.Atoi(tokens[pos])
			if err != nil {
				fmt.Fprintln(os.Stderr, "failed to read B")
				os.Exit(1)
			}
			pos++
		}
	}
	var sb strings.Builder
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			s := 0
			for k := 0; k < n; k++ {
				s += a[i][k] * b[k][j]
			}
			if j > 0 {
				sb.WriteByte(' ')
			}
			sb.WriteString(strconv.Itoa(s))
		}
		sb.WriteByte('\n')
	}
	fmt.Print(sb.String())
}
