```go
package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	input, _ := reader.ReadString('\n')

	stack := []rune{}
	bracketPairs := map[rune]rune{
		')': '(',
		']': '[',
		'}': '{',
	}

	for _, char := range input {
		switch char {
		case '(', '[', '{':
			stack = append(stack, char)
		case ')', ']', '}':
			if len(stack) == 0 || stack[len(stack)-1] != bracketPairs[char] {
				fmt.Println("no")
				return
			}
			stack = stack[:len(stack)-1]
		}
	}

	if len(stack) == 0 {
		fmt.Println("yes")
	} else {
		fmt.Println("no")
	}
}
```