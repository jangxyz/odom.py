#!/usr/bin/python

import unittest
import odom

class OdomParseTestCase(unittest.TestCase):
    def setUp(self):
        self.xml = '''
<Game Num="123" Name="Tetris"> 
  <Server Seq="10034" Name="Server01" biBasePrice="100" Unit="Gold"> 
    <TradeDate Date="10-10" Price="420" TradeCount="20" UpDownPrice="30" /> 
    <TradeDate Date="10-11" Price="390" TradeCount="42" UpDownPrice="-10" /> 
  </Server> 
</Game>'''

    def test_parse(self):
        o = odom.ODOM()
        root = o.parse(self.xml)

class OdomTestCase(unittest.TestCase):
    """ """
    def setUp(self):
        xml = '''
<Game Num="123" Name="Tetris"> 
  <Server Seq="10034" Name="Server01" biBasePrice="100" Unit="Gold"> 
    <TradeDate Date="10-10" Price="420" TradeCount="20" UpDownPrice="30" /> 
    <TradeDate Date="10-11" Price="390" TradeCount="42" UpDownPrice="-10" /> 
  </Server> 
</Game>
        '''
        o = odom.ODOM()
        self.root = o.parse(xml)

    def tearDown(self):
        pass

    def test_root(self):
        self.assertTrue(isinstance(self.root, odom.OdomElementNode))

    def test_child_node(self):
        self.assertTrue(isinstance(self.root.Server, odom.OdomElementNode))

    def test_child_node_chained(self):
        self.root.Server.TradeDate

    def test_attr(self):
        self.assertEqual(self.root._attr.Num, "123")

    def test_text(self):
        root = odom.ODOM().parse('<root><child>A Text Node</child></root>')
        self.assertEqual(root.child._text, "A Text Node")

    def test_inner_text(self):
        root = odom.ODOM().parse('<root><child>A Text Node</child></root>')
        self.assertEqual(root._text, "<child>A Text Node</child>")

    def test_dom_element(self):
        server_el = self.root._dom.getElementsByTagName("Server")[0]
        self.assertEqual(self.root.Server._dom, server_el)

    def test_dom_attribute(self):
        self.assertEqual(self.root._attr.Num, self.root._dom.getAttribute('Num'))



if __name__ == '__main__':
    unittest.main()

