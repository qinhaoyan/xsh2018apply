import React from 'react';
import {post,get} from '@util/request';
import FinishSure from './finishsure';
import './index.scss';

export default class Finish extends React.Component {
	constructor(props) {
		super(props);
		this.state={
			stage: 0,
			show: false,
			type: ''
		}
		get('/api/admin/stage')
		.then(re=>{
			if (re.success == 2){
				this.setState({
					stage: re.stage
				})
			}	
		})
		.catch(err=>{})
	}
	onChangeStage(type) {
		if (!this.state.show) {
			this.setState({
				show: true,
				type: type
			})
		}
		else {
			this.setState({
				show: false
			})
		}
	}	
	render() {
		return (
			<div className="finish">
				<div className={this.state.stage >= 1 ? "finished":"nofinish"} onClick={this.state.stage == 0 ? this.onChangeStage.bind(this, 1) : null}>初试完成</div>
				<div className={this.state.stage >= 2 ? "finished":"nofinish"} onClick={this.state.stage == 1 ? this.onChangeStage.bind(this, 2) : null}>复试完成</div>
				<div className={this.state.stage >= 3 ? "finished":"nofinish"} onClick={this.state.stage == 2 ? this.onChangeStage.bind(this, 3) : null}>终面完成</div>
				<FinishSure show={this.state.show} type={this.state.type} onChangeStage={this.onChangeStage.bind(this)}/>
			</div>
		)
	}
} 