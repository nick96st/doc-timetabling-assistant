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

var styles = {
  cstyle : {
    overlay : {
      position          : 'fixed',
      top               : 0,
      left              : 0,
      right             : 0,
      bottom            : 0,
      backgroundColor   : 'rgba(255, 255, 255, 0.75)'
    },
    content : {
      position                   : 'relative',
      top                        : '40px',
      left                       : '50%',
      right                      : '0px',
      bottom                     : '40px',
      border                     : '1px solid #ccc',
      background                 : '#fff',
      overflow                   : 'auto',
      WebkitOverflowScrolling    : 'touch',
      borderRadius               : '4px',
      outline                    : 'none',
      padding                    : '20px',
      width                      : '400px',
      height                     : '400px',
      transform: 'translate(-50%, 0)'
   }

},
sstyle : {
  overlay : {
    position          : 'fixed',
    top               : 0,
    left              : 0,
    right             : 0,
    bottom            : 0,
    backgroundColor   : 'rgba(255, 255, 255, 0.75)'
  },
  content : {
    position                   : 'relative',
    top                        : '40px',
    left                       : '50%',
    right                      : '0px',
    bottom                     : '40px',
    border                     : '1px solid #ccc',
    background                 : '#fff',
    overflow                   : 'auto',
    WebkitOverflowScrolling    : 'touch',
    borderRadius               : '4px',
    outline                    : 'none',
    padding                    : '20px',
    width                      : '400px',
    height                     : '200px',
    transform: 'translate(-50%, 0)'
 }
}
}

export {utils}
export {styles}
