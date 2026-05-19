```go
package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	writer := bufio.NewWriter(os.Stdout)

	input, err := reader.ReadString('\n')
	if err != nil || len(input) == 0 {
		writer.WriteString("error\n")
		writer.Flush()
		return
	}

	if !isValidInput(input) {
		writer.WriteString("error\n")
		writer.Flush()
		return
	}

	result := runLengthEncode(input)
	writer.WriteString(result + "\n")
	writer.Flush()
}

func isValidInput(s string) bool {
	for _, ch := range s {
		if ch < 'a' || ch > 'z' {
			return false
		}
	}
	return true
}

func runLengthEncode(s string) string {
	var result string
	count := 1

	for i := 1; i < len(s); i++ {
		if s[i] == s[i-1] {
			count++
		} else {
			result += string(s[i-1]) + fmt.Sprint(count)
			count = 1
		}
	}
	result += string(s[len(s)-1]) + fmt.Sprint(count)

	return result
}
```