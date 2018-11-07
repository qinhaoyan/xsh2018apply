import React from 'react';
import {get} from '@util/request';
import './index.scss';

export default class Search extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			isInputFocus: false
		}
		this.inputFocus = this.inputFocus.bind(this);
		this.inputBlur = this.inputBlur.bind(this);
		this.search = this.search.bind(this);
	}
	search() {
		let input = this.refs.search.value;
		if (input){
			let type = input.charCodeAt(0) < 122 ? 0 : 1;
			get('/api/admin/search', {type: type, value: input})
			.then(re=>{
				this.props.getSearchData(re);
			})
			.catch(err=>{
			})
		} 
		else {
			alert('请输入姓名/手机号查询')
		}
	}
	inputFocus() {
		this.setState({
			isInputFocus: true
		})
	}
	inputBlur() {
		this.setState({
			isInputFocus: false
		})
	}
	render() {
		return (
			<div className="search">
				<input type="text" 
					ref="search"
					placeholder="请输入姓名/手机号查询"
					onFocus={this.inputFocus}  
					onBlur={this.inputBlur} 
					onKeyPress={
						e => {
							if (e.key === 'Enter') {
								this.search();
							};
						}
					} />
				<div className="button" onClick={this.search}>
					<i className={"iconfont icon-sousuo " + (this.state.isInputFocus ? 'input-focus' : '')}/>
				</div>
			</div>
		)
	}
} 