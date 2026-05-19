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

	// Read the first line for N
	line, err := reader.ReadString('\n')
	if err != nil {
		fmt.Fprint(writer, "error\n")
		return
	}
	line = strings.TrimSpace(line)

	// Parse N
	N, err := strconv.ParseUint(line, 10, 32)
	if err != nil || N > 1000 {
		fmt.Fprint(writer, "error\n")
		return
	}

	var sum uint64 = 0

	// Read the next N lines
	for i := uint64(0); i < N; i++ {
		line, err = reader.ReadString('\n')
		if err != nil {
			fmt.Fprint(writer, "error\n")
			return
		}
		line = strings.TrimSpace(line)

		// Parse the value
		value, err := strconv.ParseUint(line, 10, 32)
		if err != nil {
			fmt.Fprint(writer, "error\n")
			return
		}

		// Check for overflow
		if sum > 4294967295-value {
			fmt.Fprint(writer, "error\n")
			return
		}
		sum += value
	}

	fmt.Fprintf(writer, "%d\n", sum)
}
```