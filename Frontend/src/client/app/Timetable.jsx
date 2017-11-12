import React from 'react'
import {render} from 'react-dom';
import TimetableSlot from './TimetableSlot.jsx';
import Modal from 'react-modal';

  const generateHeader = function() {
    var header = <thead/>
    var headerItems = [<th>Day</th>, <th>9</th>, <th>10</th>, <th>11</th>, <th>12</th> ,<th>13</th>, <th>14</th>, <th>15</th>, <th>16</th> ,<th>17</th>]
    header = <thead>
              <tr>{headerItems}</tr>
            </thead>
    return header;
  }

  const addLecture = function(props, time){
   props.openModal()
   console.log(time)
  }

  const closeModal = function(props){
    props.closeModal()
  }

  const generateRows = function(props){
    var rowItems = []
    var start = props.hours.start
    var end = props.hours.finish
    props.rows.forEach(r => {
      var cols = [<td>{r.day}</td>]
      for (var i = start; i <= end; i++ ){
        if (r[i].length == 0){
          const slot = {time: i, day: r.day}
          cols.push(<td><a onClick = {()=>addLecture(props, slot)}><TimetableSlot name = "" room = ""/></a></td>)
        }else{
        var courses = []
        r[i].forEach(s => {
          courses.push (<a onClick = {()=>addLecture(props, slot)}><TimetableSlot name = {s.name} room = {s.room}/></a>)
        })
        cols.push(<td>{courses}</td>)
      }
      }
      rowItems.push(<tr>{cols}</tr>)
    })
    return rowItems
  }



  const Timetable = (props) => {
    return(
      <div>
      <Modal isOpen={props.modalOpen}>
      <input type="text"/>
      <button onClick={()=>{closeModal(props)}}>Close</button>
      </Modal>
      <table>
       {generateHeader()}
       <tbody>
       {generateRows(props)}
       </tbody>
       </table>
       </div>
    );
  }


export default Timetable;
