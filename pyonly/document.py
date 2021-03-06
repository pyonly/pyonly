from pyonly import element
from pyonly import collection

# This Document class simulates the HTML DOM document object.
class Document:
    def __init__(self, window):
        self.window = window
        self.created_elements_index = 0             # This property is required to ensure that every created HTML element can be accessed using a unique reference.
    
    def getElementById(self, id):                   # This method simulates the document.getElementById() JavaScript method 
                                                    # that returns the element that has the ID attribute with the specified value.
                                                    # Furthermore an HTML_Element object is created including all methods/(properties) related to an HTML element.
        return element.HTML_Element(self.window, "document.getElementById('" + id + "')")
    
    async def getElementsByClassName(self, name):   # This method is similar to the document.getElementsByClassName() JavaScript method that returns a HTMLCollection object.
                                                    # Additionally, the update method of the HTMLCollection object must be executed
                                                    # so that the number of the contained HTML elements can be assigned to the len property.
        htmlCollection = collection.HTMLCollection(self.window, "document.getElementsByClassName('" + name + "')")
        await htmlCollection.update()
        return htmlCollection
    
    async def getElementsByTagName(self, name):     # This method is similar to the document.getElementsByTagName() JavaScript method.
        htmlCollection = collection.HTMLCollection(self.window, "document.getElementsByTagName('" + name + "')")
        await htmlCollection.update()
        return htmlCollection
    
    async def getElementsByTagNameNS(self, name):   # This method simulates the document.getElementsByTagNameNS() JavaScript method.
        htmlCollection = collection.HTMLCollection(self.window, "document.getElementsByTagNameNS('" + name + "')")
        await htmlCollection.update()
        return htmlCollection
    
    async def getElementsByName(self, name):        # This method simulates the document.getElementsByName() JavaScript method.
        htmlCollection = collection.HTMLCollection(self.window, "document.getElementsByName('" + name + "')")
        await htmlCollection.update()
        return htmlCollection
    
    def createElement(self, tagName):               # This method is similar to the document.createElement() JavaScript method
                                                    # that creates an Element Node with the specified name.
                                                    # A created HTML_Element object including all methods/(properties) related to an HTML element is returned.
                                                    # To create an element that can be referenced,
                                                    # the element is added to the Python.Created_Elements_references object as a new property.
                                                    # If the HTML element no longer needs to be accessed, the respective property of the Python.Created_Elements_references object should be deleted.
                                                    # Therefore, the deleteReference_command parameter of the __init__ function is given the JavaScript code to be executed
                                                    # when creating an HTML_Element object to delete the respective property of the Python.Created_Elements_references object.
        self.created_elements_index += 1
        self.window.execute('Python.Created_Elements_references.e' + str(self.created_elements_index) + ' = document.createElement("' + self.specialchars(tagName) + '");')
        return element.HTML_Element(self.window, 'Python.Created_Elements_references.e' + str(self.created_elements_index), 'delete Python.Created_Elements_references.e' + str(self.created_elements_index))
    
    def specialchars(self, s):
        s = s.replace("\\", "\\\\")
        return s.replace('"', '\\"')
