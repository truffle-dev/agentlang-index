```go
package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	r := bufio.NewReader(os.Stdin)
	w := bufio.NewWriter(os.Stdout)
	defer w.Flush()

	count := 0
	inWord := false
	for {
		b, err := r.ReadByte()
		if err != nil {
			break
		}
		ws := b == 0x20 || b == 0x09 || b == 0x0A || b == 0x0D
		if ws {
			inWord = false
		} else if !inWord {
			inWord = true
			count++
		}
	}
	fmt.Fprintln(w, count)
}
```