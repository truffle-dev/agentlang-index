```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	w := bufio.NewWriter(os.Stdout)
	defer w.Flush()

	p, _ := reader.ReadString('\n')
	t, _ := reader.ReadString('\n')
	p = strings.TrimRight(p, "\r\n")
	t = strings.TrimRight(t, "\r\n")

	count := 0
	pLen := len(p)
	for i := 0; i <= len(t)-pLen; {
		if t[i:i+pLen] == p {
			count++
			i += pLen
		} else {
			i++
		}
	}
	fmt.Fprintln(w, count)
}
```