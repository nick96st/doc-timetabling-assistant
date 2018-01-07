import React from 'react'
import {render} from 'react-dom';
import TimetableSlot from './TimetableSlot.jsx';
import Modal from 'react-modal';
import Dropdown from 'react-dropdown';
import FontAwesome from 'react-fontawesome';

class Timetable extends React.Component{

  constructor(props) {
    super(props);
    this.state={modalOpen:false}
    this.lectureChange = this.lectureChange.bind(this);
    this.roomChange = this.roomChange.bind(this);
    this.openModal = this.openModal.bind(this);

  }

 generateHeader() {
    var header = <thead/>
    var headerItems = [<th></th>, <th>Monday</th>, <th>Tuesday</th>, <th>Wednesday</th>, <th>Thursday</th> ,<th>Friday</th>]
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
    var days = {"1":"Monday","2":"Tuesday","3":"Wednesday","4":"Thusday","5":"Friday"}

    var rowItems = []
    var start = this.props.hours.start
    var end = this.props.hours.finish
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
               console.log(this.props.activeViolation)
              if (this.props.violation.name !== undefined && this.props.violation.name === s.name){
                warn = "timeslot-warning"
              }else if (this.props.violation.timeslot != undefined && days[this.props.violation.timeslot.day] == slot.day && parseInt(this.props.violation.timeslot.hour) == slot.time)
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
    return(
      <div>
      <Modal isOpen={this.state.modalOpen} style={style}>
        <Dropdown options={this.props.subjects} placeholder="Select an option" onChange={this.lectureChange} value={this.state.lecture}/>
        <Dropdown options={this.props.rooms} placeholder="Select an option" onChange={this.roomChange} value={this.state.room}/>
        <br/>
        <button onClick={()=>{this.closeModal()}}>Cancel</button>
        <button onClick={()=>{this.addLecture()}}>Save</button>
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
