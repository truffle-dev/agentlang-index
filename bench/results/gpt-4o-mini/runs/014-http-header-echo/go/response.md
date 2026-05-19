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

	client := http.Client{
		Timeout: 5 * time.Second,
	}

	resp, err := client.Get(url)
	if err != nil {
		fmt.Print("error\n")
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		fmt.Print("error\n")
		return
	}

	for name, values := range resp.Header {
		if strings.EqualFold(name, headerName) {
			fmt.Print(strings.Join(values, ", ") + "\n")
			return
		}
	}

	fmt.Print("error\n")
}
```