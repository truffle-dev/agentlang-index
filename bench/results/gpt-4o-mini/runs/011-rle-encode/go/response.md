```go
package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	writer := bufio.NewWriter(os.Stdout)
	defer writer.Flush()

	var prev byte
	var count int
	first := true

	for {
		b, err := reader.ReadByte()
		if err != nil {
			if err.Error() != "EOF" {
				fmt.Fprintln(writer, "error")
			}
			break
		}

		if first {
			prev = b
			count = 1
			first = false
		} else if b == prev {
			count++
		} else {
			fmt.Fprintf(writer, "%d %d\n", count, prev)
			prev = b
			count = 1
		}
	}

	if !first {
		fmt.Fprintf(writer, "%d %d\n", count, prev)
	}
}
```