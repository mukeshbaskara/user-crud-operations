# user-crud-operations


#---- setup -----


--> Create a GKE cluster 

--> Create a redis instance

--> Add kube context in your local

--> Add helm ingress repo to install ingress controller

		helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
		
		
--> Install Ingress controller using below command

		helm install ingress-controller ingress-nginx/ingress-nginx --namespace ingress-nginx --set controller.publishService.enabled=true --set controller.service.type=LoadBalancer --set controller.service.loadBalancerIP=34.172.202.243 
		
		(I have created and used my public ip. you should use your public ip here)
		
		
--> Check whether your ingress controller installed properly by executing following command

		kubectl get all -n <your-ingress-controller-namespace>
		
		
--> Gather redis instance information such as host, port and auth
		
--> Configure the host and port information of redis instance in the values.yaml

		redis.host and redis.port (don't add redis auth/password in the values.yaml for security reasons)
		
--> Create a static public ip address by navigating to VPC network --> Ip addresses in GCP console
		
--> Add A record in your DNS manager to map your domain name with the public ip which you created in the previous step.

--> Specify the domain name in the values.yaml in the host section of ingress.

		(In my case, I own a domain name called "cloudgeek.co.uk". I specified this domain name as ingress host)
		









#----- build & push application image to GCR ----


--> Navigate to the app folder and execute the docker commands to build, tag and push to GCR.
			
			docker build -t user-crud .
			
			docker tag <image-id> gcr.io/reflecting-surf-381016/user-crud       (I have specifed my GCR repository, you should create one for you)
			
			docker push gcr.io/reflecting-surf-381016/user-crud
		







#------ pack the helm chart & install -----


--> Navigate to the folder infra/charts/ and run below commands to pack the chart and install.

			helm package user-crud user-crud/
			
			helm install user-crud user-crud-0.1.0.tgz  --set namespace.name=<app-namespace> --set redis.auth=<base64 encoded redis auth/password>   
			
			(we should execute the above command in automation(Jenkins) to bring the password from vault if you want to promote this solution to higher envs)
			
			
--> Check whether your application pod is running by below command

			kubectl get pods -n <your app-namespace>
			
--> Check whether your ingress controller detected your ingress resource deployed in your app namespace and it is successfully routing the requests to your ingress in your app namespace.

			kubectl get pods -n <ingress controller namespace>
			kubectl logs <ingress-controller-pod-name> -n <ingress-controller-namespace>
			
--> Once the ingress-controller detects your ingress deployed in app namespace. your setup is ready for traffic.








#-------- Python CLI  usage ------

--> To retrieve the user record

	python user_client.py get --id cf17ac56-a80c-4e2f-ae3c-dc58c41e0554 --domain cloudgeek.co.uk
	
	
--> To create a user record
		
	python user_client.py create --file-path=/path/to/user.yaml --domain cloudgeek.co.uk
	
	
--> To update a user record

	python user_client.py update --id 3d59f080-bd3a-4ef9-9069-5543fe56a1ff --file-path=/path/to/user.yaml --domain cloudgeek.co.uk


--> To delete a user record

	python user_client.py delete --id 3d59f080-bd3a-4ef9-9069-5543fe56a1ff  --domain cloudgeek.co.uk

	
Note-1: These commands will print response in JSON.. Need to work on parsing the json and print the content alone..

Note-2: I have added validations in user model class. So, app will reject invalid user details.








#---------------- Improvements -------------

---> Need to write unit tests 

---> Need to pass image sha when installing helm chart instead of specifying latest in the image tag in values.yaml (will do it after submission)

---> Need to add TLS

---> Need to add frontend application.. This frontend application should face the public traffic and route the requests to our application deployed in private facing..


		
