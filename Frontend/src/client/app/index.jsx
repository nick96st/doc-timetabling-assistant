import React from 'react';
import {render} from 'react-dom';
import Timetable from './Timetable.jsx';
import axios from 'axios'
import {ReactSelectize, SimpleSelect, MultiSelect} from 'react-selectize';
import Dropdown from 'react-dropdown';
import {getDropdownData} from './Utils.jsx';
import MyCheckbox from './MyCheckbox.jsx'
import FontAwesome from 'react-fontawesome';
import Modal from 'react-modal';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {hours:{start: 9, finish: 17} ,timetable: [  {time:12, day:"Monday", room: "308", name:"Architecture", type: "lecture"},
                                {time:13, day:"Monday", room: "308", name:"Architecture", type: "lecture"},
                                //{time:16, day:"Tuesday", room: "311", name:"Hardware", type: "lecture"},
                               // {time:17, day:"Tuesday", room: "311", name:"Hardware", type: "lecture"},
                               // {time:17, day:"Tuesday", room: "311", name:"Databases I", type: "lecture"},
                              //  {time:12, day:"Wednesday", room: "308", name:"Databases I", type: "lecture"},
                                ], modalOpen:false,isOpenSaveAsModal:false,isOpenLoadModal:false,active_save:null,
                                  errorSaveAsMessage:"",
                  subjects:["Databases I", "Hardware", "Architecture"], rooms:["308", "311"] ,roomsFilter: [], coursesFilter: [], labels:[]};
    this.openModal=this.openModal.bind(this)
    this.closeModal=this.closeModal.bind(this)
    this.addLecture=this.addLecture.bind(this)
    this.removeLecture=this.removeLecture.bind(this)
    this.handleRemovingFilter=this.handleRemovingFilter.bind(this)
    this.toggleCheckbox=this.toggleCheckbox.bind(this)
    this.selectedLoadChange=this.selectedLoadChange.bind(this)
    this.saveNameInputChange=this.saveNameInputChange.bind(this)
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
    this.openSaveAs();
    }
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

  // start LOAD SAVE AS functionality
  openSaveAs() {
  console.log("opening saveas");
  this.setState({isOpenSaveAsModal:true});
  console.log(this.state.isOpenSaveAsModal);
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

  closeSaveAs() {
  console.log("closing close saveas");
  this.setState({isOpenSaveAsModal: false});
  }

  closeLoad() {
  console.log("closing load modal");
  this.setState({isOpenLoadModal: false});
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
        this.closeSaveAs();
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
    this.closeLoad();
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
    var saveAsBtn = <button class="horizontal2 save" onClick={ () => {this.openSaveAs(this.state)}}>Save As</button>
    var loadBtn = <button class="horizontal2" onClick={ () => {this.openLoad(this.state)}}>Load</button>

    var saveAsModal = <Modal isOpen={this.state.isOpenSaveAsModal}>
                     <label>Name</label><br/>
                     <label>{this.state.errorSaveAsMessage}</label> <br/>
                     <input type="text" onChange={this.saveNameInputChange} name="saveAsName"></input>
                      <button class="horizontal2" onClick={ () => this.saveAs()}> Save </button>
                      </Modal>

    var loadModal = <Modal isOpen={this.state.isOpenLoadModal}>
                    <label>Please, Select a save to load: </label>
                    <Dropdown options={this.state.possibleLoadsNameList} placeholder="Select a save"
                    onChange={this.selectedLoadChange} value={this.state.loadCandidate} />
                    <button class="horizontal2" onClick={ () => this.loadSave()}> Load </button>

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
              <div class="utilityLine">
               {saveAsBtn} {loadBtn}
              </div>
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

              {loadModal}
              {saveAsModal}
            </div>);

  }
}

render(<App/>, document.getElementById('app'));
