package main

import (
        "resource/models"
        "github.com/gin-gonic/gin"
        "net"
        "net/http"
)

var qs = models.Ttr{}

func Settings(c *gin.Context) {
        //auth := c.PostFormMap("auth")
        //id := c.DefaultPostForm("id","8")
        pod_ip := c.Query("ip")
        address := net.ParseIP(pod_ip)
        if address != nil {
                Segment := pod_ip[3:6]
                if Segment == "204" {
                        c.JSON(200, gin.H{
                                "status": http.StatusOK,
                                "Ip:Name":   qs.Get_pods_xhy(pod_ip),
                        })
                } else if Segment == "208" {
                        c.JSON(200, gin.H{
                                "status": http.StatusOK,
                                "Ip:Name":   qs.Get_pods_wx(pod_ip),
                        })
                } else {
                        c.JSON(200, gin.H{
                                "status": http.StatusOK,
                                "iddr":   "Non-k8s network segment",
                        })
                }
        } else {
                c.JSON(200, gin.H{
                        "status": http.StatusOK,
                        "iddr":   "Invalid ip address",
                })
        }
}

func main() {
        router := gin.Default()
        router.Use(gin.Recovery())
        //路由分组
        v1 := router.Group("/v1")
        {
                //调用方法
                v1.POST("/ips", Settings)
                v1.GET("/ips",Settings)
        }
        router.Run(":8000")
}
