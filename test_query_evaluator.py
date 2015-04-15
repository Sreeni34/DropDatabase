import unittest
from query_evaluator import Query_Evaluator

class TestQueryEvaluator(unittest.TestCase):

    def test_add_node(self):
        ''' 
        Tests add_node method of Query_Evaluator.
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

    def test_add_relationship(self):
        '''
        Tests add_relationship method for Query_Evaluator.
        '''
        q = Query_Evaluator()
        attrs1 = {'Label' : 'Person', 'Name' : 'Alice'}
        attrs2 = {'Label' : 'Person', 'Name' : 'Bob'}
        attrs3 = {'Label' : 'Person', 'Name' : 'John'}
        node1 = q.add_node(attrs1)
        node2 = q.add_node(attrs2)
        node3 = q.add_node(attrs3)
        edge_attrs1 = {'rel_type' : 'friend'}
        edge_attrs2 = {'rel_type' : 'cousin'}
        # Test first edge
        edge1 = q.add_relationship(node1, node2, edge_attrs1)
        self.assertEqual(edge1, (node1[0], node2[0], edge_attrs1))
        # Test second edge
        edge2 = q.add_relationship(node2, node3, edge_attrs2)
        self.assertEqual(edge2, (node2[0], node3[0], edge_attrs2))





if __name__ == '__main__':
    unittest.main()