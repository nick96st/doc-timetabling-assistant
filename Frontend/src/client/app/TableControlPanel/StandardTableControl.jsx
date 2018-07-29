import React from 'react';
import {render} from 'react-dom';
import Timetable from '../Timetable.jsx';
import axios from 'axios';
import {ReactSelectize, SimpleSelect, MultiSelect} from 'react-selectize';
import Dropdown from 'react-dropdown';
import {utils} from '../Utils.jsx';
import {styles} from '../Utils.jsx';
import SimpleCheckbox from '../SimpleCheckbox.jsx';
import FontAwesome from 'react-fontawesome';
import {CircleLoader} from 'react-spinners';
import Modal from 'react-modal';
import TableSaveLoadHandler from './SaveLoadTableControl.jsx';


class TableControlPanel extends React.Component{

    constructor(props) {
        super(props);
        this.state = {}
        this.state.saveLoadButtons = <TableSaveLoadHandler globalState={this.props.globalState}/>;
    }


    render() {

        return (

            <div>{this.state.saveLoadButtons}</div>

        );

    }

}


export default TableControlPanel;