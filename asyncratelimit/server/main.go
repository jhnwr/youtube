package main

//credits:
//https://blog.logrocket.com/rate-limiting-go-application/
//https://www.alexedwards.net/blog/how-to-rate-limit-http-requests

import (
	"encoding/json"
	"log"
	"net/http"
	"time"
)

type Message struct {
	Status string `json:"status"`
	Body   string `json:"body"`
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/", statusHandler)

	log.Print("Listening on :4000...")
	http.ListenAndServe(":4000", limit(mux))
}

func statusHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	message := Message{
		Status: "Successful",
		Body:   "please sub",
	}
	err := json.NewEncoder(w).Encode(&message)
	if err != nil {
		return
	}
	time.Sleep(1 * time.Second)
}
