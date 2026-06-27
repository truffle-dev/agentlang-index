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

	parseU32 := func(line string) (uint64, bool) {
		s := strings.TrimRight(line, " \t\r")
		if s == "" {
			return 0, false
		}
		for _, c := range s {
			if c < '0' || c > '9' {
				return 0, false
			}
		}
		v, err := strconv.ParseUint(s, 10, 64)
		if err != nil || v > 4294967295 {
			return 0, false
		}
		return v, true
	}

	lineA, err := reader.ReadString('\n')
	if err != nil && lineA == "" {
		fmt.Fprint(writer, "error\n")
		return
	}
	lineB, err2 := reader.ReadString('\n')
	if err2 != nil && lineB == "" {
		fmt.Fprint(writer, "error\n")
		return
	}

	a, ok := parseU32(strings.TrimRight(lineA, "\n"))
	if !ok {
		fmt.Fprint(writer, "error\n")
		return
	}
	b, ok := parseU32(strings.TrimRight(lineB, "\n"))
	if !ok {
		fmt.Fprint(writer, "error\n")
		return
	}
	if b == 0 {
		fmt.Fprint(writer, "error\n")
		return
	}
	fmt.Fprintf(writer, "%d\n", a/b)
}
```