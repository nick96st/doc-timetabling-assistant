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
                              value: null};
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

  getRooms(data){
    var rooms = []
    data.forEach(d => {if(rooms.indexOf(d.room) === -1) {
                      rooms.push(d.room);
                      console.log(rooms);
                      }});
    return rooms
  }

  filterTable(data, rooms){
    var rs = []
    rooms.forEach(r => {rs.push(r.value)})
    var monday = {day: "Monday" }
    var tuesday = {day: "Tuesday"}
    var wednesday = {day: "Wednesday"}
    var thursday = {day: "Thursday"}
    var friday = {day: "Friday"}
    console.log("rs is " + rs);
    data.forEach(d => {if(rs.indexOf(d.room) !== -1){
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
    console.log("GETHERE ??????1st")
    if(this.state.value == null) {
      rows = this.generateRows(this.state.timetable)
      timetable = <Timetable rows={rows}/>
    } else {
      rows = this.filterTable(this.state.timetable, this.state.value)
      timetable = <Timetable rows={rows}/>
      console.log("GETHERE ??????")
    }

    var saveBtn = <button onClick={ () => {this.saveTimetable(this.state.timetable)}}>Save</button>
    var checkBtn = <button onClick={ () => {this.checkTimetable(this.state.timetable)}}>Check</button>
    var generateBtn = <button onClick={ () => {this.generateTimetable()}}>Generate</button>
    var refreshBtn = <button onClick={ () => {}}>Refresh</button>
    var rooms = this.getRooms(this.state.timetable)
    // var dropDown = <MultiSelect placeholder="Select a fruit"
    //                             options = {rooms.map(
    //                               room => ({label: room, value: room})
    //                             )}
    //                             onValueChange = {value => alert(value)}
    //                />

    var dropDown = <MultiSelect
                    placeholder = "Select room(s)"
                    theme = "material"
                    options = {rooms.map(
                      room => ({label: room, value: room})
                    )}
                    onValuesChange = {value => {console.log("timetable CHANGEEEE" + value)
                                                console.log(value)
                                                console.log("BEFORE " + this.statevalue)
                                                this.setState({value : value})
                                                // this.forceUpdate();
                                                console.log("AFTER " + this.state.value)
                                                // var newRows = this.filterTable(this.state.timetable, value)
                                                // var filteredTimetable = <Timetable rows={newRows}/>
                                                // console.log(filteredTimetable)
                                                // this.setState({timetable: newRows})
                                                // this.setState({rows: newRows})
                                                // console.log(newRows)

                                                }}
                   />
    return( <div>
            {dropDown}
            {timetable}
            {saveBtn}
            {checkBtn}
            {generateBtn}
            {refreshBtn}
           </div>)
  }




}


render(<App/>, document.getElementById('app'));
