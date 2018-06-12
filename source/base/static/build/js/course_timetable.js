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
//        pageNumber: 1, //初始化加载第一页，默认第一页
//        pagination:true,//是否分页
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
                title:'学年学期',
                field:'semester',
                halign :"center",
                align: 'center',
            },
            {
                title:'课程编号',
                field:'course_number',
                align: 'center',
                halign :"center",
            },
             {
                title:'课程名称',
                field:'course_name',
                align: 'center',
                halign :"center",
            },
             {
                title:'上课时间地点',
                field:'time_site',
                align: 'center',
                halign :"center",
            },
             {
                title:'授课安排时间',
                field:'last_modify_time',
                align: 'center',
                halign :"center",
            },
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
    //请求服务数据时所传参数
    oTableInit.queryParams= function (params){
      var class_name=$('#classes_btn').text().trim();
        return{
              'class_name':class_name,
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

function init_drop_menu(){

   $.get('/ajax/api/v1.0/get_colleague',function(data){
       if(data.success){
         var colleague_btn=$('#colleague_btn');
         var collea_menu=$('#colleague');
         var data=data.result;
         for(var i=0,len=data.length;i<len;i++){
           if(i==0){
            colleague_btn.text(data[i].colea_name);
            colleague_btn.append('  <span class="caret"></span>');
           }
           collea_menu.append('<li><a class='+data[i].id+' href="#">'+data[i].colea_name+'</a></li>')
         }

         change_colleague_menu();
         var collea_id=data[0].id;
         get_next_organization(collea_id);
       }
   },'json');
}
function get_next_organization(collea_id){
    $.get('/ajax/api/v1.0/get_profession?collea_id='+collea_id,function(data){
                 if(data.success){
                   var profession_btn=$('#profession_btn');
                   var prof_menu=$('#profession');
                   prof_menu.empty();
                   var data=data.result;
                    for(var i=0,len=data.length;i<len;i++){
                       if(i==0){
                        profession_btn.text(data[i].prof_name);
                        profession_btn.append('  <span class="caret"></span>');
                       }
                       prof_menu.append('<li><a href="#" class='+data[i].id+'>'+data[i].prof_name+'</a></li>')
                     }
                     var prof_id=data[0].id;
                     change_profession_menu();
                     get_class(prof_id);
                 }
          },'json');
}
function get_class(prof_id){
     $.get('/ajax/api/v1.0/get_class?prof_id='+prof_id,function(data){
           if(data.success){
              var class_btn=$('#classes_btn');
               var class_menu=$('#classes');
                class_menu.empty();
                var data=data.result;
                 for(var i=0,len=data.length;i<len;i++){
                      if(i==0){
                          class_btn.text(data[i].class_name);
                           class_btn.append('  <span class="caret"></span>');
                       }
                       class_menu.append('<li><a href="#">'+data[i].class_name+'</a></li>')
                       }
                       change_class_menu();
                       var tableInit=new TableInit();
                         tableInit.Init();
                   }
              },'json');
}
function change_colleague_menu(){
       var dropdown=$('#colleague');
        dropdown.children().each(function(){
         $(this).off('click').on('click',function(event){
             var btn3=$('#colleague_btn');
             btn3.text(event.target.innerText);
             btn3.append(' <span class="caret"></span>');

             get_next_organization(event.target.className);
         });
        });
}
function change_profession_menu(){
     var dropdown=$('#profession');
        dropdown.children().each(function(){
         $(this).off('click').on('click',function(event){
             var btn3=$('#profession_btn');
             btn3.text(event.target.innerText);
             btn3.append(' <span class="caret"></span>');

             get_class(event.target.className);
         });
        });
}
function change_class_menu(){
     var dropdown=$('#classes');
        dropdown.children().each(function(){
         $(this).off('click').on('click',function(event){
             var btn3=$('#classes_btn');
             btn3.text(event.target.innerText);
             btn3.append(' <span class="caret"></span>');
         });
        });
}
function click_course_arrange_query(){

    $('#timetable-query').off('click').on('click',function(){
        refreshCourseTimeTable();
    });

}
$(document).ready(function(){

   init_drop_menu();

   click_course_arrange_query();
});