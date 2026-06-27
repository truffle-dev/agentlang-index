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

	readLine := func() (string, bool) {
		line, err := reader.ReadString('\n')
		if err != nil {
			// EOF with partial line is still a line
			if len(line) > 0 {
				return strings.TrimRight(line, " \t\r\n"), true
			}
			return "", false
		}
		return strings.TrimRight(line, " \t\r\n"), true
	}

	parseU32 := func(s string) (uint64, bool) {
		if s == "" {
			return 0, false
		}
		// Reject leading + or -
		if s[0] == '+' || s[0] == '-' {
			return 0, false
		}
		v, err := strconv.ParseUint(s, 10, 64)
		if err != nil {
			return 0, false
		}
		if v > 4294967295 {
			return 0, false
		}
		return v, true
	}

	line1, ok := readLine()
	if !ok {
		fmt.Fprint(writer, "error\n")
		return
	}

	n, valid := parseU32(line1)
	if !valid || n > 1000 {
		fmt.Fprint(writer, "error\n")
		return
	}

	var sum uint64
	for i := uint64(0); i < n; i++ {
		line, ok := readLine()
		if !ok {
			fmt.Fprint(writer, "error\n")
			return
		}
		v, valid := parseU32(line)
		if !valid {
			fmt.Fprint(writer, "error\n")
			return
		}
		sum += v
		if sum > 4294967295 {
			fmt.Fprint(writer, "error\n")
			return
		}
	}

	fmt.Fprintf(writer, "%d\n", sum)
}
```