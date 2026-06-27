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
	defer writer.Flush()

	line, _ := reader.ReadString('\n')

	stack := []rune{}
	match := map[rune]rune{')': '(', ']': '[', '}': '{'}
	openers := map[rune]bool{'(': true, '[': true, '{': true}

	balanced := true
	for _, ch := range line {
		if openers[ch] {
			stack = append(stack, ch)
		} else if open, ok := match[ch]; ok {
			if len(stack) == 0 || stack[len(stack)-1] != open {
				balanced = false
				break
			}
			stack = stack[:len(stack)-1]
		}
	}

	if balanced && len(stack) == 0 {
		fmt.Fprintln(writer, "yes")
	} else {
		fmt.Fprintln(writer, "no")
	}
}
```