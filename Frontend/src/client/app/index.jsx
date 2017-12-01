import React from 'react';
import {render} from 'react-dom';
import Timetable from './Timetable.jsx';
import axios from 'axios'
import {ReactSelectize, SimpleSelect, MultiSelect} from 'react-selectize';
import Dropdown from 'react-dropdown';
import {getDropdownData} from './Utils.jsx';
import MyCheckbox from './MyCheckbox.jsx'
import FontAwesome from 'react-fontawesome';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {hours:{start: 9, finish: 17} ,timetable: [  {time:12, day:"Monday", room: "308", name:"Architecture", type: "lecture"},
                                {time:13, day:"Monday", room: "308", name:"Architecture", type: "lecture"},
                                //{time:16, day:"Tuesday", room: "311", name:"Hardware", type: "lecture"},
                               // {time:17, day:"Tuesday", room: "311", name:"Hardware", type: "lecture"},
                               // {time:17, day:"Tuesday", room: "311", name:"Databases I", type: "lecture"},
                              //  {time:12, day:"Wednesday", room: "308", name:"Databases I", type: "lecture"},
                                ], modalOpen:false,
                  subjects:["Databases I", "Hardware", "Architecture"], rooms:["308", "311"] ,roomsFilter: [], coursesFilter: [], labels:[]};
    this.openModal=this.openModal.bind(this)
    this.closeModal=this.closeModal.bind(this)
    this.addLecture=this.addLecture.bind(this)
    this.removeLecture=this.removeLecture.bind(this)
    this.handleRemovingFilter=this.handleRemovingFilter.bind(this)
    this.toggleCheckbox=this.toggleCheckbox.bind(this)
    this.getInitialData();
  }

  getInitialData(){
  var dropdownData = getDropdownData(this)
//  this.setState({terms: dropdownData.terms, rooms: dropdownData.rooms, subjects: dropdownData.subjects})

//    this.getConstraints();
    axios.get('/choices/constraints').
    then((response) => {
        console.log(response.data)
        this.setState({labels: response.data})
    })
    .catch(function (error) {
      console.log(error);
    });
    // this.getInitialData();
  }

  componentWillMount(){
    this.selectedCheckboxes = new Set();
  }

  getConstraints(){

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

  checkTimetable(state) {
  console.log(this.state,this.selectedCheckboxes);
//    var data = {violations:["Room 311 is used by different lectures at the same time", "Class Databases I does not have enough hours"],
//                metadata:[{day:"Tuesday", time:17}, {name:"Databases I"}]}
//    this.setState({violationData:data})
     axios.post('/timetable/check', {
     timetable: state.timetable, term: state.selected_term, constraints: Array.from(this.selectedCheckboxes)
   })
   .then( (response) => {
     this.setState({violationData: response.data[0]})
    this.setState({isChecked:true})
//    this.generateViolations();


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
        var timetables = response.data.solutions;
        this.setState({timetable: timetables[0]});
        }
    })
    .catch(function (error) {
      console.log(error);
    });

  }

  generateConstraintSelector(){
    var checkboxes = []
    const labels = this.state.labels
    labels.forEach(l =>{
      checkboxes.push(<li><MyCheckbox label={l} handleChange={this.toggleCheckbox} key={l}/></li>)
    })
    var checkboxList = <ul>{checkboxes}</ul>
    return checkboxList
  }

  toggleCheckbox(label){
    if(this.selectedCheckboxes.has(label)){
      this.selectedCheckboxes.delete(label)
    }else{
      this.selectedCheckboxes.add(label)
    }
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

  generateViolations(){
    var violations = []
    const violationData = this.state.violationData;
    console.log(violationData)
    if (violationData !=  null){
      for (var i=0; i<violationData.violations.length; i++){
        const activeViolation = violationData.metadata[i];
        violations.push(<li className="violation-list-item"><span onClick={()=>{this.setState({activeViolation: activeViolation})}}>{violationData.violations[i]}</span></li>)
      }
      if(violationData.violations.length == 0 && this.state.isChecked){
      violations = <li className="check-success"><span>Timetable is valid on all selected constraints</span></li>
    }
    }
    return violations
  }


  //generate table with appropriate filters
  filterTable(timetable){
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
    var filteredTimetable = [];

    timetable.forEach(lect => {
      if (rooms.indexOf(lect.room) != -1 && courses.indexOf(lect.name) != -1){
        filteredTimetable.push(lect);
      }
    })
    return filteredTimetable
}

  handleRemovingFilter(e) {
      if(e.button == 1) {
        var prevFilter = this.state.roomsFilter;
//        console.log("prev",prevFilter,"removes",e.target.textContent);
        var index = -1;
        for (var i=0; i < this.state.roomsFilter.length ;i ++) {
           if(this.state.roomsFilter[i].label == e.target.textContent) {
            index = i;
           }
        }
        if(index >= 0) {
        this.state.roomsFilter.splice(index,1);
        this.setState({roomsFilter: this.state.roomsFilter}); // force rerender
        }
        console.log(this);
      }

    }

  render () {
    var violations = this.generateViolations()
    var constraintSelectorItems = this.generateConstraintSelector()
    var violationList = <ul className="violation-list">{violations}</ul>
    var timetable
    var ftable = this.filterTable(this.state.timetable)
    var rows = this.generateRows(ftable)
    timetable = <Timetable rows={rows} hours={this.state.hours} addLecture={this.addLecture}
                 removeLecture={this.removeLecture} openModal={this.openModal} closeModal={this.closeModal}
                 modalOpen={this.state.modalOpen} violation={this.state.activeViolation}
                 rooms={this.state.rooms} subjects={this.state.subjects}/>
    var saveBtn = <button class="horizontal2 save" onClick={ () => {this.saveTimetable(this.state.timetable)}}><span>Save</span></button>
    var checkBtn = <button class="horizontal2" onClick={ () => {this.checkTimetable(this.state)}}>Check</button>
    var generateBtn = <button class="horizontal2" onClick={ () => {this.generateTimetable(this.state.selected_term)}}>Generate</button>
    var style = {color:'white'}

    var dropDownRooms = <MultiSelect
                    placeholder = "Select Room(s)"
                    theme = "material"
                    options = {this.state.rooms.map(
                      room => ({label: room, value: room})
                    )}
                    onValuesChange = {value => {this.setState({roomsFilter : value})}}
                    renderValue = {(arg$) => {
                                        var label;
                                        label = arg$.label;
                                        return <div className='simple-value'/>,
                                        <span onClick={(e) => {this.handleRemovingFilter(e)}}>{label}</span>;

                                       }
                                  }
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
              <h1 id="top-item">Timetabling Assistant<FontAwesome name="pencil"></FontAwesome></h1>
              <h2>DEPARTMENT OF COMPUTING</h2>
              <div class="left-component">
                {selectTermDropdown}
                <div id="top-item">{dropDownRooms}</div>
                <div>{dropDownCourses}</div>
                <div style={{color: 'white'}}>
                {constraintSelectorItems}
                </div>
                <div>{saveBtn}
                {checkBtn}
                {generateBtn}</div>
                <div className="violation-console">
                {violationList}
                </div>
              </div>
              <div class="right-component">
                {timetable}
              </div>
            </div>);

  }
}

render(<App/>, document.getElementById('app'));
