```go
package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	w := bufio.NewWriter(os.Stdout)
	defer w.Flush()

	count := 0
	inWord := false
	buf, _ := io.ReadAll(reader)
	for _, b := range buf {
		if b == ' ' || b == '\t' || b == '\n' || b == '\r' {
			inWord = false
		} else if !inWord {
			inWord = true
			count++
		}
	}
	fmt.Fprintf(w, "%d\n", count)
}
```