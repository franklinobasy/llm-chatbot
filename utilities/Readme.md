# utilities
This contains files and modules which provides utility classes for managing operations related to Amazon S3 buckets and files.

#### Classes:
    - S3BucketNotFoundError: Exception raised when the specified S3 bucket cannot be found.
    - S3BucketFailToCreateError: Exception raised when an S3 bucket cannot be created.
    - FolderNotFoundError: Exception raised when the specified folder within an S3 bucket cannot be found.
    - FilesDownloadError: Exception raised when files cannot be downloaded from an S3 bucket.
    - BucketUtil: Utility class for managing S3 bucket operations including file and folder manipulation.

###### Usage:
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

## tools
This module provides decorators for performance measurement and other common tools 
used throughout the codebase. 
The module aims to enhance debugging and performance optimization 
by allowing easy integration of time measurement across functions.

Available Decorators:
- `duration`: Measures the execution time of any callable (function or method) and prints it.

Usage:
------
This module is intended to be imported and its decorators applied to various functions
throughout a project where performance measurement is necessary.

Example:
--------
```python
from tools import duration

@duration
def example_function():
    import time
    time.sleep(2)  # Simulates a delay
    return "Function has completed."

When executed, this decorates `example_function()` such that its execution time is automatically
measured and printed to stdout, along with returning its original result.

Dependencies:
-------------
- Python 3.10+ due to the use of type hints and other modern Python features.
```