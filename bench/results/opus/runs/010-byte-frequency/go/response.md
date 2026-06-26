```go
package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
)

func main() {
	var counts [256]int64
	reader := bufio.NewReader(os.Stdin)
	buf := make([]byte, 32*1024)
	for {
		n, err := reader.Read(buf)
		for i := 0; i < n; i++ {
			counts[buf[i]]++
		}
		if err == io.EOF {
			break
		}
	}
	w := bufio.NewWriter(os.Stdout)
	for i := 0; i < 256; i++ {
		if counts[i] > 0 {
			fmt.Fprintf(w, "%d %d\n", i, counts[i])
		}
	}
	w.Flush()
}
```