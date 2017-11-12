import React from 'react';
import {render} from 'react-dom';
import Timetable from './Timetable.jsx';
import axios from 'axios'




class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {hours:{start: 9, finish: 17} ,timetable: [  {time:12, day:"Monday", room: "308", name:"Architecture", type: "lecture"},
                                {time:13, day:"Monday", room: "308", name:"Architecture", type: "lecture"},
                                {time:16, day:"Tuesday", room: "311", name:"Hardware", type: "lecture"},
                                {time:17, day:"Tuesday", room: "311", name:"Hardware", type: "lecture"},
                                {time:12, day:"Wednesday", room: "308", name:"Databases I", type: "lecture"},], modalOpen:false};
    this.openModal=this.openModal.bind(this)
    this.closeModal=this.closeModal.bind(this)
  }

  openModal(){
    var hours = this.state.hours
    var timetable = this.state.timetable
    this.setState({modalOpen: true})
    console.log(this.state)
  }

  closeModal(){
    this.setState({modalOpen:false})
  }

  saveTimetable(timetable){
    axios.post('/timetable/save', {
    timetable: timetable
  })
  .then(function (response) {
    console.log(response);
  })
  .catch(function (error) {
    console.log(error);
  });
  }

  checkTimetable(timetable) {
    axios.post('/timetable/check', {
    timetable: timetable
  })
  .then(function (response) {
    console.log(response);
  })
  .catch(function (error) {
    console.log(error);
  });

  }

  generateTimetable() {
    axios.get('/timetable/generate')
    .then((response) => {
        this.fillTable(response);
    })
    .catch(function (error) {
      console.log(error);
    });

  }

  fillTable(data) {
    console.log("data in filltable",data);
    console.log("state in filltable",this.state);
    this.setState({timetable:data.data[0]});
    console.log(this.state);
  }

  generateRows(data){
    var monday = {day: "Monday", 9:[], 10:[], 11:[], 12:[], 13:[], 14:[], 15:[], 16:[], 17:[]}
    var tuesday = {day: "Tuesday", 9:[], 10:[], 11:[], 12:[], 13:[], 14:[], 15:[], 16:[], 17:[]}
    var wednesday = {day: "Wednesday", 9:[], 10:[], 11:[], 12:[], 13:[], 14:[], 15:[], 16:[], 17:[]}
    var thursday = {day: "Thursday", 9:[], 10:[], 11:[], 12:[], 13:[], 14:[], 15:[], 16:[], 17:[]}
    var friday = {day: "Friday", 9:[], 10:[], 11:[], 12:[], 13:[], 14:[], 15:[], 16:[], 17:[]}

    data.forEach(d => {if(d.day === "Monday"){ monday[d.time].push(d)}
                       if(d.day === "Tuesday"){tuesday[d.time].push(d)}
                       if(d.day === "Wednesday"){wednesday[d.time].push(d)}
                       if(d.day === "Thursday"){thursday[d.time].push(d)}
                       if(d.day === "Friday"){friday[d.time].push(d)}});
    var rows = [monday, tuesday, wednesday, thursday, friday]
    return rows
  }

  render () {
    var rows = this.generateRows(this.state.timetable)
    var timetable = <Timetable rows={rows} hours={this.state.hours} modalOpen={this.state.modalOpen} openModal={this.openModal} closeModal={this.closeModal}/>
    var saveBtn = <button onClick={ () => {this.saveTimetable(this.state.timetable)}}>Save</button>
    var checkBtn = <button onClick={ () => {this.checkTimetable(this.state.timetable)}}>Check</button>
    var generateBtn = <button onClick={ () => {this.openModal()}}>Generate</button>
    return( <div>
            {timetable}
            {saveBtn}
            {checkBtn}
            {generateBtn}
           </div>)
  }




}


render(<App/>, document.getElementById('app'));
