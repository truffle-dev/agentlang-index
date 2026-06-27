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

	var counts [256]int
	buf := make([]byte, 32768)
	for {
		n, err := reader.Read(buf)
		for i := 0; i < n; i++ {
			counts[buf[i]]++
		}
		if err != nil {
			break
		}
	}

	for i := 0; i < 256; i++ {
		if counts[i] > 0 {
			fmt.Fprintf(writer, "%d %d\n", i, counts[i])
		}
	}
}
```