import React from 'react';
import {render} from 'react-dom';
import Timetable from './Timetable.jsx';
import axios from 'axios'
import {ReactSelectize, SimpleSelect, MultiSelect} from 'react-selectize';
import Dropdown from 'react-dropdown';
import {utils} from './Utils.jsx';
import {styles} from './Utils.jsx';
import SimpleCheckbox from './SimpleCheckbox.jsx';
import FontAwesome from 'react-fontawesome';
import {CircleLoader} from 'react-spinners';
import Modal from 'react-modal';

  class TimetableContainer extends React.Component{
    constructor(props) {
      super(props);
      this.state = {hours:{start: 9, finish: 17} ,timetable: [],
                     addConstraintModal:false, constraint:{}, isOpenSaveAsModal:false,isOpenLoadModal:false,
                     active_save:null, errorSaveAsMessage:"",  constraintModal:false,
                     subjects:[],
                     courses:[],selectedCourses:[],
                     rooms:[] ,roomsFilter: [], coursesFilter: [],
                     labels:[], loading: false};

      this.saveConstraint=this.saveConstraint.bind(this)
      this.getConstraints=this.getConstraints.bind(this)
      this.constraintModuleChange=this.constraintModuleChange.bind(this)
      this.constraintDayChange=this.constraintDayChange.bind(this)
      this.constraintStartChange=this.constraintStartChange.bind(this)
      this.constraintEndChange=this.constraintEndChange.bind(this)
      this.addLecture=this.addLecture.bind(this)
      this.removeLecture=this.removeLecture.bind(this)
      this.handleRemovingFilter=this.handleRemovingFilter.bind(this)
      this.toggleCheckbox=this.toggleCheckbox.bind(this)
      this.selectedLoadChange=this.selectedLoadChange.bind(this)
      this.saveNameInputChange=this.saveNameInputChange.bind(this)
      this.getInitialData();
    }

    getInitialData(){
    var dropdownData = utils.getDropdownData(this)
      this.getConstraints();
    }

    componentWillMount(){
      this.selectedCheckboxes = new Set();
    }

    getConstraints(){
      axios.get('/choices/constraints').
      then((response) => {
          console.log(response.data)
          this.setState({labels: response.data})
      })
      .catch(function (error) {
        console.log(error);
      });
    }






  saveTimetable(timetable){
    // if knows current save just save
    if(this.state.active_save != null) {

        axios.post('/timetable/updatesave', {
        timetable: timetable,
        save_id: this.state.active_save,
        })
        .then(function (response) {
        console.log(response);
        })
        .catch(function (error) {
        console.log(error);
        });
    }
    // else prompt for name as a new save
    else {
    this.setState({isOpenSaveAsModal: true});
    }
  }

    getSelectedCourses(state) {
        var coursesArr = [];
        state.selectedCourses.forEach((element) => {coursesArr.push(element.value);})
        console.log(coursesArr);
        return coursesArr;
    }

    checkTimetable(state) {
    console.log(this.state,this.selectedCheckboxes);

    var coursesArr = this.getSelectedCourses(state);
  //    var data = {violations:["Room 311 is used by different lectures at the same time", "Class Databases I does not have enough hours"],
  //                metadata:[{day:"Tuesday", time:17}, {name:"Databases I"}]}
  //    this.setState({violationData:data})
       axios.post('/timetable/check', {
       timetable: state.timetable,
       term: state.selected_term,
       constraints: Array.from(this.selectedCheckboxes),
       courses: coursesArr,
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

    generateTimetable(state) {
    var coursesArr = this.getSelectedCourses(state);
    // if not empty select or full select
      axios.get('/timetable/generate', {
          params: {
              term: state.selected_term,
              timetable: state.timetable,
              courses: coursesArr,
              constraints: Array.from(this.selectedCheckboxes),
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

    saveConstraint(){

      axios.post('/timetable/add_constraint', {
      constraint: this.state.constraint
    })
    .then((response) => {
      this.getInitialData()
    })
    .catch(function (error) {
      console.log(error);
    });

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
     newConstraint.subject = e.value

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
          var active
          if(activeViolation == this.state.activeViolation){
            active = "violation-list-item-active"
          }else{
            active = "violation-list-item"
            }
          violations.push(<li className={active}><span onClick={()=>{this.setState({activeViolation: activeViolation})}}>{violationData.violations[i]}</span></li>)
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

      openLoad() {
      console.log("opening load");
      axios.get('/timetable/existingsaves').
        then((response) => {
            console.log(response.data)
            var possibleLoads = []
            for(var i=0; i< response.data.length; i++) {
                possibleLoads.push(response.data[i].name);
            }
            // sets the complete id+name data and a name list for the dropdown select
            this.setState({possibleLoads: response.data,possibleLoadsNameList: possibleLoads})
             this.setState({isOpenLoadModal:true});
        })
        .catch(function (error) {
          console.log(error);
        });

      }



      saveAs() {
      //takes input field
      var name = this.state.saveName;
      var timetable = this.state.timetable;
      if( name == "" || name==null) {
       this.setState({errorSaveAsMessage:"No name selected!"});
       return;
      }
      // request
      axios.post('/timetable/saveas', {
        timetable: timetable,
        save_name: name,
        })
        .then((response) => {
            this.setState({saveName:"",active_save:response.data.save_id});
            this.setState({isOpenSaveAsModal: false});
        })
        .catch(function (error) {
        console.log(error);
      });

      }

      loadSave() {
      var save_id = null;
      var e = this.state.loadCandidate;
      var obj = this.state.possibleLoads.filter(function(item) {return item.name == e });
      save_id = obj[0].id;

      axios.get('/timetable/load',  {
            params: {
                save_id: save_id
            }
        })
        .then((response) => {
        // update table and set active save info for direct save
        this.setState({timetable:response.data.table,active_save:response.data.save_id});
        // empties possible loads and list
        this.setState({possibleLoads:[],possibleLoadsNameList:[]});
        //closes the modal
        this.setState({isOpenLoadModal: false});
      }).catch(function(error) {
        });
      }

      selectedLoadChange(e) {
        console.log('e',e);
        this.setState({loadCandidate:e.value});
      }

      saveNameInputChange(e) {
      console.log("eS",e.target);
        this.setState({saveName:e.target.value});
      }

    render () {

     var days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
     var hours = []
     for(var i = this.state.hours.start; i<= this.state.hours.finish; i++){
       hours.push(i)
     }
      var violations = this.generateViolations()
      var constraintSelectorItems = this.generateConstraintSelector()
      var violationList = <ul className="violation-list">{violations}</ul>
      var ftable = this.filterTable(this.state.timetable)
      var timetable
      if(!this.state.loading){
      var rows = this.generateRows(ftable)
      timetable = <Timetable rows={rows} hours={this.state.hours} addLecture={this.addLecture}
                   removeLecture={this.removeLecture} violation={this.state.activeViolation}
                   rooms={this.state.rooms} subjects={this.state.subjects}/>
      }
      else {
        timetable = <div><CircleLoader loading={this.state.loading} color={'white'} /> Generating timetable...</div>

      }
      var saveBtn = <button class="horizontal2 save" onClick={ () => {this.saveTimetable(this.state.timetable)}}><span>Save</span></button>
      var checkBtn = <button class="horizontal2" onClick={ () => {this.checkTimetable(this.state)}}>Check</button>
      var generateBtn = <button class="horizontal2" onClick={ () => {this.generateTimetable(this.state)}}>Generate</button>
      var saveAsBtn = <button class="horizontal2 save" onClick={ () => {this.setState({isOpenSaveAsModal:true})}}>Save As</button>
      var loadBtn = <button class="horizontal2" onClick={ () => {this.openLoad()}}>Load</button>

      var saveAsModal = <Modal isOpen={this.state.isOpenSaveAsModal} style={styles.sstyle}>
                     <label className="save-error">{this.state.errorSaveAsMessage}</label><br/>
                     <label>Save as:</label>

                     <input type="text" className="save-input" onChange={this.saveNameInputChange} name="saveAsName"></input><br/>
                     <div className="button-row">
                     <button  onClick={ () => this.setState({isOpenSaveAsModal: false})}> Cancel</button>
                     <button  onClick={ () => this.saveAs()}> Save </button>
                     </div>
                      </Modal>

      var loadModal = <Modal isOpen={this.state.isOpenLoadModal} style={styles.sstyle}>
                    <label>Please, Select a save to load: </label>
                    <Dropdown options={this.state.possibleLoadsNameList} placeholder="Select a save"
                    onChange={this.selectedLoadChange} value={this.state.loadCandidate} />
                    <button  onClick={ () => this.setState({isOpenLoadModal: false})}> Cancel</button>
                    <button  onClick={ () => this.loadSave()}> Load </button>

                    </Modal>

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

      var selectCoursesMulti = <MultiSelect
                                placeholder= "Select Courses(s)"
                                theme="material"
                                options = {this.state.courses.map(
                                 course => ({label: course, value: course})
                                 )}
                                 onValuesChange = { value => {this.setState({selectedCourses: value})}}
                                 />

      var dropDownCourses = <MultiSelect
                            placeholder = "Select Subjects(s)"
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
     var constraintBtn = <button class="horizontal2" onClick={()=>{this.setState({constraintModal:true})}}>Constraints</button>

     console.log(this.state.activeViolation);
      return( <div>
                <h1 id="top-item">Timetabling Assistant<FontAwesome name="pencil"></FontAwesome></h1>
                <h2>DEPARTMENT OF COMPUTING</h2>
                <div class="left-component">
                  <h2 className="control-title"> Filter Timetable: </h2>
                  <div id="top-item">{dropDownRooms}</div>
                  <div>{dropDownCourses}</div>
                  <div style={{color: 'white'}}>
                  </div>
                  <div>{saveBtn}
                  {saveAsBtn}
                  {loadBtn}
                  {checkBtn}
                  {generateBtn}
                  {constraintBtn}
                  </div>
                  <h2 className="control-title">Select Courses to which the constraints apply:</h2>
                  {selectCoursesMulti}
                  <h2 className="control-title">Select Term(Mandatory):</h2>
                  {selectTermDropdown}
                  <div className="violation-console">
                  {violationList}
                  </div>
                </div>
                <div class="right-component">
                  {timetable}
                </div>
                <Modal isOpen={this.state.constraintModal} style={styles.cstyle}>
                <div className = "constraint-list">
                <h2 className="constraint-title"> Constraints </h2>
                {constraintSelectorItems}
                </div>
                <div className = "add-constraint-form">
                  <h2 className="constraint-title">Add a Constraint</h2>
                  <Dropdown options={this.state.subjects} placeholder="Select a module" onChange={this.constraintModuleChange} value={this.state.constraint.subject}/>
                  Cannot be scheduled on:
                  <Dropdown options={days} placeholder="Select a day" onChange={this.constraintDayChange} value={this.state.constraint.day}/>
                  between
                  <Dropdown options={hours} placeholder="Select a time" onChange={this.constraintStartChange} value={this.state.constraint.start}/>
                  and
                  <Dropdown options={hours} placeholder="Select a time" onChange={this.constraintEndChange} value={this.state.constraint.end}/>
                  <br/>
                  <button className="constraint-button" onClick={()=>{this.setState({constraintModal: false})}}>Close</button>
                  <button className="constraint-button" onClick={()=>{this.saveConstraint()}}>Add Constraint</button>
                </div>
                </Modal>
              {loadModal}
              {saveAsModal}
              </div>);

    }
  }


export default TimetableContainer;
