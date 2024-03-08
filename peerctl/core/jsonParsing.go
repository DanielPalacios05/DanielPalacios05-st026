package core

import (
	"encoding/json"
	"fmt"

	"io"
	"os"
)

// Config represents the configuration settings for a peer
type Config struct {
	ListeningIP      string `json:"listening_ip"`
	ListeningPort    int    `json:"listening_port"`
	SharedDir        string `json:"shared_dir"`
	DownloadDir      string `json:"download_dir"`
	ServerPath       string `json:"server_path"`
	PrimaryPeerURL   string `json:"primary_peer_url"`
	SecondaryPeerURL string `json:"secondary_peer_url"`
}

func parseJson(configFilePath string) Config {
	// Read the JSON configuration file
	jsonFile, err := os.Open(configFilePath)
	if err != nil {
		fmt.Println(err)
	}
	defer jsonFile.Close()

	byteValue, _ := io.ReadAll(jsonFile)

	var config Config
	json.Unmarshal(byteValue, &config)

	return config
}
