from base.models import Colleague, Profession, Classes, UserInfo
from database import db, Base
from sqlalchemy import and_


def route_colleague0():
    colleagues = ['数计学院', '经管学院', '空间中心', '电气学院', '土木学院', '物信学院']
    for item in list(colleagues):
        colleague = Colleague(colea_name=item)
        db.session.add(colleague)
    db.session.commit()


def route_colleague1():
    colleagues = ['外国语学院', '环境工程学院', '化工学院']
    for item in list(colleagues):
        colleague = Colleague(colea_name=item)
        db.session.add(colleague)
    db.session.commit()


def route_profession1():
    professions = ['计算机技术', '软件工程', '离散中心', '应用数学']
    colleague = Colleague.query.filter_by(colea_name='数计学院').first()
    for item in list(professions):
        profession = Profession(item)
        profession.colleague_id = colleague.id
        db.session.add(profession)
    db.session.commit()


def route_profession2():
    professions = ['通信工程', '电子信息工程', '电子科学与技术', '光电信息工程', '微电子', '物理学', '数字媒体与网络工程', '物联网工程']
    colleague = Colleague.query.filter_by(colea_name='物信学院').first()
    for item in list(professions):
        profession = Profession(item)
        profession.colleague_id = colleague.id
        db.session.add(profession)
    db.session.commit()


def route_profession3():
    professions = ['管理科学与工程', '工商管理', '信息管理与信息系统', '物流管理', '金融工程', '会计学', '旅游管理', '经济与产业系统管理']
    colleague = Colleague.query.filter_by(colea_name='经管学院').first()
    for item in list(professions):
        profession = Profession(item)
        profession.colleague_id = colleague.id
        db.session.add(profession)
    db.session.commit()


def route_profession4():
    professions = ['科技与教育管理']
    colleague = Colleague.query.filter_by(colea_name='经管学院').first()
    for item in list(professions):
        profession = Profession(item)
        profession.colleague_id = colleague.id
        db.session.add(profession)
    db.session.commit()


def route_class():
    profesion1 = Profession.query.filter_by(prof_name='计算机技术').first()
    profesion2 = Profession.query.filter_by(prof_name='软件工程').first()
    data = [('17专硕1班', profesion1), ('17专硕2班', profesion2)]
    for item1, item2 in list(data):
        cla = Classes(item1)
        cla.profession_id = item2.id
        db.session.add(cla)
    db.session.commit()


def route_class2():
    profesion1 = Profession.query.filter_by(prof_name='电子科学与技术').first()
    profesion2 = Profession.query.filter_by(prof_name='光电信息工程').first()
    data = [('17电子1班', profesion1), ('17光电1班', profesion2), ('17电子2班', profesion1), ('17光电2班', profesion2)]
    for item1, item2 in list(data):
        cla = Classes(item1)
        cla.profession_id = item2.id
        db.session.add(cla)
    db.session.commit()


def route_student1():
    data = [('鲍尔', 'N170427094', 2), ('库兹马', 'N170427096', 2), ('哈特', 'N170427097', 2), ('兰德尔', 'N1704270100', 2),
            ('波普', 'N170427095', 2), ('威尔', 'N170427098', 2), ('托马斯', 'N170427099', 2), ('卡鲁索', 'N1704270101', 2),
            ('祖巴茨', 'N170427093', 2), ('哈登', 'N170427092', 2), ('保罗', 'N170427091', 2), ('克莱汤普森', 'N170427090', 2)]
    for item1, item2, item3 in list(data):
        user_info = UserInfo(item1, item2, item3)
        user_info.class_id = 3
        db.session.add(user_info)
    db.session.commit()


def route_student3():
    data = [('科比', 'N170327094', 2), ('詹姆斯', 'N170327096', 2), ('奥拉迪波', 'N170327097', 2), ('库里', 'N1703270100', 2)]
    for item1, item2, item3 in list(data):
        user_info = UserInfo(item1, item2, item3)
        user_info.class_id = 2
        db.session.add(user_info)
    db.session.commit()


def route_student2():
    data = [('杜兰特', 'N170327020', 2), ('格林', 'N1703270120', 2), ('米切尔', 'N170327001', 2), ('尼克杨', 'N170327099', 2),
            ('欧文', 'N170327019', 2), ('韦德', 'N1703270110', 2), ('沃顿', 'N170327002', 2), ('英格拉姆', 'N170327098', 2), ]
    for item1, item2, item3 in list(data):
        user_info = UserInfo(item1, item2, item3)
        user_info.class_id = 2
        db.session.add(user_info)
    db.session.commit()


def route_student4():
    data = [('布莱德索', 'N170527094', 2), ('帕克', 'N170527096', 2), ('邓肯', 'N170527097', 2), ('奥拉朱旺', 'N1705270100', 2),
            ('姚明', 'N170527095', 2), ('巴特勒', 'N170527098', 2), ('唐斯', 'N170527099', 2), ('维金斯', 'N1705270101', 2),
            ('雷迪克', 'N170527093', 2), ('恩比德', 'N170527092', 2), ('本西蒙斯', 'N170527091', 2), ('乔西蒙斯', 'N170527090', 2)]
    for item1, item2, item3 in list(data):
        user_info = UserInfo(item1, item2, item3)
        user_info.class_id = 4
        db.session.add(user_info)
    db.session.commit()


def route_relation():
    a = db.session.query(Colleague.colea_name, Profession.prof_name, Classes.class_name, UserInfo.user_name,
                         UserInfo.job_number, UserInfo.last_modify_time).join(
        Colleague.professions).join(Profession.classes).join(Classes.students).filter(
        UserInfo.class_id == 2).all()
    print(a)


if __name__ == '__main__':
    route_student4()
