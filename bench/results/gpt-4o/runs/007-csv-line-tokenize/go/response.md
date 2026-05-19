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
	line, _ := reader.ReadString('\n')
	line = strings.TrimSuffix(line, "\n")

	if line == "" {
		return
	}

	var fields []string
	var currentField strings.Builder
	inQuotes := false
	i := 0

	for i < len(line) {
		char := line[i]

		if inQuotes {
			if char == '"' {
				if i+1 < len(line) && line[i+1] == '"' {
					currentField.WriteByte('"')
					i++
				} else {
					inQuotes = false
				}
			} else {
				currentField.WriteByte(char)
			}
		} else {
			if char == ',' {
				fields = append(fields, currentField.String())
				currentField.Reset()
			} else if char == '"' {
				inQuotes = true
			} else {
				currentField.WriteByte(char)
			}
		}
		i++
	}

	fields = append(fields, currentField.String())

	writer := bufio.NewWriter(os.Stdout)
	for _, field := range fields {
		fmt.Fprintln(writer, field)
	}
	writer.Flush()
}
```