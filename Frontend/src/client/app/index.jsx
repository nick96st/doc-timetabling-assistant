import React from 'react';
import {render} from 'react-dom';
import Timetable from './Timetable.jsx';
import axios from 'axios'




class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {timetable: [  {time:12, day:"Monday", room: "308", name:"Architecture", type: "lecture"},
                                {time:13, day:"Monday", room: "308", name:"Architecture", type: "lecture"},
                                {time:16, day:"Tuesday", room: "311", name:"Hardware", type: "lecture"},
                                {time:17, day:"Tuesday", room: "311", name:"Hardware", type: "lecture"},
                                {time:12, day:"Wednesday", room: "308", name:"Databases I", type: "lecture"},]};
                              //{time: 11, day: "Monday", room: "311", name: "Advanced Databases", type: "lecture"},
                              //{time: 12, day: "Monday", room: "311", name: "Advanced Databases", type: "lecture"},
                             // {time: 9, day: "Monday", room: "311", name: "Operations Research", type: "lecture"},
                             // {time: 10, day: "Monday", room: "311", name: "Operations Research", type: "lecture"},
                              //{time: 16, day: "Monday", room: "311", name: "Information and Coding"},
                              //{time: 17, day: "Monday", room: "311", name: "Information and Coding"},
                              //{time: 9, day: "Tuesday", room: "311", name: "Robotics", type: "lecture"},
                              //{time: 10, day: "Tuesday", room: "311", name: "Robotics", type: "lecture"},
                              //{time: 11, day: "Tuesday", room: "311", name: "Simulation and Modelling", type: "lecture"},
                              //{time: 12, day: "Tuesday", room: "311", name: "Simulation and Modelling", type: "lecture"},
                              //{time: 14, day: "Tuesday", room: "311", name: "Type Systems", type: "lecture"},
                              //{time: 15, day: "Tuesday", room: "311", name: "Type Systems", type: "lecture"},
                              //{time: 16, day: "Tuesday", room: "311", name: "Computer Vision", type: "lecture"},
                             // {time: 17, day: "Tuesday", room: "311", name: "Computer Vision", type: "lecture"},
                             // {time: 9, day: "Thursday", room: "311", name: "Information and Coding", type: "lecture"},
                             // {time: 10, day: "Thursday", room: "311", name: "Information and Coding", type: "lecture"},
                             // {time: 11, day: "Thursday", room: "311", name: "Robotics", type: "lecture"},
                             // {time: 12, day: "Thursday", room: "311", name: "Robotics", type: "lecture"},
                             // {time: 14, day: "Thursday", room: "311", name: "Operations Research"},
                             // {time: 15, day: "Thursday", room: "311", name: "Operations Research"},
                             // {time: 9, day: "Friday", room: "311", name: "Computer Vision", type: "lecture"},
                             // {time: 10, day: "Friday", room: "311", name: "Computer Vison", type: "lecture"},
                             // {time: 11, day: "Friday", room: "311", name: "Simulation and Modelling"},
                             // {time: 12, day: "Friday", room: "311", name: "Simulation and Modelling"},
                             // {time: 14, day: "Friday", room: "311", name: "Type Systems", type: "lecture"},
                             // {time: 15, day: "Friday", room: "311", name: "Type Systems", type: "lecture"},
                             // {time: 16, day: "Friday", room: "311", name: "Advanced Databases", type: "lecture"},
                             // {time: 17, day: "Friday", room: "311", name: "Advanced Databases", type: "lecture"}]};
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
    var monday = {day: "Monday" }
    var tuesday = {day: "Tuesday"}
    var wednesday = {day: "Wednesday"}
    var thursday = {day: "Thursday"}
    var friday = {day: "Friday"}
    data.forEach(d => {if(d.day === "Monday"){ monday[d.time] = d.name + " " + d.room}
                       if(d.day === "Tuesday"){tuesday[d.time] = d.name + " " + d.room}
                       if(d.day === "Wednesday"){wednesday[d.time] = d.name + " " + d.room}
                       if(d.day === "Thursday"){thursday[d.time] = d.name + " " + d.room}
                       if(d.day === "Friday"){friday[d.time] = d.name + " " + d.room}});
    var rows = [monday, tuesday, wednesday, thursday, friday]
    console.log(monday)
    return rows
  }

  render () {
    var rows = this.generateRows(this.state.timetable)
    var timetable = <Timetable rows={rows}/>
    var saveBtn = <button onClick={ () => {this.saveTimetable(this.state.timetable)}}>Save</button>
    var checkBtn = <button onClick={ () => {this.checkTimetable(this.state.timetable)}}>Check</button>
    var generateBtn = <button onClick={ () => {this.generateTimetable()}}>Generate</button>
    return( <div>
            {timetable}
            {saveBtn}
            {checkBtn}
            {generateBtn}
           </div>)
  }




}


render(<App/>, document.getElementById('app'));
