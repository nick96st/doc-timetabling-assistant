import React from 'react'
import {render} from 'react-dom';
import axios from 'axios'
import FontAwesome from 'react-fontawesome';

  class Login extends React.Component{
    constructor(props){
      super(props)
      this.state={username:'', password:'', error: false}
      this.updateUsernameValue=this.updateUsernameValue.bind(this)
      this.updatePasswordValue=this.updatePasswordValue.bind(this)
      this.checkError=this.checkError.bind(this)
      this.loginUser=this.loginUser.bind(this)
    }

    updateUsernameValue(evt){
      this.setState({username: evt.target.value})
      console.log("user:", this.state.username)
    }

    updatePasswordValue(evt){
      this.setState({password: evt.target.value})
      console.log("pass:", this.state.password)
    }

    checkError(){
      return(this.state.error)? "login-input-error" : "login-input"
    }

    loginUser(){
      axios.post('/timetable/login', {
      username: this.state.username,
      password: this.state.password
    })
    .then(function (response) {
      if(response.data.success){
        localStorage.setItem("username", this.state.username)
        this.props.login()
      }else{
        this.setState("error": true)
      }
    })
    .catch(function (error) {
      console.log(error);
    });
    }

    render(){
      return(
        <div>
        <h1 id="top-item">Timetabling Assistant<FontAwesome name="pencil"></FontAwesome></h1>
        <h2>DEPARTMENT OF COMPUTING</h2>
        <div className="login-div">
          <input className={this.checkError()} type='text' value={this.state.username} onChange={this.updateUsernameValue}/>
          <br/>
          <input className={this.checkError()} type='password' value={this.state.password} onChange={this.updatePasswordValue}/>
          <br/>
          <button className = "login-button" onClick = {this.props.login}>Log In </button>
        </div>
        </div>
      )
    }
  }


export default Login;
