import React from 'react';
import {post} from '@util/request';
import './index.scss';

export default class Pass extends React.Component {
	constructor(props) {
		super(props);
	}
	onChoosePass(type) {
		if(this.props.chooseList.length > 0) {
			post('/api/admin/passlist', {type: type, list: this.props.chooseList})
			.then(re=>{})
			.catch(err=>{})
		}
		else {
			alert("请选择学生")
		}
	}
	render() {
		return (
			<div className="pass">
				<div className="button">
					批量操作
					<i className="iconfont icon-xiala"/>
				</div>
				<div className="drop">
					<div className="pass1" onClick={this.onChoosePass.bind(this, 1)}>
						通过初试
					</div>
					<div className="pass2" onClick={this.onChoosePass.bind(this, 2)}>
						通过复试
					</div>
					<div className="pass3" onClick={this.onChoosePass.bind(this, 3)}>
						通过终面
					</div>
				</div>
			</div>
		)
	}
} 