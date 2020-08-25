var ec_center = echarts.init(document.getElementById('c2'),"dark");

// var mydata = [{'name':'上海','value':0},{'name':'云南','value':0}]

var ec_center_option =  {
		title: {
			text: '',
			subtext:'',
			x:'left'
		},
		tooltip: {
			trigger: 'item',
		},
		//左侧导航图标
		visualMap: {
			show:true,
			x:'left',
			y:'bottom',
			textStyle:{
				fontSize:10
			},
			splitList: [{start:0,end:0},
				{start:1,end:9},
				{start:10,end:99},
				{start:100,end:999},
				{start:1000,end:9999},
				{start:10000}],
			color:['#8A3310','#C64918','#E55B25','#F2AD92','#F9DCD1','#ffffff']
		},
		//配置属性
		series: [{
				name: '现有确诊人数',
				type: 'map',
				mapType: 'china',
				roam:false,//拖动和缩放
				itemStyle: {
					normal: {
						borderColor: '#009fe8',	//区域边框颜色
						areaColor: '#ffefd5',	//区域颜色
						borderWidth: .2, //区域边框宽度
					},//正常样式
					emphasis: {	//鼠标滑过地图高亮的设置
						areaColor: '#c7fffd',
						borderWidth: .2,
						borderColor: '#bc987e',
					}//鼠标事件区块样式
				},
				label: {
					normal: {
						show: true,	//省份名称
						fontSize:10,
					},
					emphasis: {
						show: true,
						fontSize:10,
					}
				},
				
				data: []//数据
			}]
};
ec_center.setOption(ec_center_option)

                    