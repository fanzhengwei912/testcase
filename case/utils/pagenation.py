"""
自定义分页组件,以后如果想要使用这个分页组件，你需要做如下几件事：
def pret_list(request):

    1、根据自己的情况无筛选自己的数据
    queryset = models.PrettyNum.objects.all()

    2、实例化分页对象
    obj = Pagination(request, queryset)
    context = {

        'page_queryset': obj.page_queryset,  # 分页的数据
        "page_string": obj.html(),      # 生成页码

    }
    return render(request, 'pret_list.html', context)
在HTML页面中：
1、循环分完页的数据
{% for obj in page_queryset %}
    {{obj.xx}}
{% endfor %}
2、引用生成的页码
<ul class="pagination">
    {{ page_string }}
</ul>
"""
from django.utils.safestring import mark_safe


class Pagenation(object):
    def __init__(self, request, queryset, page_param='page', size_param=10, plus=5):
        """

        :param request:请求的对象
        :param queryset:符合条件的数据（根据这个数据给她进行分页处理）
        :param page_param:在url中传递过来的获取分页的参数例如：/list/?page=12
        :param size_param:每页展示多少条数据
        :param plus: 显示当前页的前面和后面各展示多少页的页码
        """

        import copy
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        self.page_param = page_param

        # 获取当前页
        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.size = size_param
        self.plus = plus
        # 计算当前页开始到结束的起止位置
        self.stat = (self.page - 1) * self.size
        self.end = self.page * self.size
        self.queryset = queryset
        # 获取起,止位置之间的数据列表
        self.page_queryset = self.queryset[self.stat:self.end]

        # 从数据库查询数据总数
        total_count = self.queryset.count()

        # 根据查询到的总数计算出页码数
        # 总页码
        total_page_count, div = divmod(total_count, self.size)  # 总数据除每页展示数是否有余数，如果有余数给除数+1，保证余数的部分也能获取到
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count

    # 定义用于展示的分页页码
    def html(self):

        # 计算出 显示当前页的前五页，后5页

        stat_page = self.page - self.plus
        end_page = self.page + self.plus + 1
        # 页码
        self.page_str_list = []

        # 首页
        self.query_dict.setlist(self.page_param, [1])
        self.page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))
        # 上一页
        # 当前页需要大于第一页，不然就只能保持在第一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())

        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        self.page_str_list.append(prev)
        # 页码
        for i in range(stat_page, end_page):
            if i < 1 or i > self.total_page_count:
                continue
            if i == self.page:
                self.query_dict.setlist(self.page_param, [i])
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                self.query_dict.setlist(self.page_param, [i])
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            self.page_str_list.append(ele)
        # 下一页
        # 当前页需要小于总页，不然就只能保持在最后一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            pref = '<li ><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            pref = '<li ><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        self.page_str_list.append(pref)

        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        pref = '<li ><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode())
        self.page_str_list.append(pref)

        # 跳转框
        sreach_page = """
            <li>
                                <form method="get" style="float: left;margin-left: 3px">

                                        <input style="width: 100px;display: inline-block;position: relative;float: left;" type="text" name="page" class="form-control" placeholder="页码">

                                    <button class="btn btn-default" type="submit">跳转</button>

                                </form>
                            </li>"""
        self.page_str_list.append(sreach_page)
        page_string = mark_safe("".join(self.page_str_list))
        return page_string
