# MinIO 部署教程（MacBook Pro 2019，macOS）

## 引言

本教程详细说明如何在 MacBook Pro 2019（运行 macOS 系统，假设为 macOS Catalina 10.15 或更高）上部署 MinIO 开源免费版本（单机模式）。MinIO 是一个高性能、兼容 Amazon S3 的对象存储系统，适合开发测试环境。本教程确保步骤清晰、可重复，部署完成后 MinIO 将运行在本地端口 9000（API）和 9001（控制台）。

**前提条件：**
- MacBook Pro 2019（Intel 芯片，macOS 10.15 或更高，推荐 Ventura/Sonoma）。
- 已安装 Homebrew（安装命令：`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`）。
- 至少 1GB 磁盘空间用于存储数据。
- 网络端口 9000（API）和 9001（控制台）未被占用。
- 网络连接正常（用于安装 MinIO 和依赖）。
- （可选）Python 3 已安装，用于后续操作 MinIO（可通过 `brew install python3` 安装）。

**目标：**
- 部署 MinIO 单机版，运行在 `http://127.0.0.1:9000`（API）和 `http://127.0.0.1:9001`（控制台）。
- 提供浏览器访问和基本配置步骤，确保服务正常运行。

---

## 部署步骤

### 步骤 1: 安装 MinIO

1. **使用 Homebrew 安装 MinIO**（推荐，简单快速）：
   - 打开终端（Terminal）。
   - 更新 Homebrew：
     ```bash
     brew update
     ```
   - 安装 MinIO：
     ```bash
     brew install minio/stable/minio
     ```
   - 验证安装：
     ```bash
     minio --version
     ```
     输出示例：`minio version RELEASE.2025-XX-XXTXX-XX-XXX`。

   **手动安装（备用方式）**：
   - 访问 MinIO 官网下载页面：https://min.io/download#/macos。
   - 下载 macOS AMD64 二进制文件（MacBook Pro 2019 使用 Intel 芯片，选择 AMD64）。
   - 将下载的 `minio` 文件移动到 `/usr/local/bin/`：
     ```bash
     mv ~/Downloads/minio /usr/local/bin/minio
     ```
   - 赋予执行权限：
     ```bash
     chmod +x /usr/local/bin/minio
     ```

2. **创建数据存储目录**：
   - 创建用于存储 MinIO 数据的目录：
     ```bash
     mkdir -p ~/minio-data
     ```
   - 确认目录存在：
     ```bash
     ls ~
     ```
     输出应包含 `minio-data`。

### 步骤 2: 启动 MinIO 服务

1. **运行 MinIO 服务器**：
   - 在终端中运行以下命令启动 MinIO：
     ```bash
     minio server ~/minio-data --console-address ":9001"
     ```
     - `~/minio-data`：数据存储路径（可自定义）。
     - `--console-address ":9001"`：指定控制台端口为 9001（API 默认端口为 9000）。
   - 启动后，终端显示类似以下信息：
     ```
     Endpoint: http://127.0.0.1:9000 http://192.168.x.x:9000
     AccessKey: admin
     SecretKey: minioadmin

     Browser Access:
     http://127.0.0.1:9001
     ```
   - **记录 AccessKey 和 SecretKey**（默认分别为 `minioadmin` 和 `minioadmin`），用于后续配置和 Python 操作。
   - 保持终端窗口打开，MinIO 将在前台运行。

2. **验证 MinIO 运行**：
   - 打开浏览器，访问 `http://127.0.0.1:9001`。
   - 使用 `minioadmin`（AccessKey）和 `minioadmin`（SecretKey）登录。
   - 登录成功后，看到 MinIO 控制台界面，说明服务运行正常。

3. **（可选）后台运行 MinIO**：
   - 如果不想保持终端窗口打开，可使用 `nohup` 后台运行：
     ```bash
     nohup minio server ~/minio-data --console-address ":9001" > minio.log 2>&1 &
     ```
   - 查看日志：
     ```bash
     tail -f minio.log
     ```
   - 停止 MinIO：
     ```bash
     ps aux | grep minio
     kill <pid>
     ```
     （`<pid>` 为 MinIO 进程 ID）。

### 步骤 3: 配置 MinIO

1. **创建存储桶**：
   - 在浏览器中登录 MinIO 控制台（`http://127.0.0.1:9001`）。
   - 点击 “Buckets” > “Create Bucket”。
   - 输入存储桶名称（如 `mybucket`），点击 “Create”。
   - 保持默认设置（无需启用版本控制或加密）。

2. **测试存储桶**：
   - 在控制台中，点击 “mybucket” > “Upload”，上传一个测试文件（如 `test.txt`）。
   - 确认文件出现在存储桶中，验证 MinIO 功能正常。

### 步骤 4: 故障排查

- **端口被占用**：
  - 检查 9000/9001 端口：
    ```bash
    lsof -i :9000
    lsof -i :9001
    ```
  - 如果被占用，终止相关进程：`kill -9 <pid>`，或更改 MinIO 端口（如 `--console-address ":9002"`）。
- **权限问题**：
  - 确保 `~/minio-data` 目录有写入权限：
    ```bash
    chmod -R u+rw ~/minio-data
    ```
- **连接失败**：
  - 确认 MinIO 正在运行：`ps aux | grep minio`。
  - 检查防火墙设置，确保本地访问 `127.0.0.1:9000` 和 `9001` 不被阻止。

---

## 清理与卸载

- **停止 MinIO**：
  - 如果前台运行，按 `Ctrl+C` 停止。
  - 如果后台运行，找到进程 ID 并终止：
    ```bash
    ps aux | grep minio
    kill <pid>
    ```
- **卸载 MinIO**：
  - 使用 Homebrew 卸载：
    ```bash
    brew uninstall minio
    ```
  - 删除数据目录：
    ```bash
    rm -rf ~/minio-data
    ```

---

## 总结

完成上述步骤后，MinIO 将成功运行在 MacBook Pro 2019 上，API 地址为 `http://127.0.0.1:9000`，控制台地址为 `http://127.0.0.1:9001`。你可以通过浏览器管理存储桶和文件，或使用 Python SDK 进行程序化操作。后续步骤可参考 Python 操作代码，完成 ZIP 文件的上传、下载、删除和查询。