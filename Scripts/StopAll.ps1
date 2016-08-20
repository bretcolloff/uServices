# Stop and remove all containers.
Write-Host "Stopping all containers..."
docker stop $(docker ps -a -q)

Write-Host "Removing all containers..."
docker rm $(docker ps -a -q)

# Get the active machine.
$machineName = docker-machine active

Write-Host "Stopping the active machine..."
docker-machine stop $machineName

Write-Host "Removing all machines..."
docker-machine rm -f $(docker-machine ls -q)

Write-Host "Docker machines removed."
