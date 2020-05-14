# openfaas-test-repo
Load testing on openfaas

High level goal: I am trying to use a simple echo function to test the effect of autoscaling in openfaas. Basically, as i 
increase the number of function replica, I expect to see the output rate increase. In the end, I expect to achieve an output rate of 3000 qps.

Steps to reproduce the result:
1. Install openfaas and hey
2. Deploy the echo function: sudo faas-cli up -f echo-in-go.yml
3. run the receive_call.py script, by default it runs on port 5000. If you are working on a VM, use port forwarding to bypass
the firewall. For example: ssh -i ~/.ssh/id_rsa localhost -NL 0.0.0.0:9898:localhost:5000
4. Use hey to generate workload: 
hey -n 200000 -c 5  -H "X-Callback-Url: http://VM's IP:9898" -m POST http://127.0.0.1:8080/async-function/echo-in-go
Use the X-Callback-url header so you can see all the callback in the flask server. 
Use async-function endpoint so you are invokeing asynchronously. 
5. After done, stop the flask server, then you will see the time it takes to process all the requests and get an idea of the 
output rate. 

How to change the number of queue-worker and gateway-worker:
1. git clone https://github.com/openfaas/faas-netes.git
2. cd faas-netes
3. helm template \
  openfaas chart/openfaas/ \
  --namespace openfaas \
  --set basic_auth=true \
  --set gateway.replicas=5\
  --set queueWorker.replicas=5\
  --set functionNamespace=openfaas-fn > openfaas.yaml
Here it changes the number of queue-worker to be 5 and number of gateway-worker to be 5. 
4. kubectl apply -f namespaces.yml,openfaas.yaml
