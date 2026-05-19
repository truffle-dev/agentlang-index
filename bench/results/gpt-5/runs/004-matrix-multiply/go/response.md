```go
package main

import (
	"bufio"
	"io"
	"os"
	"strconv"
)

type parser struct {
	b []byte
	i int
	n int
}

func newParser(r *bufio.Reader) *parser {
	data, _ := io.ReadAll(r)
	return &parser{b: data, i: 0, n: len(data)}
}

func (p *parser) nextInt() (int, bool) {
	// Skip whitespace
	for p.i < p.n {
		c := p.b[p.i]
		if c > ' ' {
			break
		}
		p.i++
	}
	if p.i >= p.n {
		return 0, false
	}
	sign := 1
	if p.b[p.i] == '-' {
		sign = -1
		p.i++
	} else if p.b[p.i] == '+' {
		p.i++
	}
	val := 0
	found := false
	for p.i < p.n {
		c := p.b[p.i]
		if c < '0' || c > '9' {
			break
		}
		found = true
		val = val*10 + int(c-'0')
		p.i++
	}
	if !found {
		return 0, false
	}
	return sign * val, true
}

func main() {
	in := bufio.NewReader(os.Stdin)
	out := bufio.NewWriter(os.Stdout)
	defer out.Flush()

	p := newParser(in)

	N, ok := p.nextInt()
	if !ok || N < 1 || N > 5 {
		out.WriteString("error\n")
		return
	}

	A := make([][]int, N)
	B := make([][]int, N)
	for i := 0; i < N; i++ {
		A[i] = make([]int, N)
		for j := 0; j < N; j++ {
			x, ok := p.nextInt()
			if !ok {
				out.WriteString("error\n")
				return
			}
			A[i][j] = x
		}
	}
	for i := 0; i < N; i++ {
		B[i] = make([]int, N)
		for j := 0; j < N; j++ {
			x, ok := p.nextInt()
			if !ok {
				out.WriteString("error\n")
				return
			}
			B[i][j] = x
		}
	}

	C := make([][]int, N)
	for i := 0; i < N; i++ {
		C[i] = make([]int, N)
	}

	for i := 0; i < N; i++ {
		for k := 0; k < N; k++ {
			aik := A[i][k]
			if aik == 0 {
				continue
			}
			for j := 0; j < N; j++ {
				C[i][j] += aik * B[k][j]
			}
		}
	}

	for i := 0; i < N; i++ {
		for j := 0; j < N; j++ {
			if j > 0 {
				out.WriteByte(' ')
			}
			out.WriteString(strconv.Itoa(C[i][j]))
		}
		out.WriteByte('\n')
	}
}
```