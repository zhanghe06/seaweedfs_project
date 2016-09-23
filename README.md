## seaweedfs 项目实例

[seaweedfs 项目地址](https://github.com/chrislusf/seaweedfs)


## 安装

### Go (Golang)

下载页面： https://golang.org/dl/

```
$ wget https://storage.googleapis.com/golang/go1.7.1.linux-amd64.tar.gz
$ sudo tar -C /usr/local -xzf go1.7.1.linux-amd64.tar.gz
$ sudo vim /etc/profile
    export GOROOT=/usr/local/go
    export GOPATH=$HOME/code/golang
    export PATH=$PATH:$GOROOT/bin:$GOPATH/bin
$ source /etc/profile
```

或者仅为当前用户设置环境变量
```
$ vim ~/.bashrc
$ source ~/.bashrc
```

注意：使用 zsh 的用户, 需要为 zsh 设置环境变量
```
$ vim ~/.zshrc
$ source ~/.zshrc
```

### Weed

依赖 git (版本控制工具)

```
go get github.com/chrislusf/seaweedfs/weed
```


## 启动

Start Master Server
```
$ weed master
```

Start Volume Servers
```
$ mkdir /tmp/data1 /tmp/data2
$ chmod 777 /tmp/data1 /tmp/data2
$ weed volume -dir="/tmp/data1" -max=5  -mserver="localhost:9333" -port=8080 &
$ weed volume -dir="/tmp/data2" -max=10 -mserver="localhost:9333" -port=8081 &
```

```
$ weed volume -dir=/tmp/data1/ -mserver="localhost:9333" -ip="192.168.2.32" -port=8080
```

上传文件请求
```
$ curl http://localhost:9333/dir/assign
{"fid":"2,055a54a8ec","url":"127.0.0.1:8080","publicUrl":"127.0.0.1:8080","count":1}
```

上传文件
```
$ curl -X PUT -F file=@/home/zhanghe/metro.jpg http://127.0.0.1:8080/2,055a54a8ec
{"name":"metro.jpg","size":1830848}
```

删除文件
```
$ curl -X DELETE http://127.0.0.1:8080/2,055a54a8ec
{"size":1830869}
```

文件读取
```
curl "http://localhost:9333/dir/lookup?volumeId=2"
{"volumeId":"2","locations":[{"url":"127.0.0.1:8080","publicUrl":"127.0.0.1:8080"}]}
```

访问文件
- [http://127.0.0.1:8080/2,055a54a8ec.jpg](http://127.0.0.1:8080/2,055a54a8ec.jpg)
- [http://127.0.0.1:8080/2/055a54a8ec.jpg](http://127.0.0.1:8080/2/055a54a8ec.jpg)
- [http://127.0.0.1:8080/2/055a54a8ec](http://127.0.0.1:8080/2/055a54a8ec)
- [http://127.0.0.1:8080/2/055a54a8ec?height=200&width=200](http://127.0.0.1:8080/2/055a54a8ec?height=200&width=200)

