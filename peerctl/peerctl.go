package main

import (
	"encoding/json"
	"fmt"
	"io"
	"os"

	core "peerctl/core"
)

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

func main() {

	var configJson Config = parseJson("./peerConfig.json")

	numArgs := len(os.Args)

	if numArgs < 2 {
		fmt.Println("peerctl help")
		return
	}
	var initController core.Controller

	mainCommand := os.Args[1]

	if mainCommand == "init" {

		initController.MainCommand = &core.InitCommand{
			ConfigFile: core.Config(configJson),
		}

		_, err := initController.Init()
		if err == nil {
			fmt.Println(configJson)
		} else {
			panic(err)
		}

	} else if mainCommand == "stop" {
		initController.MainCommand = &core.StopCommand{
			ConfigFile: core.Config(configJson),
		}

		_, err := initController.Init()
		if err == nil {
			fmt.Println(configJson)
		} else {
			panic(err)
		}

	} else if mainCommand == "list" {
		initController.MainCommand = &core.ListCommand{
			ConfigFile:   core.Config(configJson),
			ObjectToList: os.Args[2],
		}

		resultString, err := initController.Init()
		if err == nil {
			fmt.Println(resultString)
		} else {
			panic(err)
		}

	} else if mainCommand == "fetch" {
		initController.MainCommand = &core.FetchCommand{
			ConfigFile: core.Config(configJson),
		}

		resultString, err := initController.Init()
		if err == nil {
			fmt.Println(resultString)
		} else {
			panic(err)
		}

	} else if mainCommand == "sync" {
		initController.MainCommand = &core.SyncCommand{
			ConfigFile:   core.Config(configJson),
			ObjectToSync: os.Args[2],
		}

		resultString, err := initController.Init()
		if err == nil {
			fmt.Println(resultString)
		} else {
			panic(err)
		}

	}

}
