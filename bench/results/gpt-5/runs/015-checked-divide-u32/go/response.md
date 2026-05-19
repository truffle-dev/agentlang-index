```go
package main

import (
	"bufio"
	"io"
	"os"
	"strconv"
	"strings"
	"unicode"
)

func readLine(r *bufio.Reader) (string, bool) {
	var buf []byte
	for {
		line, isPrefix, err := r.ReadLine()
		if err != nil {
			if err == io.EOF {
				if len(buf) == 0 && len(line) == 0 {
					return "", false
				}
				buf = append(buf, line...)
				return string(buf), true
			}
			return "", false
		}
		buf = append(buf, line...)
		if !isPrefix {
			return string(buf), true
		}
	}
}

func parseU32Strict(s string) (uint32, bool) {
	if len(s) == 0 {
		return 0, false
	}
	var val uint64 = 0
	const max = uint64(4294967295)
	for i := 0; i < len(s); i++ {
		c := s[i]
		if c < '0' || c > '9' {
			return 0, false
		}
		d := uint64(c - '0')
		if val > max/10 || (val == max/10 && d > max%10) {
			return 0, false
		}
		val = val*10 + d
	}
	return uint32(val), true
}

func main() {
	in := bufio.NewReader(os.Stdin)
	out := bufio.NewWriter(os.Stdout)
	defer out.Flush()

	line1, ok := readLine(in)
	if !ok {
		out.WriteString("error\n")
		return
	}
	line2, ok := readLine(in)
	if !ok {
		out.WriteString("error\n")
		return
	}

	s1 := strings.TrimRightFunc(line1, unicode.IsSpace)
	s2 := strings.TrimRightFunc(line2, unicode.IsSpace)

	a, ok := parseU32Strict(s1)
	if !ok {
		out.WriteString("error\n")
		return
	}
	b, ok := parseU32Strict(s2)
	if !ok || b == 0 {
		out.WriteString("error\n")
		return
	}

	q := uint64(a) / uint64(b)
	out.WriteString(strconv.FormatUint(q, 10))
	out.WriteByte('\n')
}
```