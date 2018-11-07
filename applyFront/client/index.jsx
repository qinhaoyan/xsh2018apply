import React from 'react';
import ReactDom from 'react-dom';
import {Router, Route, browserHistory, IndexRoute} from 'react-router';
import App from '@pages/app';
import Home from '@pages/home';
import Details from '@pages/details';
import Setting from '@pages/setting';
import Signed from '@pages/signed';
import Login from '@pages/login';
import './index.scss';

ReactDom.render(
	<Router history={browserHistory}>
		<Route path="/admin" component={App}>
			<IndexRoute component={Home} />
			<Route path="setting" component={Setting} />
			<Route path="signed" component={Signed} />
			<Route path="details/:id" component={Details} />
		</Route>
		<Route path='/admin/login' component={Login} />
	</Router>
	, document.getElementById('root')
)