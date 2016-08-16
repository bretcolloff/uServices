docker-machine create --driver hyperv rabbitmq
docker-machine env rabbitmq
docker-machine env rabbitmq | Invoke-Expression
docker run -d -p 5672:5672 -p 15672:15672 rabbitmq:3-management
