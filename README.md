# 云原生API参考

【以下k8s相关均为使用原生API，需带入k8s集群的config认证文件，并授权相关的serviceaccount。在kubernetes2.0以上版本，获取node资源API已不兼容，需要做相关修改】
一：create_project
该接口为harbor项目的创建作用，POST调用。其中代码中写死了私仓地址以及授权的用户，
需要更改使用，或者将授权用户改为参数传递。调用时需要在header头中传递用户密码

二：query_ip
该接口为根据pod ip查询对应的pod名称，适用于大规模情况下快速问题定位使用，也可配合
监控使用，GET调用，直接参数传递ip=xxx

三：query_iplist
该接口为根据deploy,statefullset,daemonset等对象名称，获取到资源下所有pod的
ip集合，其中/v1/list获取单个地址，/v2/list获取ip集合，建议使用v2。POST调用

四：dynamic-schedul
该项目是模仿网易方舟编写的一个pod动态调度模块,使用时需带入如下环境变量：
label	pod绑定的标签	string	no	如不设置该变量，则被调度对象为集群内所有Pod
url	告警发送地址	string	yes	
apikey	告警地址认证	string	yes	
values	资源阈值，为cpu以及memory的百分比	int	yes	通常设置在80
run_time	检测时长间隔	int	no	建议必须设置，且大于等于10「单位为s」，否则集群规模大易引起api超时

五：clouster-resource
该项目为获取k8s集群下All资源的项目，k8s集群默认资源计算使用比、k8s集群默认资源计算使用量、
k8s集群真实资源剩余量，并支持多种查询方式组合使用。POST调用
##获取当前集群空闲负载值
curl -s -d type={cpu or memory} http://ip:8888/v1/resource
 
##获取当前集群空闲负载百分比
curl -s -d type={cpu or memory} http://ip:8888/v2/resource
 
##获取当前集群实际未分配值
curl -s -d type={cpu or memory or all} http://ip:8888/v3/resource
 
##获取当前集群指定node空闲负载值
curl -s -d type={cpu or memory} -d node={x.x.x.x or x.x.x.x,x.x.x.x} http://ip:8888/v1/resource
 
##获取当前集群指定node空闲负载百分比
curl -s -d type={cpu or memory} -d node={x.x.x.x or x.x.x.x,x.x.x.x} http://ip:8888/v2/resource
 
##获取当前集群指定node实际未分配值
curl -s -d type={cpu or memory or all} -d node={x.x.x.x or x.x.x.x,x.x.x.x} http://ip:8888/v3/resource
 
##获取当前集群指定region空闲负载值
curl -s -d type={cpu or memory} -d region={qingdao or shanghai} http://ip:8888/v1/resource/region
 
##获取当前集群指定region空闲负载百分比
curl -s -d type={cpu or memory} -d region={qingdao or shanghai} http://ip:8888/v2/resource/region
 
##获取当前集群指定region实际未分配值
curl -s -d type={cpu or memory or all} -d region={qingdao or shanghai} http://ip:8888/v3/resource/region

