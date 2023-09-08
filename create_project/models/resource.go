package models

import (
	"bytes"
	"encoding/base64"
	"fmt"
	"net/http"
	"encoding/json"
)

type Ttr struct {
	Namespacess string
	Deploys     string
}

type RepositoryCreateRequest struct {
	Name        string `json:"name"`
	ProjectName string `json:"project_name"`
	Public      bool   `json:"public"`
}

func (u *Ttr) GreateRepository(apiURL, projectName, repositoryName, username, password string) error {
	// 构建请求体
	requestData := RepositoryCreateRequest{
		Name:        repositoryName,
		ProjectName: projectName,
		Public:      false,
	}

	// 将请求体转换为JSON
	jsonData, err := json.Marshal(requestData)
	if err != nil {
		return err
	}

	// 发送POST请求
	client := &http.Client{}
	req, err := http.NewRequest("POST", fmt.Sprintf("%s/api/v2.0/projects", apiURL), bytes.NewBuffer(jsonData))
	if err != nil {
		return err
	}
	req.Header.Set("Content-Type", "application/json")

	// 构建用户名和密码的字符串，并进行Base64编码
	auth := base64.StdEncoding.EncodeToString([]byte(username + ":" + password))

	// 设置请求头中的Authorization字段为Basic认证
	req.Header.Set("Authorization", "Basic "+auth)

	resp, err := client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	return nil
}

func (u *Ttr) GrantUserPermission(apiURL, projectName, username, password string) error {
	// 构建请求体
	requestData := map[string]interface{}{
		"role_id": 2,
		"member_user": map[string]interface{}{
			"username": "username",
		},
	}
	// 将请求体转换为JSON
	jsonData, err := json.Marshal(requestData)
	if err != nil {
		return err
	}

	// 发送POST请求
	client := &http.Client{}
	req, err := http.NewRequest("POST", fmt.Sprintf("%s/api/v2.0/projects/%s/members", apiURL, projectName), bytes.NewBuffer(jsonData))
	if err != nil {
		return err
	}
	req.Header.Set("Content-Type", "application/json")

	// 构建用户名和密码的字符串，并进行Base64编码
	auth := base64.StdEncoding.EncodeToString([]byte(username + ":" + password))

	// 设置请求头中的Authorization字段为Basic认证
	req.Header.Set("Authorization", "Basic "+auth)

	resp, err := client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	return nil
}
