import unittest
from query_evaluator import Query_Evaluator

class TestQueryEvaluator(unittest.TestCase):

    # Test add_node method

    def test_add_one_node(self):
        ''' 
        Tests add_node method of Query_Evaluator for adding a 
        single node. 
        '''
        q = Query_Evaluator()
        attrs1 = {'Label' : 'Person', 'Name' : 'You'}
        # Test single node
        node1 = q.add_node(attrs1)
        self.assertEqual(node1[0], 1)
        self.assertEqual(node1[1], attrs1)

    def test_add_many_nodes(self):
        ''' 
        Tests add_node method of Query_Evaluator for adding
        multiple nodes. 
        '''
        q = Query_Evaluator()
        attrs1 = {'Label' : 'Person', 'Name' : 'You'}
        attrs2 = {'Label' : 'Person', 'Name' : 'Me'}
        attrs3 = {'Label' : 'Person', 'Name' : 'She', 'Age' : 23}
        # Test first node
        node1 = q.add_node(attrs1)
        self.assertEqual(node1[0], 1)
        self.assertEqual(node1[1], attrs1)
        # Test second node
        node2 = q.add_node(attrs2)
        self.assertEqual(node2[0], 2)
        self.assertEqual(node2[1], attrs2)
        # Test third node
        node3 = q.add_node(attrs3)
        self.assertEqual(node3[0], 3)
        self.assertEqual(node3[1], attrs3)

        



if __name__ == '__main__':
    unittest.main()