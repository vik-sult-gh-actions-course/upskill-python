"""Module for handling file transfers between SFTP server and local filesystem."""

import os


class SftpFileTransfer:  # pylint: disable=too-few-public-methods
    """Handles file transfers between a remote SFTP server and local filesystem.

    Attributes:
        sftp_client: Connected SFTP client instance
        remote_base_path: Base path on the remote SFTP server
        local_base_path: Base path on the local filesystem
    """

    def __init__(self, sftp_client, remote_base_path, local_base_path):
        """Initialize the SFTP file transfer handler.

        Args:
            sftp_client: Connected SFTP client instance
            remote_base_path: Base path on the remote SFTP server
            local_base_path: Base path on the local filesystem
        """
        self.sftp_client = sftp_client
        self.remote_base_path = remote_base_path
        self.local_base_path = local_base_path

    def transfer_files(self):
        """Transfer all files from remote SFTP directory to local directory."""
        try:
            list_of_files = self.sftp_client.listdir(self.remote_base_path)

            for file in list_of_files:
                self._transfer_single_file(file)

        finally:
            self.sftp_client.close()

    def _transfer_single_file(self, filename):
        """Transfer a single file from remote to local.

        Args:
            filename: Name of the file to transfer
        """
        remote_path = os.path.join(self.remote_base_path, filename)
        local_path = os.path.join(self.local_base_path, filename)

        self.sftp_client.get(
            remote_path, local_path
        )  # pylint: disable=missing-final-newline
