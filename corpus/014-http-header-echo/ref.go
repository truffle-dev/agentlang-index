package main

import (
	"bufio"
	"context"
	"fmt"
	"net/http"
	"os"
	"strings"
	"time"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	url, err := reader.ReadString('\n')
	if err != nil && url == "" {
		fmt.Print("error\n")
		return
	}
	name, err2 := reader.ReadString('\n')
	if err2 != nil && name == "" {
		fmt.Print("error\n")
		return
	}
	url = strings.TrimRight(url, "\r\n \t")
	url = strings.TrimSpace(url)
	name = strings.TrimSpace(name)
	if url == "" || name == "" {
		fmt.Print("error\n")
		return
	}
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
	if err != nil {
		fmt.Print("error\n")
		return
	}
	client := &http.Client{
		CheckRedirect: func(*http.Request, []*http.Request) error {
			return http.ErrUseLastResponse
		},
	}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Print("error\n")
		return
	}
	defer resp.Body.Close()
	if resp.StatusCode != 200 {
		fmt.Print("error\n")
		return
	}
	value := resp.Header.Get(name)
	if value == "" {
		// Distinguish "missing" from "present and empty" — Go's
		// canonical Get returns "" for both. Check Values() instead.
		values := resp.Header.Values(name)
		if len(values) == 0 {
			fmt.Print("error\n")
			return
		}
		value = values[0]
	}
	fmt.Print(value + "\n")
}
