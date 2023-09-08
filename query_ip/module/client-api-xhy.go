package models

import (
        "flag"
        "k8s.io/client-go/kubernetes"
        "k8s.io/client-go/tools/clientcmd"
)

func Client_xhy() *kubernetes.Clientset {
        kubeconfigs := flag.String("kubeconfigs", "/data/app/k8s-report/xhy-conf/config", "(optional) absolute path to the kubeconfig file")
        flag.Parse()

        // 解析到config
        configs, err := clientcmd.BuildConfigFromFlags("", *kubeconfigs)
        if err != nil {
                panic(err.Error())
        }

        // 创建连接
        clientsets, err := kubernetes.NewForConfig(configs)
        if err != nil {
                panic(err.Error())
        }
        return clientsets
}
