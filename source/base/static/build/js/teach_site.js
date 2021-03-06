var TableInit = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {

         //根据窗口调整表格高度
        $(window).resize(function() {
            $('#teach_site_table').bootstrapTable('resetView', {
                height: oTableInit.tableHeight
            });
        });
        oTableInit.operateFormatter = function (value, row, index) {//赋予的参数
                return [
          '<button class="btn btn_course_modify" type="button"><i class="fa fa-paste"></i>修改</button>',
          '<button class="btn btn_course_delete" type="button"><i class="fa fa-envelope"></i> 删除</button>',
            ].join('');
         }

        $('#teach_site_table').bootstrapTable({
        method: 'get',
        contentType: "application/json",//必须要有！！！！
        url:"/ajax/api/v1.0/teach_site",//要请求数据的文件路径
        height:oTableInit.tableHeight,//高度调整
//        toolbar: '#toolbar',//指定工具栏
        striped: true, //是否显示行间隔色
//        dataField: "result",//bootstrap table 可以前端分页也可以后端分页，这里
        //我们使用的是后端分页，后端分页时需返回含有total：总记录数,这个键值好像是固定的
        //rows： 记录集合 键值可以修改  dataField 自己定义成自己想要的就好
//        pageNumber: 1, //初始化加载第一页，默认第一页
//        pagination:true,//是否分页
//        queryParamsType:'limit',//查询参数组织方式
//        queryParams:oTableInit.queryParams,//请求服务器时所传的参数
//        sidePagination:'server',//指定服务器端分页
//        pageSize:10,//单页记录数
//        pageList:[5,10,20,30],//分页步进值
        showRefresh:true,//刷新按钮
//        showColumns:true,
        clickToSelect: true,//是否启用点击选中行
//        sortable: true,      //是否启用排序
//        sortOrder: 'asc',
//        showFooter:false,
        columns:[
            {
                title:'ID',
                field:'id',
                align: 'center',
                valign: 'middle',
            },
            {
                title:'场所名称',
                field:'loc_name',
                align: 'center',
                valign: 'middle',
            },
            {
                title:'场所位置',
                field:'location',
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
            return res.result;
        }
    });
    };
    oTableInit.tableHeight=function() {
        return $(window).height() - 140;
     }
//    //请求服务数据时所传参数
//    oTableInit.queryParams= function (params){
//        return{
//            //每页多少条数据
//            limit: params.limit,
//            //请求第几页
//            offset:params.offset,
//        };
//    };
        return oTableInit;
};

function tableOperationEvent(){
    $(".btn_course_modify").off("click");
//     $(".btn_course_delete").off("click");
   window.operateEvents = {
      'click .btn_course_modify': function (e, value, row, index) {
          $('#modify_site_name').val(row.loc_name);
          $('#modify_location').val(row.location);

         $('#modifyTeachSiteModal').modal('toggle');

        $('#modifyTeachSiteForm').bootstrapValidator({
            message:'',
             feedbackIcons: {
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },
            fields:{
                 loc_name:{
                    validators:{
                        notEmpty: {
                            message: '教学场所不空'
                        },
                    }
                },
                location:{
                    validators:{
                        notEmpty: {
                            message: '教学位置不空'
                        },
                    }
                    },
                },
        });

          $('#teach_site_modify_btn').off('click').on('click',function(){
                var $form=$('#modifyTeachSiteForm');
                var bv = $form.data('bootstrapValidator');
                bv.validate();
                if(bv.isValid()){
                $.ajax({
                    url:$form.attr('action'),
                    data:$form.serialize()+'&teach_site_id='+row.id,
                    type:'PUT',
                    success:function(result){
                      if(result.success){
                        $('#modifyTeachSiteModal').modal('toggle');
                            refreshCourseTable();
                            toastr.success('修改教学场所成功');
                        }else if(result.error_msg=='200012'){
                            toastr.error('教学场所已存在');
                        }else{
                            toastr.error('修改教学场所失败');
                        }
                     },
                 });
            }
            });
       },
    };
}
function refreshCourseTable(){
    $('#teach_site_table').bootstrapTable('refresh', {url: '/ajax/api/v1.0/teach_site'});
}


$(document).ready(function(){

   tableOperationEvent();
   var tableInit=new TableInit();
   tableInit.Init();

//   addCourseValidatorForm();
});