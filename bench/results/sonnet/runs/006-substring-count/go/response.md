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
	writer := bufio.NewWriter(os.Stdout)
	defer writer.Flush()

	p, _ := reader.ReadString('\n')
	t, _ := reader.ReadString('\n')

	p = strings.TrimRight(p, "\r\n")
	t = strings.TrimRight(t, "\r\n")

	count := 0
	i := 0
	for i <= len(t)-len(p) {
		if t[i:i+len(p)] == p {
			count++
			i += len(p)
		} else {
			i++
		}
	}

	fmt.Fprintf(writer, "%d\n", count)
}
```