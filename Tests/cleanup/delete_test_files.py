import os
from functional_testing.config.configuration import DOWNLOAD_DIRECTORY
from functional_testing.config.configuration import CREATED_FILES_PATH

def delete_files_starting_with(prefix, directory):

    """
This module provides utility functions to delete test-related files from specified directories. 
It primarily supports cleanup activities post-testing by removing files that match a given prefix. 
This is particularly useful in scenarios where test execution generates temporary files that need to be cleaned up afterwards.

The module relies on environment variables to dynamically set the paths of directories involved in the testing processes, 
such as where downloaded files or created files during tests are stored. Users must configure these environment variables 
appropriately to ensure that the cleanup process targets the correct directories.

Environment Variables:
----------------------
The module uses the following environment variables to determine the directories for file cleanup operations:

- ``DOWNLOAD_DIRECTORY``: Specifies the directory path where files downloaded during tests are stored. This path is used
  by default if no other directory is specified in the cleanup function calls.
- ``CREATED_FILES_PATH``: Specifies the directory path where files created during tests are stored. This allows for
  separation of download and upload test artifacts.

Setting Environment Variables:
------------------------------
To set these environment variables in your environment, follow the instructions based on your operating system:

For Unix/Linux/macOS:
^^^^^^^^^^^^^^^^^^^^^

Open your terminal and use the ``export`` command to set each environment variable. For example:

.. code-block:: bash

   export DOWNLOAD_DIRECTORY=/path/to/download/directory
   export CREATED_FILES_PATH=/path/to/created/files/directory

These commands can be added to your shell profile file (e.g., ``.bashrc``, ``.zshrc``) to persist the variables across sessions.

For Windows:
^^^^^^^^^^^^

Use the System Properties dialog to set environment variables:

1. Open System Properties (you can search for it in the Start menu).
2. Go to the Advanced tab and click on Environment Variables.
3. Add new system variables for ``DOWNLOAD_DIRECTORY`` and ``CREATED_FILES_PATH`` with their respective paths.

Alternatively, set them temporarily in a Command Prompt window:

.. code-block:: powershell

   set DOWNLOAD_DIRECTORY=C:\\path\\to\\download\\directory
   set CREATED_FILES_PATH=C:\\path\\to\\created\\files\\directory

Functions:
----------
The module contains the following function(s):

- ``delete_files_starting_with(prefix, directory)``: Deletes files in the specified ``directory`` that 
  start with the given ``prefix``. By default, it targets the ``DOWNLOAD_DIRECTORY``. The function prints the names of 
  deleted files or indicates if no files were deleted.

Usage:
------
To use this module, import it into your test scripts and invoke ``delete_files_starting_with`` with the appropriate 
arguments. Here's an example that cleans up test-related files from both download and upload directories:

.. code-block:: python

   from functional_testing.cleanup import delete_files_starting_with, DOWNLOAD_DIRECTORY, CREATED_FILES_PATH

   # Delete downloaded test files
   delete_files_starting_with('test_', DOWNLOAD_DIRECTORY)

   # Delete uploaded/created test files
   delete_files_starting_with('test_', CREATED_FILES_PATH)

Ensure you have set the necessary environment variables as described to correctly target the cleanup directories.

.. note:: This module assumes that the specified directories exist and that the executing user has the necessary 
   permissions to delete files from them.
"""


    deleted_files = []  # Initialize an empty list to keep track of deleted files
    for filename in os.listdir(directory):
        if filename.startswith(prefix):
            os.remove(os.path.join(directory, filename))
            deleted_files.append(filename)  # Append the deleted filename to the list

    # Check if any files were deleted and print the list
    if deleted_files:
        print("Deleted files:")
        for file in deleted_files:
            print(file)
    else:
        print("No files were deleted.")



def main():
    """
    The main function that executes the cleanup process.

    This function calls `delete_files_starting_with` for both the download directory and the directory
    where created files are stored, using the prefix ``'test_'`` to identify files targeted for deletion.

    The main function is necessary because this script is intended to be executed directly, 
    specifically from a setup.sh file which automates the testing process. By defining a main function, 
    we ensure that the cleanup process is executed when the script is run as a standalone program. 
    This is controlled by the `if __name__ == "__main__":` condition at the end of the script.

    The main function is a common pattern in Python programming for providing a script entry point. 
    It allows the script to act as either reusable modules or as standalone programs.
    """
    delete_files_starting_with('test_', DOWNLOAD_DIRECTORY)
    delete_files_starting_with('test_', CREATED_FILES_PATH)

if __name__ == "__main__":
    main()
