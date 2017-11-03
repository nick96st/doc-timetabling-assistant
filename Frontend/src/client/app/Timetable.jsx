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
      console.log(r[11]);
      rowItems.push(<tr><td>{r.day}</td><td>{r[9]}</td><td>{r[10]}</td><td>{r[11]}
                    </td><td>{r[12]}</td><td>{r[13]}</td><td>{r[14]}</td>
                    <td>{r[15]}</td><td>{r[16]}</td><td>{r[17]}</td></tr>)
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
