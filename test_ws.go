package main

import (
	"fmt"
	"log"
	"time"

	"github.com/gorilla/websocket"
)

func main() {
	c, _, err := websocket.DefaultDialer.Dial("ws://localhost:8080/ws/sandbox/vtysh", nil)
	if err != nil {
		log.Fatal("dial:", err)
	}
	defer c.Close()

	// Read messages
	go func() {
		for {
			_, message, err := c.ReadMessage()
			if err != nil {
				fmt.Println("read error:", err)
				return
			}
			fmt.Printf("recv: %s", message)
		}
	}()

	time.Sleep(1 * time.Second)
	fmt.Println("Sending show version...")
	c.WriteMessage(websocket.TextMessage, []byte("show version\n"))
	
	time.Sleep(2 * time.Second)
	c.WriteMessage(websocket.TextMessage, []byte("exit\n"))
	time.Sleep(1 * time.Second)
}
