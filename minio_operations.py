# 导入 MinIO 客户端库和其他必要模块
from minio import Minio
from minio.error import S3Error
import os

# MinIO 服务器配置
MINIO_ENDPOINT = "127.0.0.1:9000"  # MinIO 服务地址
ACCESS_KEY = "admin"          # 默认访问密钥
SECRET_KEY = "minioadmin"          # 默认秘密密钥
BUCKET_NAME = "mybucket"           # 存储桶名称
ZIP_FILE = "test.zip"              # 测试用的 ZIP 文件
DOWNLOAD_PATH = "downloaded_test.zip"  # 下载文件保存路径

# 初始化 MinIO 客户端
client = Minio(
    MINIO_ENDPOINT,
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    secure=False  # 本地测试禁用 HTTPS
)

def create_bucket():
    """创建存储桶"""
    try:
        if not client.bucket_exists(BUCKET_NAME):
            client.make_bucket(BUCKET_NAME)
            print(f"存储桶 {BUCKET_NAME} 创建成功")
        else:
            print(f"存储桶 {BUCKET_NAME} 已存在")
    except S3Error as err:
        print(f"创建存储桶失败: {err}")

def upload_file():
    """上传 ZIP 文件到 MinIO"""
    try:
        client.fput_object(BUCKET_NAME, ZIP_FILE, ZIP_FILE)
        print(f"文件 {ZIP_FILE} 上传成功")
    except S3Error as err:
        print(f"上传文件失败: {err}")

def download_file():
    """从 MinIO 下载 ZIP 文件"""
    try:
        client.fget_object(BUCKET_NAME, ZIP_FILE, DOWNLOAD_PATH)
        print(f"文件 {ZIP_FILE} 下载成功到 {DOWNLOAD_PATH}")
    except S3Error as err:
        print(f"下载文件失败: {err}")

def list_objects():
    """查询存储桶中的对象"""
    try:
        objects = client.list_objects(BUCKET_NAME)
        print(f"存储桶 {BUCKET_NAME} 中的对象：")
        for obj in objects:
            print(f"- {obj.object_name}")
    except S3Error as err:
        print(f"查询对象失败: {err}")

def delete_file():
    """删除 MinIO 中的 ZIP 文件"""
    try:
        client.remove_object(BUCKET_NAME, ZIP_FILE)
        print(f"文件 {ZIP_FILE} 删除成功")
    except S3Error as err:
        print(f"删除文件失败: {err}")

if __name__ == "__main__":
    # 确保测试 ZIP 文件存在
    if not os.path.exists(ZIP_FILE):
        print(f"错误: {ZIP_FILE} 不存在，请先创建 ZIP 文件")
        print("示例命令：echo 'Hello, MinIO!' > test.txt && zip test.zip test.txt")
        exit(1)

    # 执行操作
    print("开始操作 MinIO...")
    # create_bucket()   # 创建存储桶
    # upload_file()     # 上传文件
    # list_objects()    # 查询对象
    # download_file()   # 下载文件
    # delete_file()     # 删除文件
    # list_objects()    # 再次查询，确认删除