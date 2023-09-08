package models

import (
        _ "fmt"
        metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
        "log"
)

var api_xhy = Client_xhy()
var api_wx = Client_wx()

type Ttr struct {
        Namespacess string
        Deploys     string
}

func (u *Ttr) Get_pods_wx(ips string) string {
        pods, err := api_wx.CoreV1().Pods("").List(metav1.ListOptions{})
        if err != nil {
                log.Println(err.Error())
        }
        for _, pod := range pods.Items {
                if ips == pod.Status.PodIP {
                        return pod.Status.PodIP + ":" + pod.Name
                }
        }
        return "404 Not Found"
}

func (u *Ttr) Get_pods_xhy(ips string) string {
        pods, err := api_xhy.CoreV1().Pods("").List(metav1.ListOptions{})
        if err != nil {
                log.Println(err.Error())
        }
        for _, pod := range pods.Items {
                if ips == pod.Status.PodIP {
                        return pod.Status.PodIP + ":" + pod.Name
                }
        }
        return "404 Not Found"
}
