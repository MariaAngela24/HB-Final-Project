// Build javascript object that has question id's and results

// Create an empty js object
// $(.selector) grabs all of questions
// use js .each (takes a function) add each question id as keys and each response as value

// use Ajax post to send the data to a route
"use strict";
// Creating a string of the question id's and responses that can be used for an AJAX request
data = $("#survey").serialize()
$.post("/")
print data
//put off success function until data is posting successfully 
// $.post(route, data, success)
// https://api.jquery.com/jQuery.post/
// render thanks for submitting and then return to homepage