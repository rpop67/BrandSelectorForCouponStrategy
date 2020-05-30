import React, { Component } from 'react';
import { HorizontalBar as BarChart } from 'react-chartjs-2';
import './app.css';
import './Component/loadingScreen.js';
import LoadingScreen from './Component/loadingScreen.js';

// var dataList= [ 70.0, 45.0, 34.0, 33.0, 16]
// const updatedDataList=[100, 64.28571428571429, 48.57142857142857, 47.14285714285714, 22.857142857142858]

var updatedCheckedList = [];
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
	componentDidMount() {
		console.log('CALLLLED');
		fetch('/timeBlock').then((res) => res.json()).then((data) => {
			this.setState({
				loading: false,
				time: data.block.time,
				dataList: data.block.dataList,
				labelList: data.block.labelList
			});

			console.log('mounting... ', this.state.dataList);
		});

		const { dataList } = this.state;
		var total = 0;
		var highest = dataList[0];
		dataList.map((data) => (total += data));
		console.log('total: ', total);
		var newList = [];
		dataList.map((dataValue) => (newList = [ ...newList, dataValue / highest * 100 ]));
		console.log(newList);
		this.setState({ dataList: newList });
	}

	state = {
		domains: [
			'Ecommerce sites',
			'Streaming sites',
			'Food Delivery sites',
			'Grocery Delivery sites',
			'E-Learning sites'
		],
		dataList: [],
		time: '',
		selectedDomains: [],
		labelList: [],
		loading: true
	};

	getData = () => {
		const listReturned = this.state.dataList;
		const labelListReturned = this.state.labelList;

		const data_StackedBar = {
			labels: labelListReturned,
			datasets: [
				{
					label: 'Popularity',
					data: listReturned,
					// backgroundColor: '#742774' // green
					backgroundColor: '#414f4f'
				}
			]
		};
		console.log('dataList:  ', listReturned);
		console.log(data_StackedBar);
		return data_StackedBar;
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

	onClickHandler = (event) => {
		var checkedList = this.state.selectedDomains;
		const checkedState = event.target.checked;
		const item = event.target.name;
		// console.log(item,checkedState);
		if (checkedState == true) {
			//adding the domain to the list
			checkedList = [ ...checkedList, item ];
		} else {
			//removind the entry of that domain
			if (checkedList.includes(item)) {
				for (var index = 0; index < checkedList.length; index++) {
					if (checkedList[index] == item) {
						checkedList.splice(index, 1);
					}
				}
			}
		}
		this.setState({ selectedDomains: checkedList, loading: true }, () => {
			console.log(checkedList);
			fetch('/resultPost', {
				method: 'POST',
				headers: {
					content_type: 'application/json'
				},
				body: JSON.stringify(this.state.selectedDomains)
			})
				.then((response) => {
					return response.json();
				})
				.then((data) => {
					this.setState({
						dataList: data.block.dataList,
						labelList: data.block.labelList,
						loading: false
					});
					console.log('printing list from flask: ', data.block.list);
				});
		});
		// now that the state is updated, I need to post it to flask
	};

	displayDomain = () => {
		{
			console.log('datalist:::: ', this.state.dataList);
		}
		return (
			<div className="card border-dark text-white ">
				<div class="card-header bg-dark">
					<h5>Domains Considered for coupon selection</h5>
				</div>
				<div className="card-body text-dark">
					{/* <ul className="domainList"> */}
					{this.state.domains.map((domain, i) => (
						<div class="form-check">
							<input
								type="checkbox"
								class="form-check-input"
								name={domain}
								id={domain}
								onClick={this.onClickHandler}
							/>
							<label className="form-check-label" for="materialChecked2">
								{domain}
							</label>
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
				<div className="App-header">{this.state.time}</div>
				<div className="chartsBody">
					<div className="chartBodyMain">
						<div className="domainBlock">{this.displayDomain()}</div>

						<div className="chartMain">
							{this.state.loading ? (
								<LoadingScreen />
							) : (
								<BarChart
									options={options_StackedBar}
									data={this.getData()}
									legend={legend_StackedBar}
								/>
							)}
						</div>
					</div>
				</div>
			</React.Fragment>
		);
	}
}

export default App;
