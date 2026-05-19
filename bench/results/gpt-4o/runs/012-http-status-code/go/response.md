```go
package main

import (
	"bufio"
	"fmt"
	"net/http"
	"os"
	"strings"
	"time"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	url, err := reader.ReadString('\n')
	if err != nil {
		fmt.Println("error")
		return
	}
	url = strings.TrimSpace(url)

	client := &http.Client{
		Timeout: 5 * time.Second,
	}

	resp, err := client.Get(url)
	if err != nil {
		fmt.Println("error")
		return
	}
	defer resp.Body.Close()

	fmt.Println(resp.StatusCode)
}
```