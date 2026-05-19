```go
package main

import (
	"bufio"
	"os"
)

func main() {
	writer := bufio.NewWriter(os.Stdout)
	writer.WriteString("hello\n")
	writer.Flush()
}
```