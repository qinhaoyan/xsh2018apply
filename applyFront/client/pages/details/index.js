import React from 'react';
import {Link,browserHistory} from 'react-router';
import {post,get} from '@util/request';
import './index.scss';

export default class Details extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			isloading: false,
			isloading2: false,
			name: '',
			sex: '',
			stu_id: '',
			academy: '',
			tel: '',
			QQ: '',
			email: '',
			asp: '',
			isAdjust: 0,
			pic: '',
			character: '',
			resume: '',
			audition1: '',
			scale1: '',
			audition2: '',
			scale2: '',
			audition3: '',
			scale3: '',
		}
		this.getDetail = this.getDetail.bind(this);
		let tel = props.params.id;
		this.getDetail(tel)
	}
	getDetail(tel){
		get('/api/admin/getDetail', {tel})
		.then(re=>{
			if (re.success == 2){
				this.setState({
					name: re.name,
					sex: re.sex,
					stu_id: re.stu_id,
					academy: re.academy,
					tel: re.tel,
					QQ: re.QQ,
					email: re.email,
					asp: re.asp,
					isAdjust: re.isAdjust,
					pic: re.pic,
					character: re.character,
					resume: re.resume,
					audition1: re.audition1,
					scale1: re.scale1,
					audition2: re.audition2,
					scale2: re.scale2,
					audition3: re.audition3,
					scale3: re.scale3,
				})
			}
			else {
				alert(re.message)	
			}
		})
		.catch(err=>{
			alert('系统错误，请稍后重试！')
		})
	}
	renderAudition(type) {
		let audition;
		let scale;
		let title;
		let text;
		switch (type) {
			case 1:
				title = "初试";
				break;
			case 2:
				title = "复试";
				break;
			case 3:
				title = "终面";
				break;
		}
		if (this.state['audition'+type]) {
			text = <div style={{margin: '5px 0 20px'}}>{this.state['audition'+type]}</div>
		}
		else {
			text = <textarea ref={"audition"+type} ></textarea>
		}
		audition = (<div className="audition">
				<span>{title}评价：</span>
				{text}
				
			</div>)
		scale = (<div className="scale">
				<span>{title}评分：</span>
				<input autoComplete="off" type="text" ref={'scale'+type} defaultValue={this.state['scale'+type]}/>
			</div>)
		return (<div className={'func'+type}>
				{audition}
				{scale}
			</div>)
	}
	onCommit() {
		let audition1 = this.refs.audition1 && this.refs.audition1.value,
			audition2 = this.refs.audition2 && this.refs.audition2.value,
			audition3 = this.refs.audition3 && this.refs.audition3.value,
		    scale1 = this.refs.scale1.value,
			scale2 = this.refs.scale2.value,
			scale3 = this.refs.scale3.value;
		if (!this.state.isLoading) {
			this.setState({
				isloading: true
			})
			post('/api/admin/commits', {audition1,audition2,audition3,scale1,scale2,scale3,tel:this.state.tel})
			.then(re=>{
				if (re.success == 2) {
					alert('提交成功');
				}
				if (re.success == 1) {
					alert('提交失败，请稍后重试');
				}
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
	onNext() {
		if (!this.state.isloading2){
			this.setState({
				isloading2: true
			})
			post('/api/admin/next',{tel: this.state.tel})
			.then(re=>{
				if (re.success == 2) {
					browserHistory.push('/admin/details/'+re.tel);
					this.getDetail(re.tel);
				}
				if (re.success == 4) {
					alert('暂无数据');
				}
				if (re.success == 1) {
					alert('系统错误，请稍后重试！');
				}
				if (re.success == 3) {
					alert('叫号短信发送失败，请人工叫号');
					browserHistory.push('/admin/details/' + re.tel);
				}
				this.setState({
					isloading2: false
				})
			})
			.catch(err=>{
				alert('系统错误，请稍后重试！');
				this.setState({
					isloading2: false
				})
			})
		}
		

	}
	render() {
		return (
			<div className="details">
				<div className="information">
					<div className="title">个人信息</div>
					<div className="pic">
						<img src={'/api/admin/getPic?stu_id='+this.state.stu_id} alt=""/>
					</div>
					<div className="name"><span>姓名：</span>{this.state.name}</div>
					<div className="sex"><span>性别：</span>{this.state.sex == 1 ? '男' : '女'}</div>
					<div className="stu_id"><span>学号：</span>{this.state.stu_id}</div>
					<div className="academy"><span>学院：</span>{this.state.academy}</div>
					<div className="tel"><span>电话：</span>{this.state.tel}</div>
					<div className="QQ"><span>QQ：</span>{this.state.QQ}</div>
					<div className="email"><span>邮箱：</span>{this.state.email}</div>
					<div className="asp"><span>志愿：</span>{this.state.asp}</div>
					<div className="isAdjust"><span>是否接受调剂：</span>{this.state.isAdjust == '1' ? '是' : '否'}</div>
					<div className="resume">
						<span>个人介绍：</span>
						<div>{this.state.resume}</div>
					</div>
					<div className="character">
						<span>性格测试结果：</span>
						<div>{this.state.character}</div>
					</div>
				</div>
				<div className="func">
					{this.renderAudition.call(this,1)}
					{this.renderAudition.call(this,2)}
					{this.renderAudition.call(this,3)}
				</div>
				<div className="button">
					<div className="commit" onClick={this.onCommit.bind(this)}>
						<div className="word" style={{display: this.state.isloading ? 'none':'block'}}>提交</div>
						<i className="iconfont icon-icon-loading" style={{display: this.state.isloading ? 'block':'none'}}/>
					</div>
					<div className="next" onClick={this.onNext.bind(this)}>
						<div className="word" style={{display: this.state.isloading2 ? 'none':'block'}}>下一个</div>
						<i className="iconfont icon-icon-loading" style={{display: this.state.isloading2 ? 'block':'none'}}/>
					</div>
				</div>
			</div>
		)
	}
} 