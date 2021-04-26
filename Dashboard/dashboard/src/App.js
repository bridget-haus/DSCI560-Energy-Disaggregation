import './App.css';
import { ImLeaf } from "react-icons/im";
import NeighborChart from "./charts/neighbors/Neighbors";
import DailyChart from "./charts/daily/Daily";
import ApplianceChart from "./charts/appliances/Appliances";
import UserProfile from "./other/user-info/UserInfo";
import ApplianceInfo from "./other/app-info/ApplianceInfo";
import NeighborInfo from "./other/neighbor-info/NeighborInfo";


function App() {

  return (
    <div className="App">
      <header className="App-header">
          {/*<img src={logo} className="App-logo" alt="logo" />*/}
        <span>
            <ImLeaf />
            <h1>My Energy</h1>
        </span>

      </header>
        <div className="Content">
            <div id="side-content">
                <UserProfile />
                <ApplianceInfo />
                <NeighborInfo />
            </div>
            <div id="main-content">
                <div className='Chart-Container' id='main-chart'>
                    <h2>Daily Energy Usage</h2>
                    <DailyChart />
                </div>
                <div className='Chart-Container' id="sub-charts">
                    <div className='Sub-Chart' id="app-chart">
                        <h3>Energy Usage by Appliance</h3>
                        <ApplianceChart />
                    </div>
                    <div className='Sub-Chart' id={"neighbors-chart"}>
                        <h3>Neighborhood Comparison</h3>
                        <NeighborChart />
                    </div>
                </div>
            </div>
        </div>
    </div>
  );
}



export default App;
