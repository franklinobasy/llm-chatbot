"""
Module: s3_util.py

This module provides utility classes for managing operations related to Amazon S3 buckets and files.

Classes:
    - S3BucketNotFoundError: Exception raised when the specified S3 bucket cannot be found.
    - S3BucketFailToCreateError: Exception raised when an S3 bucket cannot be created.
    - FolderNotFoundError: Exception raised when the specified folder within an S3 bucket cannot be found.
    - FilesDownloadError: Exception raised when files cannot be downloaded from an S3 bucket.
    - BucketUtil: Utility class for managing S3 bucket operations including file and folder manipulation.

Usage:
    Example usage of the BucketUtil class:

    ```python
    from s3_util import BucketUtil

    # Initialize BucketUtil instance
    util = BucketUtil(bucket_name="your-bucket-name")

    # List all folder IDs in the bucket
    folder_ids = util.list_ids()
    print("Folder IDs:", folder_ids)

    # List files in a specific folder
    folder_id = "1"
    files_in_folder = util.list_files_in_folder(folder_id)
    if files_in_folder:
        print(f"Files in folder {folder_id}: {files_in_folder}")
    else:
        print(f"No files found in folder {folder_id}.")

    # Upload a file to a specific folder
    file_name = "example.txt"
    file_content = b"Example file content"
    upload_success = util.upload_file(id=folder_id, file_name=file_name, file_content=file_content)
    if upload_success:
        print("File uploaded successfully.")
    else:
        print("Failed to upload file.")

    # Download files from a specific folder
    download_success = util.download_files(id=folder_id)
    if download_success:
        print("Files downloaded successfully.")
    else:
        print("Failed to download files.")

    # Delete a file from a specific folder
    delete_success = util.delete_file_in_folder(id=folder_id, file_name=file_name)
    if delete_success:
        print("File deleted successfully.")
    else:
        print("Failed to delete file.")
    ```
"""

import boto3
from botocore.exceptions import BotoCoreError, ClientError
import os
import shutil
import logging


class S3BucketNotFoundError(BotoCoreError):
    """Exception raised when the specified S3 bucket cannot be found."""
    fmt = "Could not find bucket - {bucket_name}, or {e}"

    def __init__(self, bucket_name, e="", **kwargs):
        """Bucket not found exception class."""
        kwargs["bucket_name"] = bucket_name
        kwargs["e"] = e
        super().__init__(**kwargs)


class S3BucketFailToCreateError(BotoCoreError):
    """Exception raised when an S3 bucket cannot be created."""
    fmt = "Failed to create S3 bucket: {reason}"

    def __init__(self, reason, **kwargs):
        """Bucket failed creation exception class."""
        kwargs["reason"] = reason
        super().__init__(**kwargs)


class FolderNotFoundError(BotoCoreError):
    """Exception raised when the specified folder within an S3 bucket cannot be found."""
    fmt = "Failed to find folder with id: {id} in bucket: {bucket_name}"

    def __init__(self, id, bucket_name, **kwargs):
        """Folder not found exception class."""
        kwargs["id"] = id
        kwargs["bucket_name"] = bucket_name
        super().__init__(**kwargs)


class FilesDownloadError(BotoCoreError):
    """Exception raised when files cannot be downloaded from an S3 bucket."""
    fmt = "Failed to download folder with id: {id} in bucket: {bucket_name}"

    def __init__(self, id, bucket_name, **kwargs):
        """Files download error exception class."""
        kwargs["id"] = id
        kwargs["bucket_name"] = bucket_name
        super().__init__(**kwargs)


