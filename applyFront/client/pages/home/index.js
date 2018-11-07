import React from 'react';
import Search from '@components/search';
import Pass from '@components/pass';
import Finish from '@components/finish';
import SwitchPage from '@components/switchpage';
import Table from '@components/table';
import {post,get} from '@util/request';
import {browserHistory} from 'react-router';
import './index.scss';

export default class Home extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			//chooseList: []
			data: [],
			count: '',
			curentpage: '',
			order: 'applyStatus',
			isloading: false
		}
		this.getData = this.getData.bind(this);
		this.getSearchData = this.getSearchData.bind(this);
		this.onChoose = this.onChoose.bind(this);
		this.onBegin = this.onBegin.bind(this);
		this.changeOrder = this.changeOrder.bind(this);

		this.getData(1, this.state.order);
	}
	onChoose(chooseList) {
		this.setState({
			chooseList: chooseList
		})
	}
	onBegin() {
		if(!this.state.isloading) {
			this.setState({
				isloading: true
			})
			post('/api/admin/begin')
			.then(re=>{
				if (re.success == 2) {
					browserHistory.push('/admin/details/' + re.tel);
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
	changeOrder(order){
		this.setState({
			order: order
		})
		this.getData(1, order);
	}
	getData(page, order='applyStatus') {
		get('/api/admin/getInformation', {page: page, order: order})
		.then(re=>{
			if (re.success === 0) {
				alert(re.message);
				browserHistory.push('/admin/login')
			}
			if (re.success === 2){
				this.getSearchData(re);
			}
			
		})
		.catch(err=>{
			alert(err);
		})
	}
	getSearchData(re) {
		this.setState({
			data: re.list,
			curentpage: re.curentpage,
			count: re.count
		})
	}
	render() {
		return (
			<div className="home">
				<div className="func">
					<Search className='search' getSearchData={this.getSearchData}/>
					{/*<Pass className="pass" chooseList={this.state.chooseList}/>*/}
					<Finish newData={this.getData}/>
					<div className="begin" onClick={this.onBegin}>
						<div className="word" style={{display: this.state.isloading ? 'none':'block'}}>开始面试</div>
						<i className="iconfont icon-icon-loading" style={{display: this.state.isloading ? 'block':'none'}}/>
					</div>
				</div>
				<Table className='content' data={this.state.data} getChooseList={this.onChoose} onChangeOrder={this.changeOrder}/>
				<div className="spages">
					<SwitchPage count={this.state.count} curentpage={this.state.curentpage} newData={this.getData} order={this.state.order}/>
				</div>
			</div>
		)
	}
} 