import React from 'react'
import {render} from 'react-dom';
import TimetableSlot from './TimetableSlot.jsx';
import Modal from 'react-modal';
import Dropdown from 'react-dropdown';
import FontAwesome from 'react-fontawesome';
import axios from 'axios';

class ExtInputTextField extends React.Component {
    constructor(props) {
         super(props);
    }
    render() {
        var forRender = <div className={this.props.className}>
                        <label>{this.props.labelText}</label><br/>
                        <label style={{color:"red"}}>{this.props.errorMessage} </label><br/>
                        <input type="text" onChange={this.props.onChange} placeholder={this.props.placeholder}/><br/>
                        </div>

     return forRender;
    }


}

class Timetable extends React.Component{

  constructor(props) {
    super(props);
    this.state={modalOpen:false,nameErrMsg:"",colNameErrMsg:"",colErrMsg:"",rowErrMsg:""};
    this.lectureChange = this.lectureChange.bind(this);
    this.roomChange = this.roomChange.bind(this);
    this.openModal = this.openModal.bind(this);

  }

 generateHeader() {
    var header = <thead/>
    var headerItems = [<th></th>]
    this.props.tableDef.days.forEach(day => { headerItems.push(<th>{day}</th>);});
//    var headerItems = [<th></th>, <th>Monday</th>, <th>Tuesday</th>, <th>Wednesday</th>, <th>Thursday</th> ,<th>Friday</th>]
    header = <thead>
              <tr>{headerItems}</tr>
            </thead>
    return header;
  }

  openModal(slot){
   this.setState({time:slot.time, day:slot.day, modalOpen:true })
  }

  closeModal(){
    this.setState({modalOpen:false})
  }

  deleteLecture(lect){
    this.props.removeLecture(lect);
  }


  generateRows(){
    var days = this.props.tableDef.days;

    var rowItems = []
    var start = this.props.tableDef.start_hour
    var end = this.props.tableDef.end_hour
    for (var i = start; i<= end; i++){
      var cols = [<td>{i}</td>]
      this.props.rows.forEach(r =>{
        var warn = ""
        const slot = {time: i, day:r.day}
        if (r[i].length == 0){
          cols.push(<td><button onClick = {()=>this.openModal(slot)} class="round"><FontAwesome name="plus"></FontAwesome></button><TimetableSlot name = "" room = ""/></td>)
        }else{
          var courses =[]
          r[i].forEach(s=>{
            const lect = s
            if (this.props.violation !== undefined){
              if (this.props.violation.subject !== undefined && this.props.violation.subject.name === s.name){
                warn = "timeslot-warning"
              }else if (this.props.violation.timeslot != undefined && days[this.props.violation.timeslot.day-1] == slot.day && parseInt(this.props.violation.timeslot.hour) == slot.time)
                warn = "timeslot-warning"
            }
            courses.push (<div className={warn} class="session"><TimetableSlot className={warn} name = {s.name} room = {s.room} lecture={lect}/>
            <div className="delete-div"><button onClick={()=>this.deleteLecture(lect)} class="delete round"> <FontAwesome name="trash-o"></FontAwesome> </button></div></div>)
            courses.push(<br/>)
          })
          cols.push(<td>{courses}<button onClick={()=>this.openModal(slot)} class="round"><FontAwesome name="plus"></FontAwesome></button></td>)
        }

      })
      rowItems.push(<tr>{cols}</tr>)
    }
    return rowItems
  }

  lectureChange(e){
    this.setState({lecture:e.value})
  }

  roomChange(e){
    this.setState({room:e.value})
  }

  addLecture(){
    var lect = {name: this.state.lecture, room: this.state.room, time:this.state.time, day:this.state.day, type:"lecture"}
    this.props.addLecture(lect)
    this.closeModal()
  }

  validateInput() {
    console.log("No validation atm");
  }

  createTableDefinition() {
    this.validateInput();

    axios.post('/create_table_size', {
       hours_start: this.newRowNum,
       hours_end: this.newColNum,
       name: this.newName,
       days: this.newColNames,
     })
     .then( (response) => {
       //set table name
       this.props.updateTableDefs(response.data.table_def,response.table_def_id,response.data.save_id);
       this.state.nameErrMsg = "";
       this.state.rowErrMsg  = "";
       this.state.colErrMsg  = "";
       this.state.colNameErrMsg = "";
       this.props.closeNewTableFunc();
       //reset error msgs
     })
     .catch( (error) => {
        if(error.response.data === "NameExists"){
          this.setState({nameErrMsg: "Name already exists."});
          return;
       }
        console.log(error);
     });

  }

    render() {

    var style = {
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
    height                     : '200px',
    transform: 'translate(-50%, 0)'

  }
}

    var cancelTableButton = "";
    // initial mandatory init forbids cancelation of modal
     if(this.props.tableDef !== null) {
     cancelTableButton =<button  onClick={this.props.closeNewTableFunc}> Cancel</button>
     }

    return(
      <div>
      <Modal isOpen={this.state.modalOpen} style={style}>
        <Dropdown options={this.props.subjects} placeholder="Select an option" onChange={this.lectureChange} value={this.state.lecture}/>
        <Dropdown options={this.props.rooms} placeholder="Select an option" onChange={this.roomChange} value={this.state.room}/>
        <br/>
        <button onClick={()=>{this.closeModal()}}>Cancel</button>
        <button onClick={()=>{this.addLecture()}}>Save</button>
      </Modal>

      <Modal isOpen={this.props.tableDef===null || this.props.isOpenNewTable} style={style}>
      <ExtInputTextField labelText="Table Name"
                         onChange={(e) => {this.newName=e.target.value}}  errorMessage={this.state.nameErrMsg}/>
      <ExtInputTextField labelText="Starting slot" placeholder="Enter number"
                         onChange={(e) => {this.newRowNum=e.target.value}}  errorMessage={this.state.rowErrMsg}/>
      <ExtInputTextField labelText="Ending slot" placeholder="Enter number"
                       onChange={(e) => {this.newColNum=e.target.value}}  errorMessage={this.state.colErrMsg}/>
      <ExtInputTextField labelText="Names of columns(comma separated)" placeholder="eg.:Monday,Tues_day,wdnsday,4day"
                       onChange={(e) => {this.newColNames=e.target.value}} errorMessage={this.state.colNameErrMsg}/>

     {cancelTableButton}
     <button  onClick={ () => this.createTableDefinition()}> Create </button>
      </Modal>
      <table>
       {this.generateHeader()}
       <tbody>
       {this.generateRows()}
       </tbody>
       </table>
       </div>
    );
  }
}


export default Timetable;
