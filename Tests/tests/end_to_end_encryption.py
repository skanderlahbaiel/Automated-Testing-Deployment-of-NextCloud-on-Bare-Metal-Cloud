"""
Testing End-to-End Encryption (E2EE) in Nextcloud Client
========================================================

This documentation provides a comprehensive guide to manually test the End-to-End Encryption (E2EE) functionality in the Nextcloud client. E2EE is designed to protect user data from access by the server or any other unauthorized entities. Due to the complexity of interacting with the GUI in a Linux environment, this test is conducted manually.

Prerequisites
-------------
Before proceeding with the testing, ensure the following prerequisites are met:

- A functioning Nextcloud server deployment.
- Access to a Linux environment with GUI support for installing and operating the Nextcloud client.
- Administrative access to the Kubernetes cluster where Nextcloud is deployed, to verify encrypted files directly on the server.

Steps
-----
1. **Install and Enable the End-to-End Encryption App**:
   Before installing the Nextcloud client, ensure the End-to-End Encryption (E2EE) app is installed and enabled on your Nextcloud server. This app is crucial for securing your files during storage and transfer.

   - **Navigate to Apps**:
     Log into your Nextcloud server web interface as an administrator.

   .. image:: ../media/screenshots/navigate_to_apps.png
      :width: 150
      :alt: Navigating to the Apps section
      :align: center

   - **Access the Apps Management Page**:
     Click on your user profile icon at the top right corner of the interface and select 'Apps' from the dropdown menu.
   
   - **Install the End-to-End Encryption App**:
     In the Apps management page, go to the 'Files' category. Find the 'End-to-End Encryption' app in the list, and click 'Download and enable'.
   
   .. image:: ../media/screenshots/download_e2ee.png
      :width: 400
      :alt: Downloading and Enabling the End-to-End Encryption App
      :align: center

   - **Enable the App**:
     After the download completes, the app will automatically be enabled. Verify this by checking that it appears in your list of enabled apps.

   **Note:**
   - Ensure that your Nextcloud server is compatible with the version of the End-to-End Encryption app you intend to install. Compatibility details are usually listed on the app’s page within the Apps management interface.


2. **Verify E2EE App Activation**:
   - Confirm the activation of the End-to-End Encryption app by navigating to 'Settings' under your profile menu. Check the 'Security' section to see if the End-to-End Encryption settings are available and configured correctly.

   .. image:: ../media/screenshots/verify_e2ee.png
      :width: 400
      :alt: Verifying End-to-End Encryption Activation
      :align: center


3. **Download and Install the Nextcloud Client**:
   This section outlines two methods to install the Nextcloud client on Linux: using Snap and using the APT repository. Follow the method that best suits your environment.

   **Using Snap:**

   - Update your package index and install snapd if it's not already installed:
   
     .. code-block:: bash

        sudo apt update
        sudo apt install snapd

   - Install the Nextcloud desktop client using Snap:

     .. code-block:: bash

        sudo snap install nextcloud-desktop-client


   **Using APT Repository (For Ubuntu 17.10 and later):**

   - Open a terminal window and add the Nextcloud PPA to your system:
   
     .. code-block:: bash

        sudo add-apt-repository ppa:nextcloud-devs/client

   - Update the package index after adding the PPA:
   
     .. code-block:: bash

        sudo apt update

   - Install the Nextcloud client:

     .. code-block:: bash

        sudo apt install nextcloud-client


   **Note:**
   
   - The Snap method is generally simpler and provides automatic updates to the Nextcloud client.
   
   - The APT method allows for more control over the installation process and may provide a more integrated system experience depending on your specific Linux distribution.

   Choose the installation method that aligns with your system management preferences and follow the corresponding steps to complete the installation.


4. **Connect the Client to the Nextcloud Server**:

   - Launch the Nextcloud client.
   
    .. image:: ../media/screenshots/login.png
      :width: 400
      :alt: Connecting Nextcloud Client to Server
      :align: center
      
   - Click on the loin button
   - Enter the URL of your Nextcloud server and provide the necessary credentials to establish a connection.
   
   .. image:: ../media/screenshots/add_uri.png
      :width: 400
      :alt: Connecting Nextcloud Client to Server
      :align: center
 
   - Accept the connection request from the server and log in to your Nextcloud account.
      
   .. image:: ../media/screenshots/accept-connection.png
      :width: 400
      :alt: Connecting Nextcloud Client to Server
      :align: center
      
   .. image:: ../media/screenshots/grant.png
      :width: 400
      :alt: Connecting Nextcloud Client to Server
      :align: center
      

      
5. **Create and Encrypt a Folder**:

   - Within the Nextcloud client, create a new folder. You can name it `TestE2EE`.
   
   .. image:: ../media/screenshots/create_new_folder.png
      :width: 400
      :alt: Creating and Encrypting a Folder
      :align: center
      
   - Inside this folder, create a new text file named `test.txt`.
   - Enter some content into the text file, for example, "This is a test for E2EE."

   .. image:: ../media/screenshots/text.png
      :width: 400
      :alt: Creating and Encrypting a Folder
      :align: center

   - Save the file. Then, right-click on the `TestE2EE` folder and select the option to encrypt the folder.
   
   .. image:: ../media/screenshots/encrypt.png
      :width: 400
      :alt: Creating and Encrypting a Folder
      :align: center

6. **Verify the File on the Server**:

   - Access your Kubernetes cluster where Nextcloud is deployed.
   
   - Use the command line to run:
   
     .. code-block:: bash

        kubectl get pv

   - Identify the persistent volume (PV) used by Nextcloud, usually tagged as `nextcloud-data`.
   - Describe the PV to find the storage path on the node:
   
     .. code-block:: bash

        kubectl describe pv nextcloud-data

   - Execute sudo -i and then access the server's storage path where Nextcloud data is stored:
   
     .. code-block:: bash
     
        sudo -i
        cd <path-to-my-nextcloud-data-pvc-directory>/data/admin/files
        cd test_E2EE
        ls
        

   - Navigate to the directory containing user files and attempt to read the contents of `test.txt`:
   
     .. code-block:: bash

        cat <username>/files/<encrypted file name>.txt
   
   .. image:: ../media/screenshots/get-describe.png
      :width: 400
      :alt: Verifying File Encryption
      :align: center
      
   .. image:: ../media/screenshots/cd.png
      :width: 400
      :alt: Verifying File Encryption
      :align: center

7. **Check Encryption**:

   - Review the output from the `cat` command.
   
   - The contents of `test.txt` should appear garbled or encrypted, indicating that E2EE is functioning correctly.
   
   .. image:: ../media/screenshots/encrypted_file.png
      :width: 400
      :alt: Checking Encryption Output
      :align: center

Conclusion
----------
This manual test confirms whether E2EE is effectively encrypting files as expected, preventing unauthorized access even if server storage is compromised. Due to the nature of manual testing, this process is recommended to be conducted periodically to ensure ongoing compliance and functionality of the E2EE feature in Nextcloud.

Note
----
For automated tests or more complex scenarios, consider scripting interactions with the Nextcloud client using tools capable of GUI automation, tailored for your specific testing environment and requirements.

"""