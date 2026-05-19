```go
package main

import (
	"bufio"
	"os"
)

func main() {
	in := bufio.NewReader(os.Stdin)
	out := bufio.NewWriter(os.Stdout)
	defer out.Flush()

	line, _ := in.ReadString('\n')

	stack := make([]byte, 0, 16)
	match := func(open, close byte) bool {
		return (open == '(' && close == ')') ||
			(open == '[' && close == ']') ||
			(open == '{' && close == '}')
	}

	for i := 0; i < len(line); i++ {
		c := line[i]
		switch c {
		case '(', '[', '{':
			stack = append(stack, c)
		case ')', ']', '}':
			if len(stack) == 0 {
				out.WriteString("no\n")
				return
			}
			top := stack[len(stack)-1]
			if !match(top, c) {
				out.WriteString("no\n")
				return
			}
			stack = stack[:len(stack)-1]
		default:
			// ignore all other characters, including '\n'
		}
	}

	if len(stack) == 0 {
		out.WriteString("yes\n")
	} else {
		out.WriteString("no\n")
	}
}
```