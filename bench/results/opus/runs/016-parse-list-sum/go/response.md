```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	w := bufio.NewWriter(os.Stdout)
	defer w.Flush()

	errOut := func() {
		fmt.Fprint(w, "error\n")
	}

	line, err := reader.ReadString('\n')
	if err != nil && len(line) == 0 {
		errOut()
		return
	}
	line = strings.TrimRight(line, " \t\r\n")

	n, ok := parseU32(line)
	if !ok || n > 1000 {
		errOut()
		return
	}

	var sum uint64
	for i := uint64(0); i < uint64(n); i++ {
		vline, err := reader.ReadString('\n')
		if err != nil && len(vline) == 0 {
			errOut()
			return
		}
		vline = strings.TrimRight(vline, " \t\r\n")
		v, ok := parseU32(vline)
		if !ok {
			errOut()
			return
		}
		sum += uint64(v)
		if sum > 4294967295 {
			errOut()
			return
		}
	}

	fmt.Fprintf(w, "%d\n", sum)
}

func parseU32(s string) (uint64, bool) {
	if len(s) == 0 {
		return 0, false
	}
	if s[0] == '+' || s[0] == '-' {
		return 0, false
	}
	for _, c := range s {
		if c < '0' || c > '9' {
			return 0, false
		}
	}
	// manual parse to avoid importing strconv
	var val uint64
	for _, c := range s {
		val = val*10 + uint64(c-'0')
		if val > 4294967295 {
			return 0, false
		}
	}
	return val, true
}
```