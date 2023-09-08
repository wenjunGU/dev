package models

import (
        "flag"
        "k8s.io/client-go/kubernetes"
        "k8s.io/client-go/tools/clientcmd"
)

func Client_wx() *kubernetes.Clientset {
        kubeconfig := flag.String("kubeconfig", "/data/app/k8s-report/wx-conf/config", "(optional) absolute path to the kubeconfig file")
        flag.Parse()

        // 解析到config
        config, err := clientcmd.BuildConfigFromFlags("", *kubeconfig)
        if err != nil {
                panic(err.Error())
        }

        // 创建连接
        clientset, err := kubernetes.NewForConfig(config)
        if err != nil {
                panic(err.Error())
        }
        return clientset
}
