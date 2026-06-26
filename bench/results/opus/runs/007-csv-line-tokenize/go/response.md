```go
package main

import (
	"bufio"
	"os"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	line, _ := reader.ReadString('\n')
	// Strip trailing newline
	if len(line) > 0 && line[len(line)-1] == '\n' {
		line = line[:len(line)-1]
	}
	if len(line) == 0 {
		return
	}

	w := bufio.NewWriter(os.Stdout)
	defer w.Flush()

	i := 0
	for {
		var field []byte
		if i < len(line) && line[i] == '"' {
			i++ // skip opening quote
			for i < len(line) {
				if line[i] == '"' {
					if i+1 < len(line) && line[i+1] == '"' {
						field = append(field, '"')
						i += 2
					} else {
						i++ // skip closing quote
						break
					}
				} else {
					field = append(field, line[i])
					i++
				}
			}
		} else {
			for i < len(line) && line[i] != ',' {
				field = append(field, line[i])
				i++
			}
		}
		w.Write(field)
		w.WriteByte('\n')
		if i >= len(line) {
			break
		}
		i++ // skip comma
	}
}
```