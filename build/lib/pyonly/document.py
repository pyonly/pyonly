# This Document class simulates the HTML DOM document object.
class Document:
    def __init__(self, window):
        self.window = window
        self.created_elements_index = 0             # This property is required to ensure that every created HTML element can be accessed using a unique reference.
    
    def getElementById(self, id):                   # This method simulates the document.getElementById() JavaScript method 
                                                    # that returns the element that has the ID attribute with the specified value.
                                                    # Furthermore an HTML_Element object is created including all methods/(properties) related to an HTML element.
        return HTML_Element(self.window, "document.getElementById('" + id + "')")
    
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
        return HTML_Element(self.window, 'Python.Created_Elements_references.e' + str(self.created_elements_index), 'delete Python.Created_Elements_references.e' + str(self.created_elements_index))
    
    def specialchars(self, s):
        s = s.replace("\\", "\\\\")
        return s.replace('"', '\\"')

# This class includes all methods/(properties) related to an HTML element.
class HTML_Element:
    def __init__(self, window, element, deleteReference_command=None):
        self.window = window                                                # The Window object is required to communicate with JavaScript.
        self.element = element                                              # This property contains the JavaScript code to access the HTML element.
        self.deleteReference_command = deleteReference_command              # This property is needed in case an HTML element is created. 
                                                                            # It contains the JavaScript code to delete the respective property 
                                                                            # of the Python.Created_Elements_references object so that the 
                                                                            # HTML element can no longer be accessed.
    
    # In the following way, simulated JavaScript HTML DOM attributes can be added to this class:
    # @property
    # async def attribute(self):
    #     return await self.window.get(self.element + ".attribute;")
    # @attribute.setter
    # def attribute(self, val):
    #     self.window.execute(self.element + '.attribute = "' + self.specialchars(val) + '";')
    
    # It changes/returns the value of an element.
    @property
    async def value(self):
        return await self.window.get(self.element + ".value;")
    @value.setter
    def value(self, val):
        self.window.execute(self.element + '.value = "' + self.specialchars(val) + '";')

    # It changes/returns the inner HTML of an element.
    @property
    async def innerHTML(self):
        return await self.window.get(self.element + ".innerHTML;")
    @innerHTML.setter
    def innerHTML(self, val):
        self.window.execute(self.element + '.innerHTML = "' + self.specialchars(val) + '";')

    # This method makes it easy to access the attributes of HTML elements that have not yet been simulated in this class.
    async def attribute(self, attr, val=None):
        if val == None:
            return await self.window.get(self.element + "." +  self.specialchars(attr) + ";")
        else:
            self.window.execute(self.element + '.' + attr + ' = "' + self.specialchars(val) + '";')
    
    # This method changes the attribute value of an HTML element.
    def setAttribute(self, attr, val):
        self.window.execute(self.element + '.setAttribute("' + self.specialchars(attr) + '", "' + self.specialchars(val) +  '");')
    
    # The HTML element is added to the body.
    def append_this_to_body(self):
        self.window.execute('document.body.appendChild(' + self.element + ');')
    
    # In case an HTML element has been created, JavaScript code is passed during the initialization of the HTML_Element object
    # allowing to delete the respective property of the Python.Created_Elements_references object
    # so that the HTML element can no longer be accessed.
    def deleteReference(self):
        if self.deleteReference_command != None:
            self.window.execute(self.deleteReference_command)
    
    def specialchars(self, s):
        s = s.replace("\\", "\\\\")
        return s.replace('"', '\\"')

