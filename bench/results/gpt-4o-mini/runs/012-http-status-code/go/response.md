```go
package main

import (
	"bufio"
	"fmt"
	"net/http"
	"os"
	"time"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	url, err := reader.ReadString('\n')
	if err != nil {
		fmt.Print("error\n")
		return
	}

	url = url[:len(url)-1] // Trim the trailing newline

	client := http.Client{
		Timeout: 5 * time.Second,
	}

	resp, err := client.Get(url)
	if err != nil {
		fmt.Print("error\n")
		return
	}
	defer resp.Body.Close()

	fmt.Printf("%d\n", resp.StatusCode)
}
```