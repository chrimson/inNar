# inNar

Interactive Narrative

docker build -t chrimson/innar:latest .

docker push

docker compose up

```
location /in/ {
    proxy_pass http://localhost:5000/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    
    proxy_set_header X-Script-Name /in;
}
```
