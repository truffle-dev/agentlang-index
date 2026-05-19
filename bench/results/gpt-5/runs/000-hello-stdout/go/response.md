```go
package main

import (
	"bufio"
	"os"
)

func main() {
	_ = bufio.NewReader(os.Stdin)
	w := bufio.NewWriter(os.Stdout)
	_, _ = w.WriteString("hello\n")
	_ = w.Flush()
}
```