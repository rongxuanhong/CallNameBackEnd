from utils.ERROR_DEFINE import J_MSG


class CustomFlaskErr(Exception):
    def __init__(self, return_code, status_code=400, payload=None):
        """

        :param return_code: 错误码
        :param status_code: 状态码
        :param payload:
        """
        Exception.__init__(self)
        self.return_code = return_code
        self.status_code = status_code
        self.payload = payload

    # 构造要返回的错误代码和错误信息的 dict
    def to_dict(self):
        rv = dict(self.payload or ())

        # 增加 dict key: return code
        rv['return_code'] = self.return_code

        # 增加 dict key: message, 具体内容由常量定义文件J_MSG中通过 return_code 转化而来
        rv['message'] = J_MSG[self.return_code]
        rv['success'] = False

        return rv
