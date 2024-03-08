package core

import (
	"log"
	"os/exec"
)

type StopCommand struct {
	ConfigFile Config
}

func (c *StopCommand) execute() (string, error) {

	cmd1 := exec.Command("docker", "compose", "-f", c.ConfigFile.ServerPath, "down")

	err1 := cmd1.Run()

	if err1 != nil {
		log.Fatal(err1)
	}

	return "", nil

}

func (c *StopCommand) checkArguments() error {
	// Set up Docker client
	return nil

}
