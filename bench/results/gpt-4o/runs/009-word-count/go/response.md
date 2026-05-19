```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"unicode"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	input, err := reader.ReadString(0)
	if err != nil && err.Error() != "EOF" {
		fmt.Println("error")
		return
	}

	wordCount := 0
	inWord := false

	for _, r := range input {
		if unicode.IsSpace(r) {
			if inWord {
				inWord = false
			}
		} else {
			if !inWord {
				inWord = true
				wordCount++
			}
		}
	}

	fmt.Printf("%d\n", wordCount)
}
```