docker build -t ureadworker .
docker run -d -p 80:80 --add-host dockermachine:10.82.53.62 ureadworker
