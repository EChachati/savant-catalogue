import logging
import os

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from fastapi import HTTPException, UploadFile, status

load_dotenv()


class FileHandler:
    SUPPORTED_FILE_TYPES = {"image/png": "png", "image/jpeg": "jpg"}
    MB: int = 1024 * 1024
    size: int
    content_type: str
    extension: str
    file: UploadFile
    url: str | None = None
    bucket_name: str
    filename: str

    def __init__(
        self,
        file: UploadFile,
        bucket_name: str | None = None,
        filename: str | None = None,
    ):
        """
        The function initializes an object with file-related attributes and
        validates the file.

        Arguments:

        * `file`: The `file` parameter is of type `UploadFile`. It represents
        the file that is being uploaded. It contains information such as the
        file's size, content type, and filename.
        * `bucket_name`: The `bucket_name` parameter is a string that
        represents the name of the bucket where the file will be stored.
         If no `bucket_name` is provided, it defaults to "savant-default".
        * `filename`: The `filename` parameter is an optional string that
        represents the desired name of the file. If a value is provided,
        it will be used as the filename for the uploaded file. If no
        value is provided, the filename of the uploaded file will be used.
        """
        self.file = file
        self.size = file.size
        self.content_type = file.content_type

        self.bucket_name = bucket_name or "savant-default"
        self.filename = filename or file.filename
        self._validate_file()

    def _validate_file(self):
        """
        The function validates the size and content type of a file and raises an
        exception if either condition is not met.
        """
        if self.size > 5 * self.MB:
            raise HTTPException(
                "File Too Big", status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
            )

        if self.content_type not in self.SUPPORTED_FILE_TYPES:
            raise HTTPException(
                f"Unsupported File type {self.content_type}. "
                f"Supported types are {self.SUPPORTED_FILE_TYPES}",
                status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            )

        self.extension = self.SUPPORTED_FILE_TYPES[self.content_type]

    async def upload_file(self):
        """
        The function `upload_file` uploads a file to an S3 bucket using the
        boto3 library and the TEBI storage service.
        """
        s3_resource = boto3.resource(
            service_name="s3",
            aws_access_key_id=os.environ["TEBI_STORAGE_KEY"],
            aws_secret_access_key=os.environ["TEBI_STORAGE_SECRET"],
            endpoint_url="https://s3.tebi.io",
        )

        bucket = s3_resource.Bucket(self.bucket_name)
        bucket.put_object(Key=self.filename, Body=self.file.file)

    def get_url_file(self):
        """
        The function `get_url_file` generates a pre-signed URL for downloading
        a file from an S3 bucket.

        Returns:
        a URL that can be used to download a file from an S3 bucket.
        """
        try:
            s3 = boto3.client(
                service_name="s3",
                aws_access_key_id=os.environ["TEBI_STORAGE_KEY"],
                aws_secret_access_key=os.environ["TEBI_STORAGE_SECRET"],
                endpoint_url="https://s3.tebi.io",
            )
            params = {"Bucket": self.bucket_name, "Key": self.filename}
            url = s3.generate_presigned_url(
                "get_object", Params=params, ExpiresIn=3600
            )
            return url

        except ClientError as e:
            logging.error(e)
            return None
