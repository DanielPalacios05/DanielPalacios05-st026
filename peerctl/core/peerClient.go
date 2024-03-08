package core

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
)

type Peer struct {
	Host   string `json:"host"`
	Port   int    `json:"port"`
	ToLink int    `json:"toLink"`
}

type FetchingInfo struct {
	PeersFetched int `json:"peersFetched"`
	FilesFetched int `json:"filesFetched"`
}

func linkPeer(peerUrl string, apiUrl string) {

	peer := struct {
		PeerUrl string `json:"peerUrl"`
		ToLink  int    `json:"toLink"`
	}{PeerUrl: peerUrl, ToLink: 1}

	jsonReq, _ := json.Marshal(peer)
	fmt.Println(string(jsonReq))
	resp, err := http.Post(apiUrl+"peers/", "application/json; charset=utf-8", bytes.NewBuffer(jsonReq))

	if err != nil {
		log.Fatalln(err)
	}

	defer resp.Body.Close()
	bodyBytes, _ := io.ReadAll(resp.Body)

	fmt.Println(string(bodyBytes))

}

func listFetchedPeers(apiUrl string) []Peer {
	var peerList []Peer
	resp, err := http.Get(apiUrl + "peers/")
	if err != nil {
		log.Fatalln(err)
	}

	defer resp.Body.Close()
	bodyBytes, _ := io.ReadAll(resp.Body)

	json.Unmarshal(bodyBytes, &peerList)

	return peerList

}

func fetchPeers(apiUrl string) FetchingInfo {

	var fetchingInfo FetchingInfo

	resp, err := http.Get(apiUrl + "fetch/peers")

	if err != nil {
		log.Fatalln(err)
	}

	defer resp.Body.Close()
	bodyBytes, _ := io.ReadAll(resp.Body)

	json.Unmarshal(bodyBytes, &fetchingInfo)

	return fetchingInfo

}

func syncFiles(apiUrl string, fileList []File) (string, error) {

	jsonBody, _ := json.Marshal(fileList)

	resp, err := http.Post(apiUrl+"files/", "application/json; charset=utf-8", bytes.NewBuffer(jsonBody))
	if err != nil {
		log.Fatalln("error en syncFiles ", err)
	}

	defer resp.Body.Close()
	bodyBytes, _ := io.ReadAll(resp.Body)

	return string(bodyBytes), nil

}

func listFiles(apiUrl string) []File {

	var fileList []File
	resp, err := http.Get(apiUrl + "files/")
	if err != nil {
		log.Fatalln(err)
	}

	defer resp.Body.Close()
	bodyBytes, _ := io.ReadAll(resp.Body)

	json.Unmarshal(bodyBytes, &fileList)
	return fileList

}
