### For Scaling the Api for we can consider using the following 
- Implement load balancers to distrubte traffic across multiple servers and use services which autoscale 
- We can use cahce like redis and others to reduce the load on database 
- We can create multple services for specific functionalities such as authentication , movie data retrieval , search etc. ie switching from monolithich to microservices 
- Using CDN or deploying servers in multiple regions and gateways to reourte the traaffic to the server with lowest latency from the user 
- we can distrubute data to multiple servers so one cannot be bottleneck 
- We can also enable pagination so we dont need to retrieve all the data in one go
- We can also use read replica database for read data tasks which will reduce burden on our primrary database