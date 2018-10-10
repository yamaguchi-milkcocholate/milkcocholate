import os
import json
from google.cloud import storage


class StorageGateway:
    """
    GCP ストレージへのサービスアカウントAPIを使うときはこのクラスを利用する
    """

    def __init__(self, bucket_name, api_key_dict):
        """

        :param bucket_name:   string バケット名
        :param api_key_dict:  dict   サービスアカウントのAPIキー 認証用にjsonを作成できるので、その内容が入っている
        [
            type, project_id,
            private_key_id,
            private_key,
            client_email,
            client_id,
            auth_uri,
            token_uri,
            auth_provider_x509_cert_url,
            client_x509_cert_url,
        ]
        """
        api_file = 'api_key.json'
        with open(api_file, 'w') as f:
            json.dump(api_key_dict, f, indent=2)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = api_file
        self._client = storage.Client()
        self._bucket = self._client.get_bucket(bucket_name)
        self.bucket_name = bucket_name
        os.remove(api_file)

    def upload(self, new_file, local_file):
        """
        CGP ストレージにホストからファイルをアップロード
        :param new_file:    GCP ストレージで作成されるファイルの名前(ディレクトリ + ファイル)
        :param local_file:  GCP ストレージで作成されるファイルの内容
        """
        blob = self._bucket.blob(new_file)
        blob.upload_from_filename(filename=local_file)
        print('Success!! upload "' + local_file + '" as name: "' + new_file + '" in bucket: [' + self.bucket_name + ']')

