#!/usr/bin/python

"""
    ODOM(Object DOM)

        A simple DOM wrapper object making access to child nodes easy.

        PARSE

        Parse a string to create an ODOM object.

            ODOM().parse(xml_string)


        CHILD NODES

        You can access a child node by

            node.ChildNodeTagName

        where ChildNodeTagName is the tag name of the child node.
        Chaining is easy

            node.ChildNodeTagName.GrandsonTagName

        and it returns a list of ODOM objects if there are siblings with same 
        tag name.

            node.ChildNodeTagName.GrandsonTagName[0]


        ATTRIBUTES

        Attributes are inside _attr,

            node._attr.href
            node._attr.title

        where href and title is the name of the attribute.


        TEXT

        Since ODOM has only ElementNode and AttributeNode in DOM terms,
        you cannot access to a 'TextNode'.
        However, you can read inner text with _text,

            node._text

        This will read appropriate text data if node had TextNode as a single 
        child. Note it doesn't behave that way when having multiple child nodes.


        DOM

        DOM members are not directly accessible because it may interfere with
        the tag name of child node, but you could still access to original dom
        object with _dom.

            node._dom.getElementsByTagName('childNodeTagName')[0]


"""
VERSION = 0.1 

import xml.dom
import xml.dom.minidom as minidom

ELEMENT_NODE = xml.dom.Node.ELEMENT_NODE
TEXT_NODE    = xml.dom.Node.TEXT_NODE

class OdomNode(object):
    def __init__(self, dom):
        self._dom = dom
        self._attr = None
        self._text = None

class OdomElementNode(OdomNode):
    def __repr__(self):
        name = self._dom.tagName
        return "<ODOM Element: %s at %#x>" % (name, id(self))

class OdomAttrNode(OdomNode):
    def __repr__(self):
        name = [a.name for a in self._dom]
        return "<ODOM Attr: %s at %#x>" % (name, id(self))


class ODOM(object):
    def parse(self, xml):
        doc = minidom.parseString(xml)
        root = self.buildElementNode(doc.childNodes[0])
        return root

    def buildElementNode(self, node):
        el = OdomElementNode(node)
        inner_text = ''
        # attr
        attr = self.buildAttributeNode(node)
        setattr(el, "_attr", attr)
        for child in node.childNodes:
            if child.nodeType == ELEMENT_NODE:
                # child
                child_el = self.buildElementNode(child)
                # set
                sibling = getattr(el, child.tagName, None)
                if sibling is not None:
                    if isinstance(sibling, OdomElementNode):
                        sibling = [sibling]
                    sibling.append(child_el)
                else:
                    sibling = child_el
                setattr(el, child.tagName, sibling)
                # text
                inner_text += child.toxml()
            elif child.nodeType == TEXT_NODE:
                if len(child.nodeValue.strip()) == 0:
                    continue
                # text
                inner_text += child.data
        el._text = inner_text
        return el

    def buildAttributeNode(self, node):
        attr = OdomAttrNode(node.attributes.values())
        for k,v in node.attributes.items():
            setattr(attr, k, v)
        return attr


