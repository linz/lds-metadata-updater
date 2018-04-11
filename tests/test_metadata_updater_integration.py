#!/usr/bin/python3

import unittest
import koordinates
import os
import sys
import types
import re

sys.path.append('../')  
from metadata_updater import metadata_updater

class TestMetadataUpdaterUpdFile(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestMetadataUpdaterUpdFile, self).__init__(*args, **kwargs)

    def setUp(self):
        """

        """

        conf_file = os.path.join(os.getcwd(), 'data/config.yaml')
        self.config = metadata_updater.ConfigReader(conf_file)
        self.lds_test_layer = '95322'

    def get_client(self):
        """
        Non test.
        Returns koordinates api client instance
        """

        return metadata_updater.get_client(self.config.domain, self.config.api_key)

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
        self.assertTrue(os.path.isfile(metadata_file))
        os.remove(metadata_file) 

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
        # The below results in v. slow tests
        self.assertTrue(len(list(all))>0)

    def test_add_to_pub_group(self):
        """
        Test getting of metadata
        1. Get client
        2. Get pub instance
        3. Get layer
        4. Get Draft
        5. Add to pub group
        """

        client = self.get_client()
        publisher = koordinates.Publish()
        layer = metadata_updater.get_layer(client, self.lds_test_layer)
        draft = metadata_updater.get_draft(layer)
        metadata_updater.add_to_pub_group(publisher, draft)
        regex = re.compile('https:\/\/data.linz.*{0}\/versions\/[0-9]*\/'.format(self.lds_test_layer))
        self.assertRegex(publisher.items[0], regex)
    
    def test_post_metadata(self):
        """
        Test getting of meta data
        1. Get client
        2. Get layer
        3. Get Matadata
        4. post unedited file back
        4. Remove file (Clean up)
        """

        client = self.get_client()
        layer = metadata_updater.get_layer(client, self.lds_test_layer)
        draft = metadata_updater.get_draft(layer)
        distination_dir = os.path.join(os.getcwd(), self.config.destination_dir)
        test_overwrite = self.config.test_overwrite
        metadata_file = metadata_updater.get_metadata(layer, distination_dir, test_overwrite)
        result = metadata_updater.post_metadata(draft, metadata_file)
        self.assertTrue(result)
        os.remove(metadata_file)
    
    def test_set_metadata(self):
        """
        1. Get Client
        2. Get Publisher
        3. Get Layer
        4. Get Draft
        5. Set metadata
        6. Check draft is in pub group
        """

        client = self.get_client()
        publisher = koordinates.Publish()
        layer = metadata_updater.get_layer(client, self.lds_test_layer)
        distination_dir = os.path.join(os.getcwd(), self.config.destination_dir)
        test_overwrite = self.config.test_overwrite
        metadata_file = metadata_updater.get_metadata(layer, distination_dir, test_overwrite)
        metadata_updater.set_metadata(layer, metadata_file, publisher)
        regex = re.compile('https:\/\/data.linz.*{0}\/versions\/[0-9]*\/'.format(self.lds_test_layer))
        self.assertRegex(publisher.items[0], regex)

if __name__ == '__main__':
    unittest.main()