param(
  [String]$machine="rabbitmq",
  [String]$reader="ureadworker"
)

# Start the docker machine.
$machineName = $machine
docker-machine create --driver hyperv $machineName
docker-machine env $machineName
docker-machine env $machineName | Invoke-Expression

# Store the machine address.
$machineAddress = docker-machine ip $machineName

# Run rabbitmq
docker run -d -p 5672:5672 -p 15672:15672 rabbitmq:3-management

# Run the read worker - This requires the container to have been built with this name.
docker run -d -p 80:80 --add-host dockermachine:$machineAddress $reader
