```go
package main

import (
	"bufio"
	"io"
	"os"
	"strconv"
)

func readLine(r *bufio.Reader) (string, error) {
	s, err := r.ReadString('\n')
	if err != nil && err != io.EOF {
		return "", err
	}
	// Trim trailing '\n'
	if len(s) > 0 && s[len(s)-1] == '\n' {
		s = s[:len(s)-1]
	}
	// Trim trailing '\r' (for Windows-style line endings)
	if len(s) > 0 && s[len(s)-1] == '\r' {
		s = s[:len(s)-1]
	}
	return s, nil
}

func main() {
	in := bufio.NewReader(os.Stdin)
	out := bufio.NewWriter(os.Stdout)
	defer out.Flush()

	p, _ := readLine(in)
	t, _ := readLine(in)

	m := len(p)
	n := len(t)
	count := 0

	if m > 0 && n >= m {
		for i := 0; i <= n-m; {
			if t[i:i+m] == p {
				count++
				i += m
			} else {
				i++
			}
		}
	}

	out.WriteString(strconv.Itoa(count))
	out.WriteByte('\n')
}
```