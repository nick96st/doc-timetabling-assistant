import React from 'react';
import {render} from 'react-dom';
import Timetable from './Timetable.jsx';
import axios from 'axios'
import {ReactSelectize, SimpleSelect, MultiSelect} from 'react-selectize';



class App extends React.Component {
  constructor(props) {
    super(props);
    this.value;
    this.state = {timetable: [  {time:12, day:"Monday", room: "308", name:"Architecture", type: "lecture"},
                                {time:13, day:"Monday", room: "308", name:"Architecture", type: "lecture"},
                                {time:16, day:"Tuesday", room: "311", name:"Hardware", type: "lecture"},
                                {time:17, day:"Tuesday", room: "311", name:"Hardware", type: "lecture"},
                                {time:12, day:"Wednesday", room: "308", name:"Databases I", type: "lecture"},],
                              roomsFilter: [], coursesFilter: []};
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

  getRooms(){
    var rooms = []
    this.state.timetable.forEach(d => {if(rooms.indexOf(d.room) === -1) {
                      rooms.push(d.room);
                      console.log(rooms);
                      }});
    return rooms
  }

  getCourses(){
    var courses = []
    this.state.timetable.forEach(d => {if(courses.indexOf(d.name) === -1) {
                      courses.push(d.name);
                      console.log(courses);
                      }});
    return courses
  }
  //generate table with appropriate filters
  filterTable(data, allRooms, allCourses){
    var rooms = []
    var courses = []
    if(this.state.roomsFilter.length == 0) {
      rooms = allRooms
    }
    if(this.state.coursesFilter.length == 0) {
      courses = allCourses
    }
    this.state.roomsFilter.forEach(r => {rooms.push(r.value)})
    this.state.coursesFilter.forEach(c => {courses.push(c.value)})
    var monday = {day: "Monday" }
    var tuesday = {day: "Tuesday"}
    var wednesday = {day: "Wednesday"}
    var thursday = {day: "Thursday"}
    var friday = {day: "Friday"}
    data.forEach(d => {if(rooms.indexOf(d.room) !== -1 && courses.indexOf(d.name) !== -1){
                         if(d.day === "Monday"){monday[d.time] = d.name + " " + d.room}
                         if(d.day === "Tuesday"){tuesday[d.time] = d.name + " " + d.room}
                         if(d.day === "Wednesday"){wednesday[d.time] = d.name + " " + d.room}
                         if(d.day === "Thursday"){thursday[d.time] = d.name + " " + d.room}
                         if(d.day === "Friday"){friday[d.time] = d.name + " " + d.room}
                       }
                       });
    var rows = [monday, tuesday, wednesday, thursday, friday]
    console.log(tuesday)
    return rows
  }


  render () {
    var rows
    var timetable
    var allRooms = this.getRooms()
    var allCourses = this.getCourses()
    rows = this.filterTable(this.state.timetable, allRooms, allCourses)
    timetable = <Timetable rows={rows}/>
    var saveBtn = <button onClick={ () => {this.saveTimetable(this.state.timetable)}}>Save</button>
    var checkBtn = <button onClick={ () => {this.checkTimetable(this.state.timetable)}}>Check</button>
    var generateBtn = <button onClick={ () => {this.generateTimetable()}}>Generate</button>

    var dropDownRooms = <MultiSelect
                    placeholder = "Select room(s)"
                    theme = "material"
                    options = {allRooms.map(
                      room => ({label: room, value: room})
                    )}
                    onValuesChange = {value => {
                                                // console.log("timetable CHANGEEEE" + value)
                                                // console.log(value)
                                                // console.log("BEFORE " + this.statevalue)
                                                this.setState({roomsFilter : value})
                                                // this.forceUpdate();
                                                // console.log("AFTER " + this.state.value)
                                                // var newRows = this.filterTable(this.state.timetable, value)
                                                // var filteredTimetable = <Timetable rows={newRows}/>
                                                // console.log(filteredTimetable)
                                                // this.setState({timetable: newRows})
                                                // this.setState({rows: newRows})
                                                // console.log(newRows)

                                                }}
                   />
    var dropDownCourses = <MultiSelect
                          placeholder = "Select Course(s)"
                          theme = "material"
                          options = {allCourses.map(
                            course => ({label: course, value: course})
                          )}
                          onValuesChange = {value =>{this.setState({coursesFilter: value})}}
                          />
    return( <div>
              <div className ='rows'>
                <div>{dropDownRooms}</div>
                <div style={{padding : 5 + 'px'}}></div>
                <div>{dropDownCourses}</div>
              </div>
            {timetable}
            {saveBtn}
            {checkBtn}
            {generateBtn}
           </div>)
  }




}


render(<App/>, document.getElementById('app'));
