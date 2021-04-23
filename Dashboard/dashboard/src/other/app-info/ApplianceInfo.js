import './ApplianceInfo.css'
import { TiLightbulb } from "react-icons/ti";
import {IoPowerSharp} from "react-icons/io5";
import { Icon, InlineIcon } from '@iconify/react';
import washingMachine from '@iconify-icons/mdi/washing-machine';


function ApplianceInfo() {
    return (
        <div className='Info-Container' id='app'>
            <h3>My Appliances</h3>
            <a>Add Appliances</a>
            <div id='appliance-list'>
                <span className='Appliance'>
                    <IoPowerSharp className='Appliance-Icon'/>Main Power
                </span>
                <span className='Appliance'>
                    <TiLightbulb className='Appliance-Icon'/>Lighting
                </span>
                <span className='Appliance'>
                    <Icon icon={washingMachine} className='Appliance-Icon'/>Washer / Dryer
                </span>


            </div>
        </div>
    );
}

export default ApplianceInfo;