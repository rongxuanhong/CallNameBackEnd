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
        oTableInit.operateFormatter = function (value, row, index) {//赋予的参数
                return [
          '<button class="btn btn_course_arrange" type="button"><i class="fa fa-paste"></i>授课安排</button>',
//          '<button class="btn btn_course_delete" type="button"><i class="fa fa-envelope"></i> 删除</button>',
            ].join('');
         }

        $('#course_arrange_table').bootstrapTable({
        method: 'get',
        contentType: "application/json",//必须要有！！
        url:"/ajax/api/v1.0/course_arrange",//要请求数据的文件路径
        height:oTableInit.tableHeight,//高度调整
//        toolbar: '#toolbar',//指定工具栏
        striped: true, //是否显示行间隔色
        dataField: "result",//bootstrap table 可以前端分页也可以后端分页，这里
        //我们使用的是后端分页，后端分页时需返回含有total：总记录数,这个键值好像是固定的
        //rows： 记录集合 键值可以修改  dataField 自己定义成自己想要的就好
        pageNumber: 1, //初始化加载第一页，默认第一页
        pagination:true,//是否分页
        queryParamsType:'limit',//查询参数组织方式
        queryParams:oTableInit.queryParams,//请求服务器时所传的参数
        sidePagination:'server',//指定服务器端分页
        pageSize:10,//单页记录数
        pageList:[5,10,20,30],//分页步进值
        showRefresh:true,//刷新按钮
//        showColumns:true,
        clickToSelect: true,//是否启用点击选中行
        toolbarAlign:'right',//工具栏对齐方式
        buttonsAlign:'right',//按钮对齐方式
//        toolbar:'#toolbar',//指定工作栏
//        sortable: true,      //是否启用排序
//        sortOrder: 'asc',
        showFooter:false,
        columns:[
            {
                title:'授课班级',
                field:'course_arrange_class',
                align: 'center',
                valign: 'middle',
            },
            {
                title:'已授课课程数',
                field:'course_arrange_number',
                align: 'center',
                valign: 'middle',
            },
            {
                title:'更新日期',
                field:'last_modify_time',
                align: 'center',
                valign: 'middle',
            },
            {
                field: 'operate',
                title: '操作',
                align: 'center',
                valign: 'middle',
                events: operateEvents,
                formatter: oTableInit.operateFormatter //自定义方法，添加操作按钮
            }
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
            //每页多少条数据
            limit: params.limit,
            //请求第几页
            offset:params.offset,
        };
    };
        return oTableInit;
};
function tableOperationEvent(){
     $(".btn_course_arrange").off("click");
      window.operateEvents = {
      'click .btn_course_arrange': function (e, value, row, index) {
            $('#courseArrangeModal').modal('toggle');

             $('#course_arrange_btn').off('click').on('click',function(){
            var course_name=$('#course_arrange_name').val();
            var week=$('#course_arrange_weeks').val();
            var time=$('#course_arrange_times').val();
            var location=$('#course_arrange_sites').val();
            var class_id=row.class_id;
//             var params={'course_name':course_name,'week':week,'time':time,'location':location,'class_id':class_id};
            var form=$('#courseArrangeForm');
            $.ajax({
                url:'/ajax/api/v1.0/course_arrange',
                data:form.serialize()+'&class_id='+class_id,
                type:'POST',
                success:function(result){
                    if(result.success){
                        toastr.success('授课安排一门课程成功');
                         $('#courseArrangeModal').modal('toggle');
                         refreshCourseArrangeTable();
                    }else if(result.error_msg=='20009'){
                          toastr.error('授课时间重复');
                    }else if(result.error_msg=='200010'){
                          toastr.error('课程已经安排');
                    }else{
                          toastr.error('授课失败');
                    }
                },
            });
        });
      },
      };
}
function drop_menu_item_change(){

    var dropdown=$('#course_arrange_site');
        dropdown.children().each(function(){
         $(this).off('click').on('click',function(event){
             var input3=$('#course_arrange_sites');
             input3.val(event.target.innerText);
//             btn3.append(' <span class="caret"></span>');
         });
        });

     var dropdown=$('#course_arrange_time');
        dropdown.children().each(function(){
         $(this).off('click').on('click',function(event){
             var input3=$('#course_arrange_times');
             input3.val(event.target.innerText);
//             btn3.append(' <span class="caret"></span>');
         });
        });
        var dropdown=$('#course_arrange_week');
        dropdown.children().each(function(){
         $(this).off('click').on('click',function(event){
             var input3=$('#course_arrange_weeks');
             input3.val(event.target.innerText);
//             input3.append(' <span class="caret"></span>');
         });
        });
}
function refreshCourseArrangeTable(){
  $('#course_arrange_table').bootstrapTable('refresh', {url: '/ajax/api/v1.0/course_arrange'});
}
$(document).ready(function(){

   tableOperationEvent();
   var tableInit=new TableInit();
   tableInit.Init();

//   addCourseArrange();
   tableOperationEvent();
   drop_menu_item_change();
});