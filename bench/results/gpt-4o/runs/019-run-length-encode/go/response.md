```go
package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	input, err := reader.ReadString('\n')
	if err != nil {
		fmt.Print("error\n")
		return
	}

	// Remove the trailing newline character
	input = input[:len(input)-1]

	if len(input) == 0 {
		fmt.Print("error\n")
		return
	}

	for i := 0; i < len(input); i++ {
		if input[i] < 'a' || input[i] > 'z' {
			fmt.Print("error\n")
			return
		}
	}

	var result []byte
	count := 1
	for i := 1; i < len(input); i++ {
		if input[i] == input[i-1] {
			count++
		} else {
			result = append(result, input[i-1])
			result = append(result, []byte(fmt.Sprintf("%d", count))...)
			count = 1
		}
	}
	result = append(result, input[len(input)-1])
	result = append(result, []byte(fmt.Sprintf("%d", count))...)

	fmt.Printf("%s\n", result)
}
```