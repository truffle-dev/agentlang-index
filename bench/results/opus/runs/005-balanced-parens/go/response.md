```go
package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	line, _ := reader.ReadString('\n')
	stack := []byte{}
	matched := true
	for i := 0; i < len(line); i++ {
		c := line[i]
		switch c {
		case '(', '[', '{':
			stack = append(stack, c)
		case ')':
			if len(stack) == 0 || stack[len(stack)-1] != '(' {
				matched = false
			} else {
				stack = stack[:len(stack)-1]
			}
		case ']':
			if len(stack) == 0 || stack[len(stack)-1] != '[' {
				matched = false
			} else {
				stack = stack[:len(stack)-1]
			}
		case '}':
			if len(stack) == 0 || stack[len(stack)-1] != '{' {
				matched = false
			} else {
				stack = stack[:len(stack)-1]
			}
		}
	}
	if matched && len(stack) == 0 {
		fmt.Println("yes")
	} else {
		fmt.Println("no")
	}
}
```