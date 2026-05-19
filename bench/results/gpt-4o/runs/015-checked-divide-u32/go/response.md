```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	reader := bufio.NewReader(os.Stdin)

	// Read first line
	line1, err := reader.ReadString('\n')
	if err != nil {
		fmt.Print("error\n")
		return
	}
	line1 = strings.TrimSpace(line1)

	// Read second line
	line2, err := reader.ReadString('\n')
	if err != nil {
		fmt.Print("error\n")
		return
	}
	line2 = strings.TrimSpace(line2)

	// Parse first number
	a, err := parseU32(line1)
	if err != nil {
		fmt.Print("error\n")
		return
	}

	// Parse second number
	b, err := parseU32(line2)
	if err != nil || b == 0 {
		fmt.Print("error\n")
		return
	}

	// Compute and print the result
	fmt.Printf("%d\n", a/b)
}

func parseU32(s string) (uint32, error) {
	if s == "" {
		return 0, fmt.Errorf("empty string")
	}
	num, err := strconv.ParseUint(s, 10, 32)
	if err != nil {
		return 0, err
	}
	return uint32(num), nil
}
```