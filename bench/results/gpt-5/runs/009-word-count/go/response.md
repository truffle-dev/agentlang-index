```go
package main

import (
	"bufio"
	"io"
	"os"
	"strconv"
)

func main() {
	r := bufio.NewReader(os.Stdin)
	data, _ := io.ReadAll(r)

	inWord := false
	var count int64 = 0
	for _, b := range data {
		switch b {
		case ' ', '\t', '\n', '\r':
			inWord = false
		default:
			if !inWord {
				count++
				inWord = true
			}
		}
	}

	w := bufio.NewWriter(os.Stdout)
	_, _ = w.WriteString(strconv.FormatInt(count, 10))
	_ = w.WriteByte('\n')
	_ = w.Flush()
}
```