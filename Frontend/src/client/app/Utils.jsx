import React from "react"
import axios from 'axios'

var utils = {
  getDropdownData: function(){
    var data = {};
    axios.get('/choices/terms').
    then((response) => {
        data.selectable_terms = response.data;
    })
    .catch(function (error) {
      console.log(error);
    });
    axios.get('/choices/subjects').
    then((response)=>{
      data.subjects = response.data;
    })
    .catch(function(error){
      console.log(error)
    })
    axios.get('/choices/rooms').
    then((response)=>{
      data.rooms = response.data;
    })
    .catch(function(error){
      console.log(error)
    })
    return data;
  }
}

module.exports = utils
