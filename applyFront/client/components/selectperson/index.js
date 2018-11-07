import React from 'react';
import Search from '@components/search';
import {post,get} from '@util/request';
import {browserHistory} from 'react-router';
import './index.scss';

export default class SelectPerson extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			show: [],
			select: props.selected
		}
		this.deleteSelect = this.deleteSelect.bind(this);
		this.removeSelect = this.removeSelect.bind(this);
		this.isInSelect = this.isInSelect.bind(this);
		this.isSended = this.isSended.bind(this);
		this.onFilter = this.onFilter.bind(this);
		this.onClose = this.onClose.bind(this);
		this.onSure = this.onSure.bind(this);
		get('/api/admin/getStudentsByStage',{stage: this.props.stage})
		.then(re=>{
			if (re.success == 2) {
				this.onFilter(re);
			}
			if (re.success == 1) {
				alert('系统错误，请联系管理员');
			}
		})
		.catch(err=>{
			alert('系统错误，请稍后重试');
		})
	}
	renderShowRow() {
		let show = this.state.show.map((item, key)=>
			(<tr key={key} className={item.sended ? 'sended' : ''}>
				<td className="choosetd"><div className="choose" onClick={this.onChoose.bind(this, key)}>
					{item.choose ? <i className="iconfont icon-xuanzhong"/> : null}
				</div></td>
				<td className="nametd">{item.name}</td>
				<td className="stu-idtd">{item.tel}</td>
			</tr>)
		);
		return show;
	}
	renderSelectRow() {
		let show = this.state.select.map((item, key)=>
			(<tr key={key}>
				<td className="choosetd"><div className="remove" onClick={this.onRemove.bind(this, key)}>
					{item.choose ? <i className="iconfont icon-yichu"/> : null}
				</div></td>
				<td className="nametd">{item.name}</td>
				<td className="stu-idtd">{item.tel}</td>
			</tr>)
		);
		return show;
	}
	onChoose(key) {
		let show = this.state.show;
		let select = this.state.select;
		if (show[key].choose) {
			show[key].choose = false
			this.deleteSelect(show[key].tel, select)
		}
		else {
		 	show[key].choose = true;
			select.push(show[key]);
		}
		this.setState({
			show: show,
			select: select
		})
	}
	onRemove(key) {
		let show = this.state.show;
		let select = this.state.select;
		this.removeSelect(select[key].tel, show);
		select.splice(key, 1);
		this.setState({
			show: show,
			select: select
		})
	}
	removeSelect(tel, show) {
		for (let i = 0; i < show.length; i++){
			if (tel == show[i].tel) {
				show[i].choose = false;
				break;
			}
		}
	}
	deleteSelect(tel, select) {
		for (let i = 0; i < select.length; i++) {
			if (tel == select[i].tel) {
				select.splice(i, 1)
				break;
			}
		}
	}
	isInSelect(id) {
		for (let item of this.state.select) {
			if (item.tel == id) {
				return true;
			}
			else {
				continue;
			}
		}
		return false;
	}
	isSended(applyStatus) {
		console.log(applyStatus, this.props.type)
		if (applyStatus == (parseInt(this.props.type)  + 1) * 100){
			return true;
		}
		else {
			return false;
		}
	}
	onFilter(re) {
		let data = re.list;
		let show = [];
		for (let item of data) {
			show.push({
				name: item.name,
				tel: item.tel,
				choose: this.isInSelect(item.tel),
				sended: this.isSended(item.applyStatus)
			})
		}
		this.setState({
			show: show
		})
	}
	onClose() {
		this.props.onClose();
	}
	onSure() {
		this.props.onClose();
		this.props.onGetSelect(this.state.select);
	}
	render() {
		return (
			<div className='select-person'>
				<div className="content">
					<i className="iconfont icon-guanbi close" onClick={this.onClose}/>
					<div className="select-search">
						<Search getSearchData={this.onFilter} />
					</div>
					<div className="show-select">
						<div className="show">
							<table border="0" cellSpacing="0" cellPadding="0">
								<thead>
									<tr>
										<td className="choosetd"></td>
										<td className="nametd">姓名</td>
										<td className="stu-idtd">学号</td>
									</tr>
								</thead>
								<tbody>
									{this.renderShowRow.call(this)}
								</tbody>
							</table>
							
						</div>
						<div className="select">
							<table border="0" cellSpacing="0" cellPadding="0">
								<thead>
									<tr>
										<td className="choosetd"></td>
										<td className="nametd">姓名</td>
										<td className="stu-idtd">学号</td>
									</tr>
								</thead>
								<tbody>
									{this.renderSelectRow.call(this)}
								</tbody>
							</table>
						</div>
					</div>
					<div className="select-button">
						<div>已选择：{this.state.select.length}人</div>
						<div className="cancel" onClick={this.onClose}>取消</div>
						<div className="sure" onClick={this.onSure}>确定</div>
					</div>
				</div>
			</div>
		)
	}
}