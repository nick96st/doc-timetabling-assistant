import React from 'react'
import {render} from 'react-dom';

  class MyCheckbox extends React.Component{
    constructor(props){
      super(props)
      this.state={isChecked:false}
      this.toggleCheckboxChange=this.toggleCheckboxChange.bind(this)
    }

    toggleCheckboxChange(){
      this.setState({isChecked: !(this.state.isChecked)})
      this.props.handleChange(this.props.label)
    }

    render(){
      return(
       <label>
        <input type="checkbox"
               value={this.props.label}
               checked={this.state.isChecked}
               onChange={this.toggleCheckboxChange}/>
        {this.props.label}
       </label>
      )
    }
  }


export default MyCheckbox;
