import './NeighborInfo.css'

function NeighborInfo() {

    return (
        <div className='Info-Container' id='neighbor'>
            <h3>My Neighbors</h3>
            <a>Add Neighbor</a>
            <div id='neighbor-list'>
                <div className='neighbor-line'>
                    <h4>My House</h4>
                    <h5>House 6</h5>
                </div>
                <div className='neighbor-line'>
                    <h4>Bridget's House</h4>
                    <h5>House 5</h5>
                </div>


            </div>
        </div>
    );

}

export default NeighborInfo;