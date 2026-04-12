package main

import (
	"os"
)

func main() {
	file, err := os.Create(os.Getenv("HOME") + "/Desktop/hello.txt")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	_, err = file.WriteString("hello world")
	if err != nil {
		panic(err)
	}
}
