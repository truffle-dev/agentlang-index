```go
package main

import (
	"bufio"
	"io"
	"os"
)

func main() {
	in := bufio.NewReader(os.Stdin)
	out := bufio.NewWriter(os.Stdout)

	data, _ := io.ReadAll(in)
	line := string(data)
	if len(line) > 0 && line[len(line)-1] == '\n' {
		line = line[:len(line)-1]
	}

	words := make([]string, 0, 16)
	n := len(line)
	i := 0
	for i < n {
		// Skip spaces
		for i < n && line[i] == ' ' {
			i++
		}
		if i >= n {
			break
		}
		// Collect word
		j := i
		for j < n && line[j] != ' ' {
			j++
		}
		words = append(words, line[i:j])
		i = j
	}

	if len(words) > 0 {
		// Reverse words
		for l, r := 0, len(words)-1; l < r; l, r = l+1, r-1 {
			words[l], words[r] = words[r], words[l]
		}
		// Write output
		for idx, w := range words {
			if idx > 0 {
				_, _ = out.Write([]byte(" "))
			}
			_, _ = out.WriteString(w)
		}
		_, _ = out.Write([]byte("\n"))
	}

	_ = out.Flush()
}
```