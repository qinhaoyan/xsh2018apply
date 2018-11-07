import React from 'react';
import Table from '@components/table';
import {get} from '@util/request';
import './index.scss';

export default class Signed extends React.Component {
	constructor(props){
		super(props);
		this.state = {
			data: []
		}
		get('/api/admin/getSigned')
		.then(re=>{
			if(re.success == 2) {
				this.setState({
					data: re.list
				})
			}
		})
	}
	render() {
		return (
			<div className="signed">
				<Table data={this.state.data} signed={true}/>
			</div>
		)
	}
}