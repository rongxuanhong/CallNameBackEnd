var TableInit = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {

         //根据窗口调整表格高度
        $(window).resize(function() {
            $('#course_arrange_table').bootstrapTable('resetView', {
                height: oTableInit.tableHeight
            });
        });

        $('#course_timetable').bootstrapTable({
        method: 'get',
        contentType: "application/json",//必须要有！！
        url:"/ajax/api/v1.0/course_time_table",
        height:oTableInit.tableHeight,//高度调整
        striped: true, //是否显示行间隔色
        dataField: "result",//bootstrap table 可以前端分页也可以后端分页，这里
        pageNumber: 1, //初始化加载第一页，默认第一页
        pagination:true,//是否分页
//        queryParamsType:'limit',//查询参数组织方式
        queryParams:oTableInit.queryParams,//请求服务器时所传的参数
        sidePagination:'server',//指定服务器端分页
//        pageSize:10,//单页记录数
//        pageList:[5,10,20,30],//分页步进值
        showRefresh:true,//刷新按钮
        clickToSelect: true,//是否启用点击选中行
        toolbarAlign:'right',//工具栏对齐方式
        buttonsAlign:'right',//按钮对齐方式

        showFooter:false,
        columns:[
            {
                title:'周一',
                field:'week_one',
                align: 'center',
                valign: 'middle',
            },
            {
                title:'周二',
                field:'week_two',
                align: 'center',
                valign: 'middle',
            },
             {
                title:'周三',
                field:'week_three',
                align: 'center',
                valign: 'middle',
            },
             {
                title:'周四',
                field:'week_four',
                align: 'center',
                valign: 'middle',
            },
             {
                title:'周五',
                field:'week_five',
                align: 'center',
                valign: 'middle',
            },
        ],
        locale:'zh-CN',//中文支持,
        responseHandler:function(res){
            //在ajax获取到数据，渲染表格之前，修改数据源
            return res;
        }
    });
    };
    oTableInit.tableHeight=function() {
        return $(window).height() - 140;
     }
    //请求服务数据时所传参数
    oTableInit.queryParams= function (params){
        return{
              'class_name':'',
//            //每页多少条数据
//            limit: params.limit,
//            //请求第几页
//            offset:params.offset,
        };
    };
        return oTableInit;
};
function refreshCourseTimeTable(){
  $('#course_timetable').bootstrapTable('refresh', {url: '/ajax/api/v1.0/course_time_table'});
}
$(document).ready(function(){

   tableOperationEvent();
   var tableInit=new TableInit();
   tableInit.Init();
});