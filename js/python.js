// Copyright (c) The PyOnly Authors. All rights reserved.
// Licensed under the Apache License, Version 2.0. See the LICENSE file on https://github.com/pyonly/pyonly/blob/master/LICENSE or in the project root for license information.

var Python = {
    schema: document.location.protocol === "https:" ? "wss" : "ws",
    port: document.location.port ? (":" + document.location.port) : "",
    url: this.schema + "://" + document.location.hostname + this.port + "/ws",
    websocket: null,
    

    init: function(__hostname, __port, __path){                                     // This method creates a WebSocket connection based on the passed arguments.
        Python.websocket = new WebSocket(Python.schema + "://" + __hostname + ":" + __port + "/" + __path);
        Python.setEvents();
    },
    auto_init: function(){                                                          // This method creates a WebSocket connection based on the hosted URL and port.
        Python.websocket = new WebSocket(Python.schema + "://" + document.location.hostname + Python.port + "/ws");
        Python.setEvents();
    },
    
    setEvents: function(){                                                          // This method combines the onmessage and onclose events with a method of the Python object. 
        Python.websocket.onmessage = Python.onMessage;
        Python.websocket.onclose = Python.onClose;                                      // The function called for the onclose event can be changed to inform the user, for example.
    },
    send: function(__s){                                                            // This method exists to send a string to Python.
        Python.websocket.send(__s);
    },
    call: function(){                                                               // This method invokes a Python function. 
        if(arguments.length >= 1){                                                      // The length of the passed arguments must be greater than one because the first argument specifies the name of the Python function to be called.
            var __args = new Array();                                                   // The rest of the arguments are added to the __args array.
            for (var __i = 1; __i < arguments.length; __i++) {
                __args.push(arguments[__i]);
            }
            var __object__arguments = {                                                 // A JavaScript object is created.
                target: "callfunc",                                                     // It contains the name of the Python function to be called (property "func_name") and the arguments to be passed.
                func_name: arguments[0],
                args: __args                                                            // Furthermore, the property "target" with the value "callfunc" is required to transmit Python what to do (calling a function).
            };
            Python.send(JSON.stringify(__object__arguments));                           // Finally, the object is converted into a JSON string to send it to JavaScript.
        }
    },
    call_async: function(){                                                         // This method invokes a Python function but compared to the call method a Promise is returned to enable a return value to be received.
        if(arguments.length >= 1){
            var __args = new Array();
            for (var __i = 1; __i < arguments.length; __i++) {
                __args.push(arguments[__i]);
            }
            var __object__arguments = {
                target: "callfunc_async",
                func_name: arguments[0],
                args: __args
            };
            Python.send(JSON.stringify(__object__arguments));
        }
        return new Promise(function(resolve, reject) {
            Python.onCallBack = function(__e){
                resolve(__e);
            };
        });
    },
    onClose: function(){                                                            // This function is executed when the WebSocket connection is closed. This function called for the onclose event can be changed (Python.websocket.onclose = function_name;).
        alert("Connection closed!");
    },
    onCallBack: function(){
        alert("ERROR CALLBACK");
    },
    onMessage: function(__e){                                                       // This method is executed when the WebSocket receives a message (JSON string).
        args_obj = JSON.parse(__e.data);                                                // Subsequently, the JSON string is converted into a JavaScript object.
        if(args_obj.task == "execute"){                                                 // The property task defines the purpose/what to do.
            eval(args_obj.code);                                                        // If the task property equals "execute", the code property is executed.
            
        }else if(args_obj.task == "get"){                                               // In case the task property equals "get", the code property is executed and the return value is received.
            var __retVal = eval(args_obj.code);                                         // Subsequently, a JavaScript object is created with the property "target" containing the value "get" to tell Python what to do with the sent data.
            var __object__arguments = {                                                 // Additionally, the args property has got the return value. Finally, the JavaScript object is converted into a JSON string to send it.
                target: "get",
                args: __retVal
            };
            Python.send(JSON.stringify(__object__arguments));
        }else if(args_obj.task == "callback"){                                          // If the task property equals "callbackcallback", the oncallBack method is invoked and the code property is passed to it to resolve the Promise with the return value of an executed Python function.
            Python.onCallBack(args_obj.code);
        }else if(args_obj.task == "call"){                                              // In case the task property is "call", the JavaScript function with the name of the func_name property of the args_obj object is invoked as a method of the window object together with the parameters of the args_obj.args property.
            var __retVal = window[args_obj.func_name].apply(null, args_obj.args);       // The return value is sent back to Python.
            if(__retVal == undefined){
                __retVal = "undefinded";
            }
            var __object__arguments = {
                target: "get",
                args: __retVal
            };
            Python.send(JSON.stringify(__object__arguments));
        }
    },
    
                                                                                    // This property is an object that manages the HTML elements created by Python.
                                                                                    // The created element is added to the Python.Created_Elements_references object as a new property.
                                                                                    // If the HTML element no longer needs to be accessed, the respective property of the Python.Created_Elements_references object should be deleted.
    Created_Elements_references: {

    }
};


