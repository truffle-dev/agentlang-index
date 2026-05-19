```go
package main

import (
	"bufio"
	"os"
	"strings"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	input, _ := reader.ReadString(0)
	words := strings.Fields(input)
	count := len(words)
	writer := bufio.NewWriter(os.Stdout)
	writer.WriteString(string(count) + "\n")
	writer.Flush()
}
```