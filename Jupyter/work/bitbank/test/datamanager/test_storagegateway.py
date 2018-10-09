import sys
import os
import unittest
sys.path.append(os.pardir + '/../')
from modules.datamanager import storagegateway


class TestStorageGateway(unittest.TestCase):

    def setUp(self):
        """
        バケット: z2vub190exbllgfuzcbmaxruzxnz
        サービスアカウントを認証するキーのjsonの各要素は標準入力から得る
        """
        bucket_name = 'z2vub190exbllgfuzcbmaxruzxnz'
        print("type: ", end="")
        dict_type = input()
        print("project_id: ", end="")
        dict_project_id = input()
        print("private_key_id: ", end="")
        dict_private_key_id = input()
        print("private_key: ", end="")
        dict_private_key = input()
        print("client_email: ", end="")
        dict_client_email = input()
        print("client_id: ", end="")
        dict_client_id = input()
        print("auth_uri: ", end="")
        dict_auth_uri = input()
        print("token_uri: ", end="")
        dict_token_uri = input()
        print("auth_provider_x509_cert_url: ", end="")
        dict_auth_provider_x509_cert_url = input()
        print("client_x509_cert_url: ", end="")
        dict_client_x509_cert_url = input()

        api_key_dict = dict()
        api_key_dict['type'] = dict_type
        api_key_dict['project_id'] = dict_project_id
        api_key_dict['private_key_id'] = dict_private_key_id
        api_key_dict['private_key'] = dict_private_key
        api_key_dict['client_email'] = dict_client_email
        api_key_dict['client_id'] = dict_client_id
        api_key_dict['auth_uri'] = dict_auth_uri
        api_key_dict['token_uri'] = dict_token_uri
        api_key_dict['auth_provider_x509_cert_url'] = dict_auth_provider_x509_cert_url
        api_key_dict['client_x509_cert_url'] = dict_client_x509_cert_url

        self.storage_gateway = storagegateway.StorageGateway(bucket_name, api_key_dict)

    def test_upload(self):
        """
        アップロードのテスト
        GCP ストレージにファイルがアップロードされているか
        :return:
        """
        self.storage_gateway.upload('sample.py', '__init__.py')

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
