var TableInit = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {

         //根据窗口调整表格高度
        $(window).resize(function() {
            $('#course_table').bootstrapTable('resetView', {
                height: oTableInit.tableHeight
            });
        });
        oTableInit.operateFormatter = function (value, row, index) {//赋予的参数
                return [
          '<button class="btn btn_course_modify" type="button"><i class="fa fa-paste"></i>修改</button>',
          '<button class="btn btn_course_delete" type="button"><i class="fa fa-envelope"></i> 删除</button>',
            ].join('');
         }

        $('#course_table').bootstrapTable({
        method: 'get',
        contentType: "application/json",//必须要有！！！！
        url:"/ajax/api/v1.0/course",//要请求数据的文件路径
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
        toolbar:'#toolbar',//指定工作栏
        sortable: true,      //是否启用排序
        sortOrder: 'asc',
        showFooter:false,
        columns:[
//            {
//                title:'全选',
//                field:'select',
//                //复选框
//                checkbox:true,
//                width:25,
//            },
            {
                title:'课程编号',
                field:'course_number',
                align: 'center',
                valign: 'middle',
                sortable:true,
            },
            {
                title:'课程名称',
                field:'course_name',
                align: 'center',
                valign: 'middle',
                sortable:true,
            },
//             {
//                title:'上课时间',
//                field:'course_time',
//                align: 'center',
//                valign: 'middle',
//                sortable:true,
//            },
            {
                title:'课程人数',
                field:'course_members',
                align: 'center',
                valign: 'middle',
                sortable:true,
            },
            {
                title:'课程周次',
                field:'course_week_times',
                align: 'center',
                valign: 'middle',
                sortable:true,
            },
            {
                title:'所在学期',
                field:'semester',
                align: 'center',
                valign: 'middle',
                sortable:true,
            },
//            {
//                title:'课程地点',
//                field:'position',
//                align: 'center',
//                valign: 'middle',
//            },
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
        var input=$('#course_query_input').val();
        course_name=(input==''?'':input);
        return{
            action:'course_list',
            //每页多少条数据
            limit: params.limit,
            //请求第几页
            offset:params.offset,
            sort:params.sort,
            sortOrder:params.order,
            course_name:course_name,
        };
    };
        return oTableInit;
};
function addCourseValidatorForm(){

   $('#btn_add_course').off('click').on('click',function(){
        $('#addCourseModal').modal('toggle');

        $('#addCourseForm').bootstrapValidator({
            message:'',
             feedbackIcons: {
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },
            fields:{
                course_number:{
                    validators:{
                        notEmpty: {
                            message: '课程编号不空'
                        },
                    }
                },
                course_name:{
                    validators:{
                        notEmpty: {
                            message: '课程名称不空'
                        },
                    }
                    },
                course_weeks:{
                    validators:{
                        notEmpty: {
                            message: '课程周次不空'
                        },
                    }
                    },
                  course_members:{
                    validators:{
                        notEmpty: {
                            message: '课程人数不空'
                        },
                    }
                    },
                course_semester:{
                    validators:{
                        notEmpty: {
                            message: '课程学期不空'
                        },
                    }
                    },
                },
        });

            $('#course_add_btn').off('click').on('click',function(){
                var $form=$('#addCourseForm');
                var bv = $form.data('bootstrapValidator');
                bv.validate();
                if(bv.isValid()){
                $.ajax({
                        url:$form.attr('action'),
                        data:$form.serialize(),
                        type:'POST',
                        success:function(result){
                          if(result.success){
                            // 提示添加成功
                            $('#addCourseModal').modal('toggle');
                            refreshCourseTable();
                            toastr.success('新增课程成功');

                            }else{
                                toastr.error('新增课程失败');
                            }
                         },
                     });
                 };
            });
   });
}

function tableOperationEvent(){
    $(".btn_course_modify").off("click");
     $(".btn_course_delete").off("click");
   window.operateEvents = {
      'click .btn_course_modify': function (e, value, row, index) {
          $('#modify_course_number').val(row.course_number);
         $('#modify_course_name').val(row.course_name);
         $('#modify_course_weeks').val(row.course_week_times);
         $('#modify_course_semester').val(row.semester);
         $('#modify_course_members').val(row.course_members);
         $('#modifyCourseModal').modal('toggle');

        $('#modifyCourseForm').bootstrapValidator({
            message:'',
             feedbackIcons: {
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },
            fields:{
                 course_number:{
                    validators:{
                        notEmpty: {
                            message: '课程编号不空'
                        },
                    }
                },
                course_name:{
                    validators:{
                        notEmpty: {
                            message: '课程名称不空'
                        },
                    }
                    },
                    course_members:{
                    validators:{
                        notEmpty: {
                            message: '课程人数不空'
                        },
                    }
                    },
                course_weeks:{
                    validators:{
                        notEmpty: {
                            message: '课程周次不空'
                        },
                    }
                    },
                course_semester:{
                    validators:{
                        notEmpty: {
                            message: '课程学期不空'
                        },
                    }
                    },
                },
        });

          $('#course_modify_btn').off('click').on('click',function(){
                var $form=$('#modifyCourseForm');
                var bv = $form.data('bootstrapValidator');
                bv.validate();
                if(bv.isValid()){
                $.ajax({
                    url:$form.attr('action'),
                    data:$form.serialize(),
                    type:'PUT',
                    success:function(result){
                      if(result.success){
                        $('#modifyCourseModal').modal('toggle');
                            refreshCourseTable();
                            toastr.success('修改课程成功');
                        }else{
                            toastr.error('修改课程失败');
                        }
                     },
                 });
            }
            });
       },
        'click .btn_course_delete': function (e, value, row, index) {

                Ewin.confirm({ message: "确认要删除选中的课程吗？" }).on(function (e) {
                    if(!e)
                        return;
                   $.ajax({
                        url:'/ajax/api/v1.0/course?course_number='+row.course_number,
                        type:'DELETE',
                        success:function(result){
                            if(result.success){
                                refreshCourseTable();
                                toastr.success('删除课程成功');
                            }else{
                                toastr.error('删除课程失败');
                            }
                         },
                     });
            });
       },
    };
}
function refreshCourseTable(){
    $('#course_table').bootstrapTable('refresh', {url: '/ajax/api/v1.0/course'});
}

function search()
{
    $('#course_query_input').bind('input propertychange',function(){
        console.log('change');
        refreshCourseTable()
    });
}

$(document).ready(function(){

   tableOperationEvent();
   var tableInit=new TableInit();
   tableInit.Init();

   addCourseValidatorForm();
   search();
});