import React from 'react'
import {render} from 'react-dom';

  const generateHeader = function() {
    var header = <thead/>
    var headerItems = [<th>Day</th>, <th>9</th>, <th>10</th>, <th>11</th>, <th>12</th> ,<th>13</th>, <th>14</th>, <th>15</th>, <th>16</th> ,<th>17</th>]
    header = <thead>
              <tr>{headerItems}</tr>
            </thead>
    return header;
  }

  const generateRows = function(props){
    var rowItems = []
    props.rows.forEach(r => {
      var cols = [<td>{r.day}</td>]
      for (var i = 9; i < 18; i++ ){
        if (r[i].length === 0){
          cols.push(<td></td>)
        }else{
        r[i].forEach(s => {
          cols.push(<td>{s.name} <br/> {s.room} </td>)
        })
      }
      }
      rowItems.push(<tr>{cols}</tr>)
    })
    return rowItems
  }

  const Timetable = (props) => {
    console.log(props.rows)
    generateRows(props)
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
