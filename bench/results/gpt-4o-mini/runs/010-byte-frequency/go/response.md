```go
package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	counts := make([]int, 256)
	reader := bufio.NewReader(os.Stdin)

	for {
		b, err := reader.ReadByte()
		if err != nil {
			break
		}
		counts[b]++
	}

	writer := bufio.NewWriter(os.Stdout)
	for i := 0; i < 256; i++ {
		if counts[i] > 0 {
			fmt.Fprintf(writer, "%d %d\n", i, counts[i])
		}
	}
	writer.Flush()
}
```