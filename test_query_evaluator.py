import unittest
from query_evaluator import QueryEvaluator
from graph_structure import GraphStructure

class TestQueryEvaluator(unittest.TestCase):

    def test_add_node(self):
        """ 
        Tests add_node method of QueryEvaluator.
        """
        gs = GraphStructure()
        q = QueryEvaluator(gs)
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
        """
        Tests add_relationship method for QueryEvaluator.
        """
        gs = GraphStructure()
        q = QueryEvaluator(gs)
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

    def test_match_node(self):
        """
        Tests match_node method for QueryEvaluator.
        """
        gs = GraphStructure()
        q = QueryEvaluator(gs)
        attrs1 = {'Label' : 'Person', 'Name' : 'Alice'}
        attrs2 = {'Label' : 'Person', 'Name' : 'Bob'}
        attrs3 = {'Label' : 'Person', 'Name' : 'John'}
        node1 = q.add_node(attrs1)
        node2 = q.add_node(attrs2)
        node3 = q.add_node(attrs3)
        # Test matching all node
        match_lst1 = q.match_node({'Label' : 'Person'})
        self.assertEqual(match_lst1, [node1, node2, node3])
        # Test matching single node
        match_lst2 = q.match_node({'Name' : 'Alice'})
        self.assertEqual(match_lst2, [node1])
        
    def test_match_rel(self):
        """
        Tests match_rel method for QueryEvaluator.
        """
        gs = GraphStructure()
        q = QueryEvaluator(gs)
        attrs1 = {'Label' : 'Person', 'Name' : 'Alice'}
        attrs2 = {'Label' : 'Person', 'Name' : 'Bob'}
        attrs3 = {'Label' : 'Person', 'Name' : 'John'}
        node1 = q.add_node(attrs1)
        node2 = q.add_node(attrs2)
        node3 = q.add_node(attrs3)
        edge_attrs1 = {'rel_type' : 'friend'}
        edge_attrs2 = {'rel_type' : 'friend', 'fam' : 'cousin'}
        edge1 = q.add_relationship(node1, node2, edge_attrs1)
        edge2 = q.add_relationship(node2, node3, edge_attrs2)
        # Test matching relationship with multiple results
        match_lst1 = q.match_rel(edge_attrs1)
        result1 = [(node1[0], node2[0], edge_attrs1), 
                    (node2[0], node3[0], edge_attrs2)]
        self.assertEqual(sorted(match_lst1), sorted(result1))
        # Test matching relationship with single results
        match_lst2 = q.match_rel(edge_attrs2)
        result2 = [(node2[0], node3[0], edge_attrs2)]
        self.assertEqual(match_lst2, result2)

    def test_match_node_rel(self):
        """
        Tests match_node_rel method for QueryEvaluator.
        """
        gs = GraphStructure()
        q = QueryEvaluator(gs)
        attrs1 = {'Label' : 'Person', 'Name' : 'Alice'}
        attrs2 = {'Label' : 'Person', 'Name' : 'Bob'}
        attrs3 = {'Label' : 'Person', 'Name' : 'John'}
        node1 = q.add_node(attrs1)
        node2 = q.add_node(attrs2)
        node3 = q.add_node(attrs3)
        edge_attrs1 = {'rel_type' : 'friend'}
        edge_attrs2 = {'rel_type' : 'friend', 'fam' : 'cousin'}
        edge1 = q.add_relationship(node1, node2, edge_attrs1)
        edge2 = q.add_relationship(node2, node3, edge_attrs2)
        edge3 = q.add_relationship(node2, node1, edge_attrs1)
        # Test matching with no results
        match_lst1 = q.match_node_rel(node1[1], edge_attrs2)
        result1 = []
        self.assertEqual(match_lst1, result1)
        # Test matching with single result
        match_lst2 = q.match_node_rel(node2[1], edge_attrs2)
        result2 = [(node2[0], node3[0], edge_attrs2)]
        self.assertEqual(match_lst2, result2)
        # Test matching with multiple result
        match_lst3 = q.match_node_rel(node2[1], {'rel_type' : 'friend'})
        result3 = [(node2[0], node1[0], edge_attrs1),
                    (node2[0], node3[0], edge_attrs2)]

        self.assertEqual(match_lst3, result3)

    def test_match_find_rel(self):
        """
        Tests match_find_rel method for QueryEvaluator.
        """
        gs = GraphStructure()
        q = QueryEvaluator(gs)
        attrs1 = {'Label' : 'Person', 'Name' : 'Alice'}
        attrs2 = {'Label' : 'Person', 'Name' : 'Bob'}
        attrs3 = {'Label' : 'Person', 'Name' : 'John'}
        node1 = q.add_node(attrs1)
        node2 = q.add_node(attrs2)
        node3 = q.add_node(attrs3)
        edge_attrs1 = {'rel_type' : 'friend'}
        edge_attrs2 = {'rel_type' : 'friend', 'fam' : 'cousin'}
        edge1 = q.add_relationship(node1, node2, edge_attrs1)
        edge2 = q.add_relationship(node2, node3, edge_attrs2)
        # Test matching with no results
        match_lst1 = q.match_find_rel(node1[1], node3[1])
        result1 = []
        self.assertEqual(match_lst1, result1)
        # Test matching with result
        match_lst2 = q.match_find_rel(node1[1], node2[1])
        result2 = [(node1[0], node2[0], edge_attrs1)]
        self.assertEqual(match_lst2, result2)

    def test_match_node_node_rel(self):
        """
        Tests match_node_node_rel method for QueryEvaluator.
        """
        gs = GraphStructure()
        q = QueryEvaluator(gs)
        attrs1 = {'Label' : 'Person', 'Name' : 'Alice'}
        attrs2 = {'Label' : 'Person', 'Name' : 'Bob'}
        attrs3 = {'Label' : 'Person', 'Name' : 'John'}
        node1 = q.add_node(attrs1)
        node2 = q.add_node(attrs2)
        node3 = q.add_node(attrs3)
        edge_attrs1 = {'rel_type' : 'friend'}
        edge_attrs2 = {'rel_type' : 'friend', 'fam' : 'cousin'}
        edge1 = q.add_relationship(node1, node2, edge_attrs1)
        edge2 = q.add_relationship(node2, node3, edge_attrs2)
        # Test matching with no results
        match_lst1 = q.match_node_node_rel(node1[1], node2[1], edge_attrs2)
        result1 = []
        self.assertEqual(match_lst1, result1)
        # Test matching with single result
        match_lst2 = q.match_node_node_rel(node1[1], node2[1], edge_attrs1)
        result2 = [(node1[0], node2[0], edge_attrs1)]
        self.assertEqual(match_lst2, result2)
        # Test matching with multiple results
        match_lst3 = q.match_node_node_rel({'Label' : 'Person'},
                        {'Label' : 'Person'}, {'rel_type' : 'friend'})
        result3 = [(node1[0], node2[0], edge_attrs1),
                    (node2[0], node3[0], edge_attrs2)]
        self.assertEqual(match_lst3, result3)


    def test_delete_node(self):
        """
        Tests delete_node method for QueryEvaluator.
        """
        gs = GraphStructure()
        q = QueryEvaluator(gs)
        attrs1 = {'Label' : 'Person', 'Name' : 'Alice'}
        attrs2 = {'Label' : 'Person', 'Name' : 'Bob'}
        attrs3 = {'Label' : 'Person', 'Name' : 'John'}
        node1 = q.add_node(attrs1)
        node2 = q.add_node(attrs2)
        node3 = q.add_node(attrs3)
        edge_attrs1 = {'rel_type' : 'friend'}
        edge_attrs2 = {'rel_type' : 'friend', 'fam' : 'cousin'}
        edge1 = q.add_relationship(node1, node2, edge_attrs1)
        edge2 = q.add_relationship(node2, node3, edge_attrs2)
        # Tests deleting no nodes
        q.delete_node({'Label' : 'Person', 'Name' : 'Fred'})
        match_lst1 = q.match({}, {}, {})
        result1 = [(node1[0], node2[0], edge_attrs1),
                    (node2[0], node3[0], edge_attrs2)]
        self.assertEqual(match_lst1, result1)
        # Tests deleting nodes
        q.delete_node({'Label' : 'Person', 'Name' : 'Bob'})
        match_lst2 = q.match({}, {}, {})
        result2 = []
        self.assertEqual(match_lst2, result2)

    def test_delete_rel(self):
        """
        Tests delete_rel method for QueryEvaluator.
        """
        gs = GraphStructure()
        q = QueryEvaluator(gs)
        attrs1 = {'Label' : 'Person', 'Name' : 'Alice'}
        attrs2 = {'Label' : 'Person', 'Name' : 'Bob'}
        attrs3 = {'Label' : 'Person', 'Name' : 'John'}
        node1 = q.add_node(attrs1)
        node2 = q.add_node(attrs2)
        node3 = q.add_node(attrs3)
        edge_attrs1 = {'rel_type' : 'friend'}
        edge_attrs2 = {'rel_type' : 'friend', 'fam' : 'cousin'}
        edge1 = q.add_relationship(node1, node2, edge_attrs1)
        edge2 = q.add_relationship(node2, node3, edge_attrs2)
        # Tests deleting no relationship
        q.delete_rel({'rel_type' : 'friend', 'fam' : 'dad'})
        match_lst1 = q.match({}, {}, {})
        result1 = [(node1[0], node2[0], edge_attrs1),
                    (node2[0], node3[0], edge_attrs2)]
        self.assertEqual(match_lst1, result1)
        # Tests deleting relationship
        q.delete_rel(edge_attrs1)
        match_lst2 = q.match({}, {}, {})
        result2 = []
        self.assertEqual(match_lst2, result2)

    def test_modify_node(self):
        """
        Tests modify_node method for QueryEvaluator.
        """
        gs = GraphStructure()
        q = QueryEvaluator(gs)
        attrs1 = {'Label' : 'Person', 'Name' : 'Alice'}
        attrs2 = {'Label' : 'Person', 'Name' : 'Bob'}
        attrs3 = {'Label' : 'Person', 'Name' : 'John'}
        node1 = q.add_node(attrs1)
        node2 = q.add_node(attrs2)
        node3 = q.add_node(attrs3)
        edge_attrs1 = {'rel_type' : 'friend'}
        edge_attrs2 = {'rel_type' : 'friend', 'fam' : 'cousin'}
        edge1 = q.add_relationship(node1, node2, edge_attrs1)
        edge2 = q.add_relationship(node2, node3, edge_attrs2)
        # Tests adding attributes to node
        q.modify_node(attrs1, {'Age' : '10'}, True)
        match_lst1 = q.match_node(attrs1)
        result1 = [(node1[0], {'Label' : 'Person', 'Name' : 'Alice', 'Age' : '10'})]
        self.assertEqual(match_lst1, result1)
        # Tests removing attributes to node
        q.modify_node(attrs1, {'Age' : '10'}, False)
        match_lst2 = q.match_node(attrs1)
        result2 = [(node1[0], attrs1)]
        self.assertEqual(match_lst2, result2)

    def test_modify_rel(self):
        """
        Test modify_rel method for QueryEvaluator.
        """
        gs = GraphStructure()
        q = QueryEvaluator(gs)
        attrs1 = {'Label' : 'Person', 'Name' : 'Alice'}
        attrs2 = {'Label' : 'Person', 'Name' : 'Bob'}
        attrs3 = {'Label' : 'Person', 'Name' : 'John'}
        node1 = q.add_node(attrs1)
        node2 = q.add_node(attrs2)
        node3 = q.add_node(attrs3)
        edge_attrs1 = {'rel_type' : 'friend'}
        edge_attrs2 = {'rel_type' : 'friend', 'fam' : 'cousin'}
        edge1 = q.add_relationship(node1, node2, edge_attrs1)
        edge2 = q.add_relationship(node2, node3, edge_attrs2)
        # Tests adding attributes to relationship
        q.modify_rel(edge_attrs2, {'like' : 'no'}, True)
        match_lst1 = q.match_rel(edge_attrs2)
        result1 = [(node2[0], node3[0], {'rel_type' : 'friend', 
                                            'fam' : 'cousin',
                                            'like' : 'no'})]
        self.assertEqual(sorted(match_lst1), sorted(result1))
        # Tests deleting attributes to relationship
        q.modify_rel(edge_attrs2, {'like' : 'no'}, False)
        match_lst2 = q.match_rel(edge_attrs2)
        result2 = [(node2[0], node3[0], edge_attrs2)]
        self.assertEqual(sorted(match_lst2), sorted(result2))



if __name__ == '__main__':
    unittest.main()