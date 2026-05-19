```go
package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
)

func readLine(r *bufio.Reader) (string, bool) {
	line, err := r.ReadBytes('\n')
	if err != nil {
		if err == io.EOF {
			if len(line) == 0 {
				return "", false
			}
			n := len(line)
			if n > 0 && line[n-1] == '\r' {
				line = line[:n-1]
			}
			return string(line), true
		}
		if len(line) == 0 {
			return "", false
		}
		n := len(line)
		if n > 0 && line[n-1] == '\r' {
			line = line[:n-1]
		}
		return string(line), true
	}
	n := len(line)
	if n > 0 && line[n-1] == '\n' {
		line = line[:n-1]
		n--
	}
	if n > 0 && line[n-1] == '\r' {
		line = line[:n-1]
	}
	return string(line), true
}

func levenshtein(a, b string) int {
	la := len(a)
	lb := len(b)
	if la == 0 {
		return lb
	}
	if lb == 0 {
		return la
	}

	prev := make([]int, lb+1)
	curr := make([]int, lb+1)

	for j := 0; j <= lb; j++ {
		prev[j] = j
	}

	for i := 1; i <= la; i++ {
		curr[0] = i
		ai := a[i-1]
		for j := 1; j <= lb; j++ {
			cost := 0
			if ai != b[j-1] {
				cost = 1
			}
			del := prev[j] + 1
			ins := curr[j-1] + 1
			sub := prev[j-1] + cost

			m := del
			if ins < m {
				m = ins
			}
			if sub < m {
				m = sub
			}
			curr[j] = m
		}
		prev, curr = curr, prev
	}

	return prev[lb]
}

func main() {
	r := bufio.NewReader(os.Stdin)
	w := bufio.NewWriter(os.Stdout)

	s1, ok := readLine(r)
	if !ok {
		s1 = ""
	}
	s2, ok := readLine(r)
	if !ok {
		s2 = ""
	}

	d := levenshtein(s1, s2)
	fmt.Fprintln(w, d)
	_ = w.Flush()
}
```