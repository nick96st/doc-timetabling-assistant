import React from "react"
import axios from 'axios'

var utils = {
  getDropdownData: function(main_this){
    var data = {};
    axios.get('/choices/terms').
    then((response) => {
        main_this.setState({selectable_terms: response.data});
    })
    .catch(function (error) {
      console.log(error);
    });
    axios.get('/choices/subjects').
    then((response)=>{
      main_this.setState({subjects: response.data});
    })
    .catch(function(error){
      console.log(error)
    })
    axios.get('/choices/rooms').
    then((response)=>{
      main_this.setState({rooms: response.data});
    })
    .catch(function(error){
      console.log(error)
    })
    return data;
  }
}

module.exports = utils
