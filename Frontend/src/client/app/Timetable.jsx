import React from 'react'
import {render} from 'react-dom';
import TimetableSlot from './TimetableSlot.jsx';

  const generateHeader = function() {
    var header = <thead/>
    var headerItems = [<th>Day</th>, <th>9</th>, <th>10</th>, <th>11</th>, <th>12</th> ,<th>13</th>, <th>14</th>, <th>15</th>, <th>16</th> ,<th>17</th>]
    header = <thead>
              <tr>{headerItems}</tr>
            </thead>
    return header;
  }

  const getTime = function(time){
    console.log(time);
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
          cols.push(<td><a onClick = {()=>getTime(slot)}><TimetableSlot name = "" room = ""/></a></td>)
        }else{
        var courses = []
        r[i].forEach(s => {
          courses.push (<a onClick = {()=>getTime(s.time)}><TimetableSlot name = {s.name} room = {s.room}/></a>)
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
      <table>
       {generateHeader()}
       <tbody>
       {generateRows(props)}
       </tbody>
       </table>
    );
  }


export default Timetable;
