import React, { Component } from 'react';
import { HorizontalBar as BarChart } from 'react-chartjs-2';
import './app.css';

var dataList= [ 70.0, 45.0, 34.0, 33.0, 16]
const updatedDataList=[100, 64.28571428571429, 48.57142857142857, 47.14285714285714, 22.857142857142858]
const data_StackedBar = {
    labels: [ 'Amazon', 'eBay', 'Tesco', 'Argos', 'Netflix' ],
    datasets: [
        {
            label: 'Popularity',
            data:updatedDataList,
            // backgroundColor: '#742774' // green
            backgroundColor: '#414f4f'
        }
    ]
};




const options_StackedBar = {
	scales: {
		xAxes: [ { stacked: true } ],
		yAxes: [ { stacked: true } ]
	}
};

const legend_StackedBar = {
	display: true,
	cursor: 'pointer'
};

class App extends Component {

    componentDidMount(){
        
        const{dataList}=this.state;
        var total=0;
        var highest=dataList[0];
        dataList.map(data=>(total+=data))
        console.log("total: ",total)
        var newList=[]
        dataList.map(dataValue=>(newList=[...newList,dataValue/highest*100]))
        console.log(newList)
        this.setState({dataList:newList})

    }





	state = {
		domains: [
			'Ecommerce sites',
			'Streaming sites',
			'Food Delivery sites',
			'Grocery Delivery sites',
			'E-Learning sites'
        ],
        dataList: [ 70.0, 45.0, 34.0, 33.0, 16]
    };

    


    
    

    // displayDomain=()=>{
    //     return (
	// 		<div className="card text-white bg-dark mb-3" >
	// 			<div class="card-header">
	// 				<h5>Domains Considered for coupon selection</h5>
	// 			</div>
	// 			<div class="card-body">
					
	// 			</div>
	// 		</div>
	// 	);
    // }

	displayDomain= () => {
        {console.log("datalist:::: ",this.state.dataList)}
		return (
			<div className="card border-dark text-white ">
				<div class="card-header bg-dark">
					<h5>Domains Considered for coupon selection</h5>
				</div>
				<div className="card-body text-dark">					
					{/* <ul className="domainList"> */}
						{this.state.domains.map((domain, i) => (
                            
							<div class="form-check">
                            <input type="checkbox" class="form-check-input" id={domain}/>
                            <label className="form-check-label" for="materialChecked2">{domain}</label>
                          </div>
								
							
						))}
					{/* </ul>				 */}
				</div>
			</div>
		);
	};

	render() {
		return (
			<React.Fragment>
				<div className="App-header">Trends Comparison Dashboard</div>
				<div className="chartsBody">
					<div className="chartBodyMain">
						<div className="domainBlock">{this.displayDomain()}</div>

						<div className="chartMain">
							<BarChart options={options_StackedBar} data={data_StackedBar} legend={legend_StackedBar} />
						</div>
					</div>
				</div>
			</React.Fragment>
            
        );
        
	}
}

export default App;
