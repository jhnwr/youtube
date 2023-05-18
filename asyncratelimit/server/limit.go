package main

import (
	"encoding/json"
	"net/http"

	"golang.org/x/time/rate"
)

var limiter = rate.NewLimiter(200, 50)


func limit(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if limiter.Allow() == false {
			message := Message{
				Status: "Error",
				Body:   "Too Many Requests",
			}

			w.Header().Set("Content-Type", "application/json")
			w.WriteHeader(http.StatusTooManyRequests)
			json.NewEncoder(w).Encode(&message)
			return
		}

		next.ServeHTTP(w, r)
	})
}
