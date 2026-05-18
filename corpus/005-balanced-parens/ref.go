// Balanced bracket checker, Go reference.
// Reads one line of printable ASCII (up to 1000 chars), prints `yes` or `no`.

package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	line, _ := reader.ReadString('\n')
	line = strings.TrimRight(line, "\n")
	stack := make([]byte, 0, 1024)
	balanced := true
	for i := 0; i < len(line); i++ {
		ch := line[i]
		switch ch {
		case '(', '[', '{':
			stack = append(stack, ch)
		case ')':
			if len(stack) == 0 || stack[len(stack)-1] != '(' {
				balanced = false
			} else {
				stack = stack[:len(stack)-1]
			}
		case ']':
			if len(stack) == 0 || stack[len(stack)-1] != '[' {
				balanced = false
			} else {
				stack = stack[:len(stack)-1]
			}
		case '}':
			if len(stack) == 0 || stack[len(stack)-1] != '{' {
				balanced = false
			} else {
				stack = stack[:len(stack)-1]
			}
		}
		if !balanced {
			break
		}
	}
	if balanced && len(stack) == 0 {
		fmt.Print("yes\n")
	} else {
		fmt.Print("no\n")
	}
}
