import React from 'react';
import {render} from 'react-dom';
import Timetable from './Timetable.jsx';
import axios from 'axios'
import {ReactSelectize, SimpleSelect, MultiSelect} from 'react-selectize';
import Dropdown from 'react-dropdown';
import {getDropdownData} from './Utils.jsx';
import SimpleCheckbox from './SimpleCheckbox.jsx'
import FontAwesome from 'react-fontawesome';
import Modal from 'react-modal';

  class TimetableContainer extends React.Component{
    constructor(props) {
      super(props);
      this.state = {hours:{start: 9, finish: 17} ,timetable: [  {time:12, day:"Monday", room: "308", name:"Architecture", type: "lecture"},
                                  {time:13, day:"Monday", room: "308", name:"Architecture", type: "lecture"},], addConstraintModal:false, constraint:{},
                                  subjects:["Databases I", "Hardware", "Architecture"], rooms:["308", "311"] ,roomsFilter: [], coursesFilter: [], labels:[]};
      this.addConstraintModal=this.addConstraintModal.bind(this)
      this.constraintModuleChange=this.constraintModuleChange.bind(this)
      this.constraintDayChange=this.constraintDayChange.bind(this)
      this.constraintStartChange=this.constraintStartChange.bind(this)
      this.constraintEndChange=this.constraintEndChange.bind(this)
      this.closeConstraintModal=this.closeConstraintModal.bind(this)
      this.addLecture=this.addLecture.bind(this)
      this.removeLecture=this.removeLecture.bind(this)
      this.handleRemovingFilter=this.handleRemovingFilter.bind(this)
      this.toggleCheckbox=this.toggleCheckbox.bind(this)
      this.getInitialData();
    }

    getInitialData(){
    var dropdownData = getDropdownData(this)

  //    this.getConstraints();
      axios.get('/choices/constraints').
      then((response) => {
          console.log(response.data)
          this.setState({labels: response.data})
      })
      .catch(function (error) {
        console.log(error);
      });
    }

    componentWillMount(){
      this.selectedCheckboxes = new Set();
    }


    addConstraintModal(){
      this.setState({addConstraintModal: true})
    }

    closeConstraintModal(){
      this.setState({addConstraintModal:false})
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
        checkboxes.push(<li><SimpleCheckbox label={l} handleChange={this.toggleCheckbox} key={l}/></li>)
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
     var newTimetable = this.state.timetable
     newTimetable.push(lect)
     this.setState({timetable: newTimetable})
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


   constraintModuleChange(e){
     var newConstraint = this.state.constraint
     newConstraint.module = e.value

   }

   constraintDayChange(e){
     var newConstraint = this.state.constraint
     newConstraint.day = e.value
   }

   constraintStartChange(e){
     var newConstraint = this.state.constraint
     newConstraint.start = e.value
   }

   constraintEndChange(e){
     var newConstraint = this.state.constraint
     newConstraint.end = e.value
   }



    generateViolations(){
      var violations = []
      const violationData = this.state.violationData;
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
      var cstyle = {
        overlay : {
          position          : 'fixed',
          top               : 0,
          left              : 0,
          right             : 0,
          bottom            : 0,
          backgroundColor   : 'rgba(255, 255, 255, 0.75)'
        },
        content : {
          position                   : 'relative',
          top                        : '40px',
          left                       : '50%',
          right                      : '0px',
          bottom                     : '40px',
          border                     : '1px solid #ccc',
          background                 : '#fff',
          overflow                   : 'auto',
          WebkitOverflowScrolling    : 'touch',
          borderRadius               : '4px',
          outline                    : 'none',
          padding                    : '20px',
          width                      : '400px',
          height                     : '400px',
          transform: 'translate(-50%, 0)'
       }
     };
     var days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
     var hours = []
     for(var i = this.state.hours.start; i<= this.state.hours.finish; i++){
       hours.push(i)
     }
      var violations = this.generateViolations()
      var constraintSelectorItems = this.generateConstraintSelector()
      var violationList = <ul className="violation-list">{violations}</ul>
      var ftable = this.filterTable(this.state.timetable)
      var rows = this.generateRows(ftable)
      var timetable = <Timetable rows={rows} hours={this.state.hours} addLecture={this.addLecture}
                   removeLecture={this.removeLecture} violation={this.state.activeViolation}
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
     var addConstrainBtn = <button class="horizontal2" onClick={()=>{this.addConstraintModal()}}>Add Constraint</button>
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
                  {generateBtn}
                  {addConstrainBtn}</div>
                  <div className="violation-console">
                  {violationList}
                  </div>
                </div>
                <div class="right-component">
                  {timetable}
                </div>
                <Modal isOpen={this.state.addConstraintModal} style={cstyle}>
                  <Dropdown options={this.state.subjects} placeholder="Select a module" onChange={this.constraintModuleChange} value={this.state.constraint.module}/>
                  Cannot be schedule on:
                  <Dropdown options={days} placeholder="Select a day" onChange={this.constraintDayChange} value={this.state.constraint.day}/>
                  between
                  <Dropdown options={hours} placeholder="Select a time" onChange={this.constraintStartChange} value={this.state.constraint.start}/>
                  and
                  <Dropdown options={hours} placeholder="Select a time" onChange={this.constraintEndChange} value={this.state.constraint.end}/>
                  <br/>
                  <button onClick={()=>{this.closeConstraintModal()}}>Cancel</button>
                  <button onClick={()=>{this.addLecture()}}>Save</button>
                </Modal>
              </div>);

    }
  }


export default TimetableContainer;
