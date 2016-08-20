param(
  [String]$machine="TextAnalysis",
  [String]$reader="ureadworker",
  [String]$divider="udivider",
  [String]$processor="uprocessor",
  [String]$writer="uwriter",
  [Int32]$dividerCount=1,
  [Int32]$processorCount=1,
  [Int32]$writerCount=1
)

Write-Host "Starting docker machine " + $machine + "..."

# Start the docker machine.
$machineName = $machine
docker-machine create --driver hyperv $machineName
docker-machine env $machineName
docker-machine env $machineName | Invoke-Expression

# Store the machine address.
$machineAddress = docker-machine ip $machineName

Write-Host "Docker machine started at " + $machineAddress
Write-Host "Starting RabbitMq..."

# Run rabbitmq
docker run -d -p 5672:5672 -p 15672:15672 rabbitmq:3-management

Write-Host "Starting ElasticSearch..."

# Run ElasticSearch
docker run -d -p 9200:9200 -p 9300:9300 elasticsearch

Write-Host "Starting Kibana..."

# Run Kibana
$elasticSearchUrl = "http://" + $machineAddress + ":9200"
docker run -d -p 5601:5601 -e ELASTICSEARCH_URL=$elasticSearchUrl kibana

Write-Host "Building containers..."
cd ..\Containers\ReadWorker
docker build -t $reader .

cd ..\ProcessWorkers\Divider
docker build -t $divider .

cd ..\Processor
docker build -t $processor .

cd ..\..\WriteWorker
docker build -t $writer .

Write-Host "Containers built, running..."

cd ..\..\TestScripts

Write-Host "Run the reader container..."
.\RunContainers.ps1 -machine $machineName -container $reader -port 80

Write-Host "Run the divider container(s)..."
.\RunContainers.ps1 -machine $machineName -container $divider -port 90 -amount $dividerCount

Write-Host "Run the processing container(s)..."
.\RunContainers.ps1 -machine $machineName -container $processor -port 100 -amount $processorCount

Write-Host "Run the writing container(s)..."
.\RunContainers.ps1 -machine $machineName -container $writer -port 200 -amount $writerCount

Write-Host "All containers started on host:"
Write-Host $machineAddress
