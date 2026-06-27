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

	if line == "" {
		return
	}

	fields := []string{}
	i := 0
	for i <= len(line) {
		if i == len(line) {
			// trailing comma produced empty field already handled below
			break
		}
		if line[i] == '"' {
			// quoted field
			i++ // skip opening quote
			var sb strings.Builder
			for i < len(line) {
				if line[i] == '"' {
					if i+1 < len(line) && line[i+1] == '"' {
						sb.WriteByte('"')
						i += 2
					} else {
						i++ // skip closing quote
						break
					}
				} else {
					sb.WriteByte(line[i])
					i++
				}
			}
			fields = append(fields, sb.String())
			// skip comma
			if i < len(line) && line[i] == ',' {
				i++
			}
		} else {
			// unquoted field
			end := strings.IndexByte(line[i:], ',')
			if end == -1 {
				fields = append(fields, line[i:])
				break
			}
			fields = append(fields, line[i:i+end])
			i += end + 1
			// if comma was last char, add empty field
			if i == len(line) {
				fields = append(fields, "")
				break
			}
		}
	}

	for _, f := range fields {
		writer.WriteString(f)
		writer.WriteByte('\n')
	}
}
```