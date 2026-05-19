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

	input, _ := reader.ReadString('\n')
	stack := []rune{}

	for _, char := range input {
		switch char {
		case '(', '[', '{':
			stack = append(stack, char)
		case ')':
			if len(stack) == 0 || stack[len(stack)-1] != '(' {
				fmt.Fprint(writer, "no\n")
				return
			}
			stack = stack[:len(stack)-1]
		case ']':
			if len(stack) == 0 || stack[len(stack)-1] != '[' {
				fmt.Fprint(writer, "no\n")
				return
			}
			stack = stack[:len(stack)-1]
		case '}':
			if len(stack) == 0 || stack[len(stack)-1] != '{' {
				fmt.Fprint(writer, "no\n")
				return
			}
			stack = stack[:len(stack)-1]
		}
	}

	if len(stack) == 0 {
		fmt.Fprint(writer, "yes\n")
	} else {
		fmt.Fprint(writer, "no\n")
	}
}
```