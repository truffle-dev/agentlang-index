```go
package main

import (
	"bufio"
	"os"
	"strings"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	writer := bufio.NewWriter(os.Stdout)
	defer writer.Flush()

	line, _ := reader.ReadString('\n')
	words := strings.Fields(line)

	if len(words) == 0 {
		return
	}

	for i := len(words) - 1; i > 0; i-- {
		writer.WriteString(words[i] + " ")
	}
	writer.WriteString(words[0] + "\n")
}
```