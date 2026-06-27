```go
package main

import (
	"bufio"
	"os"
)

func main() {
	w := bufio.NewWriter(os.Stdout)
	w.WriteString("hello\n")
	w.Flush()
}
```