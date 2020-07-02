class BootStrapForm(object):
    """设置表单使用BootStrap，创建BootStrap类，其他Form需要使用时继承这个类即可"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入{}'.format(field.label, )
