package core

import (
	"encoding/json"
	"errors"
	"strconv"
)

type ListCommand struct {
	ConfigFile   Config
	ObjectToList string
}

func (c *ListCommand) execute() (string, error) {

	if c.ObjectToList == "peers" {

		peerList := listFetchedPeers("http://" + c.ConfigFile.ListeningIP + ":" + strconv.Itoa(c.ConfigFile.ListeningPort) + "/")
		resultString, _ := json.Marshal(peerList)

		return string(resultString), nil

	} else if c.ObjectToList == "files" {

		fileList := listFiles("http://" + c.ConfigFile.ListeningIP + ":" + strconv.Itoa(c.ConfigFile.ListeningPort) + "/")
		resultString, _ := json.Marshal(fileList)
		return string(resultString), nil
	}

	return "", errors.New("invalid parameter")

}

func (c *ListCommand) checkArguments() error {
	// Set up Docker client
	return nil

}
