/*
This script saves the annotated htlm table to a csv file;
ToDo: 
- modify app.py, 
- add warning message,
- incorporate in template html  
*/ 

$.ajax({
    url: __server_py_script_name__,
    cache: false,
    contentType: "text/html; charset=UTF-8",
    data: data,
    type: "POST",
    success: success,
    error: failure
});