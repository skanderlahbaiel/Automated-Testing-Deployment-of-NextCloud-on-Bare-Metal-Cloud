from functional_testing.utils.file_management import (
    compare_hashes,
    orange_text,
)
from functional_testing.config.configuration import (
    CREATED_FILES_PATH, 
    DOWNLOAD_DIRECTORY, 
)

def file_integrity(file_name):
    """
    Verifies the integrity of a file by comparing the hash of the uploaded file with that of the downloaded file.

    This function aims to ensure data integrity by verifying that a file, once uploaded and then downloaded from
    NextCloud, remains unaltered. It computes and compares the hash values of both the uploaded and downloaded
    versions of the file located in predetermined directories. A match in hash values indicates that the file has
    maintained its integrity throughout the upload and download process.

    :param file_name: The name of the file for which integrity is being checked. This name should include any
                      file extension and match exactly between the uploaded and downloaded files.
    :type file_name: str

    :return: Returns True if the hash values of the uploaded and downloaded files match, indicating the files are
             identical and integrity is preserved. Returns False if there is a mismatch in hash values, suggesting
             the files are different and integrity may have been compromised.
    :rtype: bool

    :raises AssertionError: Raises an assertion error if the hash comparison fails, indicating the uploaded and
                            downloaded files are not the same. This may point to issues in the file transfer process
                            or unauthorized alterations of the file content.

    **Example**::

        >>> file_name = "example_document.pdf"
        >>> integrity_check = file_integrity(file_name)
        >>> if integrity_check:
        ...     print("File integrity verified.")
        ... else:
        ...     print("File integrity compromised.")

    .. note::
        The function relies on the `compare_hashes` utility to perform the hash computation and comparison. Ensure
        that `DOWNLOAD_DIRECTORY` and `CREATED_FILES_PATH` in the configuration module accurately reflect the
        paths to where the NextCloud application stores downloaded files and where uploaded files are kept,
        respectively. It assumes that the upload and the download have been performed successfully.
    """
    try:
        orange_text(f"Checking the integrity of the file {file_name}...")
        compare_hashes(file_name, DOWNLOAD_DIRECTORY, CREATED_FILES_PATH)
        print("\033[92mFile integrity test passed\033[0m")  # Print in green
        return True
    except Exception as e:
        print(f"An error occurred during medium size file integrity check: {e}")
        return False
        