import './ApplianceInfo.css'
import { TiLightbulb } from "react-icons/ti";
import {IoPowerSharp} from "react-icons/io5";
import { Icon, InlineIcon } from '@iconify/react';
import washingMachine from '@iconify-icons/mdi/washing-machine';
import { ImFire } from "react-icons/im";
import { BsPlug } from "react-icons/bs";

function ApplianceInfo() {
    return (
        <div className='Info-Container' id='app'>
            <h3>My Appliances</h3>
            <a id="edit" onClick={activateEdit}>Edit</a>
            <div id='appliance-table'>
                <div className='appliance-list'>
                    <span className='Appliance'>
                        {/*<IoPowerSharp className='Appliance-Icon'/>Main Power*/}
                    </span>
                        <span className='Appliance'>
                        <TiLightbulb className='Appliance-Icon'/>Lighting
                    </span>
                        <span className='Appliance'>
                        <Icon icon={washingMachine} className='Appliance-Icon'/>Washer / Dryer
                    </span>
                </div>
                <div className='appliance-list'>
                    <span className='Appliance'>

                    </span>
                        <span className='Appliance'>
                        <ImFire className='Appliance-Icon'/>Stove
                    </span>
                        <span className='Appliance'>
                        <BsPlug className='Appliance-Icon'/>Kitchen Outlet
                    </span>
                </div>
            </div>

        </div>
    );
}

function activateEdit() {


}


export default ApplianceInfo;