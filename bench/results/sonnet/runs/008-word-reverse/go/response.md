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
	line = strings.TrimRight(line, "\n")

	words := strings.Fields(line)
	if len(words) == 0 {
		return
	}

	for i, j := 0, len(words)-1; i < j; i, j = i+1, j-1 {
		words[i], words[j] = words[j], words[i]
	}

	writer.WriteString(strings.Join(words, " ") + "\n")
}
```