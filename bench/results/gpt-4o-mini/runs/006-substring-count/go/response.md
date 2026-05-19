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
	pattern, _ := reader.ReadString('\n')
	text, _ := reader.ReadString('\n')

	pattern = strings.TrimSpace(pattern)
	text = strings.TrimSpace(text)

	count := 0
	patternLen := len(pattern)
	textLen := len(text)

	for i := 0; i <= textLen-patternLen; {
		if text[i:i+patternLen] == pattern {
			count++
			i += patternLen
		} else {
			i++
		}
	}

	fmt.Println(count)
}
```