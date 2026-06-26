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
	w := bufio.NewWriter(os.Stdout)
	defer w.Flush()

	parse := func() (uint64, bool) {
		line, err := reader.ReadString('\n')
		if err != nil && len(line) == 0 {
			return 0, false
		}
		line = strings.TrimRight(line, "\r\n")
		line = strings.TrimRight(line, " \t")
		if len(line) == 0 {
			return 0, false
		}
		for _, c := range line {
			if c < '0' || c > '9' {
				return 0, false
			}
		}
		v, err := strconv.ParseUint(line, 10, 64)
		if err != nil || v > 4294967295 {
			return 0, false
		}
		return v, true
	}

	a, ok1 := parse()
	b, ok2 := parse()
	if !ok1 || !ok2 || b == 0 {
		fmt.Fprint(w, "error\n")
		return
	}
	fmt.Fprintf(w, "%d\n", a/b)
}
```