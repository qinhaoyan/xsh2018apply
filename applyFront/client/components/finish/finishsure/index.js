import React from 'react';
import {post,get} from '@util/request';
import './index.scss';

export default class FinishSure extends React.Component {
	constructor(props) {
		super(props);
		this.state={
			isloading: false
		}
	}
	onChangeStage(type) {
		if (!this.state.isloading){
			this.setState({
				isloading: true
			})
			post('/api/admin/changeStage', {type: type})
			.then(re=>{
				this.setState({
					stage: re.stage
				})
				this.props.newData(1);
				this.setState({
					isloading: false
				})
			})
			.catch(err=>{
				alert('系统错误，请稍后重试！');
				this.setState({
					isloading: false
				})
			})
		}
		
	}
	render() {
		let show = this.props.show ? 'fiexd' : 'none';
		console.log(show);
		debugger
		return (
			<div className="finishsure" style={{display:show}} >
				{this.state.isloading ? <div className="loading"><span></span><span></span><span></span><span></span><span></span></div>:null}
			</div>
		)
	}
} 