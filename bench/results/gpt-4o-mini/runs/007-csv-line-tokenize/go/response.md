```go
package main

import (
	"bufio"
	"bytes"
	"fmt"
	"os"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	writer := bufio.NewWriter(os.Stdout)
	defer writer.Flush()

	line, err := reader.ReadString('\n')
	if err != nil {
		fmt.Fprint(writer, "error\n")
		return
	}

	if len(line) == 0 || line == "\n" {
		return
	}

	var fields []string
	var buffer bytes.Buffer
	inQuotes := false

	for i := 0; i < len(line); i++ {
		char := line[i]

		if char == '"' {
			inQuotes = !inQuotes
			continue
		}

		if char == ',' && !inQuotes {
			fields = append(fields, buffer.String())
			buffer.Reset()
			continue
		}

		if char != '\n' {
			buffer.WriteByte(char)
		}
	}

	fields = append(fields, buffer.String())

	for _, field := range fields {
		field = bytes.ReplaceAll([]byte(field), []byte{'"'}, []byte{}).String()
		fmt.Fprintln(writer, field)
	}
}
```