```go
package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	counts := make([]int, 256)

	for {
		b, err := reader.ReadByte()
		if err != nil {
			break
		}
		counts[b]++
	}

	writer := bufio.NewWriter(os.Stdout)
	defer writer.Flush()

	for i, count := range counts {
		if count > 0 {
			fmt.Fprintf(writer, "%d %d\n", i, count)
		}
	}
}
```