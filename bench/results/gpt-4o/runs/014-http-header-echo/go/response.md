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
	url, _ := reader.ReadString('\n')
	headerName, _ := reader.ReadString('\n')

	url = strings.TrimSpace(url)
	headerName = strings.TrimSpace(headerName)

	client := &http.Client{
		Timeout: 5 * time.Second,
	}

	resp, err := client.Get(url)
	if err != nil || resp.StatusCode != http.StatusOK {
		fmt.Println("error")
		return
	}
	defer resp.Body.Close()

	headerValue := resp.Header.Get(headerName)
	if headerValue == "" {
		fmt.Println("error")
		return
	}

	fmt.Println(headerValue)
}
```