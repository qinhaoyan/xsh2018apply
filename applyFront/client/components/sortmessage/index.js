import React from 'react';
import SelectPerson from '@components/selectperson';
import {post,get} from '@util/request';
import './index.scss';

export default class SortMeassage extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			showSelect: false,
			selected: [],
			isloading: false
		}
		this.onClose = this.onClose.bind(this);
		this.onSelect = this.onSelect.bind(this);
		this.onGetSelect = this.onGetSelect.bind(this);
		this.onSendSortMessage = this.onSendSortMessage.bind(this);
	}
	onClose() {
		this.setState({
			showSelect: false
		})
	}
	onSelect() {
		this.setState({
			showSelect: true
		})
	}
	onGetSelect(select) {
		this.setState({
			selected: select
		})
	}
	onSendSortMessage() {
		let selected = this.state.selected;
		let data = [];
		for (let item of selected) {
			data.push(item.tel);
		}
		let input = [];
		for (let key in this.refs) {
			input.push(this.refs[key].value);
		}
		if (!this.state.isloading){
			this.setState({
				isloading: true
			})
			post('/api/admin/sendSortMessage', {data: data.join(','), type: this.props.type, input: input.join(',')})
			.then(re=>{
				if (re.success == 2) {
					this.setState({
						selected: []
					})
					alert(re.message);
				}
				if (re.success == 3) {
					this.setState({
						selected: []
					})
					alert(re.message +'\r'+'发送失败电话：'+re.errList.toString());
				}
				if (re.success == 1){
					alert('发送失败');
				}
				this.setState({
					isloading: false
				})
			})
			.catch(err=>{
				alert(err);
				this.setState({
					isloading: false
				})
			})
		}
	}
	render() {
		let input = [];
		for (let i = 0; i < this.props.count; i++) {
			input.push((<span key={i}><span>{i+1}：</span><input type="text" ref={'input' + i}/></span>))
		}
		return (
			<div className="sort-message">
				<div className="title">{this.props.title}</div>
				<div className="template" >
					<p dangerouslySetInnerHTML = {{ __html:this.props.template}}></p>
				</div>
				<div className="input">
					{input}
				</div>
				<div className="func">
					<div className="button" onClick={this.onSelect}>选人</div>
					<div className="button" onClick={this.onSendSortMessage}>
						<div className="word" style={{display: this.state.isloading ? 'none':'block'}}>发送</div>
						<i className="iconfont icon-icon-loading" style={{display: this.state.isloading ? 'block':'none'}}/>
					</div>
					<div className="word">已选择：{this.state.selected.length}人</div>
				</div>
				{this.state.showSelect ? <SelectPerson stage={this.props.type} type={this.props.type} selected={this.state.selected} onClose={this.onClose} onGetSelect={this.onGetSelect}/> : null}
			</div>
		)
	}
}