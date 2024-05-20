# Azure 文本转语音服务

该项目提供了一个用于将文本转换为语音的RESTful API，使用微软的Azure认知服务。该服务使用Flask构建，并可以使用Docker进行容器化。

## 功能

- 使用微软Azure认知服务将文本转换为语音。
- 可以指定语音模型、语音风格和语速。
- 使用Docker进行容器化，方便部署。
- 使用环境变量进行配置。
- 提供日志记录功能，便于监控和调试。

## 快速开始

### 前提条件

- Python 3.10
- Docker
- Azure认知服务订阅密钥和区域

### 安装

1. 克隆仓库：

    ```bash
    git clone https://github.com/zhufengme/azure-tts-service.git
    cd azure-tts-service
    ```

2. 安装依赖项（用于本地开发）：

    ```bash
    pip install Flask requests
    ```

### 配置

设置以下环境变量：

- `AZURE_SUBSCRIPTION_KEY`：你的Azure订阅密钥。
- `AZURE_REGION`：你的Azure区域。

### 本地运行服务

1. 设置环境变量：

    ```bash
    export AZURE_SUBSCRIPTION_KEY=your_azure_subscription_key
    export AZURE_REGION=your_azure_region
    ```

2. 运行Flask应用：

    ```bash
    python app.py
    ```

### 使用Docker构建和运行

1. 构建Docker镜像：

    ```bash
    docker build -t azure-tts-service .
    ```

2. 运行Docker容器：

    ```bash
    docker run -d -p 5000:5000 --name azure-tts-service -e AZURE_SUBSCRIPTION_KEY=your_azure_subscription_key -e AZURE_REGION=your_azure_region azure-tts-service
    ```

### 从DockerHub运行

你可以从DockerHub拉取镜像并直接运行。

1. 拉取Docker镜像：

    ```bash
    docker pull andiezhu/azure-tts-service
    ```

2. 运行Docker容器：

    ```bash
    docker run -d -p 5000:5000 --name azure-tts-service -e AZURE_SUBSCRIPTION_KEY=your_azure_subscription_key -e AZURE_REGION=your_azure_region andiezhu/azure-tts-service
    ```

### API使用说明

#### 端点

- `POST /tts`

#### 请求体

- `text`（字符串，必需）：要转换为语音的文本。
- `voice_name`（字符串，可选）：要使用的语音模型。默认值为`en-US-AriaNeural`。
- `style`（字符串，可选）：要使用的语音风格。默认值为`general`。
- `rate`（字符串，可选）：语速。默认值为`0%`。

#### 示例请求

```bash
curl -X POST http://localhost:5000/tts \
     -H "Content-Type: application/json" \
     -d '{
           "text": "你好，这是微软文本转语音服务的REST封装",
           "voice_name": "zh-CN-YunyangNeural",
           "style": "newscast-casual",
           "rate": "10%"
         }' --output output.wav
```

### 健康检查

该服务提供了一个健康检查端点：

- `GET /health`

#### 示例请求

```bash
curl http://localhost:5000/health
```

### 日志记录

日志记录功能可以用于监控和调试。默认情况下，日志记录到控制台和名为`app.log`的文件。

#### 查看日志

要查看日志，可以使用`docker logs`命令：

```bash
docker logs -f azure-tts-service
```

如果你配置了日志记录到文件，可以使用以下命令查看日志：

```bash
tail -f app.log
```

### 许可证

该项目使用MIT许可证 - 有关详细信息，请参阅[LICENSE](LICENSE)文件。

### 鸣谢

- [Flask](https://flask.palletsprojects.com/)
- [Requests](https://docs.python-requests.org/)
- [Microsoft Azure Cognitive Services](https://azure.microsoft.com/en-us/services/cognitive-services/)

