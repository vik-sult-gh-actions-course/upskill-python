import os

class SftpFileTransfer:
    def __init__(self, sftp_client, remote_base_path, local_base_path):
        self.sftp_client = sftp_client
        self.remote_base_path = remote_base_path
        self.local_base_path = local_base_path

    def transfer_files(self):
        """Transfer all files from remote SFTP directory to local directory"""
        try:
            list_of_files = self.sftp_client.listdir(self.remote_base_path)

            for file in list_of_files:
                self._transfer_single_file(file)

        finally:
            self.sftp_client.close()

    def _transfer_single_file(self, filename):
        """Transfer a single file from remote to local"""
        remote_path = os.path.join(self.remote_base_path, filename)
        local_path = os.path.join(self.local_base_path, filename)

        # print(f"{remote_path} >>> {local_path}")
        self.sftp_client.get(remote_path, local_path)