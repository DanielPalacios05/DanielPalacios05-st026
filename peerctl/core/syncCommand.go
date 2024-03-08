package core

import (
	"os"
	"path/filepath"
	"strconv"
)

type SyncCommand struct {
	ConfigFile   Config
	ObjectToSync string
}

type File struct {
	Filename string `json:"filename"`
	Filepath string `json:"filepath"`
}

func (c *SyncCommand) execute() (string, error) {

	var fileList []File

	if c.ObjectToSync == "files" {

		err := filepath.Walk(c.ConfigFile.SharedDir, func(path string, info os.FileInfo, err error) error {
			if err != nil {
				return err
			}
			if !info.IsDir() {
				file := File{Filename: info.Name(), Filepath: path}
				fileList = append(fileList, file)

			}
			return nil
		})

		if err != nil {
			return "", err
		}
		response, err := syncFiles("http://"+c.ConfigFile.ListeningIP+":"+strconv.Itoa(c.ConfigFile.ListeningPort)+"/", fileList)

		return response, err

	}

	return "", nil

}

func (c *SyncCommand) checkArguments() error {
	// Set up Docker client
	return nil

}
