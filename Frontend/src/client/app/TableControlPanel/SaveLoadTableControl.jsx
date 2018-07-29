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


class TableSaveLoadHandler extends React.Component{

      saveTimetable(timetable){
        // if knows current save just save
        if(this.props.globalState.active_save != null) {
            axios.post('/timetable/updatesave', {
            timetable: timetable,
            save_id: this.props.globalState.active_save,
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
        console.log(this.props);
        this.setState({isOpenSaveAsModal: true});
        }
      }


      saveAs() {
      //takes input field
      var name = this.props.globalState.saveName;
      var timetable = this.props.globalState.timetable;
      var tableDefId = this.props.globalState.tableDefId;
      // checks for a empty name
      if( name == "" || name==null) {
       this.setState({errorSaveAsMessage:"No name selected!"});
       return;
      }
      // request
      axios.post('/timetable/saveas', {
        timetable: timetable,
        save_name: name,
        table_def_id: tableDefId,
        })
        .then((response) => {
            this.props.globalState.setState({active_save:response.data.save_id});
           this.setState({isOpenSaveAsModal: false});
        })
        .catch(function (error) {
        console.log(error);
      });

      }


      loadSave() {
      var save_id = null;
      var e = this.state.loadCandidates;
      save_id = this.state.possibleLoads.filter(function(item) {return item.name == e })[0].id;

      axios.get('/timetable/load',  {
            params: {
                save_id: save_id
            }
        })
        .then((response) => {
        // update table and set active save info for direct save
        this.props.globalState.setState({timetable:response.data.table,active_save:response.data.save_id,
                       table_def:response.data.table_def,tableDefId:response.data.table_def_id});
        // empties possible loads and list
        this.setState({possibleLoads:[], possibleLoadsNameList:[]});
        //closes the modal
        this.setState({isOpenLoadModal: false});
      }).catch(function(error) {
        });
      }


      getExistingSaves() {
      axios.get('/timetable/existingsaves').
        then((response) => {
            var possibleLoads = []
            for(var i=0; i < response.data.length; i++) {
                possibleLoads.push(response.data[i].name);
            }
            // sets the complete id+name data and a name list for the dropdown select
            this.setState({possibleLoads: response.data,possibleLoadsNameList: possibleLoads})
        })
        .catch(function (error) {
          console.log(error);
        });

      }

      openLoadModal() {
         this.setState({isOpenLoadModal:true});
      }


      selectedLoadChange(e) {
        this.setState({loadCandidate:e.value});
      }

// Props:
// globalState - must have access points for table data
    constructor(props) {
        super(props);
        this.state = {}
        this.state.isOpenSaveAsModal = false;
        this.state.isOpenLoadModal = false;
        this.state.loadCandidates = [];
        this.state.possibleLoads = [];
        this.state.possibleLoadsNameList = [];
        this.state.errorSaveAsMessage = "";
        this.selectedLoadChange=this.selectedLoadChange.bind(this)
        this.state.saveBtn   = <button class="horizontal2 save" onClick={ () => {this.saveTimetable(this.props.globalState.timetable);}}><span>Save</span></button>;
        this.state.saveAsBtn = <button class="horizontal2 save" onClick={ () => {this.setState({isOpenSaveAsModal:true});}}>Save As</button>
        this.state.loadBtn   = <button class="horizontal2" onClick={ () => {this.getExistingSaves();this.openLoadModal();}}>Load</button>
    }


    render() {
        console.log(this.state);
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
                        onChange={this.selectedLoadChange} value={this.state.loadCandidates} />
                        <button  onClick={ () => this.setState({isOpenLoadModal: false})}> Cancel</button>
                        <button  onClick={ () => this.loadSave()}> Load </button>

                        </Modal>
        return (
            <span>
            {this.state.saveBtn}
            {this.state.saveAsBtn}
            {this.state.loadBtn}
            <div>
            {saveAsModal}
            {loadModal}
            </div>

            </span>
        );
    }

}


export default TableSaveLoadHandler;