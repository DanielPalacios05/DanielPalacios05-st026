package core

import (
	"encoding/json"

	"strconv"
)

type FetchCommand struct {
	ConfigFile Config
}

func (c *FetchCommand) execute() (string, error) {

	apiUrl := "http://" + c.ConfigFile.ListeningIP + ":" + strconv.Itoa(c.ConfigFile.ListeningPort) + "/"

	result, _ := json.Marshal(fetchPeers(apiUrl))

	return string(result), nil
}

func (c *FetchCommand) checkArguments() error {
	// Set up Docker client
	return nil

}
