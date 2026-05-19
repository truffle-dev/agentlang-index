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

	// Trim the newline characters from the input
	pattern = strings.TrimSpace(pattern)
	text = strings.TrimSpace(text)

	patternLength := len(pattern)
	textLength := len(text)

	count := 0
	for i := 0; i <= textLength-patternLength; {
		if text[i:i+patternLength] == pattern {
			count++
			i += patternLength
		} else {
			i++
		}
	}

	fmt.Printf("%d\n", count)
}
```