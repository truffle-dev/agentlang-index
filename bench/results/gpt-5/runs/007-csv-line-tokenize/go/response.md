```go
package main

import (
	"bufio"
	"os"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	writer := bufio.NewWriter(os.Stdout)

	line, _ := reader.ReadString('\n')
	// Remove trailing '\n' if present
	if len(line) > 0 && line[len(line)-1] == '\n' {
		line = line[:len(line)-1]
	}

	s := line
	n := len(s)

	// If the input line is empty, write nothing.
	if n == 0 {
		writer.Flush()
		return
	}

	fields := make([]string, 0, 8)
	var b []byte
	inQuotes := false

	for i := 0; i < n; {
		c := s[i]
		if inQuotes {
			if c == '"' {
				// Check for escaped quote
				if i+1 < n && s[i+1] == '"' {
					b = append(b, '"')
					i += 2
					continue
				}
				// Closing quote
				inQuotes = false
				i++
				continue
			}
			b = append(b, c)
			i++
			continue
		}

		// Not in quotes
		if c == '"' && len(b) == 0 {
			inQuotes = true
			i++
			continue
		}
		if c == ',' {
			fields = append(fields, string(b))
			b = b[:0]
			i++
			continue
		}
		b = append(b, c)
		i++
	}

	// Append the last field (may be empty)
	fields = append(fields, string(b))

	for _, f := range fields {
		writer.WriteString(f)
		writer.WriteByte('\n')
	}

	writer.Flush()
}
```