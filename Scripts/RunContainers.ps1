Param(
  [Parameter(Mandatory=$true)]
  [String]$machine,
  [Parameter(Mandatory=$true)]
  [String]$container,
  [Parameter(Mandatory=$true)]
  [Int32]$port,
  [Int32]$amount=1
)

# Store the machine address.
$machineAddress = docker-machine ip $machine

for($i=0; $i -lt $amount; $i++)
{
  $newPort = $port + $i

  # Concatenate the port mapping.
  $portMap = [String]$newPort + ":80"

  # Run the specified container.
  docker run -d -p $portMap --add-host dockermachine:$machineAddress $container
}
