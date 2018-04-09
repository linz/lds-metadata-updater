import unittest
import koordinates
import os
import sys
import types

sys.path.append('../')  
from metadata_updater import metadata_updater

class TestMetadataUpdaterUpdFile(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestMetadataUpdaterUpdFile, self).__init__(*args, **kwargs)
        self.file =  os.path.join(os.getcwd(), 'data/weed-kelp-polygons-hydro-14k-122k.iso.xml')

    def setUp(self):
        """

        """
        conf_file = os.path.join(os.getcwd(), 'data/config.yaml')
        self.config =  metadata_updater.ConfigReader(conf_file)

    def get_client(self):
        """
        Non test.
        Returns koordinates api client instance
        """
 
        return metadata_updater.get_client(self.config.domain, self.config.api_key)
# 
#     def get_layer(self, client, layer_id):
#         """
#         Non test.
#         Returns koordinates api client lib layer instance
#         """
# 
#         return metadata_updater.get_layer(client, layer_id) 
# 
# 
#     def get_metadata(self, layer, dir, overwrite):
#         """
#         Non test.
#         Returns koordinates api metadata instance
#         """
# 
#         return metadata_updater.get_metadata(layer, dir, overwrite)
# 
#     def get_draft(self, layer):
#         """
#         Non test.
#         Returns koordinates api client draft instance
#         """
# 
#         return metadata_updater.get_draft(layer)

    def test_get_client(self):
        """
        test koordinates client instance
        1. Get client
        """

        client = self.get_client()
        self.assertIsInstance(client, koordinates.client.Client)

    def test_get_layer(self):
        """
        Test getting of layer instance
        1. Get client
        2. Get layer        
        """
        
        client = self.get_client()        
        layer_id = self.config.layers[0]
        layer = metadata_updater.get_layer(client, layer_id)
        self.assertIsInstance(layer, koordinates.layers.Layer)

    def test_get_metadata(self):
        """
        Test getting of meta data
        1. Get client
        2. Get layer
        3. Get Matadata
        4. Remove file (Clean up)
        """

        client = self.get_client()
        layer_id = self.config.layers[0]
        layer = metadata_updater.get_layer(client, layer_id)
        distination_dir = os.path.join(os.getcwd(), self.config.destination_dir)
        test_overwrite = self.config.test_overwrite
        metadata_file = metadata_updater.get_metadata(layer, distination_dir, test_overwrite)
        result = self.assertTrue(os.path.isfile(metadata_file))
        if result: os.remove(metadata_file) 

    def test_update_metadata(self):
        """
        Not currently testing lds metadata updating
        could ensure a test data set is always left on the lds
        for this purpose. 
        
        edit. check it has been edited
        and then revert chnages for next test
        """
        pass        

    def test_get_draft(self):
        """
        Test getting of metadata
        1. Get client
        2. Get layer
        3. Get Draft
        """

        client = self.get_client()
        layer_id = self.config.layers[0]
        layer = metadata_updater.get_layer(client, layer_id)
        draft = metadata_updater.get_draft(layer)
        self.assertTrue(draft.is_draft_version)

    def test_iterate_all(self):
        """
        Test getting of "all" layers from catalog
        1. Get client
        2. Get layer
        3. Get 'All' layers
        """

        client = self.get_client()
        all = metadata_updater.iterate_all(client)
        self.assertIsInstance(all, types.GeneratorType)

if __name__ == '__main__':
    unittest.main()