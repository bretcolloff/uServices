Param(
  [String]$machine="mqserver3",
  [String]$reader="ureadworker",
  [Int32]$port=80
)

# Store the machine address.
$machineAddress = docker-machine ip $machine

# Concatenate the port mapping.
$portMap = [String]$port + ":80"

# Run the read worker - This requires the container to have been built with this name.
docker run -d -p $portMap --add-host dockermachine:$machineAddress $reader
