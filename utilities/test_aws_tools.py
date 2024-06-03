import pytest
from .aws_tools import BucketUtil, S3BucketNotFoundError, S3BucketFailToCreateError, FolderNotFoundError
from botocore.exceptions import ClientError

# Mocking boto3 client
import boto3
from moto import mock_aws


# Fixture for initializing BucketUtil
@pytest.fixture
def s3_util():
    with mock_aws():
        # Create a mock S3 bucket
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket="test-bucket")
        yield BucketUtil(bucket_name="test-bucket", force=True)

# Test cases
def test_bucket_util_initialization():
    # Test initialization with existing bucket
    util = BucketUtil(bucket_name="test-bucket")
    assert util.bucket_name == "test-bucket"

    # Test initialization with non-existing bucket and force=False
    with pytest.raises(S3BucketNotFoundError):
        BucketUtil(bucket_name="non-existing-bucket")

    # Test initialization with non-existing bucket and force=True
    with pytest.raises(S3BucketFailToCreateError):
        BucketUtil(bucket_name="non-existing-bucket", force=True)

def test_list_ids(s3_util):
    # Add some folders to the bucket
    s3_util.s3_client.put_object(Bucket="test-bucket", Key="folder1/")
    s3_util.s3_client.put_object(Bucket="test-bucket", Key="folder2/")
    assert s3_util.list_ids() == ["folder1", "folder2"]

def test_list_files_in_folder(s3_util):
    # Add some files to a folder
    s3_util.s3_client.put_object(Bucket="test-bucket", Key="folder1/file1.txt", Body=b"File content")
    s3_util.s3_client.put_object(Bucket="test-bucket", Key="folder1/file2.txt", Body=b"File content")
    
    # Test listing files in the folder
    assert s3_util.list_files_in_folder("folder1") == ["file1.txt", "file2.txt"]

def test_upload_file(s3_util):
    # Test uploading a file
    assert s3_util.upload_file(id="folder1", file_name="test.txt", file_content=b"Test content")
    # Verify the file was uploaded
    objects = s3_util.s3_client.list_objects_v2(Bucket="test-bucket", Prefix="folder1/")
    assert len(objects.get("Contents", [])) == 1

def test_delete_file_in_folder(s3_util):
    # Add a file to a folder
    s3_util.s3_client.put_object(Bucket="test-bucket", Key="folder1/file1.txt", Body=b"File content")

    # Test deleting the file
    assert s3_util.delete_file_in_folder(id="folder1", file_name="file1.txt")

    # Verify the file was deleted
    objects = s3_util.s3_client.list_objects_v2(Bucket="test-bucket", Prefix="folder1/")
    assert len(objects.get("Contents", [])) == 0

def test_download_files(s3_util, tmp_path):
    # Add some files to a folder
    s3_util.s3_client.put_object(Bucket="test-bucket", Key="folder1/file1.txt", Body=b"File content")
    s3_util.s3_client.put_object(Bucket="test-bucket", Key="folder1/file2.txt", Body=b"File content")

    # Test downloading files
    assert s3_util.download_files(id="folder1")

    # Verify files were downloaded
    assert (tmp_path / "folder1" / "file1.txt").is_file()
    assert (tmp_path / "folder1" / "file2.txt").is_file()

def test_create_upload_presigned_url(s3_util):
    # Test generating presigned URL
    url = s3_util.create_upload_presigned_url(id="folder1")
    assert url is not None
    assert "url" in url
    assert "fields" in url

    # Verify the presigned URL is valid by attempting to upload a file using it
