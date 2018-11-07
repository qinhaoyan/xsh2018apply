import React from 'react';
import {Link} from 'react-router';
import {post} from '@util/request';
export default class TableRow extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			pass: props.applyStatus,
			showAdjust: false,
			chooseAdjust: '',
			show: ''
		}
		/*this.state = {
			choose: false,
		}
		this.onChoose = this.onChoose.bind(this);*/
	}
/*	componentWillReceiveProps(nextProps) {
		if (nextProps.choose == 1) {
			this.setState({
				choose: true
			})
		}
		if (nextProps.choose == -1) {
			this.setState({
				choose: false
			})
		}
	}*/
/*	onChoose() {
		let id = this.props.stu_id;
		if (this.state.choose) {
			this.props.onChildChoose(this.props.stu_id, 0);
			this.setState({
				choose: false
			})
		}
		else {
			this.props.onChildChoose(this.props.stu_id, 1);
			this.setState({
				choose: true
			})
		}
	}*/
	componentWillReceiveProps(nextProps) {
		this.setState({
			pass: nextProps.applyStatus
		})
	}
	onPass(type) {
		post('/api/admin/pass', {type: type, tel: this.props.tel})
		.then(re=>{
			if (re.success == 2){
				this.setState({
					pass: re.applyStatus
				})
			}
			if (re.success == 0){
				alert(re.message)
			}
		})
		.catch(err=>{
			alert(err)
		})
	}
	renderPassButton(type) {
		switch (type) {
			case 1:
				if (this.state.pass < 204 ) {
					return (<div className={"pass-button pass-button1"} onClick={this.onPass.bind(this, 1)}>通过</div>)
				}
				if (this.state.pass == 204) {
					return (<div className={"pass-button pass-button0"}>已回绝</div>)
				}
				if (this.state.pass >= 205) {
					return (<div className={"pass-button pass-button2"}>已通过</div>)
				}
			case 2:
				if (this.state.pass < 200) {
					return (<div className={"pass-button pass-button4"}>通过</div>)
				}
				if (this.state.pass >= 205 && this.state.pass < 304) {
					return (<div className={"pass-button pass-button1"} onClick={this.onPass.bind(this, 2)}>通过</div>)
				}
				if (this.state.pass == 204) {
					return (<div className={"pass-button pass-button3"}>通过</div>)
				}
				if (this.state.pass == 304) {
					return (<div className={"pass-button pass-button0"}>已回绝</div>)
				}
				if (this.state.pass >= 305) {
					return (<div className={"pass-button pass-button2"}>已通过</div>)
				}
			case 3:
				if (this.state.pass == 204 || this.state.pass == 304) {
					return (<div className={"pass-button pass-button3"}>通过</div>)
				}
				if (this.state.pass < 305) {
					return (<div className={"pass-button pass-button4"}>通过</div>)
				}
				if (this.state.pass >= 305 && this.state.pass < 404) {
					return (<div className={"pass-button pass-button1"} onClick={this.onPass.bind(this, 3)}>通过</div>)
				}
				if (this.state.pass == 404) {
					return (<div className={"pass-button pass-button0"}>已回绝</div>)
				}
				if (this.state.pass == 405) {
					return (<div className={"pass-button pass-button2"}>已通过</div>)
				}
		}
	}
	onShowAdjust() {
		this.setState({
			showAdjust: true
		})
	}
	onCloseAdjust() {
		this.setState({
			showAdjust: false
		})
	}
	onAdjust(BU) {
		post('/api/admin/onAdjust',{tel: this.props.tel, BU: BU})
		.then(re=>{
			if (re.success == 2) {
				this.setState({
					showAdjust: false,
					show: 'none'
				})
			}
			else {
				alert(re.message);
			}
		})
		.catch(err=>{
			alert(err);
		})
	}
	renderAdjust() {
		let BU = this.props.asp.split(' ').map((re,key)=>(re.split('.')[1]));
		let BUs = ['综合部','学习部','宣传部','权益提案部','生活服务部','文艺部','体育部','女生部'];
		let Button = BUs.map((re,key)=>{
			let btn;
			if (BU.indexOf(re) > -1) {
				btn = <div className="cannot-choose" key={key}>{re}</div>
			}
			else {
				btn = <div className="can-choose"  onClick={this.onAdjust.bind(this, key+1)} key={key}>{re}</div>
			}
			return btn;
		})

		return (<div className='showAdjust'>
					<div className="content">
						<i className="iconfont icon-guanbi close" onClick={this.onCloseAdjust.bind(this)}/>
						<div className="BU">
							{Button}
						</div>
					</div>
				</div>)
	}
	render() {
		return (
			<tr style={{display: this.state.show}}>
				{/*<td>
					<div className="checkbox" onClick={this.onChoose}>
						<i className="iconfont icon-xuanzhong" style={{opacity: this.state.choose ? 1 : 0}}></i>
					</div>
				</td>*/}
				<td className='name'><Link to={'/admin/details/' + this.props.tel}>{this.props.name}</Link></td>
				<td className='stu-id'>{this.props.stu_id}</td>
				<td className='sex'>{this.props.sex}</td>
				<td className='academy'>{this.props.academy}</td>
				<td className='tel'>{this.props.tel}</td>
				<td className='QQ'>{this.props.QQ}</td>
				<td className='asp'>{this.props.asp}</td>
				{!this.props.signed ? (<td>
					<div 
						className={this.props.isAdjust == '1' && this.props.isAdjusted == '0'?"isAdjust-button" : "isAdjust-button noAdjust"}
						onClick={this.props.isAdjust == '1' && this.props.isAdjusted == '0'?this.onShowAdjust.bind(this):null}
					>调剂</div>
				</td>) : null}
				{!this.props.signed ? <td>{this.props.scale1}</td> : null}
				{!this.props.signed ? <td>{this.renderPassButton.call(this, 1)}</td> : null}
				{!this.props.signed ? <td>{this.props.scale2}</td> : null}
				{!this.props.signed ? <td>{this.renderPassButton.call(this, 2)}</td> : null}
				{!this.props.signed ? <td>{this.props.scale3}</td> : null}
				{!this.props.signed ? <td>{this.renderPassButton.call(this, 3)}</td> : null}
				{this.state.showAdjust ? this.renderAdjust.call(this) : null}
			</tr>
		)
	}
}