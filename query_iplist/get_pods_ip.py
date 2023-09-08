# --*-- coding:utf-8 --*--

from Connect import api_instance,CoreV1Api
from flask import Flask,g, request,make_response
from optparse import OptionParser
import logging,sys,json,os

def List_pods(ns,label):
    a = []
    #m = {}
    ret = CoreV1Api.list_namespaced_pod(namespace=ns,label_selector="app=%s" % label)
    for i in ret.items:
        for s in i.status.container_statuses:
            if s.ready == True:
                a.append(i.status.pod_ip)
    #m = {label:a}
    return{label:a}

def List_pod(ns,label):
    a = []
    ret = CoreV1Api.list_namespaced_pod(namespace=ns,label_selector="app=%s" % label)
    for i in ret.items:
        for s in i.status.container_statuses:
            if s.ready == True:
                a.append(i.status.pod_ip)
    if a:
        return{label:a}
    else:
        return('404')

try:
    import http.client as http_client
except ImportError:
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

app = Flask(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.ERROR)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.ERROR)
requests_log.propagate = True
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

@app.route('/v1/list',methods=['POST'])
def get_pod_ips():
    try:
        b = {}
        data = json.loads(request.data)
        for k,v in data.items():
            for i in v:
                if List_pod(k,i) != '404':
                    b = {k:List_pod(k,i)}
                    return(b)
                else:
                    return('',404, {"Content-Type": "application/json"})
    except Exception as e:
        logging.error(e)
        print(e)

@app.route('/v2/list',methods=['POST'])
def get_pods_ips():
    try:
        ret = {}
        b = {}
        data_list = []
        data = json.loads(request.data)
        for k,v in data.items():
            for i in v:
                #b.update(List_pods(k,i))
                b = {k:List_pods(k,i)}
                data_list.append(b)
        for each_dict in data_list:
            for first_k, first_v in each_dict.items():
                if first_k not in ret.keys():
                    ret.setdefault(first_k, {})
                for second_k, second_v in first_v.items():
                    if second_k not in ret[first_k].keys():
                        ret[first_k].setdefault(second_k, second_v)
                    else:
                        ret[first_k][second_k].update(second_v)
        return(ret)
    except Exception as e:
        logging.error(e)
        print(e)


if __name__ == '__main__':
    app.run(debug=True, port=5555, host='0.0.0.0')
