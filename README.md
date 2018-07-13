# Dummy Server

This is a dummy server composed of MITMProxy and Swagger-codegen, created as a test server on behalf of API such as Web service.

```
$ git clone git@github.com:TakesxiSximada/dummy-server.git
$ cd dummy-server
$ task build
$ goreman start
```

- Proxy Address: http://localhost:8080/
- Upstream API Address: http://localhost:8082/
- Access to proxy Web UI: http://localhost:8081/


### Dependencies

- [Python](https://www.python.org/)
- [Swagger Code Generator](https://github.com/swagger-api/swagger-codegen)
- [Task](https://github.com/go-task/task)
- [Goreman](https://github.com/mattn/goreman) or Foreman
