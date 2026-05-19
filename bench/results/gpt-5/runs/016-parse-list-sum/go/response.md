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

const u32max = uint64(4294967295)

func trimRightSpaces(s string) string {
	return strings.TrimRightFunc(s, unicode.IsSpace)
}

func parseU32Strict(s string) (uint64, bool) {
	if s == "" {
		return 0, false
	}
	var v uint64 = 0
	for i := 0; i < len(s); i++ {
		b := s[i]
		if b < '0' || b > '9' {
			return 0, false
		}
		d := uint64(b - '0')
		if v > u32max/10 {
			return 0, false
		}
		v *= 10
		if v > u32max-d {
			return 0, false
		}
		v += d
	}
	return v, true
}

func readTrimRightLine(r *bufio.Reader) (string, bool) {
	data, err := r.ReadBytes('\n')
	if err != nil {
		if err == io.EOF {
			if len(data) == 0 {
				return "", false
			}
		} else {
			if len(data) == 0 {
				return "", false
			}
		}
	}
	s := string(data)
	s = trimRightSpaces(s)
	return s, true
}

func writeError(w *bufio.Writer) {
	w.WriteString("error\n")
}

func main() {
	out := bufio.NewWriter(os.Stdout)
	defer out.Flush()

	args := os.Args
	if len(args) > 1 {
		argv := args[1:]
		if len(argv) < 1 {
			writeError(out)
			return
		}
		nStr := trimRightSpaces(argv[0])
		n64, ok := parseU32Strict(nStr)
		if !ok || n64 > 1000 {
			writeError(out)
			return
		}
		n := int(n64)
		if len(argv)-1 < n {
			writeError(out)
			return
		}
		var sum uint64 = 0
		for i := 0; i < n; i++ {
			s := trimRightSpaces(argv[1+i])
			v, ok := parseU32Strict(s)
			if !ok {
				writeError(out)
				return
			}
			if sum > u32max-v {
				writeError(out)
				return
			}
			sum += v
		}
		out.WriteString(strconv.FormatUint(sum, 10))
		out.WriteByte('\n')
		return
	}

	in := bufio.NewReader(os.Stdin)
	line1, ok := readTrimRightLine(in)
	if !ok {
		writeError(out)
		return
	}
	n64, ok := parseU32Strict(line1)
	if !ok || n64 > 1000 {
		writeError(out)
		return
	}
	n := int(n64)
	var sum uint64 = 0
	for i := 0; i < n; i++ {
		s, ok := readTrimRightLine(in)
		if !ok {
			writeError(out)
			return
		}
		v, ok := parseU32Strict(s)
		if !ok {
			writeError(out)
			return
		}
		if sum > u32max-v {
			writeError(out)
			return
		}
		sum += v
	}
	out.WriteString(strconv.FormatUint(sum, 10))
	out.WriteByte('\n')
}
```