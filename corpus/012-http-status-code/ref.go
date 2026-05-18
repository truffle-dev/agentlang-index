package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
	"time"
)

func main() {
	urlBytes, err := io.ReadAll(os.Stdin)
	if err != nil {
		os.Stdout.WriteString("error\n")
		return
	}
	url := strings.TrimSpace(string(urlBytes))

	client := &http.Client{
		Timeout: 5 * time.Second,
		CheckRedirect: func(req *http.Request, via []*http.Request) error {
			return http.ErrUseLastResponse
		},
	}
	resp, err := client.Get(url)
	if err != nil {
		os.Stdout.WriteString("error\n")
		return
	}
	defer resp.Body.Close()
	fmt.Printf("%d\n", resp.StatusCode)
}
