import React from 'react';
import {render} from 'react-dom';
import Timetable from './Timetable.jsx';




class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {timetable: [{time: 11, day: "Monday", room: "311", name: "Advanced Databases", type: "lecture"}, {time: 12, day: "Monday", room: "311", name: "Advanced Databases", type: "lecture"},
                              {time: 9, day: "Monday", room: "311", name: "Operations Research", type: "lecture"}, {time: 10, day: "Monday", room: "311", name: "Operations Research", type: "lecture"},
                              {time: 16, day: "Monday", room: "311", name: "Information and Coding"},{time: 17, day: "Monday", room: "311", name: "Information and Coding"},
                              {time: 9, day: "Tuesday", room: "311", name: "Robotics", type: "lecture"},{time: 10, day: "Tuesday", room: "311", name: "Robotics", type: "lecture"},
                              {time: 11, day: "Tuesday", room: "311", name: "Simulation and Modelling", type: "lecture"}, {time: 12, day: "Tuesday", room: "311", name: "Simulation and Modelling", type: "lecture"},
                              {time: 14, day: "Tuesday", room: "311", name: "Type Systems", type: "lecture"}, {time: 15, day: "Tuesday", room: "311", name: "Type Systems", type: "lecture"},
                              {time: 16, day: "Tuesday", room: "311", name: "Computer Vision", type: "lecture"}, {time: 17, day: "Tuesday", room: "311", name: "Computer Vision", type: "lecture"},
                              {time: 9, day: "Thursday", room: "311", name: "Information and Coding", type: "lecture"}, {time: 10, day: "Thursday", room: "311", name: "Information and Coding", type: "lecture"},
                              {time: 11, day: "Thursday", room: "311", name: "Robotics", type: "lecture"}, {time: 12, day: "Thursday", room: "311", name: "Robotics", type: "lecture"},
                              {time: 14, day: "Thursday", room: "311", name: "Operations Research"}, {time: 15, day: "Thursday", room: "311", name: "Operations Research"},
                              {time: 9, day: "Friday", room: "311", name: "Computer Vision", type: "lecture"}, {time: 10, day: "Friday", room: "311", name: "Computer Vison", type: "lecture"},
                              {time: 11, day: "Friday", room: "311", name: "Simulation and Modelling"}, {time: 12, day: "Friday", room: "311", name: "Simulation and Modelling"},
                              {time: 14, day: "Friday", room: "311", name: "Type Systems", type: "lecture"}, {time: 15, day: "Friday", room: "311", name: "Type Systems", type: "lecture"},
                              {time: 16, day: "Friday", room: "311", name: "Advanced Databases", type: "lecture"}, , {time: 17, day: "Friday", room: "311", name: "Advanced Databases", type: "lecture"}]};
  }

  saveTimetable(timetable){
    $.ajax({
      url:"/timetable/save",
      dataType: "json",
      data:timetable,
      success: function(data){
        //TODO: notify user alert
      }
    })
  }

  generateRows(data){
    var monday = {day: "Monday"}
    var tuesday = {day: "Tuesday"}
    var wednesday = {day: "Wednesday"}
    var thursday = {day: "Thursday"}
    var friday = {day: "Friday"}
    data.forEach(d => {if(d.day === "Monday"){ monday[d.time] = d.name}
                       if(d.day === "Tuesday"){tuesday[d.time] = d.name}
                       if(d.day === "Wednesday"){wednesday[d.time] = d.name}
                       if(d.day === "Thursday"){thursday[d.time] = d.name}
                       if(d.day === "Friday"){friday[d.time] = d.name}});
    var rows = [monday, tuesday, wednesday, thursday, friday]
    return rows
  }

  render () {
    var rows = this.generateRows(this.state.timetable)
    var timetable = <Timetable rows={rows}/>
    var saveBtn = <button onclick={this.saveTimetable(this.state.timetable)}>Save</button>
    return( <div>
            {timetable}
            {saveBtn}
           </div>)
  }




}


render(<App/>, document.getElementById('app'));
