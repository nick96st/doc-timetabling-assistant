import React from 'react';
import {render} from 'react-dom';
import Timetable from './Timetable.jsx';
import axios from 'axios'
import {ReactSelectize, SimpleSelect, MultiSelect} from 'react-selectize';
import Dropdown from 'react-dropdown';
import {getDropdownData} from './Utils.jsx'




class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {hours:{start: 9, finish: 17} ,timetable: [  {time:12, day:"Monday", room: "308", name:"Architecture", type: "lecture"},
                                {time:13, day:"Monday", room: "308", name:"Architecture", type: "lecture"},
                                {time:16, day:"Tuesday", room: "311", name:"Hardware", type: "lecture"},
                                {time:17, day:"Tuesday", room: "311", name:"Databases I", type: "lecture"},
                                {time:12, day:"Wednesday", room: "308", name:"Databases I", type: "lecture"},], modalOpen:false,
                  subjects:["Databases I", "Hardware", "Architecture"], rooms:["308", "311"] ,roomsFilter: [], coursesFilter: []};
    this.openModal=this.openModal.bind(this)
    this.closeModal=this.closeModal.bind(this)
    this.addLecture=this.addLecture.bind(this)
    this.removeLecture=this.removeLecture.bind(this)
    this.getInitialData();
  }

  getInitialData(){
  var dropdownData = getDropdownData()
  this.setState({terms: dropdownData.terms, rooms: dropdownData.rooms, subjects: dropdownData.subjects})
  }

  openModal(){
    var hours = this.state.hours
    var timetable = this.state.timetable
    this.setState({modalOpen: true})
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

  generateTimetable(selected_term) {
    axios.get('/timetable/generate', {
        params: {
            term: selected_term
        }
    })
    .then((response) => {
        if (response.data.status != "SATISFIABLE" &&
            response.data.status != "OPTIMAL") {
            console.log("ERROR");
        }
        else {
        var timetables = response.data.solutions
        this.setState({timetable: timetables[0]});
        }
    })
    .catch(function (error) {
      console.log(error);
    });

  }

  onSelectedTermChange(e) {
    this.setState({selected_term:e.value});
  }

  addLecture(lect){
   var timetable = this.state.timetable
   timetable.push(lect)
  }

  removeLecture(lect){
    var timetable = this.state.timetable
    var i = timetable.indexOf(lect);
    if (i> -1){
      timetable.splice(i, 1)
    }
    this.setState({timetable:timetable})
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


  //generate table with appropriate filters
  filterTable(data){
    var rooms = [];
    var courses = [];
    if(this.state.roomsFilter.length == 0) {
      rooms = this.state.rooms;
    }
    if(this.state.coursesFilter.length == 0) {
      courses = this.state.subjects;
    }
    this.state.roomsFilter.forEach(r => {rooms.push(r.value)});
    this.state.coursesFilter.forEach(c => {courses.push(c.value)});
    var timetable = data;
    var filteredTimetable = [];

    timetable.forEach(lect => {
      if (rooms.indexOf(lect.room) != -1 && courses.indexOf(lect.name) != -1){
        filteredTimetable.push(lect);
      }
    })
    console.log(filteredTimetable)
    return filteredTimetable
}

  render () {
    var timetable
    var ftable = this.filterTable(this.state.timetable)
    var rows = this.generateRows(ftable)
    timetable = <Timetable rows={rows} hours={this.state.hours} addLecture={this.addLecture}
                 removeLecture={this.removeLecture} openModal={this.openModal} closeModal={this.closeModal}
                 modalOpen={this.state.modalOpen}/>
    var saveBtn = <button onClick={ () => {this.saveTimetable(this.state.timetable)}}>Save</button>
    var checkBtn = <button onClick={ () => {this.checkTimetable(this.state.timetable)}}>Check</button>
    var generateBtn = <button onClick={ () => {this.generateTimetable()}}>Generate</button>

    var dropDownRooms = <MultiSelect
                    placeholder = "Select room(s)"
                    theme = "material"
                    options = {this.state.rooms.map(
                      room => ({label: room, value: room})
                    )}
                    onValuesChange = {value => {this.setState({roomsFilter : value})}}
                   />
    var dropDownCourses = <MultiSelect
                          placeholder = "Select Course(s)"
                          theme = "material"
                          options = {this.state.subjects.map(
                            course => ({label: course, value: course})
                          )}
                          onValuesChange = {value =>{this.setState({coursesFilter: value})}}
                          />
    var selectTermDropdown =  <Dropdown
                              options={this.state.selectable_terms}
                              placeholder="Select term"
                              onChange={(e) => {this.onSelectedTermChange(e);} }
                              value={this.state.selected_term}
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
            {selectTermDropdown}
           </div>)
  }

}

render(<App/>, document.getElementById('app'));
