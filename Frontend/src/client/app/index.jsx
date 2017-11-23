import React from 'react';
import {render} from 'react-dom';
import Timetable from './Timetable.jsx';
import axios from 'axios'
import {ReactSelectize, SimpleSelect, MultiSelect} from 'react-selectize';
import Dropdown from 'react-dropdown';




class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {hours:{start: 9, finish: 17} ,timetable: [  {time:12, day:"Monday", room: "308", name:"Architecture", type: "lecture"},
                                {time:13, day:"Monday", room: "308", name:"Architecture", type: "lecture"},
                                {time:16, day:"Tuesday", room: "311", name:"Hardware", type: "lecture"},
                                {time:17, day:"Tuesday", room: "311", name:"Hardware", type: "lecture"},
                                {time:12, day:"Wednesday", room: "308", name:"Databases I", type: "lecture"},], modalOpen:false,
                  subjects:["Architecture", "Hardware", "Databases I"], rooms:["308", "311"] ,roomsFilter: [], coursesFilter: []};
    this.openModal=this.openModal.bind(this)
    this.closeModal=this.closeModal.bind(this)
    this.addLecture=this.addLecture.bind(this)
    this.removeLecture=this.removeLecture.bind(this)

    // fetch terms he can select
    this.getTerms();
    //fetch subjects he can select
    this.getSubjects();
    //fetch rooms he can select
    this.fetchRooms();
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

  checkTimetable(state) {
    axios.post('/timetable/check', {
    timetable: state.timetable,
    term: state.selected_term
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
        this.fillTable(response.data.solutions);
        }
    })
    .catch(function (error) {
      console.log(error);
    });

  }

  fillTable(data) {
    console.log("data in filltable",data);
    console.log("state in filltable",this.state);
    this.setState({timetable:data[0]});
    console.log(this.state);
  }

  // fill state.selectable_terms with the terms defined on backend
  getTerms() {
    axios.get('/choices/terms').
    then((response) => {
        this.setState({selectable_terms: response.data});
    })
    .catch(function (error) {
      console.log(error);
    });
  }

  getSubjects(){
    axios.get('/choices/subjects').
    then((response)=>{
      this.setState({subjects: response.data})
    })
    .catch(function(error){
      console.log(error)
    })
  }

  fetchRooms(){
    axios.get('/choices/rooms').
    then((response)=>{
      this.setState({rooms: response.data})
    })
    .catch(function(error){
      console.log(error)
    })
  }

  onSelectedTermChange(e) {
    console.log(e.value," ",this);
    this.setState({selected_term:e.value});
    console.log("selector changed state to ",this.state);
  }

  addLecture(lect){
   var timetable = this.state.timetable
   timetable.push(lect)
   console.log(timetable)
  }

  removeLecture(lect){

    var timetable = this.state.timetable
    console.log(timetable)
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

  emptyFilter(){
    this.setState({roomsFilter:[]})
  }

  //generate table with appropriate filters
  filterTable(data, allRooms, allCourses){
    var rooms = [];
    var courses = [];
    if(this.state.roomsFilter.length == 0) {
      rooms = allRooms;
    }
    if(this.state.coursesFilter.length == 0) {
      courses = allCourses;
    }
    this.state.roomsFilter.forEach(r => {rooms.push(r.value)});
    this.state.coursesFilter.forEach(c => {courses.push(c.value)});
    var timetable = this.state.timetable;
    var filteredTimetable = [];
    timetable.forEach(lect => {
      if (rooms.indexOf(lect.room) != -1 && courses.indexOf(lect.name) != -1){
        filteredTimetable.push(lect);
      }
    })
    return filteredTimetable
}

  render () {
    var timetable
    var allRooms = this.getRooms()
    var allCourses = this.getCourses()
    var ftable = this.filterTable(this.state.timetable, allRooms, allCourses)
    var rows = this.generateRows(ftable)
    timetable = <Timetable rows={rows} hours={this.state.hours} addLecture={this.addLecture}
                 removeLecture={this.removeLecture} openModal={this.openModal} closeModal={this.closeModal}
                 modalOpen={this.state.modalOpen} rooms={this.state.rooms} subjects={this.state.subjects}/>
    var saveBtn = <button onClick={ () => {this.saveTimetable(this.state.timetable)}}>Save</button>
    var checkBtn = <button onClick={ () => {this.checkTimetable(this.state)}}>Check</button>
    var generateBtn = <button onClick={ () => {this.generateTimetable(this.state.selected_term)}}>Generate</button>

    var emptyFilterBtn = <button onClick={() => {this.emptyFilter()}}>Empty Filter</button>

    var dropDownRooms = <MultiSelect
                    placeholder = "Select room(s)"
                    theme = "material"
                    options = {allRooms.map(
                      room => ({label: room, value: room})
                    )}
                    onValuesChange = {value => {this.setState({roomsFilter : value})}}
                   />
    var dropDownCourses = <MultiSelect
                          placeholder = "Select Course(s)"
                          theme = "material"
                          options = {allCourses.map(
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
            {selectTermDropdown}
            {timetable}
            {saveBtn}
            {checkBtn}
            {generateBtn}
            {emptyFilterBtn}

           </div>)
  }

}

render(<App/>, document.getElementById('app'));
