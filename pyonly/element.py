from pyonly import style


# This class includes all methods/(properties) related to an HTML element.
class HTML_Element:
    def __init__(self, window, element, deleteReference_command=None):
        self.window = window                                                            # The Window object is required to communicate with JavaScript.
        self.element = element                                                          # This property contains the JavaScript code to access the HTML element.
        self.deleteReference_command = deleteReference_command                          # This property is needed in case an HTML element is created. 
                                                                                        # It contains the JavaScript code to delete the respective property 
                                                                                        # of the Python.Created_Elements_references object so that the 
                                                                                        # HTML element can no longer be accessed.
        
        self.style = style.StyleObject(self.window, self.element, self.specialchars)    # This object simulates the HTML DOM Style Object
    
    # The following __getattr__ and __setattr__ dunder/magic methods cover every property of the HTML Element.
    async def __getattr__(self, name):
        return await self.window.get(self.element + "."+ name +";")
    
    def __setattr__(self, name, value):
        if name == "window" or name == "element" or name == "deleteReference_command" or name == "style":   # These attributes should be added to the HTML_Element object as properties:
            self.__dict__[name] = value
        else:                                                                                               # Otherwise, a value is assigned to the property of an HTML element using JavaScript code:
            self.window.execute(self.element + '.' + name + ' = "' + self.specialchars(value) + '";')

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

