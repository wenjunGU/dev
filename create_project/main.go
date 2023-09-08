package main

import (
	"resource/models"
	"github.com/gin-gonic/gin"
	"net/http"
)

var qs = models.Ttr{}

type RequestBody struct {
	Project  string `json:"project"`
	Password string `json:"password"`
}
func Createing(c *gin.Context) {
	var requestBody RequestBody

	if err := c.ShouldBindJSON(&requestBody); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": err.Error(),
		})
		return
	}

	projectName := requestBody.Project
	repositoryName := requestBody.Project
	password := c.GetHeader("token")
	if projectName != "" && password != "" {
		err := qs.GreateRepository("http://harbor.internal.zenmen.com", projectName, repositoryName, "halo_op", password)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{
				"error": err.Error(),
			})
			return
		}
		c.JSON(http.StatusOK, gin.H{
			"status":  http.StatusOK,
			"Project": "Create Successful",
		})
	}
}


func main() {
    //gin.SetMode(gin.ReleaseMode)
    //router := gin.New()
    router := gin.Default()
    router.Use(gin.Recovery())
    // 路由分组
    v1 := router.Group("/api")
    {
        // 调用方法
        v1.POST("/create", Createing)
        v1.GET("/create", Createing)
    }
    router.Run(":8000")
}