class BucketUtil:
    """
    A utility class for managing S3 bucket operations including file and folder manipulation.
    
    This class provides methods to create and manage files within specified S3 buckets using the AWS SDK for Python (boto3).

    Attributes:
        bucket_name (str): The name of the S3 bucket.
        s3_client (boto3.client): The boto3 S3 client.
    """
    __BIN = os.path.join(os.getcwd(), "bin")

    def __init__(self, bucket_name, force=False, region="us-east-1"):
        """
        Initializes the BucketUtil class, checking for the existence of the specified S3 bucket, and optionally creating it if not present.

        Args:
            bucket_name (str): The name of the S3 bucket to manage.
            force (bool): If True, the bucket will be created if it does not exist. Defaults to False.
            region (str): The AWS region where the bucket is located (or will be created). Defaults to 'us-east-1'.
        """

        self.bucket_name = bucket_name

        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=region,
        )

        # Check that the bucket exists
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
        except ClientError as e:
            if force:
                # Create a new bucket with bucket_name
                try:
                    # create_bucket_config = {'LocationConstraint': region} if region else {}
                    res = self.s3_client.create_bucket(
                        Bucket=self.bucket_name,
                        # CreateBucketConfiguration=create_bucket_config
                    )
                    print(res)
                except ClientError as e:
                    raise S3BucketFailToCreateError(
                        reason=f"{e} Could not create bucket {self.bucket_name}"
                    )
            else:
                raise S3BucketNotFoundError(bucket_name=self.bucket_name, e=e)

    def list_ids(self):
        """
        Lists all folder-like prefixes in the bucket, which represent unique IDs.

        Returns:
            list: A list of folder IDs in the bucket.
        """

        response = self.s3_client.list_objects_v2(
            Bucket=self.bucket_name, Delimiter="/"
        )
        ids = [
            prefix.get("Prefix")[:-1] for prefix in response.get("CommonPrefixes", [])
        ]

        return ids

    def list_files_in_folder(self, id):
        """
        Lists all files within a specific folder identified by 'id' in the S3 bucket.

        Args:
            id (str): The folder ID whose files should be listed.

        Returns:
            list: A list of file names found in the specified folder. Returns an empty list if no files are found.

        Raises:
            FolderNotFoundError: If the specified folder ID does not exist in the bucket.
        """
        if id not in self.list_ids():
            raise FolderNotFoundError(id=id, bucket_name=self.bucket_name)

        try:
            # List objects in the bucket with the specified prefix (id)
            objects = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name, Prefix=f"{id}/"
            )

            file_names = [
                os.path.basename(obj["Key"]) for obj in objects.get("Contents", [])
            ]
            return file_names

        except ClientError as e:
            logging.error(e)
            return []

    def upload_file(self, id, file_name, file_content):
        """
        Uploads a file to a specific folder within the S3 bucket.

        Args:
            id (str): The folder ID where the file will be uploaded.
            file_name (str): The name of the file to upload.
            file_content (bytes): The content of the file to upload.

        Returns:
            bool: True if the file was uploaded successfully, False otherwise.
        """

        # Append the folder ID to the object_name to create a folder structure
        object_name = f"{id}/{file_name}"

        try:
            # Use put_object to upload file content directly
            self.s3_client.put_object(
                Body=file_content, Bucket=self.bucket_name, Key=object_name
            )
        except ClientError as e:
            logging.error(e)
            return False

        return True

    def delete_file_in_folder(self, id, file_name):
        """
        Deletes a specific file from a folder within the S3 bucket.

        Args:
            id (str): The folder ID from which the file will be deleted.
            file_name (str): The name of the file to delete.

        Returns:
            bool: True if the file was successfully deleted, False otherwise.
        """
        if id not in self.list_ids():
            raise FolderNotFoundError(id, self.bucket_name)

        try:
            # Construct the object key using the folder ID and file name
            object_key = f"{id}/{file_name}"

            # Delete the object from the S3 bucket
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=object_key)

            return True
        except ClientError as e:
            logging.error(e)
            return False

    def download_files(self, id):
        """
        Downloads all files from a specific folder ID within the S3 bucket to a local directory.

        Args:
            id (str): The folder ID whose files should be downloaded.

        Returns:
            bool: True if files were successfully downloaded, False otherwise.
        """
        if id not in self.list_ids():
            raise FolderNotFoundError(id, self.bucket_name)

        storage_path = os.path.join(os.getcwd(), self.__BIN, id)

        os.makedirs(storage_path, exist_ok=True)

        try:
            # List objects in the bucket with the specified prefix (id)
            objects = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name, Prefix=f"{id}/"
            )

            for obj in objects.get("Contents", []):
                # Extract the object key
                object_key = obj["Key"]

                # Extract the file name from the object key
                file_name = os.path.basename(object_key)

                # Download the file
                local_file_path = os.path.join(storage_path, file_name)
                self.s3_client.download_file(
                    self.bucket_name, object_key, local_file_path
                )

            return True
        except ClientError as e:
            logging.error(e)
            return False

    def delete_from_bin(self, id):
        """
        Deletes a local directory associated with a specific folder ID.

        Args:
            id (str): The folder ID associated with the local directory to be deleted.

        Returns:
            bool: True if the directory was successfully deleted, False otherwise.
        """

        storage_path = os.path.join(self.__BIN, id)

        if not os.path.exists(storage_path):
            return True
        try:
            shutil.rmtree(
                storage_path,
            )
            return True
        except OSError as e:
            logging.error(e)
            return False

    def delete_from_bucket(self, id):
        """
        Deletes all files and subfolders within a specific folder ID from the S3 bucket.

        Args:
            id (str): The folder ID from which files and subfolders will be deleted.

        Returns:
            bool: True if the folder was successfully deleted, False otherwise.
        """

        if id not in self.list_ids():
            raise FolderNotFoundError(id, self.bucket_name)

        try:
            # List objects in the bucket with the specified prefix (id)
            objects = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name, Prefix=f"{id}/"
            )

            # Extract and delete each object
            objects_to_delete = [
                {"Key": obj["Key"]} for obj in objects.get("Contents", [])
            ]

            if objects_to_delete:
                self.s3_client.delete_objects(
                    Bucket=self.bucket_name, Delete={"Objects": objects_to_delete}
                )
                return True
            else:
                return False

        except ClientError as e:
            logging.error(e)
            return False

    def create_upload_presigned_url(self, id, fields=None, conditions=None, expiration=3600):
        """
        Generates a presigned URL for uploading files to a specific folder ID in the S3 bucket.

        Args:
            id (str): The folder ID to which the file will be uploaded.
            fields (dict): Additional form fields to include in the presigned POST request.
            conditions (list): Conditions to include in the policy.
            expiration (int): The time in seconds for which the presigned URL is valid.

        Returns:
            dict: A dictionary containing the URL and fields for the presigned POST request, or None if an error occurs.
        """

        try:
            response = self.s3_client.generate_presigned_post(
                self.bucket_name,
                id,
                Fields=fields,
                Conditions=conditions,
                ExpiresIn=expiration,
            )
        except ClientError as e:
            logging.error(e)
            return None

        # The response contains the presigned URL and required fields
        return response


def main():
    # Example usage
    util = BucketUtil(bucket_name="your-bucket-name")
    print("Initialized S3 bucket utility for bucket:", util.bucket_name)

if __name__ == "__main__":
    main()