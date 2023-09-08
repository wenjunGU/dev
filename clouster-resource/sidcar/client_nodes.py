# --*-- coding:utf-8 --*--

from Connect import api_instance, CoreV1Api, api_nodes
from kubernetes.client.rest import ApiException
import re
from math import floor, ceil
from os import environ
from flask import Flask,g,render_template,request
import schedule,time,json

# os.environ.get('env')

class get_usage(object):

    def __init__(self):
        self.values = environ.get('values')

    def get_re(self, string):
        value = re.compile(r'\d+')
        value = re.findall(value, string)
        for i in value:
            return i

    def get_node_status(self, project, nodes_name):
        # api = client.CustomObjectsApi()
        try:
            k8s_nodes = api_nodes.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "nodes")
            for stats in k8s_nodes['items']:
                names = stats['metadata']['name']
                if names == nodes_name:
                    if project == 'cpu':
                        return (int(int(self.get_re(stats['usage']['cpu'])) / 1024 / 1024))
                    elif project == 'memory':
                        return (int(int(self.get_re(stats['usage']['memory'])) / 1024))
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_cluster_custom_object: %s\n" % e)

    #        print("Node: %s\tCPU: %sm\tMemory: %sMi" % (stats['metadata']['name'], int(int(get_re(stats['usage']['cpu'])) / 1024 / 1024), int(int(get_re(stats['usage']['memory'])) / 1024)))

    def read_node_status(self, project, nodes_name):
        cpu_ac = []
        memory_ac = []
        name = nodes_name  # str | name of the Node
        pretty = nodes_name  # str | If 'true', then the output is pretty printed. (optional)
        exact = True  # bool | Should the export be exact.  Exact export maintains cluster-specific fields like 'Namespace'. Deprecated. Planned for removal in 1.18. (optional)
        export = True  # bool | Should this value be exported.  Export strips fields that a user can not specify. Deprecated. Planned for removal in 1.18. (optional)
        try:
            api_response = CoreV1Api.read_node(name, pretty=pretty, exact=exact, export=export)
            cpu_ac.append(api_response.status.allocatable['cpu'])
            memory_ac.append(api_response.status.allocatable['memory'])
            if project == 'cpu':
                for i in cpu_ac:
                    return (int(self.get_re(i)) * 1024)
            elif project == 'memory':
                for i in memory_ac:
                    return (int(self.get_re(i)) / 1024)
        except ApiException as e:
            print("Exception when calling CoreV1Api->read_node: %s\n" % e)

    def  Usage_node_resources(self, project, nodes_name):
        # api = client.CustomObjectsApi()
        try:
            k8s_nodes = api_nodes.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "nodes")
            for stats in k8s_nodes['items']:
                names = stats['metadata']['name']
                if names == nodes_name:
                    if project == 'cpu':
                        return (int(int(self.get_re(stats['usage']['cpu'])) / 1024 / 1024 / 1024))
                    elif project == 'memory':
                        return (int(int(self.get_re(stats['usage']['memory'])) / 1024 / 1024))
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_cluster_custom_object: %s\n" % e)

    #        print("Node: %s\tCPU: %sm\tMemory: %sMi" % (stats['metadata']['name'], int(int(get_re(stats['usage']['cpu'])) / 1024 / 1024), int(int(get_re(stats['usage']['memory'])) / 1024)))

    def Allocatable_node_resources(self, project, nodes_name):
        cpu_ac = []
        memory_ac = []
        name = nodes_name  # str | name of the Node
        pretty = nodes_name  # str | If 'true', then the output is pretty printed. (optional)
        exact = True  # bool | Should the export be exact.  Exact export maintains cluster-specific fields like 'Namespace'. Deprecated. Planned for removal in 1.18. (optional)
        export = True  # bool | Should this value be exported.  Export strips fields that a user can not specify. Deprecated. Planned for removal in 1.18. (optional)
        try:
            api_response = CoreV1Api.read_node(name, pretty=pretty, exact=exact, export=export)
            cpu_ac.append(api_response.status.allocatable['cpu'])
            memory_ac.append(api_response.status.allocatable['memory'])
            if project == 'cpu':
                for i in cpu_ac:
                    return (int(int(self.get_re(i))))
            elif project == 'memory':
                for i in memory_ac:
                    return (int(int(self.get_re(i)) / 1024 / 1024))
        except ApiException as e:
            print("Exception when calling CoreV1Api->read_node: %s\n" % e)

    def get_resources_usage(self, project, nodes_name):
        if self.get_node_status(project, nodes_name) == None:
            return ('NULL')
        else:
            if project == 'cpu':
                cpu_usage = self.get_node_status(project, nodes_name) / self.read_node_status(project, nodes_name)
                return (int(cpu_usage * 100))
            elif project == 'memory':
                memory_usage = self.get_node_status(project, nodes_name) / self.read_node_status(project, nodes_name)
                return (int(memory_usage * 100))

    def Idle_nodes_resources(self, project):
        nodes = []
        values = []
        try:
            apis = CoreV1Api.list_node()
            for i in apis.items:
                values.append(self.Usage_node_resources(project, i.metadata.name))
                nodes.append(self.Allocatable_node_resources(project, i.metadata.name))
            new_list = [x for x in values if isinstance(x, (int, float))]
            return (sum(nodes) - sum(new_list))
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_node: %s\n" % e)

    def list_nodes(self, project):
        nodes = {}
        values = []
        try:
            apis = CoreV1Api.list_node()
            for i in apis.items:
                print('NodeName:{0} {1} usage is {2}%'.format(i.metadata.name, project,self.get_resources_usage(project, i.metadata.name)))
                values.append(self.get_resources_usage(project, i.metadata.name))
            And = len(values)
            Accumulation = sum(values)
            return int((round(Accumulation / And, 2)))
            # return({0}:{1}).format(i,self.get_resources_usage(project,i))
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_node: %s\n" % e)

    def Get_namespaces(self):
        ns = []
        api_response = CoreV1Api.list_namespace()
        for i in api_response.items:
            #if i.metadata.name != 'default' and i.metadata.name != 'kube-public' and i.metadata.name != 'kube-system' and i.metadata.name != 'monitoring' and i.metadata.name != 'kube-node-lease':
            if i.metadata.name != 'kube-public' and i.metadata.name != 'kube-system' and i.metadata.name != 'monitoring' and i.metadata.name != 'kube-node-lease':
                ns.append(i.metadata.name)
        return(ns)


    def Get_pods_resources(self,namespace,project):
        a = []
        k = []
        ret = CoreV1Api.list_namespaced_pod(namespace=namespace)
        for i in ret.items:
            if i.status.container_statuses != None and namespace != '' and i.status.container_statuses[0].ready != False:
                m = i.spec.containers[0].resources.limits
                if m != None and project in m:
                     for s in re.findall(r'\d+', m.get(project)):
                        if int(s) > 50:
                            s = int(s) / 1024
                     a.append(int(s))
        return(sum(a))
                #a.append([int(s) for s in re.findall(r'\d+', m.get('memory')) if int(s) > 50 % int(s) / 1024])
        #for res in a:
        #    k.extend(eval(str(res)))
        #return(sum(k))

    def Marge_ns_resources(self,project):
        ns = []
        for i in self.Get_namespaces():
            ns.append(self.Get_pods_resources(i,project))
        return(int(sum(ns)))


    def Gets_pods_resources(self, namespace, project):
        node_resources = {}
        ret = CoreV1Api.list_namespaced_pod(namespace=namespace)
        for i in ret.items:
            if i.status.container_statuses != None and namespace != '' and i.status.container_statuses[0].ready != False:
                node_name = i.spec.node_name
                if node_name not in node_resources:
                    node_resources[node_name] = []
                m = i.spec.containers[0].resources.limits
                if m != None and project in m:
                    limit = m.get(project)
                    if isinstance(limit, str):
                        for s in re.findall(r'\d+', limit):
                            if int(s) > 50:
                                s = int(s) / 1024
                            node_resources[node_name].append(int(s))
                    elif isinstance(limit, list):
                        for l in limit:
                            for s in re.findall(r'\d+', l):
                                if int(s) > 50:
                                    s = int(s) / 1024
                                node_resources[node_name].append(int(s))
        for node_name, values in node_resources.items():
            node_resources[node_name] = sum(values)
        return node_resources


    def Gets_region_resources(self,project):
        result = {}
        if project == 'cpu':
            out_file = '/config/cpu.json'
        else:
            out_file = '/config/memory.json'
        for i in obj.Get_namespaces():
            pods_resources = obj.Gets_pods_resources(i, project)
            for key, value in pods_resources.items():
                if key in result:
                    result[key] += value
                else:
                    result[key] = value
        result_json = json.dumps(result)
        with open(out_file, 'w') as file:
            file.write(result_json)
        return(result_json)


    def Gets_region_jsonfile(self,nodes,project):
        if project == 'cpu':
            out_file = '/config/cpu.json'
        else:
            out_file = '/config/memory.json'
        with open(out_file) as f:
            data = json.load(f)
        if isinstance(nodes, str):
            keys = [nodes]
        elif isinstance(nodes, list):
            keys = nodes
        else:
            raise ValueError("Invalid input type. Expected str or list.")
        total_value = sum(data[key] for key in keys if key in data)
        return(total_value)



    def Gets_all_jsonfile(self,project):
        if project == 'cpu':
            out_file = '/config/cpu.json'
        else:
            out_file = '/config/memory.json'
        with open(out_file) as f:
            data = json.load(f)
        total_value = 0
        for key in data.keys():
            total_value += data[key]
        return(total_value)


    def Idle_Cluster_resources(self, project):
        nodes = []
        values = []
        snk = []
        try:
            apis = CoreV1Api.list_node()
            for i in apis.items:
                values.append(self.Usage_node_resources(project, i.metadata.name))
                nodes.append(self.Allocatable_node_resources(project, i.metadata.name))
                snk.append(self.Gets_region_jsonfile(i.metadata.name,project))
            new_list = [x for x in values if isinstance(x, (int, float))]
            #return (sum(nodes) - sum(new_list) - self.Marge_ns_resources(project))
            return (sum(nodes) - sum(new_list) - sum(snk))
            #return (sum(nodes) - sum(new_list))
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_node: %s\n" % e)

    def Idle_Cluster_All(self):
        resource = {}
        resource.update({'cpu':self.Idle_Cluster_resources('cpu'),'memory':self.Idle_Cluster_resources('memory')})
        return resource


    def Idle_nodes_resources_Region(self, project,node):
        values = []
        nodes = []
        new_nodes = []
        try:
            apis = CoreV1Api.list_node()
            for i in apis.items:
                nodes.append(i.metadata.name)
            if isinstance(node, str):
                node = node.split(",")
                intersection = set(node) & set(nodes)
                if intersection:
                    for ik in list(intersection):
                      values.append(self.Usage_node_resources(project, ik))
                      new_nodes.append(self.Allocatable_node_resources(project, ik))
                    new_list = [x for x in values if isinstance(x, (int, float))]
                    return (sum(new_nodes) - sum(new_list))
                else:
                    return("node does not exist")
            elif isinstance(node, list):
                intersection = set(node) & set(nodes)
                if intersection:
                    for ik in list(intersection):
                        values.append(self.Usage_node_resources(project, ik))
                        new_nodes.append(self.Allocatable_node_resources(project, ik))
                    new_list = [x for x in values if isinstance(x, (int, float))]
                    return (sum(new_nodes) - sum(new_list))
                else:
                    return("node does not exist")
            else:
                return("Parameter is not list or str type")
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_node: %s\n" % e)



    def list_nodes_Region(self, project, node):
        nodes = []
        values = []
        try:
            apis = CoreV1Api.list_node()
            for i in apis.items:
                nodes.append(i.metadata.name)
            if isinstance(node, str):
                node = node.split(",")
                intersection = set(node) & set(nodes)
                if intersection:
                    for ik in list(intersection):
                      values.append(self.get_resources_usage(project, ik))
                    And = len(values)
                    Accumulation = sum(values)
                    return int((round(Accumulation / And, 2)))
                else:
                    return("node does not exist")
            elif isinstance(node, list):
                intersection = set(node) & set(nodes)
                if intersection:
                    for ik in list(intersection):
                        values.append(self.get_resources_usage(project, ik))
                    And = len(values)
                    Accumulation = sum(values)
                    return int((round(Accumulation / And, 2)))
                else:
                    return("node does not exist")
            else:
                return("Parameter is not a list type")
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_node: %s\n" % e)




    def Idle_Cluster_resources_Region(self, project,node):
        nodes = []
        values = []
        new_nodes = []
        snk = []
        try:
            apis = CoreV1Api.list_node()
            for i in apis.items:
                nodes.append(i.metadata.name)
            if isinstance(node, str):
                node = node.split(",")
                intersection = set(node) & set(nodes)
                if intersection:
                    for ik in list(intersection):
                        values.append(self.Usage_node_resources(project, ik))
                        new_nodes.append(self.Allocatable_node_resources(project, ik))
                        snk.append(self.Gets_region_jsonfile(ik,project))
                    new_list = [x for x in values if isinstance(x, (int, float))]
                    #return (sum(new_nodes) - sum(new_list) - self.Marge_ns_resources(project))
                    return (sum(new_nodes) - sum(new_list) - sum(snk))
                    #return (sum(new_nodes) - sum(new_list))
                else:
                    return("node does not exist str")
            elif isinstance(node, list):
                intersection = set(node) & set(nodes)
                if intersection:
                    for ik in list(intersection):
                        values.append(self.Usage_node_resources(project, ik))
                        new_nodes.append(self.Allocatable_node_resources(project, ik))
                        snk.append(self.Gets_region_jsonfile(ik,project))
                    new_list = [x for x in values if isinstance(x, (int, float))]
                    #return (sum(new_nodes) - sum(new_list) - self.Marge_ns_resources(project))
                    return (sum(new_nodes) - sum(new_list) - sum(snk))
                    #return (sum(new_nodes) - sum(new_list))
                else:
                    return("node does not exist list")
            else:
                return("Parameter is not a list type")
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_node: %s\n" % e)


    def Get_Label_Region(self,label):
        nodes = []
        apis = CoreV1Api.list_node()
        for i in apis.items:
            if i.metadata.labels.get('region') is not None:
                if i.metadata.labels.get('region') == label:
                    nodes.append(i.metadata.name)
        return(nodes)


    def Idle_Cluster_Region_All(self,region):
        resource = {}
        resource.update({'cpu':self.Idle_Cluster_resources_Region('cpu',self.Get_Label_Region(str(region))),'memory':self.Idle_Cluster_resources_Region('memory',self.Get_Label_Region(str(region)))})
        return resource

    def Idle_Cluster_node_All(self,node):
        resource = {}
        resource.update({'cpu':self.Idle_Cluster_resources_Region('cpu',node),'memory':self.Idle_Cluster_resources_Region('memory',node)})
        return resource

obj = get_usage()
schedule.every(1).minutes.do(lambda: obj.Gets_region_resources('memory'))
schedule.every(1).minutes.do(lambda: obj.Gets_region_resources('cpu'))
while True:
    schedule.run_pending()
    time.sleep(1)
