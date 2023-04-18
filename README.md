# jumble-api
Python API server that takes a word and re-arranges the characters randomly.  
The server has two endpoints: open ([http://{host}/random_word/{word}](http://%7Bhost%7D//random_word/%7Bword%7D)) and protected with API key authentication ([http://{host}/random_word_with_auth/{word}](http://%7Bhost%7D/random_word_with_auth/%7Bword%7D)). They both have exactly the same implementation and the only difference is the authentication prompt for the latter.
The authentication key used in this example is `"Authorization: my-secret-api-key"` taken from the HTTP request headers for simplicity purposes.
## Usage
The use of the API server is fairly simple, just send regular HTTP GET requests to one of the endpoints and include the authentication token if necessary. Here are some examples:
```
$ curl http://localhost:8000/random_word/example
"eamplxe"
$ curl -H "Authorization: my-secret-api-key" http://localhost:8000/random_word_with_auth/example
"mxplaee"
```
Also, you can open the same link with a browser or send requests with other convenient tools such as Postman.

## Standalone
#### Set up
To run the API server locally, you need to have Python 3 with `pip3` package manager installed.
Then simply clone the repo and `cd` into it.
Create a new virtual environment and activate it:  
```$ virtualenv -p python3 venv```  
```$ source venv/bin/activate```

Install the necessary packages:  
```$ pip3 install -r requirements.txt```

Start the application with the following command:  
```$ uvicorn app.app:app --host <listen_ip> port <listen_port> --reload```  
Where:  
**<listen_ip>**: IP address for API server to run on. Set to `0.0.0.0` to listen on any IP address. Default: `127.0.0.1` or `localhost`.  
 **<listen_port>**: Port to run on. Default: `8000`.
  
#### Tests
There are 5 unit tests at the moment: test with a valid input, test with an empty input, test with an invalid path, test with successful authentication, and test with failed authentication.
To execute these tests just run:  
```$ python3 -m unittest tests/test.py```

The example of successful unit tests:
![Unit tests sucess](https://drive.google.com/uc?export=download&id=1FsZq_uLboVWcIsF5tLEP4nQiXJ8epzpR)

## Docker
To (re)build the Docker image run the following command in the project root:  
```$ docker build -t {reponame}/jumble-api .```

To run the dockerized API server locally issue the following command:  
```$ docker run -d --name jumble-api {reponame}/jumble-api```

To get the IP address of created container this command may be useful:  
```$ docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' jumble-api```

Then you should be able to communicate with the endpoints in the same way as described in the [Usage section](https://github.com/ihor-chaban/jumble-api#usage) of this guide with the IP address of the Docker container.

## Kubernetes
The API server can be deployed to a Kubernetes cluster with convenient Helm charts. It consists of a deployment and a service that allows to load-balance traffic between the pods. There is no ingress in the provided solution, so to access the endpoints within the cluster, port forwarding is required.  
Verify that you have access to the correct cluster:  
```$ kubectl cluster-info```

Verify the namespace you want to deploy the chart to:  
```$ kubectl get namespaces```  
```$ kubectl get all -n default```

Deploy Helm release (the same command can be used either to install or upgrade the release):  
```$ helm upgrade --install jumbleapi helm/ --values helm/values.yaml -n default```

After the deployment is finished, verify that the new entities appeared and they are up and running. Some commands that might be useful here are:  
```$ kubectl get deployment jumbleapi -n default -o yaml```  
```$ kubectl inspect pod/jumbleapi-<replicaset-id>-<random-id> -n default```  
```$ kubectl inspect svc/jumbleapi -n default```  
```$ kubectl get all -n default -o wide```

You should see a similar output with the latter:
![Helm chart deployed](https://drive.google.com/uc?export=download&id=1mNmKwL-kpamFAKVE4_jhL5TyWtmLegLh)

To communicate with the endpoints port forwarding is required.
You can set up forwarding to a service to load-balance requests between all pods, or to a specific pod. The commands will be:  
```$ kubectl port-forward svc/jumbleapi <local_port>:8000 -n default```  
```$ kubectl port-forward pod/jumbleapi-<replicaset-id>-<random-id> <local_port>:8000 -n default```

If the port forwarding was successful you will be able to talk to the endpoints in the same way as described in the [Usage section](https://github.com/ihor-chaban/jumble-api#usage) of this guide on the **<local_port>**.
