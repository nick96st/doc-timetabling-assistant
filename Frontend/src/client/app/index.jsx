import React from 'react';
import {render} from 'react-dom';
import FontAwesome from 'react-fontawesome';
import TimetableContainer from './TimetableContainer.jsx'
import Login from './Login.jsx'

class App extends React.Component {
  constructor(props){
    super(props)
    this.state={username: ''}
    // localStorage.setItem('user', 'Duncan')
    localStorage.clear()
    this.login = this.login.bind(this)
  }

login(user){
  this.setState({username: user})
}

render(){

if(localStorage.getItem("user")){
  return(
    <TimetableContainer/>
  )
}
else{
  return(
    <Login/>
  )
}
}
}

render(<App/>, document.getElementById('app'));
