```go
package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
)

func main() {
	r := bufio.NewReader(os.Stdin)
	w := bufio.NewWriter(os.Stdout)
	defer w.Flush()

	var counts [256]uint64
	buf := make([]byte, 64*1024)

	for {
		n, err := r.Read(buf)
		if n > 0 {
			for _, b := range buf[:n] {
				counts[b]++
			}
		}
		if err == io.EOF {
			break
		}
		if err != nil {
			break
		}
	}

	for i := 0; i < 256; i++ {
		if counts[i] != 0 {
			fmt.Fprintf(w, "%d %d\n", i, counts[i])
		}
	}
}
```