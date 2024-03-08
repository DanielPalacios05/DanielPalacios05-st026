package core

import (
	"log"
	"os/exec"
	"strconv"
)

type InitCommand struct {
	ConfigFile Config
}

func (c *InitCommand) execute() (string, error) {

	cmd1 := exec.Command("docker", "compose", "-f", c.ConfigFile.ServerPath, "build")
	cmd2 := exec.Command("docker", "compose", "-f", c.ConfigFile.ServerPath, "up", "-d")

	err1 := cmd1.Run()

	if err1 != nil {
		log.Fatal(err1)
	}

	err2 := cmd2.Run()

	if err2 != nil {
		log.Fatal(err2)
	}
	apiUrl := "http://" + c.ConfigFile.ListeningIP + ":" + strconv.Itoa(c.ConfigFile.ListeningPort) + "/"
	//API call to link PrimaryPeer
	linkPeer(c.ConfigFile.PrimaryPeerURL, apiUrl)

	//API call to link SecondaryPeer
	linkPeer(c.ConfigFile.SecondaryPeerURL, apiUrl)
	return "", nil

}

func (c *InitCommand) checkArguments() error {
	// Set up Docker client
	return nil

}
