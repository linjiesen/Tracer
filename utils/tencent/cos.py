# -*- coding:utf-8 -*-

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

from django.conf import settings


def create_bucket(bucket, region="ap-shanghai"):
    """
    创建桶
    :param bucket:桶名称
    :param region: 区域
    :return
    """
    config = CosConfig(Region=region, SecretId=settings.TENCENT_COS_ID, SecretKey=settings.TENCENT_COS_KEY)
    client = CosS3Client(config)

    response = client.create_bucket(
        Bucket=bucket,
        ACL="public-read",  # private / public-read / public-read-write
    )


def upload_file(bucket, region, file_object, key):
    # 文件对象上传到当前项目的桶中
    config = CosConfig(Region=region, SecretId=settings.TENCENT_COS_ID, SecretKey=settings.TENCENT_COS_KEY)
    client = CosS3Client(config)

    response = client.upload_file_from_buffer(
        Bucket=bucket,  # 从数据库中获取桶名称
        Body=file_object,  # 文件对象
        Key=key,
    )
    return "https://{}.cos.{}.myqcloud.com/{}".format(bucket, region, key)
